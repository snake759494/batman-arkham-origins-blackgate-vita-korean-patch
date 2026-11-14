import struct, io, numpy as np
from PIL import Image
def morton(x,y,w,h):
    # vita swizzle on block grid (square-ish morton)
    m=min(w,h); k=0; idx=0; bit=0
    i=0
    while (1<<i) < m:
        idx |= ((y>>i)&1)<<(2*i) | ((x>>i)&1)<<(2*i+1); i+=1
    if w>h: idx |= (x>>i)<<(2*i)
    elif h>w: idx |= (y>>i)<<(2*i)
    return idx
def dds(data,w,h,fourcc=b'DXT5'):
    hd=struct.pack('<4sIIIIIII44xII4sIIIII5I',b'DDS ',124,0x81007,h,w,len(data),0,1,32,4,fourcc,0,0,0,0,0,0x1000,0,0,0,0)
    return Image.open(io.BytesIO(hd+data))
def unswz(data,w,h,bs=16):
    bw,bh=w//4,h//4; out=bytearray(len(data))
    for y in range(bh):
        for x in range(bw):
            s=morton(x,y,bw,bh)*bs; d=(y*bw+x)*bs
            out[d:d+bs]=data[s:s+bs]
    return bytes(out)
def swz(data,w,h,bs=16):
    bw,bh=w//4,h//4; out=bytearray(len(data))
    for y in range(bh):
        for x in range(bw):
            d=morton(x,y,bw,bh)*bs; s=(y*bw+x)*bs
            out[d:d+bs]=data[s:s+bs]
    return bytes(out)
