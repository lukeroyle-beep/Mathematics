#!/usr/bin/env python3
"""Exact endpoint and nearest-centre controls; standard library, no imports from peers.

The inequalities in ANALYTIC.md are proofs. Finite controls here check their
constants, identities, and band endpoints, and do not replace those proofs.
All checks survive python3 -O. No floating point is used.
"""
from fractions import Fraction as Q
from hashlib import sha256
import json
from math import gcd
from pathlib import Path


ROWS = (
    (15, 101, 1000002000001, Q("19.30")),
    (16, 142, 4069338437095, Q("20.04")),
    (17, 226, 28485369059659, Q("21.10")),
    (18, 324, 199397583417607, Q(23)),
    (19, 361, 1395783083923243, Q(25)),
    (17, 289, 79000000000000, Q("21.60")),
)


def require(truth, label):
    if not truth:
        raise ArithmeticError(label)


def log_bounds(x, terms=40):
    """atanh series and a geometric bound on its strictly positive tail."""
    z = (x - 1) / (x + 1)
    require(0 <= z < 1, "log domain")
    lo = 2 * sum((z ** (2*j+1) / (2*j+1) for j in range(terms)), Q(0))
    hi = lo + 2*z ** (2*terms+1) / ((2*terms+1)*(1-z*z))
    return lo, hi


def exp_lower(x, terms=91):
    require(x > 0 and terms > 0, "exp domain")
    term, total = Q(1), Q(1)
    for j in range(1, terms):
        term *= x/j
        total += term
    return total


def val7(x):
    require(x != 0, "finite valuation")
    x, v = abs(x), 0
    while x % 7 == 0:
        x //= 7
        v += 1
    return v


def coefficients(L, i, a, b, q):
    r, s = L-b*q, i-a*q
    u = min(0, r, s)
    return (7*10**(r-u), -18*10**(s-u), -25*10**(-u)), (r, s, u)


