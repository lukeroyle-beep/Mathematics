#!/usr/bin/env python3
"""Independent computational review: no imports from research arithmetic."""
import argparse
from collections import Counter
from copy import deepcopy
import hashlib
import json
from math import gcd, prod
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
REL = HERE.relative_to(ROOT).as_posix()
BASE = '61a6fdfd7f4093b77be36ed0a55fbd3ebf798b7c'


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def recover_kappa(a):
    """Inverse-exponent root, then quotient digits; no Newton/log series."""
    modulus = 3 ** a
    theta_modulus = 9 * modulus
    theta = pow(10, 4 * pow(7, -1, modulus), theta_modulus)
    need(theta % 9 == 1 and pow(theta, 7, theta_modulus) == 10000 % theta_modulus,
         'independent seventh-root readback')
    numerator = 7 * theta - 25
    need(numerator % 9 == 0, 'exact two-digit division')
    target = numerator // 9 * pow(2, -1, modulus) % modulus
    residual, inverse_step = target, pow(10, -1, modulus)
    place, divisor, value = 1, 9, 0
    digits = []
    while divisor < modulus:
        need(residual % divisor == 1, 'ternary residual precision')
        # (10^(3^h)-1)/3^(h+2) = 1 mod3, so this quotient is the digit.
        digit = (residual - 1) // divisor % 3
        value += digit * place
        digits.append(digit)
        residual = residual * pow(inverse_step, digit, modulus) % modulus
        divisor *= 3
        need(residual % divisor == 1, 'quotient-derived digit readback')
        inverse_step = pow(inverse_step, 3, modulus)
        place *= 3
    need(residual == 1 and place == 3 ** (a - 2), 'ternary recovery complete')
    need(pow(10, value, modulus) == target, 'independent discrete-log readback')
    return value, digits


def representative(kappa, a):
    modulus = 3 ** (a - 2)
    s = kappa % modulus
    return s if s % 2 else s + modulus


