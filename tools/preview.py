import sys,os,struct,numpy as np
from PIL import Image
sys.path.insert(0,os.path.dirname(__file__)); import cfon,fontbuild
def render(cf,tx,lines,scale=2):
    F=cfon.Font(open(cf,'rb').read()); img,W,H=fontbuild.decode(open(tx,'rb').read())
    size=struct.unpack('>f',F.hdr[12:16])[0]; lh=int(size*1.3)
    wmax=max(sum(F.recs[F.cmap.get(c,F.cmap[' '])][1] for c in l) for l in lines)+10
    out=Image.new('RGB',(wmax,lh*len(lines)+10),(70,70,90))
    for li,l in enumerate(lines):
        x=5;y=5+li*lh
        for c in l:
            g=F.cmap.get(c)
            if g is None: x+=8; continue
            r=F.recs[g]; x0,y0,x1,y1=round(r[4]*W),round(r[5]*H),round(r[6]*W),round(r[7]*H)
            cell=Image.fromarray(img[y0:y1,x0:x1])
            if cell.width and cell.height:
                bgc=Image.new('RGBA',cell.size,(0,0,0,0)); 
                rgb=Image.fromarray(img[y0:y1,x0:x1,:3]); a=Image.fromarray(img[y0:y1,x0:x1,3])
                blk=Image.new('RGB',cell.size,(0,0,0)); comp=Image.composite(rgb,blk,Image.fromarray(np.maximum(img[y0:y1,x0:x1,0],0)))
                out.paste(blk,(x+r[0],y+r[2]),a); out.paste(Image.new('RGB',cell.size,(255,255,255)),(x+r[0],y+r[2]),Image.fromarray(img[y0:y1,x0:x1,0]))
            x+=r[1]
    return out.resize((out.width*scale,out.height*scale),Image.NEAREST)
