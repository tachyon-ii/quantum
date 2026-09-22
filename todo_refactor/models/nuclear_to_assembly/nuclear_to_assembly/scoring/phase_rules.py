from nuclear_to_assembly.phase.rails import phase_match

def score_phase(asm):
    """
    Count bonds that violate the A↔B alternation rule.
    Works with assemblies whose nucleon.ports entries are either
    Port objects or JSON dicts with {"face":..., "phase":...}.
    """
    bad = 0
    for b in asm.bonds:
        p1 = asm.nucleons[b.n1].ports[b.face1]
        p2 = asm.nucleons[b.n2].ports[b.face2]
        if not phase_match(p1, p2):
            bad += 1
    return {"bad_phase_bonds": bad}

