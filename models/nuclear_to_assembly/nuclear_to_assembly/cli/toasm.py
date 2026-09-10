import argparse, json
from nuclear_to_assembly.assemblies.library import get_nucleus_constraints
from nuclear_to_assembly.assemblies.builder import Assembly
from nuclear_to_assembly.io_modules.writer import dump_json
from nuclear_to_assembly.io_modules.loader import load_json, validate_assembly
from nuclear_to_assembly.io_modules.visualizer import plot_assembly_json
from nuclear_to_assembly.io_modules.visualizer_trimesh import show_assembly_trimesh
from nuclear_to_assembly.scoring.score import score_from_json

def asm_to_json(asm):
    """Convert Assembly to JSON format."""
    def pose_to_dict(p):
        return {
            "id": p.id,
            "kind": p.kind,
            "R": [[float(x) for x in row] for row in p.R],
            "t": [float(x) for x in p.t],
            "ports": [{"face": f, "phase": port.phase} for f, port in p.ports.items()],
        }
    return {
        "name": asm.name,
        "nucleons": [pose_to_dict(n) for n in asm.nucleons.values()],
        "bonds": [
            {"n1": b.n1, "face1": b.face1, "n2": b.n2, "face2": b.face2}
            for b in asm.bonds
        ],
    }

def cmd_build(args):
    """Build from library, discover bonds, write JSON."""
    constraints = get_nucleus_constraints(args.nucleus)
    asm = Assembly.from_constraints(args.nucleus, constraints)
    
    # Use provided output or default to nucleus_name.json
    output = args.output if args.output else f"{args.nucleus}.json"
    dump_json(asm_to_json(asm), output)
    print(f"Written to {output}")

def cmd_auto_generate(args):
    """NEW: Automated configuration generation"""
    generator = AutomatedGenerator()
    
    A = args.mass_number
    Z = args.atomic_number
    
    if args.best_only:
        # Find single best configuration
        result = generator.find_best_configuration(A, Z)
        if result:
            dump_json(asm_to_json(result.assembly), args.output)
        else:
            print(f"No viable configurations found for A={A}, Z={Z}")
    else:
        # Generate all configurations and save top N
        results = generator.generate_all_configurations(A, Z)
        
        max_results = args.max_results if hasattr(args, 'max_results') else 5
        top_results = results[:max_results]
        
        print(f"\nTop {len(top_results)} configurations:")
        for i, result in enumerate(top_results):
            print(f"{i+1}. {result.assembly.name} (score: {result.total_score:.2f})")
            
            # Save individual files
            if args.output:
                filename = f"{args.output}_config_{i+1}.json"
                dump_json(asm_to_json(result.assembly), filename)

def cmd_score(args):
    """Load JSON and score."""
    data = load_json(args.input)
    validate_assembly(data)
    result = score_from_json(data)
    print(json.dumps(result, indent=2))

def cmd_viz(args):
    """Load JSON and visualize."""
    validate_assembly(load_json(args.input))
    plot_assembly_json(args.input, out_png=args.out, title=args.title)

def cmd_viz3d(args):
    """Load JSON and show 3D."""
    show_assembly_trimesh(args.input, bg_color=(0, 0, 0, 0))

def main():
    ap = argparse.ArgumentParser(
        prog="toasm", description="Truncated-octahedron nuclear assembly CLI"
    )
    sub = ap.add_subparsers(dest="cmd", required=True)
    
    # Build
    b = sub.add_parser("build", help="Build from library and emit JSON")
    b.add_argument("nucleus", choices=["d2", "h3_linear", "h3_orth", "h3_tri",
                                       "he3_linear", "he3_orth", "he3_tri",
                                       "he4_cross", "he4_ring"])
    b.add_argument("-o", "--output", default=None)
    b.set_defaults(func=cmd_build)
    
    # Score
    s = sub.add_parser("score", help="Score an assembly JSON")
    s.add_argument("input")
    s.set_defaults(func=cmd_score)
    
    # Viz
    v = sub.add_parser("viz", help="Visualize assembly")
    v.add_argument("input")
    v.add_argument("--out", default=None)
    v.add_argument("--title", default=None)
    v.set_defaults(func=cmd_viz)
    
    # Viz3D
    v3 = sub.add_parser("viz3d", help="Interactive 3D viewer")
    v3.add_argument("input")
    v3.set_defaults(func=cmd_viz3d)
    
    args = ap.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
