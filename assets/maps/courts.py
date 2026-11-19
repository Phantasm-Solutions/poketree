import os, random, sys
from PIL import Image, ImageDraw

# Draws the court surfaces on the Poketree palette (batch 1.4): flat, lightly textured
# surfaces with exact white lines. Writes assets/raw/courts/*.png.
# Usage: python assets/maps/courts.py <repo root>
root = sys.argv[1]
out_dir = os.path.join(root, "assets/raw/courts")
os.makedirs(out_dir, exist_ok=True)
pal = [h for h in open(os.path.join(root, "assets/palette.hex")).read().split() if len(h) == 6]
C = {h: tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (255,) for h in pal}
WHITE, NET = C["ffffff"], C["1e2430"]
T = 32


def surface(w, h, base, speckles, seed, stripes=None):
    """Base colour plus sparse palette speckles; optional mowing stripes (every `stripes` px)."""
    rnd = random.Random(seed)
    im = Image.new("RGBA", (w, h), C[base])
    px = im.load()
    for y in range(h):
        for x in range(w):
            if stripes and (x // stripes) % 2:
                px[x, y] = C[stripes_alt]
            r = rnd.random()
            acc = 0.0
            for col, p in speckles:
                acc += p
                if r < acc:
                    px[x, y] = C[col]
                    break
    return im


def rect(d, x0, y0, x1, y1, col=WHITE, w=2):
    d.rectangle([x0, y0, x1, y1], outline=col, width=w)


def line(d, pts, col=WHITE, w=2):
    d.line(pts, fill=col, width=w)


def tennis(name, base, speck, seed):
    # 5 x 9 tiles incl. run-off; doubles court 10.97 x 23.77 m drawn at ~9.76 px/m
    W, H = 5 * T, 9 * T
    im = surface(W, H, base, speck, seed)
    d = ImageDraw.Draw(im)
    s = 232 / 23.77
    cw, ch = round(10.97 * s), 232
    x0, y0 = (W - cw) // 2, (H - ch) // 2
    x1, y1 = x0 + cw - 1, y0 + ch - 1
    rect(d, x0, y0, x1, y1)
    inset = round(1.37 * s)
    line(d, [(x0 + inset, y0), (x0 + inset, y1)])
    line(d, [(x1 - inset, y0), (x1 - inset, y1)])
    mid = (y0 + y1) // 2
    sv = round(6.40 * s)
    line(d, [(x0 + inset, mid - sv), (x1 - inset, mid - sv)])
    line(d, [(x0 + inset, mid + sv), (x1 - inset, mid + sv)])
    line(d, [((x0 + x1) // 2, mid - sv), ((x0 + x1) // 2, mid + sv)])
    line(d, [((x0 + x1) // 2, y0), ((x0 + x1) // 2, y0 + 4)])
    line(d, [((x0 + x1) // 2, y1 - 4), ((x0 + x1) // 2, y1)])
    # net and posts
    line(d, [(x0 - 6, mid), (x1 + 6, mid)], NET, 2)
    d.rectangle([x0 - 8, mid - 2, x0 - 5, mid + 2], fill=NET)
    d.rectangle([x1 + 5, mid - 2, x1 + 8, mid + 2], fill=NET)
    im.save(os.path.join(out_dir, name + ".png"))


def padel():
    # 3 x 5 tiles; 10 x 20 m court with glass walls
    W, H = 3 * T, 5 * T
    im = surface(W, H, "2f86c8", [("1f5f99", 0.04), ("4fb3e6", 0.03)], 3)
    d = ImageDraw.Draw(im)
    rect(d, 0, 0, W - 1, H - 1, C["9be0f5"], 3)          # glass walls
    s = (H - 16) / 20
    x0, y0, x1, y1 = 8, 8, W - 9, H - 9
    rect(d, x0, y0, x1, y1)
    mid = (y0 + y1) // 2
    sv = round(6.95 * s)
    line(d, [(x0, mid - sv), (x1, mid - sv)])
    line(d, [(x0, mid + sv), (x1, mid + sv)])
    line(d, [((x0 + x1) // 2, mid - sv), ((x0 + x1) // 2, mid + sv)])
    line(d, [(x0 - 4, mid), (x1 + 4, mid)], NET, 2)
    im.save(os.path.join(out_dir, "padel.png"))


def multi_court():
    # 10 x 6 tiles; basketball 28 x 15 m
    W, H = 10 * T, 6 * T
    im = surface(W, H, "2f5fa8", [("1f5f99", 0.05), ("2f86c8", 0.02)], 4)
    d = ImageDraw.Draw(im)
    s = (W - 32) / 28
    x0, y0 = 16, (H - round(15 * s)) // 2
    x1, y1 = W - 17, y0 + round(15 * s)
    rect(d, x0, y0, x1, y1)
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    line(d, [(cx, y0), (cx, y1)])
    r = round(1.8 * s)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=WHITE, width=2)
    kw, kh = round(5.8 * s), round(4.9 * s)
    for side in (0, 1):
        kx0 = x0 if side == 0 else x1 - kw
        d.rectangle([kx0, cy - kh // 2, kx0 + kw, cy + kh // 2], fill=C["a83a30"], outline=WHITE, width=2)
        a = round(6.75 * s)
        hx = x0 + round(1.6 * s) if side == 0 else x1 - round(1.6 * s)
        box = [hx - a, cy - a, hx + a, cy + a]
        d.arc(box, -90 if side == 0 else 90, 90 if side == 0 else 270, fill=WHITE, width=2)
    im.save(os.path.join(out_dir, "multi_court.png"))


def stadium():
    # 44 x 26 tiles: red running track (4 lanes) around a striped football pitch
    global stripes_alt
    W, H = 44 * T, 26 * T
    R = H // 2                      # outer radius
    lane, lanes = 16, 4
    ri = R - lane * lanes           # inner radius
    stripes_alt = "5aa84a"
    grass = surface(W, H, "3f8f3a", [("2f6b3a", 0.02), ("86c45a", 0.01)], 5, stripes=T)
    track = surface(W, H, "c4503f", [("a83a30", 0.06), ("ec9a62", 0.01)], 6)
    mask_outer = Image.new("L", (W, H))
    mo = ImageDraw.Draw(mask_outer)
    mo.rounded_rectangle([0, 0, W - 1, H - 1], radius=R, fill=255)
    mask_inner = Image.new("L", (W, H))
    mi = ImageDraw.Draw(mask_inner)
    off = lane * lanes
    mi.rounded_rectangle([off, off, W - 1 - off, H - 1 - off], radius=ri, fill=255)
    im = Image.new("RGBA", (W, H))
    im.paste(track, (0, 0), mask_outer)
    im.paste(grass, (0, 0), mask_inner)
    d = ImageDraw.Draw(im)
    for k in range(1, lanes):       # lane lines
        o = k * lane
        d.rounded_rectangle([o, o, W - 1 - o, H - 1 - o], radius=R - o - 1, outline=WHITE, width=1)
    d.rounded_rectangle([off, off, W - 1 - off, H - 1 - off], radius=ri, outline=WHITE, width=2)
    # pitch 30 x 18 tiles, centred
    pw, ph = 30 * T, 18 * T
    x0, y0 = (W - pw) // 2, (H - ph) // 2
    x1, y1 = x0 + pw - 1, y0 + ph - 1
    rect(d, x0, y0, x1, y1)
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    line(d, [(cx, y0), (cx, y1)])
    r = 2 * T
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=WHITE, width=2)
    d.rectangle([cx - 2, cy - 2, cx + 2, cy + 2], fill=WHITE)
    bw, bh = 4 * T, 10 * T      # penalty boxes
    gw, gh = 2 * T, 5 * T       # goal boxes
    for side in (0, 1):
        bx = x0 if side == 0 else x1 - bw
        gx = x0 if side == 0 else x1 - gw
        rect(d, bx, cy - bh // 2, bx + bw, cy + bh // 2)
        rect(d, gx, cy - gh // 2, gx + gw, cy + gh // 2)
        px = x0 + 3 * T if side == 0 else x1 - 3 * T
        d.rectangle([px - 2, cy - 2, px + 2, cy + 2], fill=WHITE)
    im.save(os.path.join(out_dir, "stadium.png"))


stripes_alt = None
tennis("tennis_clay", "d2763c", [("a5532a", 0.05), ("ec9a62", 0.04)], 1)
tennis("tennis_hard", "2f5fa8", [("1f5f99", 0.05), ("2f86c8", 0.02)], 2)
padel()
multi_court()
stadium()

# every pixel must be on the palette
palset = set(C.values())
for f in sorted(os.listdir(out_dir)):
    im = Image.open(os.path.join(out_dir, f)).convert("RGBA")
    off = sum(1 for p in im.getdata() if p[3] and p not in palset)
    print(f"{f}: {im.size}, off-palette {off}")
