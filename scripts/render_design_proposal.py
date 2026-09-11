"""Draw original planning diagrams (SVG and PNG); this does not create game assets.

Optional dependency: Pillow. Run from any directory. Dimensions are design studies.
"""

from html import escape
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parents[1] / "mods/electric-heating-works/design"
INK, PAPER = "#243b40", "#f7f4ec"
HALL, ELECTRIC, THERMAL = "#c9d1ce", "#d9b45d", "#9bc5be"
ROAD, PALE, RED = "#dfe0d8", "#e9e6dc", "#ad5c45"


class Sheet:
    def __init__(self, width, height, title):
        self.width, self.height = width, height
        self.im = Image.new("RGB", (width * 2, height * 2), PAPER)
        self.d = ImageDraw.Draw(self.im)
        self.svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img">',
                    f'<title>{escape(title)}</title>',
                    '<desc>Original conceptual site diagram. Proposed dimensions; no game performance or engineering clearances are certified.</desc>',
                    f'<rect width="100%" height="100%" fill="{PAPER}"/>']

    def rect(self, x, y, w, h, fill, stroke=INK, sw=1):
        self.d.rectangle((x*2, y*2, (x+w)*2, (y+h)*2), fill=fill, outline=stroke, width=max(1, int(sw*2)))
        self.svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

    def line(self, points, fill=INK, sw=2):
        self.d.line([(x*2, y*2) for x, y in points], fill=fill, width=max(1, int(sw*2)))
        values = " ".join(f"{x},{y}" for x, y in points)
        self.svg.append(f'<polyline points="{values}" fill="none" stroke="{fill}" stroke-width="{sw}"/>')

    def circle(self, x, y, r, fill, stroke=INK, sw=1):
        self.d.ellipse(((x-r)*2, (y-r)*2, (x+r)*2, (y+r)*2), fill=fill, outline=stroke, width=max(1, int(sw*2)))
        self.svg.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

    def text(self, x, y, text, size=18, fill=INK, bold=False):
        candidates = [Path(os.environ.get("WINDIR", "/nonexistent")) / "Fonts" / ("segoeuib.ttf" if bold else "segoeui.ttf"),
                      Path("/usr/share/fonts/truetype/dejavu") / ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf")]
        font = next((ImageFont.truetype(str(p), size*2) for p in candidates if p.exists()), ImageFont.load_default(size=size*2))
        self.d.text((x*2, y*2), text, font=font, fill=fill, anchor="lt")
        self.svg.append(f'<text x="{x}" y="{y+size*.82}" font-family="Segoe UI,DejaVu Sans,sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" fill="{fill}">{escape(text)}</text>')

    def save(self, name):
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / f"{name}.svg").write_text("\n".join(self.svg + ["</svg>"]) + "\n", encoding="utf-8", newline="\n")
        self.im.resize((self.width, self.height), Image.Resampling.LANCZOS).save(OUT / f"{name}.png")


CONCEPTS = [
    dict(id="a", name="The civic powerhouse", size=(150,112), yard=(12,12,94,37),
         hall=(12,61,78,30), annex=(12,93,42,10), tanks=[(119,70),(119,94)],
         notes=["Recommended starting point", "A broad switchyard fronts the hall.", "Strong public-works silhouette.", "Short electrical and pipe routes.", "Integrated placement to investigate."],
         gate=(72,112), control=(110,33,25,13)),
    dict(id="b", name="The linear works", size=(180,90), yard=(12,12,100,33),
         hall=(12,54,90,24), annex=(110,59,23,18), tanks=[(150,26),(150,61)],
         notes=["For a long industrial corridor", "Long hall and parallel electrical yard.", "Clear expansion direction.", "Wider frontage and pipe runs.", "Integrated placement to investigate."],
         gate=(120,90), control=(116,12,18,16)),
    dict(id="c", name="The paired campus", size=(168,120), yard=(10,10,100,37),
         hall=(12,65,84,30), annex=(12,99,42,10), tanks=[(137,74),(137,102)],
         notes=["Fallback layout for modularity", "Receiving yard and thermal works", "have separate access corridors.", "Two placement zones are possible.", "Separate yard does not raise limits."],
         gate=(75,120), control=(119,21,32,17)),
]


