#!/usr/bin/env python3
"""Independent review of the declared smooth family by trial-digit lifts."""
import hashlib,json
from pathlib import Path

def check(ok,msg):
 if not ok:raise RuntimeError(msg)

def recover(L):
 k,T=1,6
 while T<=L:k+=1;T*=7
 M=7**k
 target=(7*pow(10,L,M)-25)*pow(18,-1,M)%M
 r,m,t=3,7,6
 value=pow(10,r,M);generator=pow(10,t,M)
 for depth in range(1,k):
  target_next=target%(7*m)
  trial=value;matches=[]
  for digit in range(7):
   if trial%(7*m)==target_next:matches.append((digit,trial))
   trial=trial*generator%M
  check(len(matches)==1,'trial digit not unique')
  digit,value=matches[0]
  r+=digit*t;m*=7;t*=7;generator=pow(generator,7,M)
 check(t==T and m==M and 0<=r<T,'period/representative')
 check(pow(10,r,M)==target,'final congruence')
 return k,r

def main():
 HERE=Path(__file__).resolve().parent
 receipt=json.loads((HERE/'search.json').read_text())
 check(hashlib.sha256((HERE/'search.py').read_bytes()).hexdigest()==receipt['source_sha256'],
       'reviewed search source hash')
 check(hashlib.sha256((HERE/'search_scope.json').read_bytes()).hexdigest()==receipt['scope_sha256'],
       'reviewed search scope hash')
 lengths=set()
 for p in (17,898129):
  for a in range(201):
   for b in range(41):
    S=3**a*p**b
    if S>=31 and S%7==3 and (S+4)//7%2==1 and S%5:
     lengths.add((S+4)//7)
 digest=hashlib.sha256();counts={'outside':0,'excluded_five':0,'fail':0,'pass':0}
 for L in sorted(lengths):
  k,r=recover(L);S=7*L-4
  if not 3<=r<L:category='outside';residue='-'
  else:
   u=pow(10,L,9*S)
   check(u%9==1,'exact integer division of modular residue')
   R=(u-1)//9
   n=(7*R-2-2*pow(10,r,S))%S
   residue=9*n
   category='excluded_five' if S%5==0 else ('pass' if n==0 else 'fail')
  counts[category]+=1
  digest.update(f'{L}:{k}:{r}:{category}:{residue}\n'.encode('ascii'))
 expected=receipt['families']['smooth_sum_powers']
 check(len(lengths)==expected['candidate_lengths'],'length count')
 check(counts==expected['counts'],'partition counts')
 check(digest.hexdigest()==expected['ordered_results_sha256'],'ordered digest')
 print(json.dumps({'status':'PASS','method':'trial all seven lift digits; repunit via exact division of10^Lmod9S minus1','lengths':len(lengths),'counts':counts,'ordered_results_sha256':digest.hexdigest(),'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'search_source_sha256':receipt['source_sha256'],'search_scope_sha256':receipt['scope_sha256']},indent=2,sort_keys=True))
if __name__=='__main__':main()
