#!/usr/bin/env python3
"""Exact finite controls for PRIME_DENSITY.md; no numerical density proof."""
import json
from collections import Counter
from math import gcd, isqrt

D = 7**7 * 10**5 - 25**7


def require(condition, message):
    if not condition:
        raise ValueError(message)


def prime(n):
    return n >= 2 and all(n % d for d in range(2, isqrt(n) + 1))


def record(p, exhaustive=True):
    require(prime(p) and p % 7 == 3, f"bad prime {p}")
    require(gcd(p, 2 * 3 * 5 * 7 * D) == 1, f"bad reduction {p}")
    L = (p + 4) // 7
    y = pow(10, 5 * pow(7, -1, p - 1), p)
    require(pow(y, 7, p) == pow(10, 5, p), "seventh-root identity")
    require(pow(10, L, p) == y, "Fermat identity")
    A = (7 * y - 25) * pow(180, -1, p) % p
    B = (7 * y - 25) * pow(18000, -1, p) % p
    require(A == 100 * B % p and B != 0, "radicand identity")
    square_character = pow(A, (p - 1) // 2, p)
    d = gcd(6, p - 1)
    sixth_character = pow(B, (p - 1) // d, p)
    h_roots = [x for x in range(p) if
               (pow(180 * x*x + 25, 7, p) - pow(7, 7, p) * pow(10, 5, p)) % p == 0]
    sixth_roots = [x for x in range(p) if pow(x, 6, p) == B]
    require(bool(h_roots) == (square_character == 1), "H square equivalence")
    require(bool(sixth_roots) == (sixth_character == 1), "sixth character equivalence")
    require(not sixth_roots or h_roots, "sixth test refines square test")
    require(len(h_roots) in (0, 2), "square fiber count")
    require(len(sixth_roots) in (0, d), "sixth fiber count")
    if exhaustive:
        ys = [z for z in range(p) if pow(z, 7, p) == pow(10, 5, p)]
        require(ys == [y], "unique seventh root")
        q_roots = [x for x in range(p) if
                   (pow(18000 * pow(x, 6, p) + 25, 7, p)
                    - pow(7, 7, p) * pow(10, 5, p)) % p == 0]
        require(q_roots == sixth_roots, "sextic polynomial equivalence")
    return {"p": p, "L": L, "y": y, "A": A, "B": B,
            "D_mod_p": D % p, "square_character": square_character,
            "sixth_character": sixth_character, "H_roots": h_roots,
            "sixth_roots": sixth_roots}


def group_controls():
    affine = [(a, b) for a in range(1, 7) for b in range(7)]
    require(len(affine) == 42, "affine size")
    conjugations = 0
    for b in range(7):
        fixed = [j for j in range(7) if (3*j + b) % 7 == j]
        require(fixed == [(-b * pow(2, -1, 7)) % 7], "unique fixed index")
        start = (fixed[0] + 1) % 7
        orbit, j = [], start
        while j not in orbit:
            orbit.append(j)
            j = (3*j+b) % 7
        require(len(orbit) == 6 and j == start, "six-cycle")
        for c in range(7):
            for j in range(7):
                lhs = (3*(j-c)+b+c) % 7
                rhs = (3*j+b-2*c) % 7
                require(lhs == rhs, "translation conjugacy")
                conjugations += 1
    fibers = {}
    for epsilon in (1, -1):
        counts = [sum((epsilon*k+c) % 6 == k for k in range(6))
                  for c in range(6)]
        require(counts == ([6, 0, 0, 0, 0, 0] if epsilon == 1 else
                           [2, 0, 2, 0, 2, 0]), "sixth fiber actions")
        fibers[str(epsilon)] = counts
    return {"affine_elements": len(affine), "conjugation_checks": conjugations,
            "sixth_fiber_fixed_point_counts": fibers}


def main():
    controls = [record(p) for p in (31, 59, 199, 283)]
    require(controls[0]["H_roots"] == [], "31 no-root control")
    require(controls[1]["H_roots"] == [26, 33], "59 root control")
    require(controls[2]["sixth_character"] == 107, "199 character")
    require([pow(107, k, 199) for k in (2, 3, 6)] == [106, 198, 1],
            "199 primitive sextic character")
    require(controls[3]["sixth_character"] == 1, "283 trivial character")
    for p in (59, 283):
        L = (p + 4) // 7
        passes = [i for i in range(3, L, 6) if
                  (7*pow(10, L, 9*p)-18*pow(10, i, 9*p)-25) % (9*p) == 0]
        require(passes == [], "root-passing necessary-only control")
    stats = Counter()
    for p in range(31, 10001):
        if p % 7 != 3 or not prime(p):
            continue
        if gcd(p, 2 * 3 * 5 * 7 * D) != 1:
            stats["bad_primes_omitted"] += 1
            continue
        row = record(p)
        stats["good_primes_checked"] += 1
        stats["square_passes"] += bool(row["H_roots"])
        stats["sixth_passes"] += bool(row["sixth_roots"])
        stats[f"mod3_{p % 3}_checked"] += 1
        stats[f"mod3_{p % 3}_sixth_passes"] += bool(row["sixth_roots"])
    require(stats["square_passes"] > 0 and stats["sixth_passes"] > 0,
            "nonzero positive controls")
    print(json.dumps({"status": "PASS", "scope": "finite algebraic controls, not density proof",
                      "D": D, "controls": controls, "group_controls": group_controls(),
                      "prime_bound_inclusive": 10000, "finite_counts": dict(sorted(stats.items()))},
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
