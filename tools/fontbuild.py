"""Rebuild a cfon/ctxr pair: replace kana/kanji glyph slots with Hangul glyphs."""
import sys, os, struct, numpy as np
from PIL import Image, ImageFont, ImageDraw, ImageFilter
sys.path.insert(0, os.path.dirname(__file__))
import cfon, ctxr

HDR = 0xC0

def is_cjk(c):
    o = ord(c)
    return 0x3040 <= o <= 0x30FF or 0x4E00 <= o <= 0x9FFF or c in '々〆〃'

# ---------------- DXT5 ----------------
def decode(tex):
    d = tex[HDR:]; W = 4096; H = len(d) // W
    im = ctxr.dds(ctxr.unswz(d, W, H), W, H).convert('RGBA')
    return np.array(im), W, H

def enc_blocks(px):
    """px: (N,16,4) uint8 -> (N,16) bytes DXT5"""
    N = px.shape[0]
    a = px[:, :, 3].astype(np.int32)
    a0 = a.max(1); a1 = a.min(1)
    pal = np.stack([a0, a1] + [((7 - i) * a0 + i * a1) // 7 for i in range(1, 7)], 1)  # 8 entries
    idx = np.abs(a[:, :, None] - pal[:, None, :]).argmin(2)
    same = a0 == a1; idx[same] = 0
    bits = np.zeros(N, np.uint64)
    for i in range(16): bits |= idx[:, i].astype(np.uint64) << np.uint64(3 * i)
    out = np.zeros((N, 16), np.uint8)
    out[:, 0] = a0; out[:, 1] = a1
    for i in range(6): out[:, 2 + i] = ((bits >> np.uint64(8 * i)) & np.uint64(255)).astype(np.uint8)
    # colour: treat as grey (use mean of rgb)
    l = px[:, :, :3].astype(np.int32).mean(2)
    lmax = l.max(1); lmin = l.min(1)
    def g565(v):
        v = np.clip(np.round(v), 0, 255).astype(np.int32)
        r = (v * 31 + 127) // 255; g = (v * 63 + 127) // 255
        return (r << 11) | (g << 5) | r, ((r << 3) | (r >> 2)), ((g << 2) | (g >> 4))
    c0, r0, g0 = g565(lmax); c1, r1, g1 = g565(lmin)
    # ensure c0 > c1 (4-colour mode)
    swap = c0 < c1
    c0, c1 = np.where(swap, c1, c0), np.where(swap, c0, c1)
    e0 = np.where(swap, (r1 + g1 + r1) / 3, (r0 + g0 + r0) / 3)
    e1 = np.where(swap, (r0 + g0 + r0) / 3, (r1 + g1 + r1) / 3)
    cp = np.stack([e0, e1, (2 * e0 + e1) / 3, (e0 + 2 * e1) / 3], 1)
    ci = np.abs(l[:, :, None] - cp[:, None, :]).argmin(2)
    eq = c0 == c1
    ci[eq] = 0
    cb = np.zeros(N, np.uint32)
    for i in range(16): cb |= ci[:, i].astype(np.uint32) << np.uint32(2 * i)
    out[:, 8] = c0 & 255; out[:, 9] = c0 >> 8; out[:, 10] = c1 & 255; out[:, 11] = c1 >> 8
    for i in range(4): out[:, 12 + i] = (cb >> np.uint32(8 * i)) & 255
    return out

def encode_region(tex, img, W, H, blocks):
    """re-encode given set of (bx,by) blocks from img into swizzled tex bytes"""
    tex = bytearray(tex); bw, bh = W // 4, H // 4
    bl = sorted(blocks)
    px = np.stack([img[by * 4:by * 4 + 4, bx * 4:bx * 4 + 4].reshape(16, 4) for bx, by in bl])
    enc = enc_blocks(px)
    for (bx, by), e in zip(bl, enc):
        o = HDR + ctxr.morton(bx, by, bw, bh) * 16
        tex[o:o + 16] = e.tobytes()
    return bytes(tex)

# ---------------- glyph render ----------------
def ink_bbox(arr):
    ys, xs = np.nonzero(arr > 64)
    if len(xs) == 0: return None
    return xs.min(), ys.min(), xs.max() + 1, ys.max() + 1

def build(cfon_path, ctxr_path, ttf, chars, out_cfon, out_ctxr, ref='漢', scale=1.0, bold=0, preview=None, adv_delta=0, space=None):
    F = cfon.Font(open(cfon_path, 'rb').read())
    tex = open(ctxr_path, 'rb').read()
    img, W, H = decode(tex)
    img_orig = img.copy()
    rr = F.recs[F.cmap[ref]]
    rx0, ry0, rx1, ry1 = round(rr[4] * W), round(rr[5] * H), round(rr[6] * W), round(rr[7] * H)
    rw0, rh0 = rx1 - rx0, ry1 - ry0
    ib0 = ink_bbox(img[ry0:ry1, rx0:rx1, 0])           # kanji ink box inside its cell
    hang = sorted(set(chars))
    cells = []
    for c, g in zip(F.c3, F.i3):
        if not is_cjk(c): continue
        r = F.recs[g]
        x0, y0, x1, y1 = round(r[4] * W), round(r[5] * H), round(r[6] * W), round(r[7] * H)
        cells.append((g, x0, y0, x1, y1))
    # largest uniform cell (<= reference cell) that still gives enough slots
    best = None
    for s in range(0, 12):
        for t in range(0, 12):
            cw, ch = rw0 - s, rh0 - t
            n = sum(1 for g, x0, y0, x1, y1 in cells if x1 - x0 >= cw and y1 - y0 >= ch)
            if n >= len(hang) + 8 and (best is None or cw * ch > best[0] * best[1]): best = (cw, ch)
    if best is None: raise SystemExit('not enough slots')
    rw, rh = best
    slots = [c for c in cells if c[3] - c[1] >= rw and c[4] - c[2] >= rh]
    dx, dy = (rw0 - rw) // 2, (rh0 - rh) // 2
    mx = max(1, min(ib0[0], rw0 - ib0[2])); my = max(1, min(ib0[1], rh0 - ib0[3]))
    mx = min(mx, max(1, (rw - (ib0[2] - ib0[0])) // 2 if rw < rw0 else mx)); my = min(my, max(1, (rh - (ib0[3] - ib0[1])) // 2 if rh < rh0 else my))
    ib = (mx, my, rw - mx, rh - my)
    ink_h = ib[3] - ib[1]; ink_w = ib[2] - ib[0]
    rr = list(rr); rr[0] += dx; rr[2] += dy
    # font size: make '한' ink height ~= kanji ink height * scale
    size = 8
    while True:
        f = ImageFont.truetype(ttf, size + 1); bb = f.getbbox('한')
        if bb[3] - bb[1] > ink_h * scale: break
        size += 1
    font = ImageFont.truetype(ttf, size)
    bb = font.getbbox('한')
    oy = ib[1] + (ink_h - (bb[3] - bb[1])) / 2 - bb[1]
    # clear every cjk slot (old glyphs not used anymore)
    dirty = set()
    def touch(x0, y0, x1, y1):
        for by in range(y0 // 4, (y1 + 3) // 4):
            for bx in range(x0 // 4, (x1 + 3) // 4): dirty.add((bx, by))
    for c, g in zip(F.c3, F.i3):
        if is_cjk(c):
            r = F.recs[g]; x0, y0, x1, y1 = round(r[4] * W), round(r[5] * H), round(r[6] * W), round(r[7] * H)
            img[y0:y1, x0:x1] = 0; touch(x0, y0, x1, y1)
    # mimic original alpha style, measured on Latin reference glyphs
    def cellof(c):
        r = F.recs[F.cmap[c]]; return img_orig[round(r[5]*H):round(r[7]*H), round(r[4]*W):round(r[6]*W)]
    ratios = [(cellof(c)[..., 3] > 128).sum() / max(1, (cellof(c)[..., 0] > 128).sum()) for c in 'BGMHOE' if c in F.cmap]
    outline = float(np.median(ratios)) > 1.3
    newmap = {}
    for ch, (g, x0, y0, x1, y1) in zip(hang, slots):
        cell = Image.new('L', (rw, rh), 0); d = ImageDraw.Draw(cell)
        gb = font.getbbox(ch); gw = gb[2] - gb[0]
        ox = ib[0] + (ink_w - gw) / 2 - gb[0]
        d.text((ox, oy), ch, font=font, fill=255)
        m = np.array(cell)
        if bold: m = np.array(Image.fromarray(m).filter(ImageFilter.MaxFilter(3)))
        if outline:
            a = np.maximum(np.array(Image.fromarray(m).filter(ImageFilter.MaxFilter(3))), m).astype(np.uint8)
        else:
            a = m.copy()
        blk = np.zeros((rh, rw, 4), np.uint8); blk[..., 0] = blk[..., 1] = blk[..., 2] = m; blk[..., 3] = a
        img[y0:y0 + rh, x0:x0 + rw] = blk
        r = F.recs[g]
        met = list(rr[:4]); met[1] += adv_delta
        F.recs[g] = met + [x0 / W, y0 / H, (x0 + rw) / W, (y0 + rh) / H]
        newmap[ch] = g
    if space is not None: F.recs[F.cmap[' ']][1] = space
    # rebuild 3-byte table: keep non-cjk entries, add hangul, sorted by codepoint
    ent = [(c, g) for c, g in zip(F.c3, F.i3) if not is_cjk(c)] + list(newmap.items())
    ent.sort(key=lambda x: ord(x[0]))
    F.c3 = [c for c, _ in ent]; F.i3 = [g for _, g in ent]
    open(out_cfon, 'wb').write(F.build())
    open(out_ctxr, 'wb').write(encode_region(tex, img, W, H, dirty))
    if preview is not None:
        Image.fromarray(img).save(preview)
    return size, len(hang), len(slots)
