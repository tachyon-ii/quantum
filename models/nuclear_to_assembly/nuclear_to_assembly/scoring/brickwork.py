from nuclear_to_assembly.geometry.to_geometry import angle_deg_by_faces, face_class, is_orthogonal, is_opposite

def score_brickwork(asm):
    bonds = asm.bonds
    orth = 0
    shear_pen = 0
    curv_pen = 0.0

    # curvature weighting: prefer S–S (penalty=0) vs H–H (penalty>0)
    CURV_W = {"S": 1.0, "H": 1.15}  # tweak later

    # pairwise check for orthogonality & shear (coplanar/collinear sequences)
    for i,b1 in enumerate(bonds):
        f1a, f1b = b1.face1, b1.face2
        # curvature
        c1 = CURV_W[face_class(f1a)]
        c2 = CURV_W[face_class(f1b)]
        curv_pen += max(c1,c2) - 1.0  # zero for S–S; >0 for any H
        for j,b2 in enumerate(bonds):
            if j<=i: continue
            f2a = b2.face1
            ang = angle_deg_by_faces(f1a, f2a)
            if is_orthogonal(f1a, f2a, tol_deg=7.5): orth += 1
            if abs(ang-180.0) < 7.5: shear_pen += 1

    return {
        "orthogonal_links": orth,
        "shear_penalty": shear_pen,
        "curvature_penalty": round(curv_pen, 3)
    }
