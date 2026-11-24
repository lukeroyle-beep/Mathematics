"""Exact quotient enumeration; use --run to check the counted candidates."""
import argparse
from itertools import combinations_with_replacement, product
from math import gcd, prod

def search(length, width=5, restricted=None, perform=False):
    if not 1 <= length <= 23:
        raise ValueError('length must be between 1 and 23')
    if not 1 <= width <= length:
        raise ValueError('suffix width must be between 1 and length')
    if restricted is not None and (len(restricted) != length or
                                   any(d not in '13579' for d in restricted)):
        raise ValueError('multiset must contain exactly length digits from 13579')
    alphabet='3579' if restricted is None else ''.join(sorted(set(restricted)))
    suffixes=[]
    if restricted is None:
        for suffix in product(alphabet,repeat=width):
            suffixes.append((int(''.join(suffix)), tuple(suffix.count(d) for d in alphabet)))
    else:
        limits = tuple(restricted.count(d) for d in alphabet)
        used = [0] * len(alphabet)
        def suffix_tree(remaining, value):
            if remaining == 0:
                suffixes.append((value,tuple(used)))
                return
            for i,d in enumerate(alphabet):
                if used[i] < limits[i]:
                    used[i] += 1
                    suffix_tree(remaining-1,10*value+int(d))
                    used[i] -= 1
        suffix_tree(width,0)
    hits=set(); checked=0; nsets=0
    multisets = combinations_with_replacement(alphabet,length) if restricted is None else [tuple(sorted(restricted))]
    for digits in multisets:
        nsets+=1
        counts=tuple(digits.count(d) for d in alphabet)
        s=sum(map(int,digits));p=prod(map(int,digits));D=s*p
        lo=(int(''.join(digits))+D-1)//D
        hi=int(''.join(reversed(digits)))//D
        if lo>hi: continue
        g9=gcd(D,9)
        if s%g9: continue
        m9=9//g9
        r9=((s//g9)*pow(D//g9,-1,m9))%m9
        g=gcd(D,10**width)
        period=(10**width)//g
        inverse=pow(D//g,-1,period)
        period_inv=pow(period,-1,m9)
        stride=period*m9
        for tail,quota in suffixes:
            if tail%g or any(x>y for x,y in zip(quota,counts)):continue
            r0=(tail//g)*inverse%period
            residue=r0+period*((r9-r0)*period_inv%m9)
            start=lo+(residue-lo)%stride
            if start>hi: continue
            checked+=(hi-start)//stride+1
            if perform:
                for q in range(start,hi+1,stride):
                    value=D*q;word=str(value)
                    if all(word.count(d)==c for d,c in zip(alphabet,counts)):
                        assert value%(sum(map(int,word))*prod(map(int,word)))==0
                        assert value not in hits
                        hits.add(value)
    print(length,width,nsets,checked,sorted(hits) if perform else 'NOT_CHECKED',flush=True)
if __name__=='__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('length', type=int)
    parser.add_argument('width', type=int, help='number of final decimal places to constrain')
    parser.add_argument('--multiset', help='one exact multiset of odd digits, allowing 1 for controls')
    parser.add_argument('--run', action='store_true', help='check all candidate integers')
    args = parser.parse_args()
    try:
        search(args.length, args.width, restricted=args.multiset, perform=args.run)
    except ValueError as exc:
        parser.error(str(exc))
