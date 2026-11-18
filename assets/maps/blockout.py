import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # outputs land next to this script
from PIL import Image, ImageDraw, ImageFont

VW, VH = 1306, 924          # traced in the 1306x924 view of the aerial
TW, TH = 96, 68             # map size in tiles
T = 32
sx, sy = TW / VW, TH / VH

TERRAIN = [  # gid, name, colour, blocked
 (1, "outside",   "#3b3b3b", True),
 (2, "garden",    "#86b86f", False),
 (3, "lawn",      "#62a552", False),
 (4, "path",      "#dccdb0", False),
 (5, "building",  "#8a6f5a", True),
 (6, "water",     "#4fa3d9", True),
 (7, "sand",      "#e8d39a", False),
 (8, "clay",      "#d2763c", False),
 (9, "hard",      "#3f7fc4", False),
 (10,"pitch",     "#3f8f3a", False),
 (11,"track",     "#c4503f", False),
 (12,"court_grn", "#5aa86b", False),
 (13,"kids",      "#b07a4f", False),
]
G = {n: g for g, n, c, b in TERRAIN}
COL = {g: c for g, n, c, b in TERRAIN}
BLOCK = {g for g, n, c, b in TERRAIN if b}

grid = Image.new("L", (TW, TH), G["outside"])
d = ImageDraw.Draw(grid)
def P(pts): return [(x * sx, y * sy) for x, y in pts]
def poly(pts, t): d.polygon(P(pts), fill=G[t])
def rect(x0, y0, x1, y1, t): poly([(x0,y0),(x1,y0),(x1,y1),(x0,y1)], t)
def line(pts, t, w=1): d.line(P(pts), fill=G[t], width=w)
def ell(x0, y0, x1, y1, t): d.ellipse(P([(x0,y0),(x1,y1)]), fill=G[t])

# club grounds
poly([(0,250),(220,195),(380,115),(560,70),(700,40),(840,60),(930,170),(1306,520),
      (1306,780),(800,860),(330,905),(0,900)], "garden")
# paving around club house and terraces
poly([(100,300),(300,250),(360,420),(340,570),(180,590),(60,500)], "path")
# club house west
poly([(110,300),(240,270),(285,330),(260,440),(140,445)], "building")
rect(40,580,110,700,"building"); rect(0,760,120,885,"building")
rect(140,750,290,890,"building")
# small pool
rect(325,225,450,305,"path"); rect(340,240,440,292,"water")
# kids water play + buildings (north)
rect(385,110,535,190,"building"); rect(460,160,540,215,"water"); ell(520,200,595,248,"sand")
# main pool + covered hall
rect(630,110,700,185,"path"); rect(640,120,692,175,"water")
poly([(690,90),(830,80),(850,165),(700,180)], "building")
# Greenheart: ring path then lawn
poly([(350,480),(410,365),(500,320),(600,280),(650,330),(690,470),(680,575),(600,590),(470,595),(390,575),(355,540)], "path")
poly([(365,480),(420,375),(505,333),(598,295),(638,338),(675,470),(665,560),(598,575),(472,580),(400,560),(370,530)], "lawn")
ell(510,290,605,360,"sand")
# kids garden
ell(290,550,400,660,"kids")
# small courts row (padel / multi)
rect(430,595,675,695,"path"); rect(440,605,505,690,"hard"); rect(510,600,665,680,"court_grn")
# tennis: hard (top) and clay blocks
poly([(710,228),(820,215),(852,292),(760,302)], "hard")
poly([(600,258),(708,240),(782,402),(688,414)], "clay")
poly([(758,305),(880,282),(915,360),(792,390)], "clay")
# tennis pavilion
poly([(686,415),(960,350),(972,392),(700,462)], "building")
# parking + east block
rect(880,210,965,285,"path"); poly([(900,285),(1060,265),(1090,375),(960,350)], "building")
# track + pitch + multi court
ell(672,432,1302,752,"track")
ell(700,458,1278,728,"pitch")
poly([(1120,478),(1235,470),(1268,622),(1150,630)], "hard")
# south buildings
rect(350,700,575,890,"building"); rect(575,700,640,760,"path")
rect(640,725,775,840,"building"); rect(790,765,910,825,"building")
poly([(920,750),(1210,735),(1215,810),(925,825)], "building")
# main walks
line([(330,700),(700,700),(700,600)], "path", 2)
line([(300,560),(355,520)], "path", 2)
line([(650,330),(700,250)], "path", 1)
line([(690,470),(700,600)], "path", 1)
line([(560,860),(560,890)], "path", 2)   # gate walk (position to confirm)

