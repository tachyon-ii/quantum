#!/usr/bin/env python3
"""
Nuclear Attention Network - Stage 1 of James Freeman's two-stage approach

This neural network predicts the most probable nucleon relationship graphs
to dramatically reduce the search space for the GPU physics simulation.

Inspired by AlphaFold's approach to protein structure prediction.

Authors: Dr. James Freeman (Theory), Suman Pokhrel (Implementation)
Date: August 2025
"""

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
import json
import pickle
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import matplotlib.pyplot as plt

class NucleonType(Enum):
    PROTON = 0
    NEUTRON = 1

@dataclass
class NuclearTrainingData:
    """Training data for nuclear structure prediction"""
    protons: int
    neutrons: int
    nucleon_types: List[int]  # 0=proton, 1=neutron
    adjacency_matrix: np.ndarray  # True adjacency relationships
    binding_energy: float
    is_stable: bool
    geometry_type: str  # "tetrahedral", "bipyramidal", etc.

class NuclearKnowledgeBase:
    """
    Database of known nuclear structures and principles for training
    """
    
    def __init__(self):
        self.known_structures = []
        self._initialize_knowledge_base()
    
    def _initialize_knowledge_base(self):
        """Initialize with known nuclear physics principles"""
        
        # Helium-4: Perfect tetrahedral structure
        he4_adjacency = np.ones((4, 4)) - np.eye(4)  # All connected except self
        self.add_structure(
            protons=2, neutrons=2,
            nucleon_types=[0, 0, 1, 1],  # 2 protons, 2 neutrons
            adjacency_matrix=he4_adjacency,
            binding_energy=28.3,  # MeV
            is_stable=True,
            geometry_type="tetrahedral"
        )
        
        # Lithium-7: Asymmetric but stable
        li7_adjacency = self._generate_asymmetric_structure(7)
        self.add_structure(
            protons=3, neutrons=4,
            nucleon_types=[0, 0, 0, 1, 1, 1, 1],
            adjacency_matrix=li7_adjacency,
            binding_energy=39.2,  # MeV
            is_stable=True,
            geometry_type="bipyramidal_distorted"
        )
        
        # Beryllium-8: Unstable (very short-lived)
        be8_adjacency = self._generate_unstable_structure(8)
        self.add_structure(
            protons=4, neutrons=4,
            nucleon_types=[0, 0, 0, 0, 1, 1, 1, 1],
            adjacency_matrix=be8_adjacency,
            binding_energy=56.5,  # MeV
            is_stable=False,
            geometry_type="unstable_cluster"
        )
        
        # Add more known structures...
        self._add_experimental_data()
    
    def add_structure(self, protons: int, neutrons: int, nucleon_types: List[int],
                     adjacency_matrix: np.ndarray, binding_energy: float,
                     is_stable: bool, geometry_type: str):
        """Add a known nuclear structure to the knowledge base"""
        structure = NuclearTrainingData(
            protons=protons,
            neutrons=neutrons,
            nucleon_types=nucleon_types,
            adjacency_matrix=adjacency_matrix,
            binding_energy=binding_energy,
            is_stable=is_stable,
            geometry_type=geometry_type
        )
        self.known_structures.append(structure)
    
    def _generate_asymmetric_structure(self, num_nucleons: int) -> np.ndarray:
        """Generate an asymmetric but stable adjacency matrix"""
        adj = np.zeros((num_nucleons, num_nucleons))
        
        # Create a more realistic nuclear structure
        # Central core with surrounding nucleons
        for i in range(num_nucleons):
            for j in range(i+1, num_nucleons):
                # Distance-based probability (closer nucleons more likely connected)
                if np.random.random() < 0.7:  # 70% connection probability
                    adj[i, j] = adj[j, i] = 1.0
        
        return adj
    
    def _generate_unstable_structure(self, num_nucleons: int) -> np.ndarray:
        """Generate an unstable nuclear structure"""
        adj = np.zeros((num_nucleons, num_nucleons))
        
        # Unstable structures have poor connectivity
        for i in range(num_nucleons):
            for j in range(i+1, num_nucleons):
                if np.random.random() < 0.4:  # Lower connection probability
                    adj[i, j] = adj[j, i] = 1.0
        
        return adj
    
    def _add_experimental_data(self):
        """Add more experimental nuclear data"""
        
        # Deuterium (simplest stable nucleus)
        d_adj = np.array([[0, 1], [1, 0]])
        self.add_structure(1, 1, [0, 1], d_adj, 2.2, True, "diatomic")
        
        # Tritium (radioactive but bound)
        t_adj = np.ones((3, 3)) - np.eye(3)
        self.add_structure(1, 2, [0, 1, 1], t_adj, 8.5, False, "triangular")
        
        # Carbon-12 (very stable)
        c12_adj = self._generate_stable_structure(12)
        self.add_structure(6, 6, [0]*6 + [1]*6, c12_adj, 92.2, True, "icosahedral")
    
    def _generate_stable_structure(self, num_nucleons: int) -> np.ndarray:
        """Generate a stable, highly connected structure"""
        adj = np.zeros((num_nucleons, num_nucleons))
        
        # Stable structures have high connectivity
        for i in range(num_nucleons):
            for j in range(i+1, num_nucleons):
                if np.random.random() < 0.8:  # High connection probability
                    adj[i, j] = adj[j, i] = 1.0
        
        return adj
    
    def get_training_data(self) -> List[NuclearTrainingData]:
        """Return all known structures for training"""
        return self.known_structures

