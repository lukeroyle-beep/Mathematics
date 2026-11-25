#!/usr/bin/env python3
"""Declared finite arithmetic searches for a counterexample to broad E.

No inherited witness filters are used. This standalone implementation does
not import either audit checker. All checks survive python -O.
"""
import hashlib
import json
from math import gcd
from pathlib import Path

HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def threshold(length):
    k, period = 1, 6
    while period <= length:
        k += 1
        period *= 7
    return k, period


def representative(length):
    k, period = threshold(length)
    final_modulus = 7**k
    target = (7*pow(10,length,final_modulus)-25) % final_modulus
    r, m, step = 3, 7, 6
    value = pow(10,r,final_modulus)
    generator = pow(10,step,final_modulus)
    for _ in range(1,k):
        next_m=7*m
        y=18*(value%next_m)
        b=target%next_m
        require((b-y)%m==0, 'incoming lift precision')
        g=generator%next_m
        require((g-1)%m==0, 'generator precision')
        c=(g-1)//m
        require(c%7!=0, 'nonzero lift coefficient')
        digit=((b-y)//m)*pow(y*c,-1,7)%7
        r+=digit*step
        value=value*pow(generator,digit,final_modulus)%final_modulus
        generator=pow(generator,7,final_modulus)
        m,step=next_m,7*step
    require(step==period and 0<=r<period, 'least representative')
    require((7*pow(10,length,m)-18*pow(10,r,m)-25)%m==0,
            'independent final power congruence')
    return k,r


def geometric(length, modulus):
    """Return 10**length and repunit R_length modulo modulus, without /9."""
    power, repunit = 1, 0
    for bit in bin(length)[2:]:
        repunit = repunit*(power+1) % modulus
        power = power*power % modulus
        if bit == '1':
            repunit = (10*repunit+1) % modulus
            power = 10*power % modulus
    return power, repunit


def fmod(length, position, modulus):
    return (7*pow(10,length,modulus)-18*pow(10,position,modulus)-25)%modulus


def classify(length):
    k, r = representative(length)
    s = 7*length-4
    if not 3 <= r < length:
        return [length, k, r, 'outside', None]
    rem = fmod(length,r,9*s)
    independent_n = (7*geometric(length,s)[1]-2-2*pow(10,r,s))%s
    require(rem == 9*independent_n, 'independent full-sum recurrence')
    category = 'excluded_five' if s%5==0 else ('pass' if rem==0 else 'fail')
    return [length,k,r,category,rem]


def certify(length, position):
    s=7*length-4
    k,_=threshold(length)
    require(length>=5 and length%2==1 and 3<=position<length and s%5!=0,
            'counterexample broad domain')
    require(fmod(length,position,9*s)==0, 'full digit sum')
    t=k
    require(fmod(length,position,7**t)==0, 'certified uniqueness depth')
    while fmod(length,position,7**(t+1))==0:
        t+=1
        require(t<k+100, 'depth resource limit: unresolved')
    nmod=(7*geometric(length,7**(t+1))[1]-2-2*pow(10,position,7**(t+1)))%(7**(t+1))
    require(9*nmod % (7**(t+1))==fmod(length,position,7**(t+1)),
            'independent exact depth')
    require(t<=length-3, 'possible full witness requires separate full-divisor verification')
    m=7**t; step=6*7**(t-1)
    y=18*pow(10,position,7*m)
    b=7*pow(10,length,7*m)-25
    c=(pow(10,step,7*m)-1)//m
    digit=((b-y)//m)*pow(y*c,-1,7)%7
    return {'L':length,'i':position,'S':s,'K':k,'exact_depth':t,
            'F_mod_9S':0,'F_mod_7t':0,'F_mod_7t_plus_1':fmod(length,position,7**(t+1)),
            'n_mod_S_by_geometric_sum':0,'n_mod_7t_plus_1':nmod,
            'preceding_zero_lifts':t-k,'first_nonzero_lift':digit,
            'lifted_representative':position+digit*step}


def controls():
    for length in range(5,42,2):
        require(geometric(length,7*length-4)[1] == ((10**length-1)//9)%(7*length-4),
                'literal repunit control')
        k,r=representative(length)
        m=7**k
        hits=[i for i in range(6*7**(k-1)) if (7*10**length-18*pow(10,i,m)-25)%m==0]
        require(hits==[r], 'complete power-cycle control')
    return {'literal_lengths':19,'complete_cycle_lengths':19}


def main():
    scope=json.loads((HERE/'search_scope.json').read_text())
    require(scope['recorded_before_execution'], 'scope record required')
    result={'scope_sha256':hashlib.sha256((HERE/'search_scope.json').read_bytes()).hexdigest(),
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'controls':controls(),'families':{},'counterexamples':[]}
    all_seen={}
    smooth=scope['families'][0]
    candidates=set()
    generated=0
    for p in smooth['p']:
        for a in range(smooth['a_inclusive'][0],smooth['a_inclusive'][1]+1):
            for b in range(smooth['b_inclusive'][0],smooth['b_inclusive'][1]+1):
                generated+=1
                s=3**a*p**b
                if s>=31 and s%7==3 and ((s+4)//7)%2==1 and s%5!=0:
                    candidates.add((s+4)//7)
    def evaluate(name, lengths, extra):
        counts={'outside':0,'excluded_five':0,'fail':0,'pass':0}
        digest=hashlib.sha256()
        for length in sorted(lengths):
            row=all_seen.get(length)
            if row is None:
                row=classify(length)
                all_seen[length]=row
            counts[row[3]]+=1
            digest.update((':'.join('-' if x is None else str(x) for x in row)+'\n').encode())
            if row[3]=='pass' and not any(x['L']==length for x in result['counterexamples']):
                result['counterexamples'].append(certify(length,row[2]))
        result['families'][name]={'candidate_lengths':len(lengths),'minimum_L':min(lengths) if lengths else None,
                                 'maximum_L':max(lengths) if lengths else None,'counts':counts,
                                 'ordered_results_sha256':digest.hexdigest(),**extra}
    evaluate('smooth_sum_powers',candidates,{'raw_parameter_pairs':generated})
    cycle=scope['families'][1]
    candidates=set(); raw_pairs=0;generated_sums=0; useful=[]
    for d in range(cycle['d_inclusive'][0],cycle['d_inclusive'][1]+1):
        powers=[10**x for x in range(d)]
        modulus=10**d-1
        for a in range(d):
            for b in range(d):
                raw_pairs+=1
                s=gcd(7*powers[a]-18*powers[b]-25,modulus)
                while s%7==0:
                    s//=7
                while True:
                    generated_sums+=1
                    if s>=31 and s%7==3 and s%5!=0:
                        length=(s+4)//7
                        if length%2==1 and length%d==a:
                            candidates.add(length)
                            if length>9999999:
                                useful.append({'d':d,'a':a,'b':b,'S':s,'L':length})
                    if s%3:
                        break
                    s//=3
    evaluate('complete_cycle_gcd',candidates,{'raw_exponent_pairs':raw_pairs,'generated_sums_with_duplicates':generated_sums,
                                           'beyond_audit_generators':useful})
    result['distinct_lengths_total']=len(all_seen)
    result['beyond_audit_distinct_lengths']=sum(x>9999999 for x in all_seen)
    result['scope_complete']=True
    print(json.dumps(result,sort_keys=True,indent=2))


if __name__=='__main__':
    main()
