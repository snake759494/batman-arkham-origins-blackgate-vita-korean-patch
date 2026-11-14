"""Rebuild ozzy.psp2arc (Korean) from the original archive.

usage: python tools/build.py <original ozzy.psp2arc> <output ozzy.psp2arc>
fonts/: NanumSquareNeo-bRg.ttf, NanumSquareNeo-cBd.ttf, NanumSquareNeo-dEb.ttf
"""
import sys, os, json, tempfile
sys.path.insert(0, os.path.dirname(__file__))
import psarc, locbuild, fontbuild, psarc_patch
R = os.path.join(os.path.dirname(__file__), '..')
src, out = sys.argv[1], sys.argv[2]
ko = json.load(open(os.path.join(R, 'text', 'ko.json'), encoding='utf8'))
f = open(src, 'rb'); t = psarc.read_toc(f)
names = psarc.read_entry(f, t, t['ents'][0]).decode('utf8').split('\n')
idx = {n: i + 1 for i, n in enumerate(names)}
def get(p): return psarc.read_entry(f, t, t['ents'][idx[p]])
rep = {}
for fn, tr in ko.items():
    p = '/ozzy/loc/_vta/' + fn
    rep[p] = locbuild.rebuild(get(p), tr)
chars = sorted(set(c for d in ko.values() for v in d.values() for s in v for c in s if 0xAC00 <= ord(c) <= 0xD7A3))
print('hangul', len(chars))
FONTS = {  # name: (ttf, advance delta, space advance)
    'bm_game':            ('NanumSquareNeo-bRg.ttf', -1, 5),
    'linefeed':           ('NanumSquareNeo-bRg.ttf', -1, 8),
    'chainprinter_small': ('NanumSquareNeo-bRg.ttf', -1, 6),
    'chainprinter':       ('NanumSquareNeo-cBd.ttf', -1, 8),
    'voxbold':            ('NanumSquareNeo-dEb.ttf', 0, 6),
    'bm_header':          ('NanumSquareNeo-dEb.ttf', -3, 14),
}
tmp = tempfile.mkdtemp()
for fn, (ttf, ad, sp) in FONTS.items():
    pc, pt = '/ozzy/fonts/_vta/%s.cfon' % fn, '/ozzy/fonts/_vta/_vta/%s.ctxr' % fn
    ic, it, oc, ot = [os.path.join(tmp, x) for x in ('i.cfon', 'i.ctxr', 'o.cfon', 'o.ctxr')]
    open(ic, 'wb').write(get(pc)); open(it, 'wb').write(get(pt))
    print(fn, fontbuild.build(ic, it, os.path.join(R, 'fonts', ttf), chars, oc, ot, adv_delta=ad, space=sp))
    rep[pc] = open(oc, 'rb').read(); rep[pt] = open(ot, 'rb').read()
    for x in (ic, it, oc, ot): os.remove(x)
os.rmdir(tmp); f.close()
psarc_patch.patch(src, out, rep)
print('written', out, len(rep), 'files')