def main():
    two_lo, two_hi = log_bounds(Q(2))
    seven_lo0, seven_hi0 = log_bounds(Q(7, 4))
    ten_lo0, ten_hi0 = log_bounds(Q(5, 4))
    seven_lo, seven_hi = seven_lo0+2*two_lo, seven_hi0+2*two_hi
    ten_lo, ten_hi = ten_lo0+3*two_lo, ten_hi0+3*two_hi
    require(seven_hi < 2 < ten_lo, "simple log bounds")
    # C=126 log(10)^2/log(7)^4; exact rational upper bound.
    require(126*ten_hi**2 < Q(189, 4)*seven_lo**4, "coefficient <189/4")
    require(168*ten_hi**2 < 63*seven_lo**4, "inherited derivative coefficient")
    ratio_log_lo, _ = log_bounds(ten_lo/seven_hi)
    require(ratio_log_lo > Q(3, 20), "log(log7/log10)+2/5 <1/4")

    results = []
    for k, c, X, m in ROWS:
        H = Q(c, 2)+Q(k*k, c)+2
        rhs = (Q(X, c)+Q(1, 2))/H+1
        lower = exp_lower(m-Q(1, 4))
        E = 3+252*(k+1)**3+Q(189, 4)*c**3*H*m*m
        require(lower > rhs, "91-term exponential comparison")
        require(E < X, "strict endpoint exclusion")
        require(m >= 10 and m >= 2, "constant and scaling branches")
        require(6*7**(k-2) < X < 6*7**(k-1), "row belongs to stated K")
        min_b = 4*k+1
        require(900 < min_b**2*m*m, "degree branch at every allowed b")
        for b in range(min_b, c+1):
            Hb = Q(b, 2)+Q(k*k, b)+2
            require(Hb <= H, "monotone nearest span height")
            # Entire degree branch, not its logarithmic factor alone.
            for D in range(1, b+1):
                require(225*seven_hi**2*D <= b**3*m*m, "actual-D branch")
        results.append({
            "K": k, "c": c, "X": X, "m": str(m), "H": str(H),
            "E": str(E), "X_minus_E": str(X-E),
            "exponential_terms": 91,
            "exp_lower_minus_rhs_floor": (lower-rhs).__floor__(),
        })

    # Exact polynomial transformation and nearest-rounding/span controls.
    identity_controls = nearest_negative_r = singular_derivatives = ties = 0
    for L in range(5, 62, 2):
        F0 = 7*10**L-25
        for i in range(3, L):
            F = F0-18*10**i
            for b in range(2, min(L, 15)+1):
                q0 = L//b
                q1 = q0+1
                q = (2*L+b)//(2*b)  # ties upward; either tie would be valid
                require(q in (q0, q1), "nearest quotient range")
                for a in range(1, b):
                    if gcd(a, b) != 1:
                        continue
                    C0, (_, _, u0) = coefficients(L, i, a, b, q0)
                    C1, (_, _, u1) = coefficients(L, i, a, b, q1)
                    for old, new, degree in zip(C0, C1, (b, a, 0)):
                        require(Q(new) == Q(10)**(u0-u1-degree)*old,
                                "Q_new(X)=10^(u0-u1) Q_old(X/10)")
                    C, (r, s, u) = coefficients(L, i, a, b, q)
                    x = 10**q
                    require(C[0]*x**b+C[1]*x**a+C[2] == 10**(-u)*F,
                            "polynomial value")
                    derivative = b*C[0]*x**(b-1)+a*C[1]*x**(a-1)
                    d = val7(derivative)
                    require(d == val7(7*b*10**L-18*a*10**i), "derivative valuation")
                    if a % 7:
                        require(d == 0, "regular derivative")
                    elif a % 49 == 0:
                        require(d == 1, "twice-divisible numerator")
                    else:
                        require(d == 1+val7(b*10**(L-i)-18*(a//7)),
                                "singular derivative identity")
                    span = max(0, r, s)-u
                    h = b*i-a*L
                    require(abs(2*r) <= b, "nearest remainder")
                    require(span <= Q(b, 2)+Q(abs(h), b), "nearest span")
                    identity_controls += 1
                    nearest_negative_r += r < 0
                    singular_derivatives += d > 1
                    ties += abs(2*r) == b
    require(nearest_negative_r > 0 and singular_derivatives > 0 and ties > 0,
            "nonvacuous rounding and singular controls")

    # Transport and dependent-root correction are algebraic proofs in the note.
    # These elementary exact checks bind the inherited upper-K argument.
    R = lambda k: 1+252*(k+1)**2*((k+1)+k**8+2*k**6)
    require(R(20)+1 < 6*7**18, "K>=20 induction base")
    require(6**10 < 7*5**10, "degree ten induction ratio")
    require(R(19)+2 == 1721427606158403, "inherited square cutoff")
    B = 1000002000000
    require(6*7**13 < B < 6*7**14, "inherited B lies in K15")
    bands = (
        (15, 102, 225, B+1, 6*7**14-1),
        (16, 143, 256, 6*7**14+1, 6*7**15-1),
        (17, 227, 288, 6*7**15+1, 79000000000000-1),
    )
    original_control = (6*7**15+1, 6*7**16-1)
    require(original_control == (28485369059659, 199397583417605),
            "original K17 b289 interval")
    require(all(lo % 2 and hi % 2 for _, _, _, lo, hi in bands), "odd endpoints")
    require(sum(bhi-blo+1 for _, blo, bhi, _, _ in bands) == 300, "300 denominators")
    base = Path(__file__).resolve().parent.parent
    refs = ("explicit-length/README.md", "explicit-length/MOVING_CENTRES.md",
            "explicit-length/ROUTE2.md", "uniform-bound/ANALYTIC.md", "uniform-bound/SOURCES.md")
    print(json.dumps({
        "status": "PASS", "rows": results,
        "controls": {"polynomial_identities": identity_controls,
                     "negative_nearest_remainder": nearest_negative_r,
                     "singular_derivative": singular_derivatives, "rounding_ties": ties},
        "bands": bands, "b289_original_odd_interval": original_control,
        "reference_sha256": {p: sha256((base/p).read_bytes()).hexdigest() for p in refs},
        "new_Lean_formalization": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