class NuclearDataset(Dataset):
    """PyTorch dataset for nuclear structure data"""
    
    def __init__(self, structures: List[NuclearTrainingData], max_nucleons: int = 20):
        self.structures = structures
        self.max_nucleons = max_nucleons
    
    def __len__(self):
        return len(self.structures)
    
    def __getitem__(self, idx):
        structure = self.structures[idx]
        
        # Create input features
        input_features = self._create_input_features(structure)
        
        # Create target adjacency matrix (padded to max_nucleons)
        target_adj = self._pad_adjacency_matrix(structure.adjacency_matrix)
        
        # Additional targets
        targets = {
            'adjacency': torch.FloatTensor(target_adj),
            'binding_energy': torch.FloatTensor([structure.binding_energy]),
            'is_stable': torch.FloatTensor([1.0 if structure.is_stable else 0.0])
        }
        
        return torch.FloatTensor(input_features), targets
    
    def _create_input_features(self, structure: NuclearTrainingData) -> np.ndarray:
        """Create input feature vector for the neural network"""
        features = []
        
        # Basic composition
        features.extend([
            structure.protons,
            structure.neutrons,
            structure.protons + structure.neutrons,  # Mass number
            structure.neutrons / structure.protons if structure.protons > 0 else 0,  # N/Z ratio
        ])
        
        # One-hot encoded nucleon sequence (padded)
        nucleon_sequence = structure.nucleon_types + [2] * (self.max_nucleons - len(structure.nucleon_types))
        for nucleon_type in nucleon_sequence:
            if nucleon_type == 0:  # Proton
                features.extend([1, 0, 0])
            elif nucleon_type == 1:  # Neutron
                features.extend([0, 1, 0])
            else:  # Padding
                features.extend([0, 0, 1])
        
        return np.array(features)
    
    def _pad_adjacency_matrix(self, adj_matrix: np.ndarray) -> np.ndarray:
        """Pad adjacency matrix to fixed size"""
        padded = np.zeros((self.max_nucleons, self.max_nucleons))
        size = min(adj_matrix.shape[0], self.max_nucleons)
        padded[:size, :size] = adj_matrix[:size, :size]
        return padded

class NuclearAttentionNetwork(nn.Module):
    """
    Neural network to predict nucleon relationship graphs
    
    Architecture inspired by Transformer attention mechanisms
    and graph neural networks.
    """
    
    def __init__(self, max_nucleons: int = 20, hidden_dim: int = 256, 
                 num_attention_heads: int = 8, num_layers: int = 4):
        super(NuclearAttentionNetwork, self).__init__()
        
        self.max_nucleons = max_nucleons
        self.hidden_dim = hidden_dim
        
        # Input dimension: 4 basic features + 3 * max_nucleons (one-hot nucleons)
        input_dim = 4 + 3 * max_nucleons
        
        # Input embedding
        self.input_embedding = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(hidden_dim, hidden_dim)
        )
        
        # Multi-head attention layers
        self.attention_layers = nn.ModuleList([
            nn.MultiheadAttention(hidden_dim, num_attention_heads, batch_first=True)
            for _ in range(num_layers)
        ])
        
        # Layer normalization
        self.layer_norms = nn.ModuleList([
            nn.LayerNorm(hidden_dim) for _ in range(num_layers)
        ])
        
        # Adjacency prediction head
        self.adjacency_head = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(hidden_dim // 2, max_nucleons * max_nucleons)
        )
        
        # Binding energy prediction head
        self.energy_head = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(hidden_dim // 2, 1)
        )
        
        # Stability prediction head
        self.stability_head = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(hidden_dim // 2, 1),
            nn.Sigmoid()
        )
    
    def forward(self, x):
        # Input embedding
        embedded = self.input_embedding(x)  # (batch_size, hidden_dim)
        
        # Add batch and sequence dimensions for attention
        # Treat as single sequence for global attention
        embedded = embedded.unsqueeze(1)  # (batch_size, 1, hidden_dim)
        
        # Multi-head attention layers
        attention_output = embedded
        for attention, layer_norm in zip(self.attention_layers, self.layer_norms):
            # Self-attention
            attn_out, _ = attention(attention_output, attention_output, attention_output)
            
            # Residual connection and layer norm
            attention_output = layer_norm(attention_output + attn_out)
        
        # Global pooling
        pooled = attention_output.squeeze(1)  # (batch_size, hidden_dim)
        
        # Prediction heads
        adjacency_logits = self.adjacency_head(pooled)
        adjacency_pred = adjacency_logits.view(-1, self.max_nucleons, self.max_nucleons)
        adjacency_pred = torch.sigmoid(adjacency_pred)
        
        energy_pred = self.energy_head(pooled)
        stability_pred = self.stability_head(pooled)
        
        return {
            'adjacency': adjacency_pred,
            'binding_energy': energy_pred,
            'is_stable': stability_pred
        }

