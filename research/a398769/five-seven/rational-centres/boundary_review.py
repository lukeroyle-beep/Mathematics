#!/usr/bin/env python3
"""Fresh reviewer boundary coverage checks; independent of author control programs.

Uses literal original decimal words on small intervals and direct modular
arithmetic on short intervals straddling giant endpoints. No search-code imports.
All checks survive Python -O. Review-only artifact; does not replace full runs.
"""
import csv
import hashlib
import json
import math
from pathlib import Path
import random
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
REVIEWED_COMMIT = "9eaa913f515e62667dbf706ec723043c5b0a193c"
EXPECTED_SOURCES = {
    "primary.cpp": "df836b0630320b9607047d3d06222eef85eeb8eab7559cd37f4d0fa6da6303c4",
    "independent.cpp": "01df856047ba73f5c279f8b0ca8e203c9443242f9f24a7c8d1b2ebb0e652772c",
}


def small_intervals(root):
    rng=random.Random(398769)
    cases=[(4,b,lo,hi,d) for b in (2,8,9,15,50,51,98,99) for lo,hi in ((5,5),(6,6),(6,19),(9,9),(10,10),(10,101)) for d in (1,2,4)]
    cases += [(rng.choice([1,2,4,7,15,19]), rng.choice(list(range(2,65))+[99,100,101,102,225,256,288,289,361]), lo,lo+rng.randrange(160),rng.randrange(1,7)) for lo in (rng.randrange(5,900) for _ in range(90))]
    counts=dict(cases=0,pair_occurrences=0,singular7_occurrences=0,singular49_occurrences=0,h_zero=0,h_lower=0,h_upper=0,even_endpoint_cases=0,singletons=0)
    digest=hashlib.sha256()
    for K,b,lo,hi,d in cases:
     expected=[];sum_count=free_count=0
     for L in range(lo,hi+1):
      if L%2==0:continue
      for i in range(3,L,6):
       word='7'*(L-i-1)+'5'+'7'*(i-1)+'5';n=int(word)
       if n%7**d:continue
       for a in range(max(1,(b*i-K*K+L-1)//L),min(b-1,(b*i+K*K)//L)+1):
        if math.gcd(a,b)!=1:continue
        h=b*i-a*L;expected.append((a,h,L,i))
        counts['singular7_occurrences']+=a%7==0
        counts['singular49_occurrences']+=a%49==0
        counts['h_zero']+=h==0;counts['h_lower']+=h==-K*K;counts['h_upper']+=h==K*K
        S=sum(map(int,word))
        if S%5:free_count+=1;sum_count+=n%S==0
     expected.sort()
     for engine in ('primary','independent'):
      command=[str(root/engine),'--K',str(K),'--b',str(b),'--lo',str(lo),'--hi',str(hi),'--pairs',str(root/'pairs.csv'),'--pairs22',str(root/'deep.csv'),'--json',str(root/'receipt.json')]
      if engine=='primary':command+=['--depth','22','--at',str(d)]
      else:command+=['--depth',str(d)]
      p=subprocess.run(command,text=True,capture_output=True)
      if p.returncode:raise RuntimeError((engine,K,b,lo,hi,d,p.stderr))
      actual=[tuple(map(int,row)) for row in csv.reader((root/'pairs.csv').open())]
      if actual!=expected:raise RuntimeError((engine,K,b,lo,hi,d,'different',set(actual)-set(expected),set(expected)-set(actual)))
      receipt=json.loads((root/'receipt.json').read_text())
      if (receipt['pairs13'],receipt['fivefree13'],receipt['sum13'],receipt['pairs22'])!=(len(expected),free_count,sum_count,0):raise RuntimeError(('counts',engine,K,b,lo,hi,d))
     counts['cases']+=1;counts['pair_occurrences']+=len(expected);counts['even_endpoint_cases']+=(lo%2==0 or hi%2==0);counts['singletons']+=lo==hi
     digest.update((str((K,b,lo,hi,d))+'\n').encode());digest.update(('\n'.join(','.join(map(str,r)) for r in expected)+'\n').encode())
    return dict(status='PASS',**counts,sha256=digest.hexdigest())


def giant_intervals(root):
    cases=[]
    for K,bs,anchors in [(15,(102,147,225),(1000002000001,4069338437093)),(16,(143,196,256),(4069338437095,28485369059657)),(17,(227,287,288,289),(28485369059659,78999999999999,199397583417605))]:
     for b in bs:
      for lo in anchors:
       for d in (1,3):cases.append((K,b,lo-1,lo+8,d))
    digest=hashlib.sha256();total=singular=sumpos=0
    for K,b,lo,hi,d in cases:
     expected=[];free=passed=0
     for L in range(lo,hi+1):
      if not L%2:continue
      for a in range(1,b):
       if math.gcd(a,b)!=1:continue
       h=-K*K+((-a*L+K*K)%b)
       while h<=K*K:
        i=(a*L+h)//b
        if 3<=i<L and i%6==3 and (7*pow(10,L,7**d)-18*pow(10,i,7**d)-25)%7**d==0:
         expected.append((a,h,L,i));singular+=a%7==0;S=7*L-4
         if S%5:
          free+=1
          nmod=(7*((pow(10,L,9*S)-1)//9)-2-2*pow(10,i,S))%S
          passed+=nmod==0
        h+=b
     expected.sort()
     for engine in ('primary','independent'):
      cmd=[str(root/engine),'--K',str(K),'--b',str(b),'--lo',str(lo),'--hi',str(hi),'--pairs',str(root/'pairs.csv'),'--pairs22',str(root/'deep.csv'),'--json',str(root/'receipt.json')]
      cmd+=['--depth','22','--at',str(d)] if engine=='primary' else ['--depth',str(d)]
      subprocess.run(cmd,check=True)
      actual=[tuple(map(int,row)) for row in csv.reader((root/'pairs.csv').open())]
      if actual!=expected:raise RuntimeError((engine,K,b,lo,hi,d,'pairs'))
      r=json.loads((root/'receipt.json').read_text())
      if (r['pairs13'],r['fivefree13'],r['sum13'],r['pairs22'])!=(len(expected),free,passed,0):raise RuntimeError((engine,K,b,lo,hi,d,'counts'))
     total+=len(expected);sumpos+=passed
     digest.update((str((K,b,lo,hi,d))+'\n').encode());digest.update(('\n'.join(','.join(map(str,r)) for r in expected)+'\n').encode())
    return dict(status='PASS',cases=len(cases),pairs=total,singular=singular,sum_passes=sumpos,sha256=digest.hexdigest())


def main():
    hashes = {name: hashlib.sha256((HERE/name).read_bytes()).hexdigest()
              for name in EXPECTED_SOURCES}
    if hashes != EXPECTED_SOURCES:
        raise RuntimeError("Reviewed implementation source changed")
    with tempfile.TemporaryDirectory(prefix="a398769-boundary-review-") as directory:
        root = Path(directory)
        for engine in ("primary", "independent"):
            subprocess.run(["clang++", "-O2", "-std=c++17", str(HERE/(engine+".cpp")),
                            "-o", str(root/engine)], check=True)
        small = small_intervals(root)
        giant = giant_intervals(root)
    print(json.dumps({"status": "PASS", "reviewed_implementation_commit": REVIEWED_COMMIT,
                      "source_sha256": hashes, "small_intervals": small,
                      "giant_endpoint_intervals": giant}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
