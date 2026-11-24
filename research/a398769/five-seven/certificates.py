#!/usr/bin/env python3
"""Exact modular certificates for the two-five audit; Python standard library.

This verifies finite arithmetic, not the analytic theorems or their applications.
Run without -O: assertions are the certificate checks.
"""

import json


def certify_order(modulus, period):
    """For periods 6*7^a, checking the prime quotients proves minimality."""
    assert pow(10, period, modulus) == 1
    witnesses = {q: pow(10, period // q, modulus)
                 for q in (2, 3, 7) if period % q == 0}
    assert all(value != 1 for value in witnesses.values())
    return witnesses


def main():
    assert [pow(10, j, 7) for j in range(6)] == [1, 3, 2, 6, 4, 5]
    assert (10**6 - 1) % 7 == 0 and (10**6 - 1) % 49 != 0
    rows = []
    modulus, period = 7, 6
    solutions = [j for j in range(period) if pow(10, j, modulus) == 2575 % modulus]
    assert len(solutions) == 1
    exponent = solutions[0]
    for k in range(1, 9):
        if k > 1:
            modulus *= 7
            # Every new solution reduces to the old unique class.
            lifts = [exponent + t * period for t in range(7)
                     if pow(10, exponent + t * period, modulus) == 2575 % modulus]
            assert len(lifts) == 1
            exponent = lifts[0]
            period *= 7
        witnesses = certify_order(modulus, period)
        assert 0 <= exponent < period
        assert pow(10, exponent, modulus) == 2575 % modulus
        rows.append(dict(k=k, modulus=modulus, period=period,
                         least_exponent=exponent, order_witnesses=witnesses))
    assert [r['least_exponent'] for r in rows] == [3, 39, 81, 1551, 1551, 30363, 30363, 2853939]
    assert (rows[1]['least_exponent'], rows[1]['period']) == (39, 42)
    assert (rows[7]['least_exponent'], rows[7]['period']) == (2853939, 4941258)

    # Candidate necessity: v_7(10^L-2575) >= L-3. The 49 test
    # applies for L>=5; after it forces L>=39, the 7^8 test applies.
    below_cutoff = [L for L in range(5, 100000, 2) if (L - 39) % 42 == 0]
    assert min(below_cutoff) == 39
    assert all(L - 3 >= 8 for L in below_cutoff)
    survivors = [L for L in below_cutoff if (L - 2853939) % 4941258 == 0]
    assert not survivors

    # 7*10^L mod49 depends only on L mod6; 10^i depends on i mod42.
    residue_pairs = [(ell, j) for ell in (1, 3, 5) for j in range(3, 42, 6)
                     if (7 * pow(10, ell, 49) - 18 * pow(10, j, 49) - 25) % 49 == 0]
    assert residue_pairs == [(1, 39), (3, 3), (5, 15)]
    next_position = min(j for _, j in residue_pairs if j != 3)
    assert next_position == 15
    print(json.dumps(dict(exponent_lifts=rows, modulo_49_pairs=residue_pairs,
                          lengths_passing_49_below_cutoff=len(below_cutoff),
                          survivors_below_cutoff=survivors,
                          next_position_permitted_modulo_49=next_position), indent=2))


if __name__ == '__main__':
    main()