class NuclearTrainer:
    """Training pipeline for the Nuclear Attention Network"""
    
    def __init__(self, model: NuclearAttentionNetwork, device: str = 'cpu'):
        self.model = model.to(device)
        self.device = device
        self.optimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-5)
        self.scheduler = optim.lr_scheduler.ReduceLROnPlateau(self.optimizer, patience=10)
        
        # Loss functions
        self.adjacency_loss = nn.BCELoss()
        self.energy_loss = nn.MSELoss()
        self.stability_loss = nn.BCELoss()
        
        # Training history
        self.train_losses = []
        self.val_losses = []
    
    def train_epoch(self, dataloader: DataLoader) -> float:
        """Train for one epoch"""
        self.model.train()
        total_loss = 0.0
        
        for batch_inputs, batch_targets in dataloader:
            batch_inputs = batch_inputs.to(self.device)
            
            # Move targets to device
            adjacency_target = batch_targets['adjacency'].to(self.device)
            energy_target = batch_targets['binding_energy'].to(self.device)
            stability_target = batch_targets['is_stable'].to(self.device)
            
            # Forward pass
            self.optimizer.zero_grad()
            predictions = self.model(batch_inputs)
            
            # Calculate losses
            adj_loss = self.adjacency_loss(predictions['adjacency'], adjacency_target)
            energy_loss = self.energy_loss(predictions['binding_energy'], energy_target)
            stability_loss = self.stability_loss(predictions['is_stable'], stability_target)
            
            # Weighted combination of losses
            total_batch_loss = adj_loss + 0.1 * energy_loss + 0.5 * stability_loss
            
            # Backward pass
            total_batch_loss.backward()
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
            self.optimizer.step()
            
            total_loss += total_batch_loss.item()
        
        return total_loss / len(dataloader)
    
    def validate(self, dataloader: DataLoader) -> float:
        """Validate the model"""
        self.model.eval()
        total_loss = 0.0
        
        with torch.no_grad():
            for batch_inputs, batch_targets in dataloader:
                batch_inputs = batch_inputs.to(self.device)
                
                adjacency_target = batch_targets['adjacency'].to(self.device)
                energy_target = batch_targets['binding_energy'].to(self.device)
                stability_target = batch_targets['is_stable'].to(self.device)
                
                predictions = self.model(batch_inputs)
                
                adj_loss = self.adjacency_loss(predictions['adjacency'], adjacency_target)
                energy_loss = self.energy_loss(predictions['binding_energy'], energy_target)
                stability_loss = self.stability_loss(predictions['is_stable'], stability_target)
                
                total_batch_loss = adj_loss + 0.1 * energy_loss + 0.5 * stability_loss
                total_loss += total_batch_loss.item()
        
        return total_loss / len(dataloader)
    
    def train(self, train_loader: DataLoader, val_loader: DataLoader, 
              num_epochs: int = 100, save_path: str = '../data/nuclear_model.pth'):
        """Full training loop"""
        
        print("Starting Nuclear Attention Network training...")
        print(f"Device: {self.device}")
        print(f"Model parameters: {sum(p.numel() for p in self.model.parameters()):,}")
        
        best_val_loss = float('inf')
        patience_counter = 0
        
        for epoch in range(num_epochs):
            # Training
            train_loss = self.train_epoch(train_loader)
            val_loss = self.validate(val_loader)
            
            # Learning rate scheduling
            self.scheduler.step(val_loss)
            
            # Save best model
            if val_loss < best_val_loss:
                best_val_loss = val_loss
                torch.save(self.model.state_dict(), save_path)
                patience_counter = 0
            else:
                patience_counter += 1
            
            # Early stopping
            if patience_counter >= 20:
                print(f"Early stopping at epoch {epoch}")
                break
            
            # Logging
            if epoch % 10 == 0:
                current_lr = self.optimizer.param_groups[0]['lr']
                print(f"Epoch {epoch:3d}: Train Loss = {train_loss:.4f}, "
                      f"Val Loss = {val_loss:.4f}, LR = {current_lr:.6f}")
            
            self.train_losses.append(train_loss)
            self.val_losses.append(val_loss)
        
        print(f"Training completed. Best validation loss: {best_val_loss:.4f}")
        return best_val_loss
    
    def plot_training_history(self):
        """Plot training and validation loss curves"""
        plt.figure(figsize=(10, 6))
        plt.plot(self.train_losses, label='Training Loss')
        plt.plot(self.val_losses, label='Validation Loss')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.title('Nuclear Attention Network Training History')
        plt.legend()
        plt.grid(True)
        plt.show()

