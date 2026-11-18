import json, sys, os
from collections import Counter
from PIL import Image

root = sys.argv[1]  # poketree repo
ts_dir = os.path.join(root, "assets/raw/tilesets")
pal = {tuple(int(h[i:i+2], 16) for i in (0, 2, 4)) for h in open(os.path.join(root, "assets/palette.hex")).read().split()}

SETS = {"A": ("path-grass", "path", "grass"), "B": ("water-path", "water", "path"), "C": ("sand-grass", "sand", "grass")}
tiles = {}  # (set, (nw,ne,sw,se) as terrain names) -> image
for k, (name, lower, upper) in SETS.items():
    img = Image.open(os.path.join(ts_dir, name + ".png")).convert("RGBA")
    off = [p[:3] for p in img.getdata() if p[3] > 0 and p[:3] not in pal]
    print(f"{name}: {img.size}, off-palette pixels {len(off)}, transparent {sum(1 for p in img.getdata() if p[3] < 255)}")
    meta = json.load(open(os.path.join(ts_dir, name + ".json")))
    t = meta["tileset_data"]["tiles"]
    print(f"  tiles {len(t)}")
    for tile in t:
        c = tile["corners"]; b = tile["bounding_box"]
        key = tuple(lower if c[d] == "lower" else upper for d in ("NW", "NE", "SW", "SE"))
        tiles[key] = img.crop((b["x"], b["y"], b["x"] + b["width"], b["y"] + b["height"]))

# full tiles shared across sets must match exactly (pro pastes chained terrain)
for terr, (s1, s2) in {"grass": ("A", "C"), "path": ("A", "B")}.items():
    print(f"shared {terr} full tile present: {(terr,)*4 in tiles}")

# test patch: Greenheart, small pool, club house edge, kids water play from the blockout
tmj = json.load(open(os.path.join(root, "assets/maps/ngsc-blockout.tmj")))
W = tmj["width"]; ground = tmj["layers"][0]["data"]
names = {t["id"] + 1: t["type"] for t in tmj["tilesets"][0]["tiles"]}
TERR = {"garden": "grass", "lawn": "grass", "path": "path", "water": "water", "sand": "sand"}
FLAT = {"building": (138, 111, 90), "outside": (59, 59, 59), "clay": (210, 118, 60), "hard": (63, 127, 196),
        "kids": (176, 122, 79), "court_grn": (90, 168, 107), "pitch": (63, 143, 58), "track": (196, 80, 63)}
x0, y0, x1, y1 = 26, 6, 56, 33
def terr(x, y): return TERR.get(names[ground[y * W + x]], "grass")
out = Image.new("RGBA", ((x1 - x0) * 32, (y1 - y0) * 32))
bad = Counter()
for y in range(y0, y1):
    for x in range(x0, x1):
        n = names[ground[y * W + x]]
        if n in FLAT:
            out.paste(Image.new("RGBA", (32, 32), FLAT[n] + (255,)), ((x - x0) * 32, (y - y0) * 32)); continue
        key = (terr(x, y), terr(x + 1, y), terr(x, y + 1), terr(x + 1, y + 1))
        tile = tiles.get(key)
        if tile is None:
            bad[tuple(sorted(set(key)))] += 1
            maj = Counter(key).most_common(1)[0][0]
            tile = tiles[(maj,) * 4]
        out.paste(tile, ((x - x0) * 32, (y - y0) * 32))
out.save(os.path.join(root, "assets/maps/terrain-test-patch.png"))
print("unmatched corner combos:", dict(bad))

