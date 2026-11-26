#!/usr/bin/env python3
"""Restartable independent full enumeration with source- and bound-bound receipts."""
import argparse
import csv
import hashlib
import io
import json
import math
from pathlib import Path
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
BASE = '81dce203b1eecc61ec9fda36bc812095e2c89724'
BANDS = ((15,102,225,1000002000001,4069338437093),
         (16,143,256,4069338437095,28485369059657),
         (17,227,288,28485369059659,78999999999999))
CONTROL = (17,289,28485369059659,199397583417605)


def require(ok, why):
    if not ok:
        raise RuntimeError(why)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def targets():
    for k,low_b,high_b,low_l,high_l in BANDS:
        for b in range(low_b,high_b+1):
            yield (k,b,low_l,high_l)
    yield CONTROL


def name(target):
    return 'K%d-b%d.json' % target[:2]


def independently_count(k,b):
    nums = [a for a in range(1,b) if math.gcd(a,b)==1]
    raw = len(nums)*(2*k*k+1)
    compatible = sum((h-3*b+a)%(2*math.gcd(3,a))==0 for a in nums for h in range(-k*k,k*k+1))
    return len(nums),raw,compatible


def verify_receipt(receipt, target, source_hash):
    k,b,lo,hi = target
    for key,value in zip(('K','b','lo','hi'),target):
        require(receipt[key]==value, 'wrong bound '+key)
    require(receipt['depth']==13 and receipt['h_limit']==k*k, 'wrong search depth/radius')
    require(receipt['source_sha256']==source_hash, 'stale independent source')
    require(receipt['baseline_commit']==BASE, 'wrong baseline')
    expected = independently_count(k,b)
    actual = tuple(receipt[x] for x in ('reduced_numerators','raw_lines','compatible_lines'))
    require(expected==actual, 'independent labelled-line count disagreement')
    for key in ('pairs13_sha256','pairs22_sha256'):
        require(len(receipt[key])==64 and set(receipt[key])<=set('0123456789abcdef'), 'invalid SHA-256')
    require(len(receipt['survivors22'])==receipt['pairs22'], 'depth22 survivor retention')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output',type=Path,default=HERE/'receipts'/'independent')
    p.add_argument('--binary',type=Path)
    p.add_argument('--verify-only',action='store_true')
    args=p.parse_args()
    source=HERE/'independent.cpp'; source_hash=digest(source)
    planned=list(targets()); require(len(planned)==301 and len(set(planned))==301,'partition plan')
    args.output.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='a398769-independent-') as directory:
        scratch=Path(directory)
        binary=scratch/(args.binary.name if args.binary else 'independent')
        if not args.verify_only:
            subprocess.run(['c++','-O3','-std=c++17',str(source),'-o',str(binary)],check=True)
            if args.binary:
                require(digest(args.binary)==digest(binary),'supplied binary differs from freshly compiled source')
            binary_hash=digest(binary)
        for target in planned:
            destination=args.output/name(target)
            if destination.exists():
                verify_receipt(json.loads(destination.read_text()),target,source_hash)
                continue
            require(not args.verify_only,'missing partition '+destination.name)
            k,b,lo,hi=target
            pair_path,deep_path,raw_path=[scratch/x for x in ('pairs.csv','deep.csv','raw.json')]
            command=[str(binary),'--K',str(k),'--b',str(b),'--lo',str(lo),'--hi',str(hi),
                     '--pairs',str(pair_path),'--pairs22',str(deep_path),'--json',str(raw_path)]
            subprocess.run(command,check=True)
            receipt=json.loads(raw_path.read_text())
            pair_bytes=pair_path.read_bytes(); deep_bytes=deep_path.read_bytes()
            require(pair_bytes.count(b'\n')==receipt['pairs13'],'pair stream count')
            require(deep_bytes.count(b'\n')==receipt['pairs22'],'depth22 stream count')
            receipt.update(source_sha256=source_hash, baseline_commit=BASE,
                           pairs13_sha256=hashlib.sha256(pair_bytes).hexdigest(),
                           pairs22_sha256=hashlib.sha256(deep_bytes).hexdigest(),
                           survivors22=[list(map(int,row)) for row in csv.reader(io.StringIO(deep_bytes.decode()))],
                           command=['./independent','--K',str(k),'--b',str(b),'--lo',str(lo),'--hi',str(hi),
                                    '--pairs','pairs.csv','--pairs22','pairs22.csv','--json','result.json'],
                           binary_sha256=binary_hash, binary_source_binding='fresh compilation with c++ -O3 -std=c++17')
            verify_receipt(receipt,target,source_hash)
            temporary=destination.with_suffix('.tmp')
            temporary.write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
            temporary.replace(destination)
            print(json.dumps({'completed':destination.name,'pairs13':receipt['pairs13'],'pairs22':receipt['pairs22']}),flush=True)
            pair_path.unlink();deep_path.unlink();raw_path.unlink()
    actual_names={x.name for x in args.output.glob('*.json')}
    expected_names={name(x) for x in planned}
    require(actual_names==expected_names,'missing or unexpected partition files')
    results=[]
    for k,bl,bh,lo,hi in BANDS:
        rows=[json.loads((args.output/name(t)).read_text()) for t in planned if t[0]==k and bl<=t[1]<=bh]
        totals={field:sum(row[field] for row in rows) for field in ('raw_lines','compatible_lines','pairs13','fivefree13','sum13','pairs22','fivefree22','sum22')}
        results.append(dict(K=k,partitions=len(rows),**totals))
    result={'status':'PASS','partitions':300,'control_partitions':1,'source_sha256':source_hash,'bands':results,
            'receipt_sha256':{filename:digest(args.output/filename) for filename in sorted(actual_names)}}
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':
    main()
