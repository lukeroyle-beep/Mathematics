#!/usr/bin/env python3
"""Independent exact recovery from original decimal blocks; no project imports.

Run from any directory.  Output is deterministic, including a hash of this
source.  All acceptance checks raise explicitly and remain active under -O.
No enormous word or full 7**(L-2) is constructed: a failing original-word
residue at a depth <= L-2 is already an exact divisibility disproof.
"""

import hashlib
import json
from math import gcd
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def concatenate(left, right, modulus):
    """Pairs are (decimal value, 10**decimal length), both modulo modulus."""
    x, tx = left
    y, ty = right
    return ((x * ty + y) % modulus, tx * ty % modulus)


def repeated_digit(digit, length, modulus):
    require(0 <= digit <= 9 and length >= 0 and modulus > 0, "bad block")
    result = (0, 1 % modulus)
    block = (digit % modulus, 10 % modulus)
    while length:
        if length & 1:
            result = concatenate(result, block, modulus)
        block = concatenate(block, block, modulus)
        length //= 2
    return result


def original_word(L, s, modulus):
    require(0 < s < L, "original word requires an actual position")
    result = repeated_digit(7, L - s - 1, modulus)
    result = concatenate(result, (5 % modulus, 10 % modulus), modulus)
    result = concatenate(result, repeated_digit(7, s - 1, modulus), modulus)
    return concatenate(result, (5 % modulus, 10 % modulus), modulus)[0]


def original_digits(L, s):
    return "7" * (L - s - 1) + "5" + "7" * (s - 1) + "5"


