import argparse, json
<<<<<<< HEAD
from nuclear_to_assembly.assemblies.d2 import build_d2_ss
from nuclear_to_assembly.assemblies.he3 import build_he3_ss_orth, build_he3_ss_linear
from nuclear_to_assembly.assemblies.h3  import build_h3_ss_orth,  build_h3_ss_linear
from nuclear_to_assembly.assemblies.he4 import build_he4_cross, build_he4_ring

# NEW IMPORTS for Li-7, C-12, and O-16
from nuclear_to_assembly.assemblies.li7 import build_li7_linear, build_li7_compact, build_li7_ring
from nuclear_to_assembly.assemblies.c12 import build_c12_tetrahedral, build_c12_layered, build_c12_alpha_cluster
from nuclear_to_assembly.assemblies.o16 import build_o16_double_cube, build_o16_spherical, build_o16_alpha_tetrahedral, build_o16_layered_cube
from nuclear_to_assembly.assemblies.automated_generator import AutomatedGenerator

=======
from nuclear_to_assembly.assemblies.library import get_nucleus_constraints
from nuclear_to_assembly.assemblies.builder import Assembly
>>>>>>> 8d637b2cd5f6ab67ad138219aca1aee08c849e6b
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
<<<<<<< HEAD
    if args.which == "d2":
        if args.variant.upper() != "S_S":
            raise SystemExit("Only S_S variant scaffolded for now.")
        asm = build_d2_ss(name=args.name)

    elif args.which == "he4":
        var = args.variant.lower()
        if var in ("cross", "default"):
            asm = build_he4_cross(name=args.name)
        elif var == "ring":
            asm = build_he4_ring(name=args.name)
        else:
            raise SystemExit("he4 variants: cross | ring")

    elif args.which == "he3":
        var = args.variant.lower()
        if var in ("orth", "default"):
            asm = build_he3_ss_orth(name=args.name)
        elif var == "linear":
            asm = build_he3_ss_linear(name=args.name)
        else:
            raise SystemExit("he3 variants: orth | linear")

    elif args.which == "h3":
        var = args.variant.lower()
        if var in ("orth", "default"):
            asm = build_h3_ss_orth(name=args.name)
        elif var == "linear":
            asm = build_h3_ss_linear(name=args.name)
        else:
            raise SystemExit("h3 variants: orth | linear")

    # NEW: Li-7 support
    elif args.which == "li7":
        var = args.variant.lower()
        if var in ("linear", "default"):
            asm = build_li7_linear(name=args.name)
        elif var == "compact":
            asm = build_li7_compact(name=args.name)
        elif var == "ring":
            asm = build_li7_ring(name=args.name)
        else:
            raise SystemExit("li7 variants: linear | compact | ring")

    # NEW: C-12 support
    elif args.which == "c12":
        var = args.variant.lower()
        if var in ("tetrahedral", "default"):
            asm = build_c12_tetrahedral(name=args.name)
        elif var == "layered":
            asm = build_c12_layered(name=args.name)
        elif var == "alpha":
            asm = build_c12_alpha_cluster(name=args.name)
        else:
            raise SystemExit("c12 variants: tetrahedral | layered | alpha")

    # NEW: O-16 support
    elif args.which == "o16":
        var = args.variant.lower()
        if var in ("double_cube", "default"):
            asm = build_o16_double_cube(name=args.name)
        elif var == "spherical":
            asm = build_o16_spherical(name=args.name)
        elif var == "alpha_tetrahedral":
            asm = build_o16_alpha_tetrahedral(name=args.name)
        elif var == "layered_cube":
            asm = build_o16_layered_cube(name=args.name)
        else:
            raise SystemExit("o16 variants: double_cube | spherical | alpha_tetrahedral | layered_cube")

    else:
        raise SystemExit("build choices: d2 | he3 | h3 | he4 | li7 | c12 | o16")

    dump_json(asm_to_json(asm), args.output)
=======
    """Build from library, discover bonds, write JSON."""
    constraints = get_nucleus_constraints(args.nucleus)
    asm = Assembly.from_constraints(args.nucleus, constraints)
    
    # Use provided output or default to nucleus_name.json
    output = args.output if args.output else f"{args.nucleus}.json"
    dump_json(asm_to_json(asm), output)
    print(f"Written to {output}")
>>>>>>> 8d637b2cd5f6ab67ad138219aca1aee08c849e6b

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
<<<<<<< HEAD

    # Re-wrap into simple Assembly-like object for scoring
    class P: pass
    nucleons = {}
    for n in data["nucleons"]:
        p = P(); p.kind = n["kind"]; p.ports = {pp["face"]: pp for pp in n["ports"]}
        nucleons[n["id"]] = p
    class A: pass
    A = A(); A.nucleons = nucleons
    A.bonds = [type("B", (), b) for b in data["bonds"]]

    ch = count_channels(A)
    bw = score_brickwork(A)
    ph = score_phase(A)
    
    # Enhanced scoring output
    total_score = 0
    total_score += bw["orthogonal_links"] * 10
    total_score -= bw["shear_penalty"] * 5
    total_score -= bw["curvature_penalty"] * 3
    total_score += ch["NP"] * 20
    total_score -= ch["PP"] * 10
    total_score -= ch["NN"] * 10
    total_score -= ph["bad_phase_bonds"] * 50
    
    result = {
        "channels": ch, 
        "brickwork": bw, 
        "phase": ph,
        "total_score": round(total_score, 2)
    }
    
    print(json.dumps(result, indent=2))

