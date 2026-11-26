#!/usr/bin/env python3
"""Declared sparse high-depth search: sixteen odd samples per K=16..128."""
import hashlib,json
from pathlib import Path

def require(ok, message):
    if not ok: raise ValueError(message)

def residue(L, i, M):
    return (7*pow(10,L,M)-18*pow(10,i,M)-25)%M

def representative(L, K):
    r,m,T=3,7,6
    for k in range(1,K):
        M=7*m
        y=18*pow(10,r,M)%M
        b=(7*pow(10,L,M)-25)%M
        delta=(b-y)%M
        require(delta%m==0,'incoming congruence')
        c=(pow(10,T,M)-1)//m
        a=(delta//m)*pow(y*c,-1,7)%7
        r+=a*T;m=M;T*=7
    require(0<=r<T and residue(L,r,m)==0,'least logarithm')
    return r

def run():
    rows=[]
    for K in range(16,129):
        lo,hi=6*7**(K-2),6*7**(K-1)
        for j in range(16):
            L=lo+1+2*((j*(hi-lo-2))//30)
            require(lo<L<hi and L%2 and L>10**12,'sample band')
            i=representative(L,K);S=7*L-4
            row={'L':L,'i':i,'K':K,'band_sample':j,'actual':3<=i<L}
            if row['actual']:
                row['F_mod_9S']=residue(L,i,9*S)
                d=K
                while residue(L,i,7**(d+1))==0:
                    d+=1
                    require(d<K+128,'unresolved depth cap')
                row.update(depth=d,F_mod_7_next=residue(L,i,7**(d+1)),
                           category='five' if S%5==0 else 'sum_fail' if row['F_mod_9S'] else 'joint')
            else:row['category']='outside'
            rows.append(row)
    counts={key:sum(r['category']==key for r in rows) for key in ('outside','five','sum_fail','joint')}
    print(json.dumps({'status':'NO WITNESS IN THE STATED SEARCH' if not counts['joint'] else 'JOINT PAIRS REQUIRE INVESTIGATION',
                      'scope':{'K_first':16,'K_last':128,'samples_per_band':16,'L_formula':'6*7**(K-2)+1+2*floor(j*(6*7**(K-1)-6*7**(K-2)-2)/30), j=0..15'},
                      'length_count':len(rows),'categories':counts,'rows':rows,
                      'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2,sort_keys=True))

if __name__=='__main__':run()
