import struct
def rv(b,p):
    ln=0; sh=0
    while True:
        c=b[p]; p+=1; ln|=(c&0x7f)<<sh; sh+=7
        if not c&0x80: return ln,p
def wv(ln):
    o=bytearray()
    while True:
        c=ln&0x7f; ln>>=7
        if ln: o.append(c|0x80)
        else: o.append(c); return bytes(o)
def parse(b):
    assert b[:4]==b'LOCL'
    hdr=b[:0x20]; n=struct.unpack('>I',b[0x1c:0x20])[0]; p=0x20; recs=[]
    for i in range(n):
        t=struct.unpack('>I',b[p:p+4])[0]; p+=4; segs=[]
        for j in range(t):
            ln,p=rv(b,p); s=b[p:p+ln].decode('utf8'); p+=ln
            segs.append([s,b[p:p+8]]); p+=8
        recs.append(segs)
    return hdr,recs,b[p:]
def build(hdr,recs,tail):
    out=bytearray(hdr[:0x1c]+struct.pack('>I',len(recs)))
    for segs in recs:
        out+=struct.pack('>I',len(segs))
        for s,ex in segs:
            e=s.encode('utf8'); out+=wv(len(e))+e+ex
    return bytes(out+tail)
def tables(tail):
    nl,nk=struct.unpack('>II',tail[:8]); v=struct.unpack('>%dI'%(nl*nk*2),tail[8:8+nl*nk*8])
    tb=[[(v[(l*nk+k)*2],v[(l*nk+k)*2+1]) for k in range(nk)] for l in range(nl)]
    return nl,nk,tb,tail[8+nl*nk*8:]
