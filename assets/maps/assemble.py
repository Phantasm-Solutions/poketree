import hashlib, json, os, shutil, sys
from collections import Counter
from PIL import Image

# Batch 1.5: turns the blockout into the game map.
#  1. maps blockout terrains to the five tilesets and repairs edges no tileset covers (by paving them)
#  2. paints the ground with Wang tiles on a half-tile-offset dual grid and packs the used tiles
#  3. places courts and props, writes collision
#  4. writes public/maps/ngsc.tmj, public/maps/*.png, public/sprites/*.png and assets/manifest.json
# Usage: python assets/maps/assemble.py <repo root>
root = sys.argv[1]
A = lambda *p: os.path.join(root, *p)
T = 32

# ---------- terrain ----------
tmj = json.load(open(A("assets/maps/ngsc-blockout.tmj")))
W, H = tmj["width"], tmj["height"]
names = {t["id"] + 1: t["type"] for t in tmj["tilesets"][0]["tiles"]}
raw = [names[g] for g in tmj["layers"][0]["data"]]
TERR = {"garden": "grass", "lawn": "grass", "outside": "grass", "pitch": "grass", "track": "grass",
        "path": "path", "clay": "path", "hard": "path", "court_grn": "path",
        "water": "water", "sand": "sand", "kids": "sand", "building": "roof"}
terr = [TERR[n] for n in raw]

SETS = [("path-grass", "path", "grass"), ("water-path", "water", "path"), ("sand-grass", "sand", "grass"),
        ("roof-path", "path", "roof"), ("sand-path", "path", "sand")]
wang = {}
for name, lower, upper in SETS:
    img = Image.open(A("assets/raw/tilesets", name + ".png")).convert("RGBA")
    for t in json.load(open(A("assets/raw/tilesets", name + ".json")))["tileset_data"]["tiles"]:
        c, b = t["corners"], t["bounding_box"]
        key = tuple(lower if c[d] == "lower" else upper for d in ("NW", "NE", "SW", "SE"))
        wang[key] = img.crop((b["x"], b["y"], b["x"] + b["width"], b["y"] + b["height"]))


def at(x, y):
    return terr[min(max(y, 0), H - 1) * W + min(max(x, 0), W - 1)]


def corners(x, y):  # dual grid: render cell (x, y) has logical tiles (x-1..x, y-1..y) at its corners
    return (at(x - 1, y - 1), at(x, y - 1), at(x - 1, y), at(x, y))


PRI = {"sand": 1, "grass": 2, "water": 4, "roof": 5}
repaired = 0
for _ in range(50):
    changed = False
    for y in range(H + 1):
        for x in range(W + 1):
            k = corners(x, y)
            if k in wang:
                continue
            low = min((t for t in set(k) if t != "path"), key=PRI.get)
            for dx, dy in ((-1, -1), (0, -1), (-1, 0), (0, 0)):
                tx, ty = min(max(x + dx, 0), W - 1), min(max(y + dy, 0), H - 1)
                if terr[ty * W + tx] == low:
                    terr[ty * W + tx] = "path"; repaired += 1; changed = True
    if not changed:
        break
assert all(corners(x, y) in wang for y in range(H + 1) for x in range(W + 1)), "unrepaired corners"

# pack the Wang tiles actually used
atlas_tiles, index, ground = [], {}, []
for y in range(H + 1):
    for x in range(W + 1):
        k = corners(x, y)
        if k not in index:
            index[k] = len(atlas_tiles); atlas_tiles.append(wang[k])
        ground.append(index[k] + 1)