def recover_class(a, L):
    """Solve the sum condition via every ternary child, starting modulo 9.

    At each step y=10**r and z=10**step modulo S.  All three children
    r+j*step are tested modulo the next power of three.  Cached cubing
    updates z.  No logarithms, Hensel algebraic roots or known residues enter.
    """
    S = 3**a
    all_sevens = repeated_digit(7, L, S)[0]
    target = (all_sevens - 2) * pow(2, -1, S) % S
    require(target % 9 == 1, "target outside the powers of ten")
    r, step, y, z, modulus = 0, 1, 1, 10 % S, 9
    digit_counts = [0, 0, 0]
    while modulus < S:
        modulus *= 3
        children = [j for j in range(3) if y * pow(z, j, S) % modulus == target % modulus]
        require(len(children) == 1, "ternary child not unique")
        j = children[0]
        digit_counts[j] += 1
        r += j * step
        y = y * pow(z, j, S) % S
        step *= 3
        z = pow(z, 3, S)
    require(step == 3 ** (a - 2), "wrong order")
    require(0 <= r < step and pow(10, r, S) == target, "class recovery failed")
    require(pow(10, step, S) == 1, "order does not divide d")
    require(a == 2 or pow(10, step // 3, S) != 1, "order smaller than d")
    s = r if r % 2 else r + step
    require(s % 6 == 3 and 0 <= s < 2 * step, "wrong joint representative")
    return s, digit_counts


def classify(a):
    require(a >= 7 and a % 6 == 1, "unsupported family exponent")
    S = 3**a
    require((S + 4) % 7 == 0, "length not integral")
    L = (S + 4) // 7
    d = 3 ** (a - 2)
    s, digits = recover_class(a, L)
    require(L < 2 * d and L % 2 == 1 and S % 5, "family conditions")
    actual = 3 <= s < L
    row = dict(a=a, L=L, S=S, d=d, D=2*d, s=s, i=s if actual else None,
               actual=actual, s_mod_126=s % 126, ternary_digit_counts=digits,
               g=None, q=None, t=None, first_fail_depth=None,
               first_fail_modulus=None, first_fail_n_residue=None,
               n_mod_S=None, n_mod_25S=None, F_mod_9S=None,
               seven_residues=None, full_witness=False)
    if not actual:
        require(s >= L, "unclassified range failure")
        row["exclusion"] = "joint representative outside [3,L)"
        return row
    g = gcd(L, s)
    row.update(g=g, q=L//g)
    row["n_mod_S"] = original_word(L, s, S)
    row["n_mod_25S"] = original_word(L, s, 25*S)
    row["F_mod_9S"] = (7*pow(10, L, 9*S)-18*pow(10, s, 9*S)-25) % (9*S)
    require(row["n_mod_S"] == row["n_mod_25S"] == row["F_mod_9S"] == 0,
            "same-position full sum condition failed")
    residues, modulus = [], 1
    # A resource guard is an error, never a classification or an exclusion.
    for depth in range(1, 33):
        modulus *= 7
        residue = original_word(L, s, modulus)
        residues.append(residue)
        F_residue = (7*pow(10, L, modulus)-18*pow(10, s, modulus)-25) % modulus
        require(9*residue % modulus == F_residue, "block/formula disagreement")
        if residue:
            require(depth <= L - 2, "failure is later than the witness threshold")
            row.update(t=depth-1, first_fail_depth=depth,
                       first_fail_modulus=modulus, first_fail_n_residue=residue,
                       seven_residues=residues,
                       exclusion="original word fails a required seven-power divisor")
            break
    else:
        raise ArithmeticError("valuation unresolved at depth 32; no exclusion claimed")
    return row


def literal_controls():
    checked = 0
    for L in range(3, 65):
        for s in range(1, L):
            digits = original_digits(L, s)
            n = int(digits)
            for modulus in (7, 49, 343, 25*(7*L-4), 9*(7*L-4)):
                require(original_word(L, s, modulus) == n % modulus, "literal block mismatch")
            require(9*n == 7*10**L-18*10**s-25, "literal F identity")
            checked += 1
    L, s = 313, 51
    digits = original_digits(L, s)
    n = int(digits)
    S = sum(map(int, digits))
    product = 1
    for digit in digits:
        product *= int(digit)
    F = 7*10**L-18*10**s-25
    require(S == 7*L-4 and product == 25*7**(L-2) and F == 9*n,
            "literal original predicate data")
    exact_word_predicate = n % (product*S) == 0
    exact_F_predicate = F % (225*S*7**(L-2)) == 0
    require(exact_word_predicate == exact_F_predicate == False, "full predicate control")
    require(F % S == 0 and F % (9*S) == 17496 and n % S == 1944,
            "lost factor nine not detected")
    # Complete literal enumeration of the small a=7 family, independent of
    # modular class recovery, checks that a miss cannot conceal another s.
    small_a, small_L = 7, (3**7+4)//7
    eligible = [j for j in range(3, small_L, 6)
                if int(original_digits(small_L, j)) % (3**small_a) == 0]
    recovered, _ = recover_class(small_a, small_L)
    require(eligible == ([recovered] if recovered < small_L else []),
            "small actual-position class is incomplete")
    return dict(literal_pairs=checked, literal_length_range=[3,64],
                lost_factor_nine=dict(L=L, s=s, S=S, n_mod_S=n % S,
                                     F_mod_S=F % S, F_mod_9S=F % (9*S),
                                     PS_divides_n=exact_word_predicate,
                                     full_F_divides=exact_F_predicate),
                complete_a7=dict(a=small_a,L=small_L,s=recovered,eligible=eligible))


def main():
    exponents = sorted(set([25, 1231, 1567, 1573, 1579] + list(range(31,100,6))))
    rows = [classify(a) for a in exponents]
    indexed = {r["a"]: r for r in rows}
    require(not indexed[1573]["actual"] and indexed[1573]["s_mod_126"] == 123,
            "1573 pilot does not reproduce")
    require(indexed[1579]["actual"] and indexed[1579]["seven_residues"] == [0,14],
            "1579 pilot does not reproduce")
    require(indexed[1231]["actual"] and indexed[1231]["t"] == 4,
            "depth-four control does not reproduce")
    require(indexed[25]["actual"] and indexed[25]["n_mod_25S"] == 0
            and indexed[25]["seven_residues"] == [0,0,294], "sum-positive control")
    require(indexed[1567]["actual"] and indexed[1567]["seven_residues"] == [0,7],
            "inherited 1567 control")
    out = dict(schema="a398769-original-block-independent-v1",
               source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               method="original decimal blocks; unique ternary child at each digit; no project imports",
               exponents=exponents, rows=rows, controls=literal_controls(),
               claims=dict(new_family_exponents=[1573,1579],
                           no_full_witness=True, valuation_guard_is_failure=True,
                           no_universal_individual_exclusion=True,
                           no_Lean_verification=True))
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
