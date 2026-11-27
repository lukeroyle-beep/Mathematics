#!/usr/bin/env python3
"""Fresh candidate enumeration and original decimal blocks; no arithmetic imports.

Every ternary digit tests all three lifts.  The target is obtained from the
all-seven word modulo S, never by cancelling 9 from an F residue.  Checks
are explicit exceptions and remain active under python3 -O.
"""

from hashlib import sha256
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
INHERITED = HERE.parent / "power-three"
BASE = "42e6a151c5279905a3e02b859c6fae737178fd7d"


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def append(left, right, modulus):
    """Blocks are (value, 10**length), with both entries reduced modulo m."""
    return ((left[0] * right[1] + right[0]) % modulus,
            left[1] * right[1] % modulus)


def block(digit, length, modulus):
    require(0 <= digit <= 9 and length >= 0 and modulus > 0, "block domain")
    answer, power = (0, 1 % modulus), (digit % modulus, 10 % modulus)
    while length:
        if length % 2:
            answer = append(answer, power, modulus)
        power = append(power, power, modulus)
        length //= 2
    return answer


def original_word(length, position, modulus):
    require(3 <= position < length, "original decimal position is actual")
    answer = (0, 1 % modulus)
    for digit, count in ((7, length-position-1), (5, 1), (7, position-1), (5, 1)):
        answer = append(answer, block(digit, count, modulus), modulus)
    return answer[0]


def solve_class(a):
    require(a >= 7 and a % 6 == 1, "admissible exponent")
    S, d = 3**a, 3**(a-2)
    L = (S+4)//7
    require(7*L == S+4 and L < 2*d, "integral length and unique actual class")
    # n = the all-seven decimal word - 2 - 2*10**s.
    target = (block(7, L, S)[0]-2) * pow(2, -1, S) % S
    require(target % 9 == 1, "principal-unit target")
    exponent, value, generator, period, modulus = 0, 1, 10, 1, 9
    digest = sha256()
    for depth in range(3, a+1):
        modulus *= 3
        candidates = []
        for digit in range(3):
            trial_value = value * pow(generator, digit, S) % S
            if trial_value % modulus == target % modulus:
                candidates.append((digit, trial_value))
        require(len(candidates) == 1, "exactly one of all three ternary lifts")
        digit, value = candidates[0]
        exponent += digit * period
        digest.update(f"{depth}:{digit}\n".encode())
        period *= 3
        generator = pow(generator, 3, S)
    require(modulus == S and period == d and value == target, "complete lifting")
    require(pow(10, exponent, S) == target, "independent exponentiation readback")
    require(pow(10, d, S) == 1 and pow(10, d//3, S) != 1, "exact order")
    s = exponent if exponent % 2 else exponent+d
    require(3 <= s < 2*d and s % 6 == 3, "unique joint representative")
    require((7*pow(10, L, 9*S)-18*pow(10, s, 9*S)-25) % (9*S) == 0,
            "complete same-position sum readback with factor nine")
    return {"a": a, "L": L, "S": S, "d": d, "D": 2*d,
            "s": s, "ternary_lift_sha256": digest.hexdigest()}


def classify(a):
    row = solve_class(a)
    L, s, S = row["L"], row["s"], row["S"]
    row.update(actual=s < L, i=s if s < L else None, t=None,
               first_fail_depth=None, first_fail_n_residue=None)
    if s >= L:
        row["verdict"] = "class_miss"
        return row
    row["n_mod_S"] = original_word(L, s, S)
    row["n_mod_25S"] = original_word(L, s, 25*S)
    require(row["n_mod_S"] == row["n_mod_25S"] == 0, "original non-seven factors")
    residues = []
    for depth in range(1, 65):
        residue = original_word(L, s, 7**depth)
        residues.append(residue)
        if residue:
            require(depth <= L-2, "first failure is before inclusive witness threshold")
            row.update(t=depth-1, first_fail_depth=depth,
                       first_fail_n_residue=residue, seven_residues=residues,
                       verdict="seven_power_failure")
            return row
    raise ArithmeticError(f"a={a}: no failure by depth 64; no exclusion claimed")


def controls():
    positive = classify(25)
    require((positive["L"], positive["s"], positive["t"], positive["seven_residues"])
            == (121041229921, 40582608819, 2, [0, 0, 294]), "a=25 positive sum control")
    L, s = 313, 51
    digits = [7]*L
    digits[-1], digits[-s-1] = 5, 5
    n = int("".join(map(str, digits)))
    S, P = sum(digits), 1
    for digit in digits:
        P *= digit
    F = 7*10**L-18*10**s-25
    require(F == 9*n and S == 7*L-4 and P == 25*7**(L-2), "literal digit identities")
    require((n % (P*S) == 0) == (F % (225*S*7**(L-2)) == 0), "original full test")
    require(original_word(L, s, S) == n % S, "literal-block agreement")
    negative = {"L": L, "s": s, "S": S, "F_mod_S": F % S,
                "F_mod_9S": F % (9*S), "n_mod_S": n % S}
    require((negative["F_mod_S"], negative["F_mod_9S"], negative["n_mod_S"])
            == (0, 17496, 1944), "lost-factor-nine control")
    # Independent exhaustive original words at a=7 test actual-class completeness.
    small = classify(7)
    actual = [i for i in range(3, small["L"]) if i % 6 == 3
              and original_word(small["L"], i, small["S"]) == 0]
    require(actual == [small["s"]], "complete small original-word enumeration")
    return {"a25": positive, "lost_factor_nine": negative,
            "a7_exhaustive_actual_positions": actual}


def main():
    files = [INHERITED/name for name in ("individuals.json", "individuals-independent.json")]
    previous = [json.loads(path.read_text()) for path in files]
    require(all([r["a"] for r in data["cases"]] == list(range(31,1562,6)) for data in previous),
            "inherited range is exactly 256 specified exponents")
    finite = [classify(a) for a in range(31,104,6)]
    for row in finite:
        for data in previous:
            old = next(item for item in data["cases"] if item["a"] == row["a"])
            for key in ("a", "L", "S", "d", "D", "s", "i", "t",
                        "first_fail_depth", "first_fail_n_residue"):
                require(row[key] == old[key], f"inherited comparison a={row['a']}, {key}")
    new = classify(1567)
    require(new["actual"] and new["t"] == 1 and new["seven_residues"] == [0,7],
            "a=1567 independently recovered result")
    result = {"schema": 1, "base_main": BASE,
              "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
              "method": "fresh all-three-candidate ternary lift; original decimal blocks; no arithmetic imports",
              "inherited_receipt_sha256": {path.name: sha256(path.read_bytes()).hexdigest() for path in files},
              "finite_pair_starts": list(range(31,100,6)),
              "finite_rows_including_crossing_successor": finite,
              "cutoff_crossing_pair": [97,103], "new_a1567": new,
              "controls": controls(),
              "next_unchecked_individual_exponent": 1573,
              "consecutive_whole_length_endpoint_unchanged": 1000002000000,
              "lean_verification_performed": False}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
