def count_channels(asm):
    NP = NP_SS = NP_HH = 0
    PP = NN = 0
    for b in asm.bonds:
        # Check if nucleons exist before accessing them
        if b.n1 not in asm.nucleons:
            raise KeyError(f"Nucleon '{b.n1}' referenced in bond but not found in assembly nucleons. Available nucleons: {list(asm.nucleons.keys())}")
        if b.n2 not in asm.nucleons:
            raise KeyError(f"Nucleon '{b.n2}' referenced in bond but not found in assembly nucleons. Available nucleons: {list(asm.nucleons.keys())}")
            
        k1 = asm.nucleons[b.n1].kind
        k2 = asm.nucleons[b.n2].kind
        cls = "SS" if b.face1.startswith("S") and b.face2.startswith("S") else \
              "HH" if b.face1.startswith("H") and b.face2.startswith("H") else "MIX"
        if {k1,k2}=={"proton","neutron"}:
            NP += 1
            if cls=="SS": NP_SS += 1
            if cls=="HH": NP_HH += 1
        elif k1==k2=="proton":
            PP += 1
        elif k1==k2=="neutron":
            NN += 1
    return {"NP":NP, "NP_S_S":NP_SS, "NP_H_H":NP_HH, "PP":PP, "NN":NN}