ground = list(grid.get_flattened_data()) if hasattr(grid,'get_flattened_data') else list(grid.getdata())
collision = [1 if g in BLOCK else 0 for g in ground]

def bbox(x0,y0,x1,y1):
    return dict(x=round(x0*sx)*T, y=round(y0*sy)*T,
                width=max(1,round((x1-x0)*sx))*T, height=max(1,round((y1-y0)*sy))*T)
ZONES = [
 ("tennis_courts",   600,215,915,414), ("club_house",  110,270,285,445),
 ("greenheart",      365,295,675,580), ("pool_small",  325,225,450,305),
 ("pool_main",       630,110,700,185), ("covered_hall",690,80,850,180),
 ("kids_water_play", 385,110,595,248), ("kids_garden", 290,550,400,660),
 ("small_courts",    430,595,675,695), ("football_pitch",700,458,1110,728),
 ("running_track",   672,432,1302,752),("multi_court", 1120,470,1268,630),
 ("main_gate",       530,860,590,900),
]
objs = [dict(id=i+1, name=n, type="zone", rotation=0, visible=True, **bbox(*b))
        for i, (n, *b) in enumerate(ZONES)]

# placeholder tileset
ts = Image.new("RGB", (T * len(TERRAIN), T))
td = ImageDraw.Draw(ts)
for g, n, c, b in TERRAIN:
    td.rectangle([(g-1)*T, 0, g*T-1, T-1], fill=c)
ts.save("blockout-tiles.png")

tmj = dict(type="map", version="1.10", tiledversion="1.11.0", orientation="orthogonal",
  renderorder="right-down", infinite=False, width=TW, height=TH, tilewidth=T, tileheight=T,
  nextlayerid=4, nextobjectid=len(objs)+1,
  properties=[dict(name="source", type="string", value="Blockout traced from NGSC aerial (Giza Party deck, slide 13)")],
  tilesets=[dict(firstgid=1, name="blockout", image="blockout-tiles.png", imagewidth=T*len(TERRAIN),
    imageheight=T, tilewidth=T, tileheight=T, tilecount=len(TERRAIN), columns=len(TERRAIN),
    margin=0, spacing=0,
    tiles=[dict(id=g-1, type=n, properties=[dict(name="blocked", type="bool", value=b)]) for g,n,c,b in TERRAIN])],
  layers=[
    dict(id=1, name="ground", type="tilelayer", width=TW, height=TH, x=0, y=0, opacity=1, visible=True, data=ground),
    dict(id=2, name="collision", type="tilelayer", width=TW, height=TH, x=0, y=0, opacity=0.5, visible=False,
         data=[G["outside"] if c else 0 for c in collision]),
    dict(id=3, name="zones", type="objectgroup", draworder="topdown", x=0, y=0, opacity=1, visible=True, objects=objs),
  ])
json.dump(tmj, open("ngsc-blockout.tmj", "w"))

# preview with zone labels
S = 12
prev = Image.new("RGB", (TW*S, TH*S))
pd = ImageDraw.Draw(prev)
for i, g in enumerate(ground):
    x, y = i % TW, i // TW
    pd.rectangle([x*S, y*S, x*S+S-1, y*S+S-1], fill=COL[g])
try: font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 13)
except: font = ImageFont.load_default()
for o in objs:
    x0, y0 = o["x"]//T*S, o["y"]//T*S
    pd.rectangle([x0, y0, x0+o["width"]//T*S, y0+o["height"]//T*S], outline="white")
    pd.text((x0+3, y0+2), o["name"], fill="white", font=font, stroke_width=2, stroke_fill="black")
prev.save("ngsc-blockout-preview.png")
ref = Image.open("../raw/reference/ngsc-aerial.png").resize((TW*S, TH*S))
side = Image.new("RGB", (TW*S*2+12, TH*S), "white"); side.paste(ref,(0,0)); side.paste(prev,(TW*S+12,0))
side.save("ngsc-blockout-vs-aerial.png")
print("blocked tiles:", sum(collision), "of", len(collision))
