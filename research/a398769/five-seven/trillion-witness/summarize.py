#!/usr/bin/env python3
"""Package a completed primary TSV; arithmetic is checked by independent/ separately."""
import argparse,collections,csv,gzip,hashlib,json
from pathlib import Path

def require(ok,message):
    if not ok:raise ValueError(message)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('stream',type=Path)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--first',type=int,default=1000000000001)
    ap.add_argument('--count',type=int,default=1000000)
    args=ap.parse_args()
    require(args.first>=5 and args.first%2 and args.count>0,'scope domain')
    counts=collections.Counter({k:0 for k in ('outside','five','sum_fail','joint')})
    depths=collections.Counter();zeros=collections.Counter();maxima=[];maxd=-1;n=0;ks=set()
    with args.stream.open() as f:
        for r in csv.DictReader(f,delimiter='\t'):
            L=int(r['L']);require(L==args.first+2*n,'gap-free endpoints');n+=1
            require(r['category'] in counts,'category');counts[r['category']]+=1;ks.add(int(r['K']))
            if r['depth']!='-':
                d=int(r['depth']);depths[d]+=1;zeros[d-int(r['K'])]+=1
                require(d<L-2,'full seven condition not rejected; investigate candidate')
                if d>maxd:maxd=d;maxima=[]
                if d==maxd:maxima.append({k:int(v) if v.isdigit() else v for k,v in r.items()})
    require(n==args.count,'length count')
    raw=args.stream.read_bytes();packed=gzip.compress(raw,compresslevel=9,mtime=0)
    args.output.mkdir(parents=True,exist_ok=True)
    (args.output/'contiguous.tsv.gz').write_bytes(packed)
    source=Path(__file__).with_name('scan.cpp')
    r={'status':'NO WITNESS IN THE STATED SEARCH','first_odd':args.first,
       'last_odd':args.first+2*(n-1),'odd_lengths':n,'K_values':sorted(ks),
       'categories':dict(counts),'exact_depth_histogram_all_actual':dict(sorted(depths.items())),
       'zero_lift_histogram_all_actual':dict(sorted(zeros.items())),
       'greatest_exact_depth':maxd,'all_greatest_depth_pairs':maxima,
       'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
       'stream_sha256':hashlib.sha256(raw).hexdigest(),
       'gzip_sha256':hashlib.sha256(packed).hexdigest(),
       'uncompressed_bytes':len(raw),'compressed_bytes':len(packed)}
    (args.output/'contiguous.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:r[k] for k in ('status','odd_lengths','categories','greatest_exact_depth')},sort_keys=True))

if __name__=='__main__':main()
