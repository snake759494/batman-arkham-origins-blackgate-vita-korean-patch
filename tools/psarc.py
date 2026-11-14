import struct, zlib, sys, os
def read_toc(f):
    f.seek(0)
    h=f.read(32)
    magic,ver,comp,toclen,esz,n,bs,flags=struct.unpack('>4sI4sIIIII',h)
    toc=f.read(toclen-32)
    ents=[]
    for i in range(n):
        e=toc[i*esz:(i+1)*esz]
        md5=e[:16]; blk=struct.unpack('>I',e[16:20])[0]
        usz=int.from_bytes(e[20:25],'big'); off=int.from_bytes(e[25:30],'big')
        ents.append([md5,blk,usz,off])
    nb_bytes=2 if bs<=0x10000 else 3
    rest=toc[n*esz:]
    nblk=len(rest)//nb_bytes
    zs=[int.from_bytes(rest[i*nb_bytes:(i+1)*nb_bytes],'big') for i in range(nblk)]
    return dict(ver=ver,comp=comp,toclen=toclen,esz=esz,n=n,bs=bs,flags=flags,ents=ents,zs=zs)
def read_entry(f,t,e):
    md5,blk,usz,off=e; bs=t['bs']; out=bytearray(); f.seek(off); i=blk
    while len(out)<usz:
        z=t['zs'][i]; i+=1
        if z==0: out+=f.read(bs); continue
        d=f.read(z)
        if d[:2] in (b'\x78\xda',b'\x78\x9c',b'\x78\x01',b'\x78\x5e'):
            try: out+=zlib.decompress(d); continue
            except Exception: pass
        out+=d
    return bytes(out[:usz])
if __name__=='__main__':
    src,dst=sys.argv[1],sys.argv[2]
    f=open(src,'rb'); t=read_toc(f)
    names=read_entry(f,t,t['ents'][0]).decode('utf8').split('\n')
    print(t['n'],len(names),hex(t['bs']))
    only=sys.argv[3] if len(sys.argv)>3 else None
    for nm,e in zip(names,t['ents'][1:]):
        if only and only not in nm.lower(): continue
        p=os.path.join(dst,nm.lstrip('/'))
        os.makedirs(os.path.dirname(p),exist_ok=True)
        open(p,'wb').write(read_entry(f,t,e))
