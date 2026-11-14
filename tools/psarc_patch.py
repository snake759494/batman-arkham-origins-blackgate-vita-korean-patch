"""Write a patched PSARC: original data kept verbatim, replaced files appended at the end."""
import struct, zlib, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import psarc

def patch(src, dst, repl):
    """repl: {'/ozzy/...path': bytes}"""
    f = open(src, 'rb'); t = psarc.read_toc(f)
    names = psarc.read_entry(f, t, t['ents'][0]).decode('utf8').split('\n')
    idx = {n: i + 1 for i, n in enumerate(names)}
    bs = t['bs']; zs = list(t['zs']); ents = [list(e) for e in t['ents']]
    f.seek(0, 2); end = f.tell()
    newdata = bytearray()
    for name, data in repl.items():
        i = idx[name]
        blk0 = len(zs); off_rel = len(newdata)
        for p in range(0, max(len(data), 1), bs):
            raw = data[p:p + bs]
            c = zlib.compress(raw, 9)
            if len(c) < len(raw):
                newdata += c; zs.append(len(c))
            else:
                newdata += raw; zs.append(0 if len(raw) == bs else len(raw))
        ents[i][1] = blk0; ents[i][2] = len(data); ents[i][3] = ('NEW', off_rel)
    nb = 2 if bs <= 0x10000 else 3
    toclen = 32 + len(ents) * t['esz'] + len(zs) * nb
    delta = toclen - t['toclen']
    datastart = end + delta
    toc = bytearray()
    for md5, blk, usz, off in ents:
        if isinstance(off, tuple): o = datastart + off[1]
        else: o = off + delta
        toc += md5 + struct.pack('>I', blk) + usz.to_bytes(5, 'big') + o.to_bytes(5, 'big')
    for z in zs: toc += z.to_bytes(nb, 'big')
    f.seek(0); hdr = bytearray(f.read(32))
    struct.pack_into('>I', hdr, 12, toclen)
    with open(dst, 'wb') as o:
        o.write(hdr); o.write(toc)
        f.seek(t['toclen'])
        while True:
            b = f.read(1 << 24)
            if not b: break
            o.write(b)
        o.write(newdata)
    f.close()
