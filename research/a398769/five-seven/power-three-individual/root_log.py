#!/usr/bin/env python3
"""Pinned inherited Newton/logarithm method, extended to the two new members.

This explicitly reuses power-three/individuals.py; independent_decimal.py
recovers the same classes without that code or those algorithms.
"""
from hashlib import sha256
import importlib.util
import json
from math import gcd
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'power-three' / 'individuals.py'
EXPONENTS = [25] + list(range(31, 100, 6)) + [1231, 1567, 1573, 1579]


def need(ok, message):
    if not ok:
        raise ArithmeticError(message)


def main():
    spec = importlib.util.spec_from_file_location('inherited_newton_log', SOURCE)
    old = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(old)
    theta, C, kappa = old.parameters(1580)
    theta2, C2, kappa2 = old.parameters(1586)
    need(theta2 % 3**1582 == theta and C2 % 3**1580 == C and
         kappa2 % 3**1578 == kappa, 'independent precision stability')
    cases = []
    for a in EXPONENTS:
        row = old.member(a, theta, kappa)
        L, s, S = row['L'], row['s'], row['S']
        actual = 3 <= s < L
        row.update(actual=actual, s_mod_126=s % 126, F_mod_9S=old.Fmod(L, s, 9*S),
                   g=None, p=None, q=None, q_fourth_gt_L=None,
                   n_mod_S=None, n_mod_25S=None, seven_residues=None)
        if actual:
            g = gcd(L, s)
            # F/9 mod M is obtained at precision 9M before division.
            n_mod_S = old.Fmod(L, s, 9*S)//9
            n_mod_25S = old.Fmod(L, s, 225*S)//9
            residues = [old.Fmod(L, s, 7**m)*pow(9, -1, 7**m) % 7**m
                        for m in range(1, row['first_fail_depth']+1)]
            row.update(g=g, p=s//g, q=L//g, q_fourth_gt_L=(L//g)**4 > L,
                       n_mod_S=n_mod_S, n_mod_25S=n_mod_25S, seven_residues=residues)
            need(n_mod_S == n_mod_25S == 0, 'non-seven factors at actual position')
            need(residues == [0]*row['t']+[row['first_fail_n_residue']], 'first nonzero residue')
            need((7*(L//g)*kappa-4*(s//g)) % row['d'] == 0,
                 'ternary rational-position relation')
        cases.append(row)
    by_a = {r['a']: r for r in cases}
    need(not by_a[1573]['actual'] and by_a[1573]['s_mod_126'] == 123,
         'a1573 class miss despite shallow congruence')
    need(by_a[1579]['actual'] and by_a[1579]['seven_residues'] == [0,14],
         'a1579 actual shallow failure')
    need(by_a[1231]['actual'] and by_a[1231]['t'] == 4, 'actual depth-four control')
    need(by_a[25]['seven_residues'] == [0,0,294], 'positive sum control')
    L,s,S = 313,51,2187
    nine = dict(L=L,s=s,S=S,F_mod_S=old.Fmod(L,s,S),
                F_mod_9S=old.Fmod(L,s,9*S),n_mod_S=old.Fmod(L,s,9*S)//9)
    need((nine['F_mod_S'],nine['F_mod_9S'],nine['n_mod_S']) == (0,17496,1944),
         'lost factor nine')
    result = dict(schema=1, base_main='a9edeb0a96bd56d55f3c96767f5154e69cb8ceda',
                  method='Explicit reuse of inherited Newton root and 3-adic logarithm',
                  source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                  inherited_source_path=str(SOURCE.relative_to(HERE.parents[3])),
                  inherited_source_sha256=sha256(SOURCE.read_bytes()).hexdigest(),
                  precision_checks=[1580,1586], exponents=EXPONENTS,
                  cases=cases, lost_factor_nine=nine)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
