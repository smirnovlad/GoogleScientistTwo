"""Closure checks of the second version's statistics. Fixed seeds; standard library only."""
import math, random
def binom_cdf(k,n,p): return sum(math.comb(n,i)*p**i*(1-p)**(n-i) for i in range(k+1))
def cp_upper(x,n,a=0.05):  # one-sided Clopper-Pearson upper bound, by bisection
    if x==n: return 1.0
    lo,hi=0.0,1.0
    for _ in range(100):
        mid=(lo+hi)/2
        if binom_cdf(x,n,mid)>a: lo=mid
        else: hi=mid
    return (lo+hi)/2
print("== IR-31.3 / IR-31.6 one-sided 95% CP upper bounds")
for x,n in ((0,59),(0,99),(0,299),(0,97),(1,97),(2,97),(5,20),(6,20),(10,30),(11,30),(18,50),(19,50)):
    print(f"{x}/{n}: {cp_upper(x,n):.4f}")

rng=random.Random(11)
def chi2(k): return sum(rng.gauss(0,1)**2 for _ in range(k))
print("\n== IR-4.3 power: paired t, n=5, effect 4 SD of per-seed difference, two-sided alpha 0.01 (t>4.604)")
R=200000; hit=0
for _ in range(R):
    d=[4+rng.gauss(0,1) for _ in range(5)]
    m=sum(d)/5; s=math.sqrt(sum((x-m)**2 for x in d)/4)
    hit+= abs(m/(s/math.sqrt(5)))>4.604
print(f"power ~ {hit/R:.4f}; P(>=95 of 100 flagged) ~ {1-binom_cdf(94,100,hit/R):.4f}")

print("\n== IR-3.6 control: 100 honest rows against ONE baseline variance estimate (s=5), q=0.0626")
R=20000; ge5=0; counts=[]
for _ in range(R):
    sb=chi2(4)/4
    c=sum((chi2(4)/4)/sb<0.0626 for _ in range(100))
    counts.append(c); ge5+= c>=5
print(f"P(>=5 honest flagged) correlated = {ge5/R:.4f}  (independent binomial: {1-binom_cdf(4,100,0.01):.4f}); mean flagged {sum(counts)/R:.2f}")

print("\n== IR-23.2: per-row two-sided 3-sigma rate, P(>=3 of 100)")
p=math.erfc(3/math.sqrt(2)); print(f"p={p:.5f}, P(>=3)={1-binom_cdf(2,100,p):.5f}")

print("\n== IR-8.1 repeat count: n=ceil((3s/d)^2) per row; SE of the DIFFERENCE of two row means")
for ratio in (1,2,5):  # d/sigma
    n=math.ceil((3/ratio)**2); se=math.sqrt(2/n)
    print(f"delta={ratio} sigma: n={n}, 3*SE(diff)={3*se:.3f} sigma vs delta={ratio}; needed n={math.ceil(2*(3/ratio)**2)}")

print("\n== null control 'no re-fit' arm: prediction from E[max_m] vs regression on the arm's own search gain")
print("E[max20]*1/(sqrt5*sqrt2) =", round(1.8675/(math.sqrt(5)*math.sqrt(2)),4), "; selection on report:", round(1.8675*math.sqrt(2/5),4))
# a loop that is NOT a single max: subset gate (keep if subset score>0), then max of survivors' full-set score
def loop(R=40000, m=10, s=5):
    sa=1/math.sqrt(s); se=1/math.sqrt(s); out_s=out_r=0.0
    for _ in range(R):
        best=None
        for i in range(m):
            a=rng.gauss(0,sa)
            sub=a+rng.gauss(0,se)*math.sqrt(2)      # subset: fewer items, more eval noise
            if sub<=0: continue
            full=a+rng.gauss(0,se)                   # full-set search score, fresh eval draw
            if best is None or full>best[0]: best=(full,a)
        if best is None: best=(0.0,0.0)
        out_s+=best[0]; out_r+=best[1]+rng.gauss(0,se)
    return out_s/R, out_r/R
s_,r_=loop(); e10=1.5388
print(f"gated loop, m=10: search gain {s_:.3f}, no-refit report gain {r_:.3f}; E[max_m] formula {e10/(math.sqrt(5)*math.sqrt(2)):.3f}; 0.5*own search gain {0.5*s_:.3f}")