def cmd_compare(args):
    """NEW: Compare multiple assemblies"""
    assemblies = []
    
    for input_file in args.inputs:
        try:
            data = load_json(input_file)
            validate_assembly(data)
            assemblies.append((input_file, data))
        except Exception as e:
            print(f"Error loading {input_file}: {e}")
            continue
    
    if len(assemblies) < 2:
        print("Need at least 2 valid assemblies to compare")
        return
    
    print(f"Comparing {len(assemblies)} assemblies:")
    print("-" * 80)
    print(f"{'Assembly':<25} | {'NP':<4} | {'PP':<4} | {'NN':<4} | {'Orth':<4} | {'Phase':<5} | {'Score':<6}")
    print("-" * 80)
    
    for filename, data in assemblies:
        # Quick scoring
        class P: pass
        nucleons = {}
        for n in data["nucleons"]:
            p = P(); p.kind = n["kind"]; p.ports = {pp["face"]: pp for pp in n["ports"]}
            nucleons[n["id"]] = p
        class A: pass
        A = A(); A.nucleons = nucleons
        A.bonds = [type("B", (), b) for b in data["bonds"]]

        ch = count_channels(A)
        bw = score_brickwork(A)
        ph = score_phase(A)
        
        total_score = (bw["orthogonal_links"] * 10 - bw["shear_penalty"] * 5 - 
                      bw["curvature_penalty"] * 3 + ch["NP"] * 20 - 
                      ch["PP"] * 10 - ch["NN"] * 10 - ph["bad_phase_bonds"] * 50)
        
        name = data.get("name", filename)[:24]
        print(f"{name:<25} | {ch['NP']:<4} | {ch['PP']:<4} | {ch['NN']:<4} | "
              f"{bw['orthogonal_links']:<4} | {ph['bad_phase_bonds']:<5} | {total_score:<6.1f}")
=======
    result = score_from_json(data)
    print(json.dumps(result, indent=2))
>>>>>>> 8d637b2cd5f6ab67ad138219aca1aee08c849e6b

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
<<<<<<< HEAD
    b = sub.add_parser("build", help="Build canonical assembly and emit JSON")
    b.add_argument("which", choices=["d2", "he3", "h3", "he4", "li7", "c12", "o16"])
    b.add_argument("--variant", default="default")
    b.add_argument("--name", default="Assembly")
    b.add_argument("-o", "--output", default=None)
    b.set_defaults(func=cmd_build)

    # NEW: Auto-generate
    auto = sub.add_parser("auto", help="Automatically generate optimal configurations")
    auto.add_argument("mass_number", type=int, help="A (total nucleons)")
    auto.add_argument("atomic_number", type=int, help="Z (protons)")
    auto.add_argument("--best-only", action="store_true", help="Generate only the best configuration")
    auto.add_argument("--max-results", type=int, default=5, help="Maximum configurations to generate")
    auto.add_argument("-o", "--output", default=None, help="Output file prefix")
    auto.set_defaults(func=cmd_auto_generate)

=======
    b = sub.add_parser("build", help="Build from library and emit JSON")
    b.add_argument("nucleus", choices=["d2", "h3_linear", "h3_orth", 
                                       "he3_linear", "he3_orth", 
                                       "he4_cross", "he4_ring"])
    b.add_argument("-o", "--output", default=None)
    b.set_defaults(func=cmd_build)
    
>>>>>>> 8d637b2cd5f6ab67ad138219aca1aee08c849e6b
    # Score
    s = sub.add_parser("score", help="Score an assembly JSON")
    s.add_argument("input")
    s.set_defaults(func=cmd_score)
<<<<<<< HEAD

    # NEW: Compare
    comp = sub.add_parser("compare", help="Compare multiple assemblies")
    comp.add_argument("inputs", nargs="+", help="Assembly JSON files to compare")
    comp.set_defaults(func=cmd_compare)

    # Viz (matplotlib snapshot)
    v = sub.add_parser("viz", help="Visualize assembly as static 3D plot (matplotlib)")
=======
    
    # Viz
    v = sub.add_parser("viz", help="Visualize assembly")
>>>>>>> 8d637b2cd5f6ab67ad138219aca1aee08c849e6b
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
<<<<<<< HEAD
    main()
=======
    main()
>>>>>>> 8d637b2cd5f6ab67ad138219aca1aee08c849e6b
