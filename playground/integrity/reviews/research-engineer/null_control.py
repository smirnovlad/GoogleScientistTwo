"""Checks of the statistics behind IR-12/IR-14 (null-idea control) and IR-31 (planted corpus).
Deterministic: every simulation uses a fixed seed. Pure standard library."""
import math, random, statistics as st

def phi(x):  # standard normal pdf
    return math.exp(-x*x/2)/math.sqrt(2*math.pi)
def Phi(x):  # standard normal cdf
    return 0.5*(1+math.erf(x/math.sqrt(2)))

def emax(m, lo=-10, hi=10, n=200000):
    """E and SD of the max of m iid N(0,1), by numerical integration."""
    h=(hi-lo)/n; e=e2=0.0
    for i in range(n+1):
        x=lo+i*h; w=0.5 if i in (0,n) else 1.0
        f=m*phi(x)*Phi(x)**(m-1)
        e+=w*x*f*h; e2+=w*x*x*f*h
    return e, math.sqrt(e2-e*e)

print("== order statistics of m iid N(0,1)")
for m in (2,4,9,10,20,30,40):
    e,s=emax(m); print(f"m={m:3d}  E[max]={e:.4f}  SD[max]={s:.4f}")

print("\n== single-run decidability of the null control (m=20, unit noise)")
for t in (0.5,1.0,1.5):
    fp=1-Phi(t)            # guarded arm (report gain ~ N(0,1)) exceeds t: control wrongly fails
    fn=Phi(t)**20          # unguarded arm (max of 20) falls below t: control wrongly passes
    print(f"threshold {t}: P(guarded > t)={fp:.3f}  P(unguarded max20 < t)={fn:.4f}")

print("\n== replications R needed so both arms separate at 3 SE")
e20,s20=emax(20)
for R in (1,10,30,100,1000):
    print(f"R={R:5d}: SE guarded mean={1/math.sqrt(R):.3f}  SE unguarded mean={s20/math.sqrt(R):.3f}")

print("\n== fit-seed (artifact) noise carried from search to report by selection")
# score_i,split = a_i + e_i,split ; a_i shared by both splits (artifact), e independent per split
rng=random.Random(20261002)
def sim(sig_a, sig_e, m=20, R=20000, k=1):
    # k seeds averaged per row: artifact noise sd sig_a/sqrt(k); eval noise per split sig_e/sqrt(k)
    sa=sig_a/math.sqrt(k); se=sig_e/math.sqrt(k)
    rep=[]; srch=[]
    for _ in range(R):
        best=None
        for i in range(m):
            a=rng.gauss(0,sa); s=a+rng.gauss(0,se)
            if best is None or s>best[0]: best=(s,a)
        srch.append(best[0]); rep.append(best[1]+rng.gauss(0,se))
    return st.mean(srch), st.mean(rep)
for sa,se in ((0.0,1.0),(0.5,1.0),(1.0,1.0),(1.0,0.5),(1.0,0.2)):
    s,r=sim(sa,se)
    print(f"sigma_artifact={sa} sigma_eval={se}: mean search gain of winner={s:.3f}, mean REPORT gain={r:.3f} "
          f"(theory {sa**2/math.sqrt(sa**2+se**2)*e20 if sa+se>0 else 0:.3f})")
s,r=sim(1.0,0.5,k=5); print(f"same (1.0,0.5) but 5 seeds averaged per row: search={s:.3f} report={r:.3f}")

print("\n== success rule at the null: P(report gain > 0) and a one-sided test")
print("P(gain>0 | null) = 0.5 ; P(gain > 1.645*SE | null) = %.3f" % (1-Phi(1.645)))

print("\n== IR-31 planted-corpus sizing")
z=1.959964
n=z*z*0.25/0.1**2; print(f"Wald worst case, half-width 0.10: n={n:.2f} -> {math.ceil(n)}")
for h in (0.05,):
    n=z*z*0.25/h**2; print(f"Wald worst case, half-width {h}: n={n:.1f} -> {math.ceil(n)}")
def wilson(k,n,z=1.959964):
    p=k/n; d=1+z*z/n; c=(p+z*z/(2*n))/d; w=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return c-w, c+w
for k,n in ((0,97),(2,97),(48,97),(97,97),(18,20),(0,20)):
    lo,hi=wilson(k,n); print(f"Wilson 95% for {k}/{n}: [{lo:.3f}, {hi:.3f}]")
# per-kind split of 97 positives into 3 kinds
n3=97/3; print(f"97 split over 3 attack kinds ~{n3:.0f} each: worst-case Wald half-width {z*math.sqrt(0.25/n3):.3f}")
# false-positive rate near 1 percent, half-width 0.5 percent
n=z*z*0.01*0.99/0.005**2; print(f"FPR ~1%, half-width 0.5%: clean items n={n:.0f}")
# rule of three: zero events in n -> 95% upper bound ~3/n
for n in (97,300): print(f"0 misses in {n}: one-sided 95% upper bound ~ {1-0.05**(1/n):.4f}")

print("\n== power cost of carving a fraction f of the official test set into search")
for f in (0.1,0.2,0.3,0.5):
    print(f"f={f}: report SE x{1/math.sqrt(1-f):.3f}; minimal detectable effect x{1/math.sqrt(1-f):.3f}")
