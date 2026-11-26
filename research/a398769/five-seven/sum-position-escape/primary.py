#!/usr/bin/env python3
"""Exact F-based arithmetic; no expansion of giant decimal words."""
from collections import Counter
from hashlib import sha256
import json
from math import gcd, lcm, prod
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = '9d958f86fc81188de68af97909614e23a186df9f'
B = 1_000_002_000_000


def require(ok, message):
    if not ok:
        raise ArithmeticError(message)


def Fmod(L, i, modulus):
    return (7 * pow(10, L, modulus) - 18 * pow(10, i, modulus) - 25) % modulus


def nmod(L, i, modulus):
    f = Fmod(L, i, 9 * modulus)
    require(f % 9 == 0, 'exact division by nine')
    return f // 9


def valuation(n, p):
    require(n != 0, 'valuation of zero')
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    return v


def Kof(L):
    k, period = 1, 6
    while period <= L:
        k, period = k + 1, period * 7
    return k


def family(a, previous=None):
    require(a >= 7 and a % 6 == 1, 'admissible exponent')
    S = 3 ** a
    require((S + 4) % 7 == 0, 'integral length')
    L, d = (S + 4) // 7, 3 ** (a - 2)
    D = 2 * d
    # q=(7*10^L-25)/9 mod S requires modulus 9S before division.
    numerator = (7 * pow(10, L, 9 * S) - 25) % (9 * S)
    require(numerator % 9 == 0, 'sum numerator')
    C = (numerator // 9) * pow(2, -1, S) % S
    require(C % 27 == 1, 'sum subgroup and mod3 exponent compatibility')
    # Independently solve each next ternary digit with fresh modular powers.
    if previous is None:
        r, period, first_depth = 0, 1, 3
    else:
        require(a == previous['a'] + 6, 'successive recurrence input')
        r, period = previous['s'] % previous['d'], previous['d']
        first_depth = previous['a'] + 1
        require(pow(10, r, previous['S']) == C % previous['S'],
                'previous sum class really reduces from new target')
    for depth in range(first_depth, a + 1):
        modulus = 3 ** depth
        choices = [r + digit * period for digit in range(3)
                   if pow(10, r + digit * period, modulus) == C % modulus]
        require(len(choices) == 1, 'unique ternary lift')
        r = choices[0]
        period *= 3
    require(period == d and pow(10, r, S) == C, 'full sum log')
    require(pow(10, d, S) == 1 and pow(10, d // 3, S) != 1, 'exact sum order')
    s = r if r % 2 else r + d
    require(3 <= s < D and s % 6 == 3 and D > L, 'unique CRT position class')
    require(nmod(L, s, S) == 0, 'class full digit sum')
    i = s if s < L else None
    t = fail = fail_n = None
    if i is not None:
        # Bound is a fail-closed resource guard, never an exclusion criterion.
        for m in range(1, 257):
            residue = Fmod(L, i, 7 ** m)
            if residue:
                t, fail = m - 1, m
                fail_n = residue * pow(9, -1, 7 ** m) % (7 ** m)
                require(nmod(L, i, 7 ** m) == fail_n, 'n and F depth agreement')
                require(t < L - 2, 'putative witness requires separate certificate')
                require(Fmod(L, i, 7 ** t) == 0, 'preceding seven power')
                break
        require(t is not None, 'unresolved depth: do not claim exclusion')
    return dict(a=a, L=L, S=S, d=d, D=D, class_residue=s, s=s, i=i,
                t=t, first_fail_depth=fail, first_fail_n_residue=fail_n,
                K=Kof(L), n_mod_S=0,
                outcome='CLASS_MISSES_INTERVAL' if i is None else 'SEVEN_POWER_FAIL')


def literal_checks():
    counts = Counter()
    nine_negative = sum_positive = None
    for L in range(5, 322, 2):
        for i in range(3, L):
            word = '7' * (L - i - 1) + '5' + '7' * (i - 1) + '5'
            n = int(word)
            S = sum(map(int, word))
            P = prod(map(int, word))
            F = 7 * 10 ** L - 18 * 10 ** i - 25
            require(F == 9 * n and S == 7 * L - 4 and P == 25 * 7 ** (L - 2), 'literal identity')
            require((n % (P * S) == 0) == (F % (225 * S * 7 ** (L - 2)) == 0), 'original predicate')
            require(nmod(L, i, S) == n % S, 'literal sum modulus')
            require(nmod(L, i, 343) == n % 343, 'literal seven modulus')
            if i % 6 == 3 and S % 5 and S % 3 == 0 and F % S == 0 and n % S and nine_negative is None:
                nine_negative = dict(L=L, i=i, word=word, S=S, F_mod_S=0, F_mod_9S=F % (9*S), n_mod_S=n % S)
            if n % S == 0:
                counts['sum_pass'] += 1
                if S % 3 == 0 and S % 5 and sum_positive is None:
                    sum_positive = dict(L=L, i=i, word=word, S=S, n_mod_S=0)
            counts['words'] += 1
            counts['full_witnesses'] += n % (P*S) == 0
    require(nine_negative is not None and sum_positive is not None, 'nonvacuous controls')
    return dict(counts=dict(counts), factor_nine_negative=nine_negative, positive_sum=sum_positive)


def order(S):
    x = 10 % S
    d = 1
    while x != 1:
        x = x * 10 % S
        d += 1
        require(d <= S, 'order termination')
    return d


def general_class_checks():
    comparisons = 0
    actual_classes = 0
    for L in range(5, 160, 2):
        S = 7 * L - 4
        if S % 5 == 0:
            continue
        d, actual = order(S), [i for i in range(3, L) if nmod(L, i, S) == 0 and i % 6 == 3]
        D = lcm(d, 6)
        if not actual:
            continue
        s = actual[0] % D
        if s < 3:
            s += ((3-s+D-1)//D)*D
        M = (L-1-s)//D
        require(actual == [s+D*h for h in range(M+1)], 'complete bounded sum class')
        c = 1 + valuation(D, 7)
        for m in range(1, 6):
            modulus = 7 ** m
            G = pow(10, D, modulus)
            Y = (7 * pow(10, L, modulus)-25) * pow(18 * pow(10,s,modulus), -1, modulus) % modulus
            Q = 7 ** max(0, m-c)
            require(pow(G, Q, modulus)==1, 'period divides')
            if Q>1:
                require(pow(G,Q//7,modulus)!=1, 'exact period')
            roots = [h for h in range(Q) if pow(G,h,modulus)==Y]
            compatible = Y % (7 ** min(m,c)) == 1
            require(len(roots) == int(compatible), 'shallow/deep compatibility')
            for h in range(M+1):
                require((Fmod(L,s+D*h,modulus)==0) == (bool(roots) and h%Q==roots[0]), 'bounded class equivalence')
                comparisons += 1
        actual_classes += 1
    # Force all shallow branches, including c>K-like abstract controls.
    subgroup_controls = 0
    for e in range(4):
        D = 6 * 7**e
        c = e+1
        for m in range(1,6):
            modulus, Q = 7**m, 7**max(0,m-c)
            G = pow(10,D,modulus)
            cycle = {pow(G,h,modulus) for h in range(Q)}
            require(len(cycle)==Q, 'subgroup size')
            for Y in range(1,modulus):
                require((Y in cycle)==(Y % 7**min(c,m)==1), 'all units membership')
                subgroup_controls += 1
    return dict(actual_classes=actual_classes,bounded_comparisons=comparisons,subgroup_controls=subgroup_controls)


def deadline_controls():
    # Synthetic unit targets, explicitly not claims of decimal witnesses.
    records = []
    for L in (9,15,31):
        K, i = Kof(L), 3
        for t in (L-3,L-2):
            # 18*10^i+7^t is a unit target whose difference at i has exact v7=t.
            target = 18 * 10**i + 7**t
            r = next(z for z in range(6) if (target-18*pow(10,z,7))%7==0)
            period = 6
            first = None
            for j in range(1,t+1):
                modulus = 7**(j+1)
                lifts = [r+b*period for b in range(7)
                         if (target-18*pow(10,r+b*period,modulus))%modulus==0]
                require(len(lifts)==1,'unique synthetic lift')
                next_r = lifts[0]
                if j>=K and next_r!=r and first is None:
                    first=j
                if j==K-1:
                    require(next_r==i,'synthetic actual r_K')
                r,period=next_r,period*7
            require(first==t,'exact first change index')
            require((target-18*10**i)%(7**(L-2))==0 if t==L-2 else (target-18*10**i)%(7**(L-2))!=0, 'deadline sides')
            records.append(dict(L=L,i=i,t=t,K=K,first_change=first,passes_seven_threshold=t>=L-2))
    return records


def main():
    control = family(25)
    require((control['L'],control['i'],control['t'])==(121041229921,40582608819,2),'inherited positive control')
    cases = []
    previous = control
    for a in range(31,794,6):
        previous = family(a, previous)
        cases.append(previous)
    require(len(cases)==128 and all(row['L']>B for row in cases),'exact requested coverage')
    transitions=[]
    for left,right in zip([control]+cases,cases):
        a,S,L=left['a'],left['S'],left['L']
        require(right['L']-L==104*S,'length recurrence')
        require(pow(10,right['L'],9*S)==pow(10,L,9*S),'two extra powers of three')
        delta=right['s']-left['s']
        require(delta%left['D']==0 and 0<=delta//left['D']<=728,'compatible position classes')
        transitions.append(dict(a=a,next_a=right['a'],class_digit=delta//left['D']))
    counts=Counter(row['outcome'] for row in cases)
    histogram=Counter(str(row['t']) for row in cases if row['i'] is not None)
    result=dict(status='PASS',base_main=BASE,source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
        coverage=dict(first_a=31,last_a=793,step=6,count=128,first_L=cases[0]['L'],last_L=cases[-1]['L'],
                      whole_length_endpoint_inclusive=B,new_consecutive_lengths=0),
        counts=dict(counts),actual_valuation_histogram=dict(sorted(histogram.items())),
        cases=cases,control_a25=control,transitions=transitions,
        literal_checks=literal_checks(),general_classes=general_class_checks(),deadline_controls=deadline_controls(),
        full_witness_found=False,global_escape_proved=False,new_Lean_verification=False)
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
