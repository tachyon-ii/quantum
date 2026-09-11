# README_ID10T — fire up the 3D nuclear viewer, look at things

For when you just want to see it. Grace `.ghost`, 2026-09-11, for James at 36,000 ft.

## 1. Run it

```
cd /Users/cgios/cgios.ai/QUANTUM/models/nuclear_to_assembly
export PYTHONPATH=.
python3 -m nuclear_to_assembly.cli.toasm viz3d he4_cross.json
```

Drag = rotate. Scroll = zoom. `q` = close. Red = proton, blue = neutron.

If it complains about a window: `pip3 install pyglet --break-system-packages` and go again.

## 2. What else is on the shelf

The library builds A ≤ 4 by name (`build d2 | h3_linear | h3_orth | h3_tri | he3_linear |
he3_orth | he3_tri | he4_cross | he4_ring`). Heavier ones exist only as hand-built JSON in
this directory from earlier passes — none scored against anything, treat as sketches:

```
python3 -m nuclear_to_assembly.cli.toasm viz3d c12_alpha_fixed2.json
python3 -m nuclear_to_assembly.cli.toasm viz3d c12_tetrahedral_test.json
python3 -m nuclear_to_assembly.cli.toasm viz3d c12_layered.json
python3 -m nuclear_to_assembly.cli.toasm viz3d o16_double_cube_test.json
python3 -m nuclear_to_assembly.cli.toasm viz3d li7_final.json
```

Other verbs on any JSON:

```
python3 -m nuclear_to_assembly.cli.toasm score  <file>.json
python3 -m nuclear_to_assembly.cli.toasm viz    <file>.json --out <file>.png --title "<name>"
```

`./gen_players.sh` rebuilds, scores and draws every A ≤ 4 assembly into `players/` and
prints the bond table that `docs/three-term-binding.md` §5a carries. Never hand-edit that
table; run the script.

## 3. What you're looking at in he4_cross

Two protons on one edge, two neutrons on the opposite edge. In a regular tetrahedron
opposite edges are always perpendicular skew lines, and there is exactly **one** way to
colour four vertices 2 + 2 up to rotation — so "no matter how you arrange it you get
crossed p–p and n–n pairs" is not a tendency, it is a theorem. The p–p axis and the n–n
axis cross at 90°, offset along the common perpendicular: a quadrupole, the "magnet".

Symmetry of that object: D2d. It has an S4 (rotate 90°, reflect) so it is **achiral** —
its mirror image is itself, turned.

## 4. The next question (posit, James 2026-09-11)

Add a second alpha. Two D2d tetrahedra in contact have a relative twist φ between their
p–p axes. φ = 0° or 90° keeps a mirror; **any other φ is chiral** — two enantiomers, ±φ.
Three in a triangle (C-12) with a common twist is a propeller, chiral the same way.

So the leaf's job is not "is C-12 chiral" but "**what φ does the packing force?**" If the
Kelvin-cell contacts only close at φ ∈ {0°, 90°}, no chirality. If they close at some other
φ, the nucleus is a screw and the sign is a new integer.

Falsifier, so it's on the table before anyone builds: a chiral ground state in a nucleus
shows up as a **parity doublet** — a near-degenerate opposite-parity partner (the pear-shaped
Ra-224 family does this at a few hundred keV). C-12's first negative-parity level is the
3⁻ at 9.64 MeV; there is no 0⁻ partner anywhere near the ground state. So a static chiral
C-12 is already out; a chiral *packing* would have to tunnel between its enantiomers fast
enough that the ground state is the symmetric combination — which at nuclear energies it
would. Then chirality is real in the geometry and invisible in the spectrum, and the place
it could still show is in **what it costs** — the binding, via the contact count at that φ.
That is the alpha-ladder test (`specs/alpha-ladder.md`), which is why the geometry has to
be built first and the numbers read second.
