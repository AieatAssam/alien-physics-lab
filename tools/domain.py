"""Where a claim applies: species, particle count, and every pairwise distance in the initial setup."""
import math


def in_domain(domain, setup):
    parts = setup["particles"]
    if len(parts) > domain["max_particles"]:
        return False
    if any(p["species"] not in domain["species"] for p in parts):
        return False
    lo, hi = domain["r_range"]
    for i, a in enumerate(parts):
        for b in parts[i + 1:]:
            if not lo <= math.dist(a["pos"], b["pos"]) <= hi:
                return False
    return True


if __name__ == "__main__":
    dom = {"species": ["A", "B"], "r_range": [0.5, 6.0], "max_particles": 2}
    near = {"particles": [{"species": "A", "pos": [0, 0]}, {"species": "B", "pos": [2, 0]}]}
    far = {"particles": [{"species": "A", "pos": [0, 0]}, {"species": "B", "pos": [9, 0]}]}
    assert in_domain(dom, near) and not in_domain(dom, far)
    print("domain ok")
