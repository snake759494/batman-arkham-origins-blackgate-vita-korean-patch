import struct
class Font:
    def __init__(s,b):
        s.raw=b; s.hdr=b[:0x14]; n=struct.unpack('>I',b[16:20])[0]
        s.recs=[list(struct.unpack('>4b4f',b[0x14+i*20:0x28+i*20])) for i in range(n)]
        p=0x14+n*20
        def arr(p,sz,fmt):
            c=struct.unpack('>I',b[p:p+4])[0]; return list(struct.unpack('>%d%s'%(c,fmt),b[p+4:p+4+c*sz])),p+4+c*sz
        s.ascii,p=arr(p,2,'H')
        s.i2,p=arr(p,2,'H'); c2,p=arr(p,2,'H')
        s.i3,p=arr(p,2,'H'); c3,p=arr(p,4,'I')
        s.c2=[x.to_bytes(2,'big').decode('utf8') for x in c2]
        s.c3=[x.to_bytes(4,'big')[1:].decode('utf8') for x in c3]
        s.tail=b[p:]
        s.cmap={chr(i):g for i,g in enumerate(s.ascii)}
        s.cmap.update(zip(s.c2,s.i2)); s.cmap.update(zip(s.c3,s.i3))
    def build(s):
        o=bytearray(s.hdr[:16]+struct.pack('>I',len(s.recs)))
        for r in s.recs: o+=struct.pack('>4b4f',*r)
        def arr(l,fmt): return struct.pack('>I',len(l))+struct.pack('>%d%s'%(len(l),fmt),*l)
        o+=arr(s.ascii,'H')+arr(s.i2,'H')+arr([int.from_bytes(c.encode(),'big') for c in s.c2],'H')
        o+=arr(s.i3,'H')+arr([int.from_bytes(c.encode(),'big') for c in s.c3],'I')
        return bytes(o+s.tail)