def plan(s, concept, ox, oy, k, detail=True):
    def rect(x,y,w,h,fill,stroke=INK,sw=1):s.rect(ox+x*k,oy+y*k,w*k,h*k,fill,stroke,sw)
    def line(points,fill=INK,sw=2):s.line([(ox+x*k,oy+y*k) for x,y in points],fill,sw)
    def text(x,y,t,size=15,bold=False):s.text(ox+x*k,oy+y*k,t,size,bold=bold)
    width,height=concept["size"]
    rect(0,0,width,height,PALE)
    # A service loop remains outside major equipment and buildings.
    rect(4,4,width-8,height-8,ROAD,ROAD)
    rect(10,10,width-20,height-20,PALE,PALE)
    gx,gy=concept["gate"]
    rect(gx-4,height-10,8,18,ROAD,ROAD)
    # Yard blocks: top-down equipment symbols, not an electrical clearance drawing.
    x,y,w,h=concept["yard"]
    rect(x,y,w,h,"#e9ddbb")
    bays=[x+12,x+32,x+57,x+78]
    for bx in bays:
        line([(bx,y+3),(bx,y+h-3)],INK,1)
        line([(bx-4,y+5),(bx+4,y+5)],INK,3)
        for dx in [-3,0,3]:
            rect(bx+dx-.5,y+8,1,3,ELECTRIC)
            rect(bx+dx-.7,y+13,1.4,3,ELECTRIC)
        if bx in bays[:2]:
            line([(bx,-5),(bx,y+3)],RED,2)
        else:
            rect(bx-5,y+h-10,10,8,ELECTRIC)
            for n in range(5):line([(bx-5+n*2,y+h-9),(bx-5+n*2,y+h-3)],INK,1)
    for dy in [18,20]:line([(x+4,y+dy),(x+w-4,y+dy)],RED,2)
    cx,cy,cw,ch=concept["control"]
    rect(cx,cy,cw,ch,HALL)
    # Below-grade plant cable route; endpoints describe the visual narrative only.
    hx,hy,hw,hh=concept["hall"]
    line([(x+w-10,y+h),(x+w-10,hy-5),(hx+hw-8,hy-5),(hx+hw-8,hy)],RED,3)
    rect(hx,hy,hw,hh,HALL)
    for bx in range(6,int(hw),6):line([(hx+bx,hy),(hx+bx,hy+hh)],"#92a3a2",1)
    rect(hx+4,hy+hh*.4,hw-8,hh*.2,"#8ca5a6")
    ax,ay,aw,ah=concept["annex"]
    rect(ax,ay,aw,ah,HALL)
    # Tank diameter is a visual envelope, not a declared game storage capacity.
    for tx,ty in concept["tanks"]:
        s.circle(ox+tx*k,oy+ty*k,9*k,THERMAL)
        s.circle(ox+tx*k,oy+ty*k,7.5*k,THERMAL)
        line([(hx+hw,hy+hh/2),(tx-12,hy+hh/2),(tx-12,ty),(tx-9,ty)],"#408b82",3)
    pipex=concept["tanks"][0][0]-12
    header_y=sum(ty for tx,ty in concept["tanks"])/len(concept["tanks"])
    for dx in [0,2]:line([(hx+hw,hy+hh/2+dx),(pipex,hy+hh/2+dx),(pipex,header_y+dx),(width+5,header_y+dx)],"#408b82",2)
    if concept['id']=='c':
        rect(0,51,width,8,ROAD,ROAD)
        for xx in range(0,width,6):line([(xx,55),(xx+3,55)],RED,1)
        rect(-6,24,16,8,ROAD,ROAD)
        if detail:text(-1,20,"YARD ACCESS",12,True)
    if detail:
        text(x+3,y+h+2,"RECEIVING SWITCHYARD",17,True)
        text(hx+4,hy+3,"ELECTRIC BOILER HALL",18,True)
        text(ax+2,ay+2,"PUMPS / SERVICES",13,True)
        text(cx+2,cy+2,"CONTROL",13,True)
        text(width+7,header_y-4,"HEAT",13,True)
        text(1,-10,"INCOMING HV LINES",14,True)
        text(gx-13,height+10,"ROAD ACCESS",13,True)


