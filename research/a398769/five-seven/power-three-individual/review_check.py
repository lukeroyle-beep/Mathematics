#!/usr/bin/env python3
"""Independent exact-commit computational review and retained receipt checker."""
import argparse
from copy import deepcopy
from hashlib import sha256
import importlib.util
import json
from math import gcd
import os
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BASE = 'a9edeb0a96bd56d55f3c96767f5154e69cb8ceda'
IMPLEMENTATION = '561cd96effccc9362255ac6c766445fafaec3145'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(data):
    return sha256(data).hexdigest()


def load(name):
    return json.loads((HERE/name).read_text())


def git(*args):
    return subprocess.check_output(['git',*args],cwd=ROOT)


def repunit_word(L, s, modulus):
    """Original 7*repunit minus the two changed digits; retain division by9."""
    need(0<s<L and modulus>0,'actual word range')
    numerator=(pow(10,L,9*modulus)-1)%(9*modulus)
    need(numerator%9==0,'repunit division remains exact')
    return (7*(numerator//9)-2-2*pow(10,s,modulus))%modulus


def independent_rows():
    primary=load('root_log.json')['cases']
    blocks=load('independent_decimal.json')['rows']
    expected=[25]+list(range(31,100,6))+[1231,1567,1573,1579]
    need([r['a'] for r in primary]==[r['a'] for r in blocks]==expected,'all17 members')
    fields=('a','L','S','d','D','s','i','actual','s_mod_126','g','q','t',
            'first_fail_depth','first_fail_n_residue','n_mod_S','n_mod_25S','seven_residues')
    result=[]
    for x,y in zip(primary,blocks):
        need(all(x[k]==y[k] for k in fields),'independent shared row fields')
        a,L,s,S,d=x['a'],x['L'],x['s'],x['S'],x['d']
        need(S==3**a and 7*L==S+4 and d==3**(a-2) and 3<=s<2*d and s%6==3,'exact class data')
        # Entire joint class: the exact order d and odd representative modulo2d.
        need(pow(10,d,S)==1 and pow(10,d//3,S)!=1 and L<2*d,'unique actual class domain')
        target=((7*(pow(10,L,9*S)-1)//9-2)*pow(2,-1,S))%S
        need(pow(10,s,S)==target,'independent digit-sum class readback')
        need(x['actual']==(3<=s<L),'actuality')
        row=dict(a=a,actual=x['actual'])
        if not x['actual']:
            need(s>=L and x['i'] is None and x['t'] is None,'class miss has no original word')
        else:
            g=gcd(L,s)
            need(x['g']==g and x['q']==L//g and x['p']==s//g,'independent gcd')
            need((7*x['q']*(s%d)-4*x['p'])%d==0,'ternary rational relation')
            need(repunit_word(L,s,25*S)==0,'original n mod25S')
            vals=[repunit_word(L,s,7**m) for m in range(1,x['first_fail_depth']+1)]
            need(vals==[0]*x['t']+[x['first_fail_n_residue']]==x['seven_residues'],'repunit residues')
            need(vals[-1]!=0 and len(vals)==x['t']+1<=L-2,'inclusive full-witness deadline')
            row.update(g=g,t=x['t'],n_mod_25S=0,original_residues=vals)
        result.append(row)
    # Literal original predicate, independent of both submitted implementations.
    L,s=313,51
    digits=[7]*L;digits[0]=digits[s]=5
    n=sum(digit*10**i for i,digit in enumerate(digits))
    S=sum(digits);P=1
    for digit in digits:P*=digit
    F=7*10**L-18*10**s-25
    need(F==9*n and S==2187 and P==25*7**311,'literal predicate coefficients')
    need(n%(P*S)!=0 and F%(9*P*S)!=0,'literal full predicate disproved')
    need((F%S,F%(9*S),n%S)==(0,17496,1944),'literal lost-nine negative')
    return result


def deep_permutations():
    # L_(u+1)=729L_u-416, independently of the supplied modular-power engine.
    m=6;modulus=7**m;order=6*7**(m-2);period=7**(m-2)
    results=[]
    for s in (39,81,123,165,207,249,291):
        L=(3**31+4)//7
        images=[];zeros=[]
        for u in range(period):
            F=(7*pow(10,L,modulus)-18*pow(10,s,modulus)-25)%modulus
            need(F%49==0,'fixed-s depth two')
            images.append(F//49)
            if F==0:zeros.append(u)
            L=(729*L-416)%order
        need(sorted(images)==list(range(period)) and len(zeros)==1,'complete depth-six permutation')
        # Independently test all 7 children at each depth, no derivative formula.
        r,step=0,1
        for depth in range(3,m+1):
            children=[]
            for c in range(7):
                u=r+c*step
                exact_L=(3**(31+6*u)+4)//7
                if (7*pow(10,exact_L,7**depth)-18*pow(10,s,7**depth)-25)%7**depth==0:
                    children.append(u)
            need(len(children)==1,'direct seven-child lift')
            r=children[0];step*=7
        need(zeros==[r],'independent permutation and direct lifting agree')
        results.append(dict(s=s,depth=m,indices=period,root=r))
    return results


def aggregate_corruptions():
    spec=importlib.util.spec_from_file_location('reviewed_aggregate',HERE/'verify.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    values=[load(name) for name in ('root_log.json','independent_decimal.json','math-checks.json','index_lift.json')]
    names=module.corruption_checks(values)
    # Coordinated changes to both engines must also fail, not only disagreement.
    for label in ('coordinated_zero_residue','coordinated_false_range'):
        p,b,m,i=deepcopy(values)
        if label=='coordinated_zero_residue':
            for row in (p['cases'][-1],b['rows'][-1]):
                row['first_fail_n_residue']=0;row['seven_residues']=[0,0]
        else:
            for rows in (p['cases'],b['rows']):
                next(row for row in rows if row['a']==1573)['actual']=True
        try:module.compare(p,b,m,i)
        except (ValueError,TypeError):names.append(label)
        else:raise ValueError('coordinated invalid evidence accepted')
    return names


def build():
    subprocess.run(['git','merge-base','--is-ancestor',BASE,IMPLEMENTATION],cwd=ROOT,check=True)
    subprocess.run(['git','merge-base','--is-ancestor',IMPLEMENTATION,'HEAD'],cwd=ROOT,check=True)
    paths=git('diff','--name-only',BASE,IMPLEMENTATION).decode().splitlines()
    need(paths and all(p=='README.md' or p.startswith('research/a398769/five-seven/power-three-individual/') for p in paths),'bounded implementation diff')
    bound={}
    for path in paths:
        committed=git('show',IMPLEMENTATION+':'+path)
        need((ROOT/path).read_bytes()==committed,'implementation changed since review: '+path)
        bound[path]=digest(committed)
    command=[sys.executable]+(['-O'] if sys.flags.optimize else [])+[str(HERE/'verify.py'),'--run']
    subprocess.run(command,cwd=ROOT,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),check=True,stdout=subprocess.DEVNULL)
    review_files=['COMPUTATIONAL_REVIEW.md','MATH_REVIEW.md','review_check.py']
    return dict(schema='a398769-individual-final-review-v1',status='PASS',
                base_main=BASE,reviewed_implementation_commit=IMPLEMENTATION,
                builder_context='/root',reviewer_context='/root/final_computational_review',
                implementation_sha256=bound,
                review_only_sha256={name:digest((HERE/name).read_bytes()) for name in review_files},
                independent_repunit_rows=independent_rows(),
                independent_depth_six_permutations=deep_permutations(),
                corruption_controls_rejected=aggregate_corruptions(),
                common_factor_theorem='separate independent mathematical review',
                individual_family='OPEN',named_excluded_family_lengths=259,
                next_individual_exponent=1585,whole_length_endpoint_inclusive=1000002000000,
                unrestricted_five_seven='OPEN',wider_digit_one='OPEN',Lean_verification_performed=False)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write',action='store_true')
    args=parser.parse_args()
    result=build()
    if args.write:(HERE/'review-checks.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    else:need(result==load('review-checks.json'),'retained review evidence')
    print('PASS: exact-commit independent computational review; 17 rows, seven depth-six permutations, 11 corruptions')


if __name__=='__main__':main()
