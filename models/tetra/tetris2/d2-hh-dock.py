#!/usr/bin/env python3
# test_clean_viz.py
"""
Test clean visualization.
"""

import sys
sys.path.append('nuclear_assembly')

from assemblies.d2 import D2Unit
from io_modules.visualizer import UnifiedVisualizer

def main():
    # Create D2
    print("Creating D2 unit...")
    d2 = D2Unit()
    
    # Create visualizer
    viz = UnifiedVisualizer()
    
    # Test different visualization modes
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--wireframe', action='store_true', help='Show as wireframe')
    parser.add_argument('--no-ports', action='store_true', help='Hide port outlines')
    parser.add_argument('--port-rotation', choices=['vertices', 'edges'], 
                       default='vertices',
                       help='Port triangle orientation: vertices or edges')
    args = parser.parse_args()
    
    # Visualize
    viz.visualize_assembly(
        d2, 
        show_ports=not args.no_ports,
        wireframe=args.wireframe,
        port_rotation=args.port_rotation
    )    
    print(f"\nPort rotation: {args.port_rotation}")
    if args.port_rotation == 'edges':
        print("  → Star of David pattern at connection")
    else:
        print("  → Triangles point to hexagon vertices")

if __name__ == "__main__":
    main()
