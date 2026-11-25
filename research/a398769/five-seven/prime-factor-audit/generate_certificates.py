#!/usr/bin/env python3
"""Rebuild full n-1 Lucas certificates; SymPy is used only for discovery.

The checked-in certificates can be verified with checker.py using only the
Python standard library. No SymPy primality verdict is part of that proof.
"""

import json
import math

import sympy

ROOTS = (2, 3, 5, 7, 13, 23, 211, 1237, 1289, 1327, 2609, 7043, 11399,
         11831, 903649, 555700252411, 4920652182747643,
         958850750886621892231, 4240701096684867281569789303)


def main():
    records = {}

    def build(n):
        if n in records:
            return
        if n == 2:
            records[n] = {"n": "2", "base": None, "factors": []}
            return
        factors = sorted((int(p), int(e)) for p, e in sympy.factorint(n - 1).items())
        if math.prod(p**e for p, e in factors) != n - 1:
            raise RuntimeError("discovery did not completely factor n-1")
        for p, _ in factors:
            build(p)
        a = 2
        while not (pow(a, n - 1, n) == 1 and
                   all(math.gcd(pow(a, (n - 1) // p, n) - 1, n) == 1
                       for p, _ in factors)):
            a += 1
            if a >= n:
                raise RuntimeError(f"no Lucas witness for {n}")
        records[n] = {"n": str(n), "base": str(a),
                      "factors": [[str(p), e] for p, e in factors]}

    for n in ROOTS:
        build(n)
    print(json.dumps({"method": "full n-1 Lucas certificates",
                      "roots": [str(n) for n in ROOTS],
                      "certificates": [records[n] for n in sorted(records)]},
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
