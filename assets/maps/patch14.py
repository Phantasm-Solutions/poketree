import json, os, sys
from collections import Counter
from PIL import Image

# Paints the batch 1.4 test patch (assets/maps/art-test-patch.png): all five tilesets,
# court sprites and props over part of the blockout. A preview only; 1.5 does the real assembly.
# Usage: python assets/maps/patch14.py <repo root>
root = sys.argv[1]
A = lambda p: os.path.join(root, p)
T = 32

SETS = [("path-grass", "path", "grass"), ("water-path", "water", "path"), ("sand-grass", "sand", "grass"),
        ("roof-path", "path", "roof"), ("sand-path", "path", "sand")]
tiles = {}
for name, lower, upper in SETS:
    img = Image.open(A(f"assets/raw/tilesets/{name}.png")).convert("RGBA")
    for t in json.load(open(A(f"assets/raw/tilesets/{name}.json")))["tileset_data"]["tiles"]:
        c, b = t["corners"], t["bounding_box"]
        key = tuple(lower if c[d] == "lower" else upper for d in ("NW", "NE", "SW", "SE"))
        tiles[key] = img.crop((b["x"], b["y"], b["x"] + b["width"], b["y"] + b["height"]))

tmj = json.load(open(A("assets/maps/ngsc-blockout.tmj")))
W = tmj["width"]
ground = tmj["layers"][0]["data"]
names = {t["id"] + 1: t["type"] for t in tmj["tilesets"][0]["tiles"]}
TERR = {"garden": "grass", "lawn": "grass", "outside": "grass", "path": "path", "water": "water",
        "sand": "sand", "kids": "sand", "building": "roof"}       # court surfaces sit on path


def terr(x, y):
    return TERR.get(names[ground[y * W + x]], "path")


x0, y0, x1, y1 = 6, 8, 68, 44
out = Image.new("RGBA", ((x1 - x0) * T, (y1 - y0) * T))
bad = Counter()
for y in range(y0, y1):
    for x in range(x0, x1):
        key = (terr(x, y), terr(x + 1, y), terr(x, y + 1), terr(x + 1, y + 1))
        tile = tiles.get(key)
        if tile is None:
            bad[tuple(sorted(set(key)))] += 1
            tile = tiles[(Counter(key).most_common(1)[0][0],) * 4]
        out.paste(tile, ((x - x0) * T, (y - y0) * T))


def put(path, tx, ty, anchor="bottom"):
    """Place a sprite with its bottom-centre (props) or top-left (courts) at tile coords."""
    im = Image.open(A(path)).convert("RGBA")
    px, py = round((tx - x0) * T), round((ty - y0) * T)
    if anchor == "bottom":
        px, py = px - im.width // 2, py - im.height
    out.alpha_composite(im, (px, py))


# courts over the tennis block
for i, kind in enumerate(["clay", "clay", "clay", "hard"]):
    put(f"assets/raw/courts/tennis_{kind}.png", 45 + i * 5.5, 17, "topleft")
P = "assets/raw/props/"
# Greenheart: fountain, palms on the ring, benches, lamps, shade trees
put(P + "fountain.png", 39, 34)
for tx, ty in [(31, 30), (35, 26), (43, 26), (47, 31), (46, 39), (32, 39)]:
    put(P + "palm.png", tx, ty)
for tx, ty in [(37, 37), (41, 37)]:
    put(P + "bench.png", tx, ty)
for tx, ty in [(36, 33), (42, 33)]:
    put(P + "lamp_post.png", tx, ty)
for tx, ty in [(29, 35), (49, 35)]:
    put(P + "shade_tree.png", tx, ty)
# small pool deck
for tx, ty in [(26, 17), (29, 17), (32, 17)]:
    put(P + "pool_umbrella.png", tx, ty)
# club house entrance and planting
put(P + "clubhouse_entrance.png", 15, 34)
for tx, ty in [(11, 35), (19, 35), (23, 26), (23, 29)]:
    put(P + "shrub.png", tx, ty)
for tx, ty in [(8, 20), (24, 22)]:
    put(P + "shade_tree.png", tx, ty)
# kids water play and garden
put(P + "splash_pad.png", 36.5, 15)
put(P + "playground.png", 25.5, 44)

out.save(A("assets/maps/art-test-patch.png"))
print("patch", out.size, "unmatched corner combos:", dict(bad))