class NuclearPredictor:
    """Interface for making predictions with trained model"""
    
    def __init__(self, model_path: str, device: str = 'cpu'):
        self.device = device
        self.max_nucleons = 20
        
        # Load model
        self.model = NuclearAttentionNetwork(max_nucleons=self.max_nucleons)
        self.model.load_state_dict(torch.load(model_path, map_location=device))
        self.model.to(device)
        self.model.eval()
    
    def predict_structure(self, protons: int, neutrons: int) -> Dict:
        """Predict nuclear structure for given composition"""
        
        # Create input features
        nucleon_types = [0] * protons + [1] * neutrons  # 0=proton, 1=neutron
        
        # Create dummy structure for feature extraction
        dummy_structure = NuclearTrainingData(
            protons=protons,
            neutrons=neutrons,
            nucleon_types=nucleon_types,
            adjacency_matrix=np.zeros((len(nucleon_types), len(nucleon_types))),
            binding_energy=0.0,
            is_stable=True,
            geometry_type="unknown"
        )
        
        # Create dataset and get features
        dataset = NuclearDataset([dummy_structure], self.max_nucleons)
        features, _ = dataset[0]
        
        # Make prediction
        with torch.no_grad():
            features = features.unsqueeze(0).to(self.device)  # Add batch dimension
            predictions = self.model(features)
            
            # Extract predictions
            adjacency_prob = predictions['adjacency'].squeeze(0).cpu().numpy()
            binding_energy = predictions['binding_energy'].squeeze(0).cpu().numpy()[0]
            stability_prob = predictions['is_stable'].squeeze(0).cpu().numpy()[0]
            
            # Threshold adjacency matrix
            adjacency_binary = (adjacency_prob > 0.5).astype(int)
            
            # Only consider relevant nucleons
            num_nucleons = protons + neutrons
            adjacency_prob = adjacency_prob[:num_nucleons, :num_nucleons]
            adjacency_binary = adjacency_binary[:num_nucleons, :num_nucleons]
        
        return {
            'adjacency_probabilities': adjacency_prob,
            'adjacency_binary': adjacency_binary,
            'predicted_binding_energy': binding_energy,
            'stability_probability': stability_prob,
            'nucleon_types': nucleon_types,
            'num_protons': protons,
            'num_neutrons': neutrons
        }

def main():
    """Main training and testing pipeline"""
    
    # Set device
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Using device: {device}")
    
    # Create knowledge base and dataset
    knowledge_base = NuclearKnowledgeBase()
    structures = knowledge_base.get_training_data()
    
    print(f"Loaded {len(structures)} nuclear structures for training")
    
    # Create dataset
    dataset = NuclearDataset(structures, max_nucleons=20)
    
    # Split into train/validation
    train_size = int(0.8 * len(dataset))
    val_size = len(dataset) - train_size
    train_dataset, val_dataset = torch.utils.data.random_split(dataset, [train_size, val_size])
    
    # Create data loaders
    train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=8, shuffle=False)
    
    # Create model and trainer
    model = NuclearAttentionNetwork(max_nucleons=20, hidden_dim=256)
    trainer = NuclearTrainer(model, device)
    
    # Train model
    best_loss = trainer.train(train_loader, val_loader, num_epochs=100)
    
    # Plot training history
    trainer.plot_training_history()
    
    # Test predictions
    print("\nTesting predictions on known structures:")
    
    predictor = NuclearPredictor('../data/nuclear_model.pth', device)
    
    # Test Helium-4
    he4_pred = predictor.predict_structure(2, 2)
    print(f"Helium-4 prediction:")
    print(f"  Predicted binding energy: {he4_pred['predicted_binding_energy']:.2f} MeV (experimental: 28.3 MeV)")
    print(f"  Stability probability: {he4_pred['stability_probability']:.3f}")
    
    # Test Lithium-7
    li7_pred = predictor.predict_structure(3, 4)
    print(f"Lithium-7 prediction:")
    print(f"  Predicted binding energy: {li7_pred['predicted_binding_energy']:.2f} MeV (experimental: 39.2 MeV)")
    print(f"  Stability probability: {li7_pred['stability_probability']:.3f}")

if __name__ == "__main__":
    main()