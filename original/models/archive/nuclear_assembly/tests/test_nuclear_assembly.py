#!/usr/bin/env python3
# test_nuclear_assembly.py
"""
Test script for nuclear assembly modules.
"""

import sys
import os
sys.path.append('nuclear_assembly')

def test_basic_import():
    """Test that all modules can be imported."""
    print("Testing imports...")
    try:
        from geometry.tetra_base import TruncatedTetrahedron
        from geometry.face_labeling import LabeledTetrahedron
        from geometry import constants
        from assemblies.d2 import D2Unit
        from assemblies.he4 import He4Ring
        from assemblies.builder import NuclearBuilder
        from scoring.belt_energy import BeltScorer
        from io_modules.json_schema import AssemblySerializer
        from io_modules.visualizer import SimpleVisualizer
        print("✓ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_tetrahedron():
    """Test basic tetrahedron creation."""
    print("\nTesting TruncatedTetrahedron...")
    try:
        from geometry.tetra_base import TruncatedTetrahedron
        tet = TruncatedTetrahedron(edge_length=1.0)
        print(f"✓ Created tetrahedron with {len(tet.vertices)} vertices")
        
        hex_faces, tri_faces = tet.get_face_indices()
        print(f"✓ Has {len(hex_faces)} hexagonal faces and {len(tri_faces)} triangular faces")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_labeled_tetrahedron():
    """Test face labeling."""
    print("\nTesting LabeledTetrahedron...")
    try:
        from geometry.face_labeling import LabeledTetrahedron
        import numpy as np
        
        tet = LabeledTetrahedron(edge_length=1.0)
        print(f"✓ Created labeled tetrahedron")
        
        # Check face labels
        h0 = tet.get_face('H0')
        print(f"✓ H0 face has {len(h0)} vertices: {h0}")
        
        ports = tet.get_port_pairs()
        print(f"✓ Has {len(ports)} H-T port pairs")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_d2_assembly():
    """Test D2 unit creation."""
    print("\nTesting D2 assembly...")
    try:
        from assemblies.d2 import D2Unit
        
        d2 = D2Unit()
        print(f"✓ Created D2 unit")
        
        free_faces = d2.get_free_faces()
        print(f"✓ Proton has {len(free_faces['proton'])} free faces")
        print(f"✓ Neutron has {len(free_faces['neutron'])} free faces")
        
        d2_dict = d2.to_dict()
        print(f"✓ Exported to dictionary with bond type: {d2_dict['bond']['type']}")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_he4_assembly():
    """Test He4 ring creation."""
    print("\nTesting He4 assembly...")
    try:
        from assemblies.he4 import He4Ring
        
        he4_L = He4Ring(chirality='L')
        print(f"✓ Created He4 ring with L chirality")
        
        he4_R = He4Ring(chirality='R')
        print(f"✓ Created He4 ring with R chirality")
        
        chi_L = he4_L.get_chirality_sign()
        chi_R = he4_R.get_chirality_sign()
        print(f"✓ Chirality signs: L={chi_L}, R={chi_R}")
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_scoring():
    """Test belt energy scoring."""
    print("\nTesting belt energy scoring...")
    try:
        from scoring.belt_energy import BeltScorer
        
        scorer = BeltScorer(alpha=1.0)
        
        # Test single bond energy
        ht_energy = scorer.bond_energy('HT', k=2)
        print(f"✓ H-T bond energy: {ht_energy:.4f}")
        
        # Test assembly scoring
        test_bonds = [
            {'type': 'HT', 'k': 2},
            {'type': 'HT', 'k': 2},
            {'type': 'HT', 'k': 2},
            {'type': 'HT', 'k': 2}
        ]
        
        result = scorer.score_assembly(test_bonds)
        print(f"✓ He4 total energy: {result['total_energy']:.4f} for {result['n_bonds']} bonds")
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_json_io():
    """Test JSON import/export."""
    print("\nTesting JSON I/O...")
    try:
        from io_modules.json_schema import AssemblySerializer
        from assemblies.d2 import D2Unit
        
        # Create a D2 unit
        d2 = D2Unit()
        assembly = {
            'name': 'test_D2',
            'components': [('D2', d2.to_dict())],
            'bonds': [d2.bond]
        }
        
        # Export to JSON
        serializer = AssemblySerializer()
        json_str = serializer.export_assembly(assembly)
        print(f"✓ Exported assembly to JSON ({len(json_str)} chars)")
        
        # Import from sample file
        import os
        sample_file = 'nuclear_assembly/data/samples/D2_base.json'
        if os.path.exists(sample_file):
            imported = serializer.import_assembly(sample_file)
            print(f"✓ Imported {imported['name']} from sample file")
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def main():
    """Run all tests."""
    print("="*60)
    print("NUCLEAR ASSEMBLY TEST SUITE")
    print("="*60)
    
    tests = [
        test_basic_import,
        test_tetrahedron,
        test_labeled_tetrahedron,
        test_d2_assembly,
        test_he4_assembly,
        test_scoring,
        test_json_io
    ]
    
    results = []
    for test in tests:
        try:
            success = test()
            results.append((test.__name__, success))
        except Exception as e:
            print(f"✗ Test {test.__name__} failed with exception: {e}")
            results.append((test.__name__, False))
    
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for name, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! The system is working.")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Check the errors above.")

if __name__ == "__main__":
    main()
