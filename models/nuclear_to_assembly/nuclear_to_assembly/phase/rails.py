def _phase_of(port) -> str:
    """
    Return the phase label 'A' or 'B' from either:
      - a Port object with attribute .phase, or
      - a plain dict with key 'phase'.
    """
    # Port-like object?
    ph = getattr(port, "phase", None)
    if ph is not None:
        return ph
    # JSON/dict-like
    if isinstance(port, dict):
        return port.get("phase")
    # Fallback
    return None


def validate_ports(nucleon) -> list[str]:
    """
    Basic checks: phases must be 'A' or 'B'; face labels must exist.
    Works with NucleonPose.ports as dict[str, Port] or dict[str, dict].
    """
    msgs = []
    for face, port in nucleon.ports.items():
        ph = _phase_of(port)
        if ph not in ("A", "B"):
            msgs.append(f"{nucleon.id}:{face} invalid phase {ph!r}")
    return msgs


def phase_match(port1, port2) -> bool:
    """
    Enforce A↔B alternation across bonds.
    Accepts Port objects or dicts (from JSON).
    """
    ph1 = _phase_of(port1)
    ph2 = _phase_of(port2)
    # If either missing, treat as mismatch to force a visible error upstream
    if ph1 not in ("A", "B") or ph2 not in ("A", "B"):
        return False
    return ph1 != ph2

