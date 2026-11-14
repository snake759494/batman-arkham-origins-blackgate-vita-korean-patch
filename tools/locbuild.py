import sys,os,struct
sys.path.insert(0,os.path.dirname(__file__)); import cloc
def rebuild(b, ko):
    """ko: {key:[segs]}; JP & EN columns both point to Korean strings (timings from JP record)."""
    h,r,t=cloc.parse(b); nl,nk,tb,rest=cloc.tables(t)
    recs=[list(x) for x in r]
    pool={}  # dedupe by (text tuple, timing tuple)
    new=[]
    keyidx=[]
    for k in range(nk):
        ki,ei=tb[0][k]; _,ji=tb[1][k]
        key=r[ki][0][0]; src=r[ji]
        if key in ko:
            segs=[[s,ex] for s,(_,ex) in zip(ko[key],src)]
        else:
            segs=[list(x) for x in src]
        new.append((ki,segs))
    # build record list: keep keys at their indices, then append strings
    out=[]; remap={}
    keys=sorted(set(ki for ki,_ in new))
    for ki in keys: remap[ki]=len(out); out.append(r[ki])
    tab=[]
    for ki,segs in new:
        sig=tuple((s,bytes(ex)) for s,ex in segs)
        if sig not in pool: pool[sig]=len(out); out.append([[s,ex] for s,ex in segs])
        tab.append((remap[ki],pool[sig]))
    tail=struct.pack('>II',2,nk)
    for l in range(2):
        for a,bb in tab: tail+=struct.pack('>II',a,bb)
    return cloc.build(h,out,tail)