def original_n(L, s, modulus):
    """Repunit modulo 9m, divide exactly; independent of block concatenation."""
    need(0 < s < L, 'actual word required')
    residue = (pow(10, L, 9 * modulus) - 1) % (9 * modulus)
    need(residue % 9 == 0, 'repunit exact division')
    return (7 * (residue // 9) - 2 - 2 * pow(10, s, modulus)) % modulus


def basic_row(kappa, a):
    S, L = 3 ** a, (3 ** a + 4) // 7
    s = representative(kappa, a)
    need(3 <= s < 2 * 3 ** (a - 2) and s % 6 == 3, 'odd representative domain')
    need((7 * pow(10, L, 9 * S) - 18 * pow(10, s, 9 * S) - 25) % (9 * S) == 0,
         'same-position factor nine')
    result = dict(a=a, L=L, s=s, actual=s < L)
    if s >= L:
        result.update(t=None, first_fail_depth=None, first_nonzero_n_residue=None)
        return result
    need(original_n(L, s, 25 * S) == 0, 'original non-seven factors')
    residues = []
    for m in range(1, 65):
        modulus = 7 ** m
        r = original_n(L, s, modulus)
        residues.append(r)
        if r:
            need(m <= L - 2, 'failure must be at or before inclusive deadline')
            result.update(g=gcd(L, s), q=L // gcd(L, s), n_mod_25S=0,
                          t=m-1, first_fail_depth=m, first_fail_modulus=modulus,
                          first_nonzero_n_residue=r, n_residues=residues)
            return result
    raise ValueError('UNRESOLVED: independent depth cap reached')


def independent_lift(L, sb, D, depth=8):
    """Choose a zero by exhaustive children, never by the proposed coefficient."""
    root, period = 0, 1
    result = [dict(depth=1, j=0, period=1)]
    children = []
    for m in range(1, depth):
        modulus = 7 ** (m + 1)
        values = [(7 * pow(10, L, modulus)
                   - 18 * pow(10, sb + 2 * D * (root + c * period), modulus)
                   - 25) % modulus for c in range(7)]
        hits = [c for c, value in enumerate(values) if value == 0]
        need(len(hits) == 1, 'independent unique child')
        old = values[0]
        need(old % (7 ** m) == 0, 'carry precision')
        need(all(values[c] == (old + 2 * c * 7 ** m) % modulus for c in range(7)),
             'proposed coefficient against every independent child')
        need(hits[0] == (-4 * (old // 7 ** m)) % 7, 'proposed digit formula')
        children.append(values)
        root += hits[0] * period
        period *= 7
        result.append(dict(depth=m+1, j=root, period=period))
    # Independently enumerate all 2401 j via multiplicative progression.
    modulus = 7 ** 5
    constant = (7 * pow(10, L, modulus) - 25) % modulus
    power, step = pow(10, sb, modulus), pow(10, 2 * D, modulus)
    zeros = []
    for j in range(2401):
        if (constant - 18 * power) % modulus == 0:
            zeros.append(j)
        power = power * step % modulus
    need(zeros == [result[4]['j']], 'full depth-five period agrees')
    return result, children


def validate_certificate(receipt, expected, selected):
    need(receipt['status'] == 'PASS' and receipt['base_main'] == BASE, 'receipt identity')
    need([r['a'] for r in receipt['rows']] == selected, 'selected domain')
    for row in receipt['rows']:
        real = expected[row['a']]
        for key in ('L', 's_b', 's_a', 'k', 'K', 'j_5', 'g', 'q', 'actual',
                    'n_mod_25S', 't', 'first_fail_depth', 'first_fail_modulus',
                    'first_nonzero_n_residue', 'n_residues'):
            need(row[key] == real[key], 'independent row field: '+key)
        need(row['F_mod_9S'] == 0 and row['full_witness'] is False, 'exact predicate outcome')
        need(row['lifts']['roots'] == real['roots'], 'complete independent lift roots')
        need([x['direct_child_F_residues'] for x in row['lifts']['transitions']]
             == real['children'], 'every independent child residue')
    earlier = receipt['inherited_259']['rows']
    need([r['a'] for r in earlier] == list(range(31, 1585, 6)), 'earlier domain')
    for row in earlier:
        real = expected[row['a']]
        need(row['actual'] == real['actual'] and row['t'] == real['t'], 'earlier classification')
        if real['actual']:
            need(row['first_fail_depth'] == real['first_fail_depth'] and
                 row['first_nonzero_n_residue'] == real['first_nonzero_n_residue'],
                 'earlier original-word failure')
    need(receipt['named_family_members_excluded'] == 262 and
         receipt['last_family_exponent'] == 1597 and receipt['next_family_exponent'] == 1603,
         'family count and endpoints')
    need(receipt['class_misses'] == 85 and receipt['actual_candidates'] == 177 and
         receipt['valuation_histogram'] == {'1':154, '2':19, '3':3, '4':1}, 'summary')
    need(receipt['whole_length_endpoint_inclusive'] == 1000002000000 and
         receipt['Lean_verification'] is False and receipt['moving_family'] == 'OPEN' and
         receipt['no_depth_cap_exclusions'] is True, 'scope remains honest')


def run(commit=None):
    kappa, digits = recover_kappa(1597)
    expected = {a: basic_row(kappa, a) for a in range(31, 1598, 6)}
    selected = [1231, 1579, 1585, 1591, 1597]
    for a in selected:
        row = expected[a]
        sb, D = representative(kappa, a-6), 3 ** (a-8)
        roots, children = independent_lift(row['L'], sb, D)
        row.update(s_b=sb, s_a=row['s'], k=(row['s']-sb)//(2*D),
                   K=(row['L']-1-sb)//(2*D), j_5=roots[4]['j'], roots=roots,
                   children=children)
        need(0 <= row['k'] <= 728 and row['k'] <= row['K'] <= 468,
             'actual increment bound')
    receipt = json.loads((HERE/'certificates.json').read_text())
    validate_certificate(receipt, expected, selected)
    need([trace['a'] for trace in receipt['ternary_traces']]
         == receipt['ternary_recovery_exponents'], 'complete recovery trace domain')
    for trace in receipt['ternary_traces']:
        a = trace['a']
        need(trace['ternary_digits'] == a-2 and trace['digits_low_first']
             == ''.join(map(str, digits[:a-2])), 'independent complete ternary digit trace')
    report = (HERE/'EXACT_CERTIFICATES.md').read_text()
    printed_fields = 0
    for a in (1585,1591,1597):
        section = report.split('### a='+str(a)+', b='+str(a-6)+'\n', 1)[1]
        block = section.split('```text\n',1)[1].split('```',1)[0]
        printed = dict(line.split(' = ',1) for line in block.strip().splitlines())
        need(set(printed) == {'L','s_b','s_a','k','K','j_5'}, 'printed integer domain')
        for key, value in printed.items():
            need(int(value) == expected[a][key], 'printed exact integer mismatch: '+key)
            printed_fields += 1
    table_rows = [line for line in report.splitlines()
                  if line.startswith('| ') and line.split('|')[1].strip().isdigit()]
    need(len(table_rows) == 5, 'printed certificate table domain')
    for line in table_rows:
        columns = [part.strip() for part in line.split('|')[1:-1]]
        row = expected[int(columns[0])]
        need(list(map(int,columns[1:6])) == [row[k] for k in ('k','K','j_5','g','t')]
             and columns[6] == str(row['first_nonzero_n_residue'])+' modulo '+
             str(row['first_fail_modulus']), 'printed table mismatch')
    need(expected[1579]['K'] == 467 and expected[1579]['j_5'] == 119
         != expected[1579]['k'] == 205, 'in-range wrong actual increment')
    need(expected[1231]['t'] == 4 and expected[1231]['k'] == 377
         and expected[1231]['j_5'] == 720 > expected[1231]['K'], 'depth-four control')
    need(representative(kappa, 1573) >= (3 ** 1573 + 4)//7,
         'nonactual predecessor used unchanged')
    positive = basic_row(kappa, 25)
    need(positive['n_residues'] == [0,0,294], 'nonzero positive control')
    need(expected[31]['n_residues'] == [0,35], 'inherited base')
    literal = '7'*(313-51-1)+'5'+'7'*(51-1)+'5'
    n, S, P = int(literal), sum(map(int, literal)), prod(map(int, literal))
    nine = dict(F_mod_S=9*n % S, F_mod_9S=9*n % (9*S), n_mod_S=n % S,
                PS_divides_n=n % (P*S) == 0)
    need(nine == dict(F_mod_S=0, F_mod_9S=17496, n_mod_S=1944, PS_divides_n=False),
         'literal product/sum lost-factor-nine control')
    need(original_n(313,51,25*S) == n % (25*S), 'independent repunit versus literal')
    histogram = Counter(str(r['t']) for r in expected.values() if r['actual'])
    need(dict(histogram) == {'1':154,'2':19,'3':3,'4':1}, 'fresh full histogram')
    need(sum(not r['actual'] for r in expected.values()) == 85, 'fresh class misses')
    # Independent full-integer crossover checks and exact rearrangement.
    need(3**1585 > 7*624000**61*1605**122, 'corollary crossover')
    need(3*1605**122 > 1606**122, 'corollary induction')
    corollary = json.loads((HERE/'corollary-checks.json').read_text())
    need(corollary['finite_exponents'] == list(range(31,1585,6)) and
         corollary['finite_count'] == 259, 'corollary complete finite range')
    for row in corollary['finite_rows']:
        real = expected[row['a']]
        need(row['actual'] == real['actual'], 'corollary actuality')
        if real['actual']:
            need(row['t'] == real['t'] and
                 row['first_fail_n_residue'] == real['first_nonzero_n_residue'],
                 'corollary finite residue')
    mutations = []
    for field in ('s_a', 's_b', 'k', 'K', 'j_5', 'g', 't', 'n_mod_25S',
                  'first_fail_depth', 'first_nonzero_n_residue'):
        altered = deepcopy(receipt)
        altered['rows'][0][field] += 1
        mutations.append((field, altered))
    altered = deepcopy(receipt)
    altered['rows'][0]['t'] = 1
    altered['rows'][0]['first_fail_depth'] = 2
    altered['rows'][0]['first_fail_modulus'] = 49
    altered['rows'][0]['first_nonzero_n_residue'] = 14
    altered['rows'][0]['n_residues'] = [0,14]
    mutations.append(('coordinated plausible wrong valuation', altered))
    altered = deepcopy(receipt)
    altered['inherited_259']['rows'].pop(0)
    mutations.append(('omitted finite base', altered))
    altered = deepcopy(receipt)
    altered['rows'][0]['lifts']['transitions'][0]['direct_child_F_residues'][0] += 7
    mutations.append(('child coefficient evidence', altered))
    for label, altered in mutations:
        try:
            validate_certificate(altered, expected, selected)
        except (ValueError, KeyError):
            pass
        else:
            raise ValueError('corruption accepted: '+label)
    tracked_hashes = {}
    if commit:
        subprocess.run(['git','merge-base','--is-ancestor',BASE,commit], cwd=ROOT, check=True)
        paths = subprocess.check_output(['git','ls-tree','-r','--name-only',commit,
                                         '--',REL,'README.md'], cwd=ROOT).decode().splitlines()
        for name in paths:
            # Review artifacts are added after the implementation commit.
            if Path(name).name in ('independent_review.py','independent-review.json','REVIEW.md'):
                continue
            content = subprocess.check_output(['git','show',commit+':'+name], cwd=ROOT)
            need((ROOT/name).read_bytes() == content, 'reviewed implementation changed: '+name)
            tracked_hashes[name] = digest(content)
        need(len(tracked_hashes) >= 12, 'review must bind complete implementation')
    return dict(status='PASS', reviewed_implementation_commit=commit,
                source_sha256=digest(Path(__file__).read_bytes()),
                implementation_sha256=tracked_hashes,
                method='modular-inverse root and quotient ternary digits; independent repunit modulo 9m',
                kappa_precision=1595, ternary_digits_sha256=digest(bytes(digits)),
                freshly_recovered_family_members=262, first_exponent=31,
                last_exponent=1597, next_exponent=1603, class_misses=85,
                actual_candidates=177, exact_valuation_histogram=dict(sorted(histogram.items())),
                selected_rows=[expected[a] for a in selected],
                depth_five_classes_enumerated=2401*len(selected),
                all_children_checked=7*7*len(selected),
                printed_exact_integer_fields_checked=printed_fields,
                printed_table_rows_checked=len(table_rows),
                rejected_corruptions=[label for label,_ in mutations],
                lost_factor_nine=nine, positive_control_a25=positive,
                complete_finite_corollary_remainder=259,
                moving_position_bound='unresolved beyond the stated sufficient subfamilies',
                Lean_verification=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--commit')
    parser.add_argument('--check', type=Path)
    args = parser.parse_args()
    result = run(args.commit)
    text = json.dumps(result, indent=2, sort_keys=True)+'\n'
    if args.check:
        need(text == args.check.read_text(), 'independent retained receipt mismatch')
    print(text, end='')


if __name__ == '__main__':
    main()