for c in CONCEPTS:
    s=Sheet(1400,1040,c['name'])
    s.text(60,35,"PHOBOS' ELECTRIC HEATING WORKS",19,bold=True)
    s.text(60,75,f"{c['id'].upper()}  /  {c['name']}",38,bold=True)
    w,h=c['size']
    s.text(60,130,f"{w} x {h} m study envelope  |  original site concept  |  11 September 2026",18)
    plan(s,c,60,235,4.7)
    s.text(985,220,"DESIGN INTENT",18,bold=True)
    for i,note in enumerate(c['notes']):s.text(985,264+i*34,note,17,bold=(i==0))
    s.text(985,490,"PLAN KEY",18,bold=True)
    for i,(color,label) in enumerate([(ELECTRIC,"Electrical equipment"),(HALL,"Hall and service buildings"),(THERMAL,"Hot-water tanks / pipes"),(ROAD,"Maintenance circulation")]):
        s.rect(985,530+i*38,20,20,color)
        s.text(1018,530+i*38,label,16)
    s.text(985,724,"SCALE",16,bold=True)
    s.line([(985,768),(1079,768)],INK,4)
    s.line([(985,760),(985,776)],INK,2)
    s.line([(1079,760),(1079,776)],INK,2)
    s.text(985,784,"20 m",15)
    s.line([(60,936),(1340,936)],"#b7bdb3",1)
    s.text(60,958,"Planning drawing; no game asset, fixed power rating or certified equipment clearance.",18)
    s.text(60,993,"Multiple drawn bays do not establish additive input capacity or simulated redundancy.",16)
    s.save(f"concept-{c['id']}")

s=Sheet(1500,770,"Three Electric Heating Works site concepts")
s.text(50,30,"A REPUBLIC-SCALE ELECTRIC HEATING WORKS",32,bold=True)
s.text(50,80,"Three original layout studies. Shared scale; footprints and equipment arrangements remain proposals.",20)
for i,c in enumerate(CONCEPTS):
    x=50+i*490
    s.text(x,145,c['id'].upper()+"  /  "+c['name'],24,bold=True)
    s.text(x,185,f"{c['size'][0]} x {c['size'][1]} m" + ("  |  RECOMMENDED" if i==0 else ""),17,fill=RED)
    plan(s,c,x,260,2.3,False)
    for j,t in enumerate(c['notes'][1:3]):s.text(x,610+j*30,t,18)
s.line([(50,706),(1450,706)],"#b7bdb3",1)
s.text(50,729,"Amber: switchyard equipment    Grey: buildings    Teal: hot-water systems    Plans are not in-game screenshots.",18)
s.save('concept-comparison')

s=Sheet(1400,720,"Architectural character study for concept A")
s.text(60,35,"A  /  ARCHITECTURAL CHARACTER",34,bold=True)
s.text(60,90,"Proposed 1970s-1980s industrial modernism; original design, not a historical reconstruction.",20)
s.line([(60,450),(1340,450)],INK,3)
s.rect(120,240,700,210,HALL)
for x in range(120,821,70):s.line([(x,240),(x,450)],"#647f7c",4)
s.rect(120,285,700,70,"#8ca5a6")
for x in range(132,810,23):s.line([(x,286),(x,354)],PAPER,2)
s.rect(170,215,600,25,"#8ca5a6")
s.rect(225,375,85,75,RED)
s.rect(355,375,85,75,RED)
s.rect(680,389,180,61,"#aebeb8")
for x in [960,1130]:
    s.rect(x,235,125,215,THERMAL)
    for yy in [253,298,343,388]:s.line([(x,yy),(x+125,yy)],"#588d85",1)
    s.line([(x+110,243),(x+110,438)],INK,2)
s.line([(810,401),(990,401),(990,421),(1140,421)],"#408b82",6)
s.text(120,475,"REPEATED STRUCTURAL BAYS + GLAZING",18,bold=True)
s.text(950,475,"INSULATED WATER TANKS",18,bold=True)
s.text(60,538,"MATERIAL DIRECTION",18,bold=True)
for i,(color,label) in enumerate([(HALL,"Warm concrete"),(RED,"Oxide-red doors"),("#8ca5a6","Blue-grey glazing"),(THERMAL,"Pale tank cladding")]):
    x=60+i*330;s.rect(x,580,45,45,color);s.text(x+60,590,label,18)
s.text(60,672,"Unscaled elevation sketch. No combustion stack or cooling tower; receiving switchyard shown in the site plans.",17)
s.save('architectural-character')
print('Wrote five original diagram pairs (SVG + PNG).')
