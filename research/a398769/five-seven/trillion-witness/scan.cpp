// Exact finite representative search. C++17, unsigned 128-bit products.
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
using U = std::uint64_t;
using W = __uint128_t;
static void need(bool ok, const char* why) { if (!ok) throw std::runtime_error(why); }
static U mul(U a,U b,U m) { return W(a)*b%m; }
static U power(U a,U e,U m) { U r=1; for(;e;e>>=1,a=mul(a,a,m)) if(e&1) r=mul(r,a,m); return r; }
static U fmod(U L,U i,U m) { return (W(7)*power(10,L,m)+W(19)*m-W(18)*power(10,i,m)-25)%m; }
int main(int argc,char**argv) { try {
  need(argc==3,"usage: scan FIRST_ODD COUNT");
  std::size_t p=0; U first=std::stoull(argv[1],&p); need(p==std::string(argv[1]).size(),"first parse");
  U count=std::stoull(argv[2],&p); need(p==std::string(argv[2]).size(),"count parse");
  need(first>=5 && first%2 && count>0 && count<=10000000,"range domain");
  need(first<=4000000000000ULL && 2*(count-1)<=4000000000000ULL-first,"range resource bound");
  U q[23],T[23],c[23]; q[0]=1;
  for(int k=1;k<=22;++k) {q[k]=7*q[k-1];T[k]=6*q[k-1];}
  for(int k=1;k<22;++k) {U v=power(10,T[k],q[k+1]);need(v%q[k]==1,"order lift");c[k]=(v-1)/q[k];need(c[k]%7!=0,"primitive lift");}
  const U low=7; std::vector<int> log(q[low],-1); U v=1;
  for(U r=0;r<T[low];++r){need(log[v]<0,"duplicate low log");log[v]=r;v=v*10%q[low];} need(v==1,"low cycle closure");
  const U inverse[7]={0,1,4,5,2,3,6};
  U tenL[23];for(int k=1;k<=22;++k)tenL[k]=power(10,first,q[k]);
  std::cout<<"L\tK\tr\tcategory\tdepth\tF_mod_9S\tF_mod_7_next\tnext_lift\n";
  for(U j=0;j<count;++j){
    U L=first+2*j,S=7*L-4; int K=1;while(T[K]<=L)++K;
    int k=1;U r=3;
    if(K>=int(low)) { U m=q[low];U B=(W(7)*tenL[low]+m-25)%m;U inv18=power(18,T[low]-1,m);int lr=log[mul(B,inv18,m)];need(lr>=0,"unit log");r=lr;k=low; }
    for(;k<K;++k){U m=q[k],M=q[k+1],y=mul(18,power(10,r,M),M),B=(W(7)*tenL[k+1]+M-25)%M;
      U d=(B+M-y)%M;need(d%m==0,"incoming congruence");U a=(d/m)*inverse[(y%7)*c[k]%7]%7;r+=a*T[k];
    }
    need(r<T[K] && fmod(L,r,q[K])==0,"final representative");
    if(r<3 || r>=L) std::cout<<L<<'\t'<<K<<'\t'<<r<<"\toutside\t-\t-\t-\t-\n";
    else {
      U rem=fmod(L,r,9*S);int d=K;
      while(d<22 && fmod(L,r,q[d+1])==0)++d;
      need(d<22,"depth guard exhausted: unresolved, not excluded");U next=fmod(L,r,q[d+1]);
      need(next && next%q[d]==0,"exact depth");
      U y=mul(18,power(10,r,q[d+1]),q[d+1]);
      U a=(next/q[d])*inverse[(y%7)*c[d]%7]%7;need(a>0,"nonzero lift");
      const char* cat=S%5==0?"five":rem?"sum_fail":"joint";
      std::cout<<L<<'\t'<<K<<'\t'<<r<<'\t'<<cat<<'\t'<<d<<'\t'<<rem<<'\t'<<next<<'\t'<<a<<'\n';
      if(std::string(cat)=="joint")std::cerr<<"JOINT "<<L<<' '<<r<<" depth "<<d<<'\n';
    }
    for(int z=1;z<=22;++z)tenL[z]=mul(tenL[z],100,q[z]);
  }
  return 0;
} catch(const std::exception&e) {std::cerr<<e.what()<<'\n';return 1;} }