COLS = 8
atlas = Image.new("RGBA", (COLS * T, -(-len(atlas_tiles) // COLS) * T))
for i, im in enumerate(atlas_tiles):
    atlas.paste(im, ((i % COLS) * T, (i // COLS) * T))

# collision on logical tiles: roofs, water and everything outside the club
blocked = [1 if terr[i] in ("roof", "water") or raw[i] == "outside" else 0 for i in range(W * H)]

# ---------- objects ----------
zones = {o["name"]: o for o in tmj["layers"][2]["objects"]}
courts = tmj["layers"][3]["objects"]
occ = [terr[i] == "water" for i in range(W * H)]    # tiles props may not use (roofs take decals, outside takes trees)


def Z(name):
    z = zones[name]; return z["x"] // T, z["y"] // T, (z["x"] + z["width"]) // T, (z["y"] + z["height"]) // T


for c in courts:
    for y in range(c["y"] // T, (c["y"] + c["height"]) // T):
        for x in range(c["x"] // T, (c["x"] + c["width"]) // T):
            occ[y * W + x] = True

SPRITES = {}     # key -> source png
for d, keys in (("props", None), ("courts", None), ("decals", None)):
    for f in sorted(os.listdir(A("assets/raw", d))):
        SPRITES[f[:-4]] = A("assets/raw", d, f)
size = {k: Image.open(p).size for k, p in SPRITES.items()}
SOLID = {"palm", "shade_tree", "fountain", "lamp_post", "playground", "main_gate", "splash_pad", "shrub"}
props = []


def place(key, tx, ty, need=None, mark=True):
    """Place sprite `key` with its bottom-centre at the bottom-centre of tile (tx, ty).
    Footprint = the sprite's bottom row of tiles. `need` = terrains allowed under the footprint."""
    w, h = size[key]
    fw = max(1, w // T)
    fx0 = tx - (fw - 1) // 2
    cells = [(fx0 + i, ty) for i in range(fw)]
    if any(not (0 <= cx < W and 0 <= cy < H) for cx, cy in cells):
        return False
    if need is not None and any(occ[cy * W + cx] or terr[cy * W + cx] not in need for cx, cy in cells):
        return False
    px = round(fx0 * T + fw * T / 2 - w / 2)
    props.append(dict(key=key, x=px, y=(ty + 1) * T - h, w=w, h=h))
    if mark:
        for cx, cy in cells:
            occ[cy * W + cx] = True
    return True


def h01(*a):  # deterministic noise in [0, 1)
    return int(hashlib.md5(repr(a).encode()).hexdigest()[:8], 16) / 2 ** 32


def far(kind, tx, ty, dist):
    return all(max(abs(p[1] - tx), abs(p[2] - ty)) >= dist for p in placed.get(kind, []))


placed = {}


def put(kind, key, tx, ty, need, dist):
    if far(kind, tx, ty, dist) and place(key, tx, ty, need):
        placed.setdefault(kind, []).append((key, tx, ty)); return True
    return False


# landmarks
x0, y0, x1, y1 = Z("greenheart")
lawn = [(x, y) for y in range(y0, y1) for x in range(x0, x1) if raw[y * W + x] == "lawn"]
cx = round(sum(p[0] for p in lawn) / len(lawn)); cy = round(sum(p[1] for p in lawn) / len(lawn))
place("fountain", cx, cy, mark=True)
x0, y0, x1, y1 = Z("club_house")
roofs = [(x, y) for y in range(y0, y1 + 2) for x in range(x0, x1) if 0 <= y < H and terr[y * W + x] == "roof"]
bx = round(sum(p[0] for p in roofs) / len(roofs)); by = max(p[1] for p in roofs if abs(p[0] - bx) <= 1)
place("clubhouse_entrance", bx, by + 1)
x0, y0, x1, y1 = Z("main_gate")
place("main_gate", (x0 + x1) // 2, y1 - 1)
# spawn: the nearest free walkable tile just inside the gate (where Phase 2 puts the character)
gx, gy = (x0 + x1) // 2, y1 - 4
spawn = min(((x, y) for y in range(H) for x in range(W) if not blocked[y * W + x] and not occ[y * W + x]
             and terr[y * W + x] == "path"), key=lambda p: (p[0] - gx) ** 2 + (p[1] - gy) ** 2)
x0, y0, x1, y1 = Z("kids_garden")
place("playground", (x0 + x1) // 2, (y0 + y1) // 2 + 1)
for tx in (35, 38):
    place("splash_pad", tx, 15)
# football goals on the pitch's goal lines (stadium sprite: pitch spans tiles 6..32 of 38, centre row 11)
st = next(c for c in courts if c["name"] == "stadium")
sx, sy = st["x"] // T, st["y"] // T
props.append(dict(key="football_goal_w", x=(sx + 6) * T - 16, y=(sy + 10) * T, w=32, h=64))
props.append(dict(key="football_goal_e", x=(sx + 32) * T - 16, y=(sy + 10) * T, w=32, h=64))
# pool umbrellas on the deck row just north of each pool
for y in range(1, H):
    for x in range(W):
        if terr[y * W + x] == "path" and terr[(y + 1) * W + x] == "water" if y + 1 < H else False:
            put("umbrella", "pool_umbrella", x, y, {"path"}, 3)

# Greenheart: palms on the lawn edge, benches and lamps on the ring path
x0, y0, x1, y1 = Z("greenheart")
def nb(x, y, t):
    return any(0 <= x + dx < W and 0 <= y + dy < H and terr[(y + dy) * W + x + dx] == t
               for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
for y in range(y0, y1 + 1):
    for x in range(x0, x1 + 1):
        if raw[y * W + x] == "lawn" and nb(x, y, "path"):
            put("palm", "palm", x, y, {"grass"}, 4)
for y in range(y0 - 1, y1 + 2):
    for x in range(x0 - 1, x1 + 2):
        if 0 <= y < H and terr[y * W + x] == "path" and any(raw[(y + dy) * W + x + dx] == "lawn"
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) if 0 <= y + dy < H):
            if h01("b", x, y) < 0.5:
                put("bench", "bench", x, y, {"path"}, 6)
            else:
                put("lamp", "lamp_post", x, y, {"path"}, 6)
# a loose ring of shade trees inside Greenheart, leaving the middle open as a lawn
for (x, y) in lawn:
    if (x - cx) ** 2 + (y - cy) ** 2 > 36 and h01("g", x, y) < 0.12:
        put("tree", "shade_tree", x, y, {"grass"}, 4)

# lamps along every other walk
for y in range(H):
    for x in range(W):
        if terr[y * W + x] == "path" and nb(x, y, "grass") and h01("l", x, y) < 0.25:
            put("lamp", "lamp_post", x, y, {"path"}, 8)
# shrubs where grass meets a building apron
for y in range(H):
    for x in range(W):
        if terr[y * W + x] == "grass" and raw[y * W + x] != "outside" and nb(x, y, "path") and \
                any(terr[(y + dy) * W + x + dx] == "roof" for dx in (-2, -1, 0, 1, 2) for dy in (-2, -1, 0, 1, 2)
                    if 0 <= x + dx < W and 0 <= y + dy < H) and h01("s", x, y) < 0.5:
            put("shrub", "shrub", x, y, {"grass"}, 3)
# trees through the gardens, denser along the club's edge; palms mixed in
for y in range(H):
    for x in range(W):
        if terr[y * W + x] != "grass":
            continue
        edge = raw[y * W + x] == "outside"
        r = h01("t", x, y)
        if edge and r < 0.35:
            put("edge", "shade_tree" if r < 0.25 else "palm", x, y, {"grass"}, 2)
        elif not edge and raw[y * W + x] == "garden" and r < 0.10:
            put("tree", "palm" if r < 0.03 else "shade_tree", x, y, {"grass"}, 3)
# rooftop details on roof tiles away from the roof's edge
for y in range(1, H - 1):
    for x in range(1, W - 1):
        if all(terr[(y + dy) * W + x + dx] == "roof" for dx in (-1, 0, 1) for dy in (-1, 0, 1)):
            r = h01("r", x, y)
            if r < 0.06:
                put("ac", "roof_ac", x, y, {"roof"}, 3)
            elif r < 0.09:
                put("sky", "roof_skylight", x, y, {"roof"}, 4)

# ---------- write ----------
pub = A("public")
os.makedirs(os.path.join(pub, "maps"), exist_ok=True)
os.makedirs(os.path.join(pub, "sprites"), exist_ok=True)
atlas.save(os.path.join(pub, "maps", "terrain.png"))
col = Image.new("RGBA", (T, T), (196, 80, 63, 110))
col.save(os.path.join(pub, "maps", "collision.png"))
used = {p["key"] for p in props} | {c["name"] for c in courts}
for k in sorted(used):
    shutil.copyfile(SPRITES[k], os.path.join(pub, "sprites", k + ".png"))

oid = 0
def nid():
    global oid; oid += 1; return oid

NT = len(atlas_tiles)
out = dict(type="map", version="1.10", tiledversion="1.11.0", orientation="orthogonal", renderorder="right-down",
  infinite=False, width=W, height=H, tilewidth=T, tileheight=T, nextlayerid=7,
  properties=[dict(name="source", type="string", value="assets/maps/assemble.py from ngsc-blockout.tmj")],
  tilesets=[
    dict(firstgid=1, name="terrain", image="terrain.png", imagewidth=atlas.width, imageheight=atlas.height,
         tilewidth=T, tileheight=T, tilecount=NT, columns=COLS, margin=0, spacing=0),
    dict(firstgid=NT + 1, name="collision", image="collision.png", imagewidth=T, imageheight=T,
         tilewidth=T, tileheight=T, tilecount=1, columns=1, margin=0, spacing=0)],
  layers=[
    # dual grid: one more row and column than the map, shifted half a tile up-left
    dict(id=1, name="ground", type="tilelayer", width=W + 1, height=H + 1, x=0, y=0, offsetx=-T // 2,
         offsety=-T // 2, opacity=1, visible=True, data=ground),
    dict(id=2, name="collision", type="tilelayer", width=W, height=H, x=0, y=0, opacity=1, visible=False,
         data=[NT + 1 if b else 0 for b in blocked]),
    dict(id=3, name="courts", type="objectgroup", draworder="topdown", x=0, y=0, opacity=1, visible=True,
         objects=[dict(id=nid(), name=c["name"], type="sprite", x=c["x"], y=c["y"], width=c["width"],
                       height=c["height"], rotation=0, visible=True) for c in courts]),
    dict(id=4, name="props", type="objectgroup", draworder="topdown", x=0, y=0, opacity=1, visible=True,
         objects=[dict(id=nid(), name=p["key"], type="sprite", x=p["x"], y=p["y"], width=p["w"], height=p["h"],
                       rotation=0, visible=True,
                       properties=[dict(name="solid", type="bool", value=p["key"] in SOLID)])
                  for p in sorted(props, key=lambda p: p["y"] + p["h"])]),
    dict(id=5, name="zones", type="objectgroup", draworder="topdown", x=0, y=0, opacity=1, visible=False,
         objects=[dict(o, id=nid()) for o in tmj["layers"][2]["objects"]] +
                 [dict(id=nid(), name="spawn", type="spawn", point=True, rotation=0, visible=True, width=0, height=0,
                       x=spawn[0] * T + T // 2, y=spawn[1] * T + T // 2)]),
  ])
out["nextobjectid"] = oid + 1
json.dump(out, open(os.path.join(pub, "maps", "ngsc.tmj"), "w"))

manifest = dict(version=1, maps=dict(ngsc="maps/ngsc.tmj"),
                tilesets={"terrain": "maps/terrain.png", "collision": "maps/collision.png"},
                images={k: f"sprites/{k}.png" for k in sorted(used)})
json.dump(manifest, open(A("assets/manifest.json"), "w"), indent=2)

# ---------- preview ----------
img = Image.new("RGBA", (W * T, H * T))
for i, g in enumerate(ground):
    x, y = i % (W + 1), i // (W + 1)
    img.paste(atlas_tiles[g - 1], (x * T - T // 2, y * T - T // 2))
for c in courts:
    img.alpha_composite(Image.open(SPRITES[c["name"]]).convert("RGBA"), (c["x"], c["y"]))
for p in sorted(props, key=lambda p: p["y"] + p["h"]):
    im = Image.open(SPRITES[p["key"]]).convert("RGBA")
    px, py = p["x"], p["y"]
    if px < 0 or py < 0:
        im = im.crop((max(0, -px), max(0, -py), im.width, im.height)); px, py = max(px, 0), max(py, 0)
    img.alpha_composite(im, (px, py))
img.save(A("assets/maps/ngsc-map-preview.png"))
print("spawn tile:", spawn)
print(f"terrain tiles repaired: {repaired}; atlas tiles: {NT}; props: {len(props)} "
      f"{dict(Counter(p['key'] for p in props))}; courts: {len(courts)}; blocked: {sum(blocked)}/{W * H}")
