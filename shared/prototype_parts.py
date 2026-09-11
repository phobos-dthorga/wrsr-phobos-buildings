"""Original prototype parts for Phobos building studies, MIT, 2026.
Generated review geometry, not final game meshes. No external assets are loaded.
"""
import math
import bpy
from mathutils import Vector

COPYRIGHT = "Copyright (c) 2026 Phobos A. D'thorga"


def palette():
    colors = {
        "concrete": (.46, .48, .43), "foundation": (.25, .29, .28),
        "steel": (.31, .39, .42), "roof": (.115, .17, .18),
        "glass": (.075, .19, .23), "red": (.38, .075, .038),
        "tank": (.48, .66, .62), "porcelain": (.20, .075, .033),
        "conductor": (.40, .43, .41), "asphalt": (.105, .135, .14),
        "gravel": (.34, .34, .29), "ground": (.24, .29, .23),
        "marking": (.65, .62, .46), "paper": (.73, .74, .69),
    }
    result = {}
    for name, color in colors.items():
        material = bpy.data.materials.new("mat_" + name)
        material.diffuse_color = (*color, 1)
        material.use_nodes = True
        node = material.node_tree.nodes.get("Principled BSDF")
        node.inputs["Base Color"].default_value = (*color, 1)
        node.inputs["Roughness"].default_value = .64
        if name in ("steel", "conductor"):
            node.inputs["Metallic"].default_value = .55
            node.inputs["Roughness"].default_value = .36
        if name == "glass":
            node.inputs["Metallic"].default_value = .30
            node.inputs["Roughness"].default_value = .22
        if name in ("concrete", "gravel", "asphalt", "ground"):
            noise = material.node_tree.nodes.new("ShaderNodeTexNoise")
            noise.inputs["Scale"].default_value = 5 if name == "concrete" else 18
            noise.inputs["Detail"].default_value = 2
            bump = material.node_tree.nodes.new("ShaderNodeBump")
            bump.inputs["Strength"].default_value = .19
            bump.inputs["Distance"].default_value = .06
            material.node_tree.links.new(noise.outputs["Fac"], bump.inputs["Height"])
            material.node_tree.links.new(bump.outputs["Normal"], node.inputs["Normal"])
        material["license"] = "MIT"
        material["copyright"] = COPYRIGHT
        material["status"] = "prototype Blender material; native shader untested"
        result[name] = material
    return result


class Mesh:
    """Collect simple solids in one reusable mesh; no operator-per-bolt overhead."""
    def __init__(self):
        self.vertices, self.faces, self.slots, self.smooth = [], [], [], []

    def add(self, vertices, faces, material, smooth=False):
        offset = len(self.vertices)
        self.vertices.extend(tuple(v) for v in vertices)
        self.faces.extend(tuple(i + offset for i in face) for face in faces)
        self.slots.extend([material] * len(faces))
        self.smooth.extend([smooth] * len(faces))

    def box(self, center, size, material="concrete"):
        x, y, z = center
        a, b, c = (v / 2 for v in size)
        self.add([(x-a,y-b,z-c),(x+a,y-b,z-c),(x+a,y+b,z-c),(x-a,y+b,z-c),
                  (x-a,y-b,z+c),(x+a,y-b,z+c),(x+a,y+b,z+c),(x-a,y+b,z+c)],
                 [(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],
                 material)

    def bar(self, a, b, radius, material="steel", sides=12):
        a, b = Vector(a), Vector(b)
        axis = (b-a).normalized()
        helper = Vector((0,0,1)) if abs(axis.z) < .9 else Vector((0,1,0))
        u = axis.cross(helper).normalized()
        v = axis.cross(u).normalized()
        vertices = [p + radius * (math.cos(i*math.tau/sides)*u +
                    math.sin(i*math.tau/sides)*v) for p in (a,b) for i in range(sides)]
        faces = [tuple(reversed(range(sides))), tuple(range(sides, 2*sides))]
        faces.extend((i,(i+1)%sides,(i+1)%sides+sides,i+sides) for i in range(sides))
        self.add(vertices, faces, material, True)
        self.smooth[-sides-2] = self.smooth[-sides-1] = False

    def cyl(self, center, radius, height, material="steel", sides=32):
        x, y, z = center
        self.bar((x,y,z-height/2), (x,y,z+height/2), radius, material, sides)

    def ring(self, center, radius, thickness=.045, material="steel", sides=64):
        x, y, z = center
        for i in range(sides):
            a, b = i*math.tau/sides, (i+1)*math.tau/sides
            self.bar((x+radius*math.cos(a),y+radius*math.sin(a),z),
                     (x+radius*math.cos(b),y+radius*math.sin(b),z), thickness, material, 6)

    def insulator(self, x, y, base, height=1.3):
        self.cyl((x,y,base+height/2), .13, height, "porcelain", 12)
        for i in range(8):
            self.cyl((x,y,base+.12+i*(height-.22)/7), .23, .075, "porcelain", 12)
        self.cyl((x,y,base+height+.08), .13, .16, "conductor", 12)

    def finish(self, name, materials):
        mesh = bpy.data.meshes.new(name)
        mesh.from_pydata(self.vertices, [], self.faces)
        keys = list(dict.fromkeys(self.slots))
        for key in keys:
            mesh.materials.append(materials[key])
        indices = {key:i for i,key in enumerate(keys)}
        for face, key, smooth in zip(mesh.polygons, self.slots, self.smooth):
            face.material_index = indices[key]
            face.use_smooth = smooth
        mesh.update()
        mesh["copyright"] = COPYRIGHT
        mesh["license"] = "MIT"
        mesh["status"] = "original visual prototype; no UV/LOD/native acceptance"
        return mesh


def industrial_bay(height=18):
    m = Mesh()
    m.box((3,0,height/2),(6,.50,height))
    m.box((3,-.30,.7),(6,.18,1.4),"foundation")
    m.box((3,-.30,9.4),(5.35,.08,8.0),"glass")
    for x in (.24,5.76):
        m.box((x,-.38,height/2),(.38,.45,height),"concrete")
    for x in (1.2,2.4,3.6,4.8):
        m.box((x,-.37,9.4),(.07,.10,8.1),"steel")
    for z in (5.35,9.4,13.45):
        m.box((3,-.38,z),(5.5,.12,.12),"steel")
    for z in (4.4,14.5,17.6):
        m.box((3,-.36,z),(6,.23,.18),"concrete")
    return m


def roof_bay(span=30, height=18):
    m = Mesh()
    m.box((3,span/2,height+.18),(6,span+.8,.36),"roof")
    for y in (.3,span-.3):
        m.box((3,y,height+.5),(6,.20,.7),"concrete")
    m.box((3,span/2,height+1.0),(5.75,8,1.65),"roof")
    for y in (span/2-4.03,span/2+4.03):
        m.box((3,y,height+1.0),(5.45,.08,1.10),"glass")
        for x in (1,2,3,4,5):
            m.box((x,y,height+1.0),(.07,.15,1.15),"steel")
    m.box((3,span/2,height+1.92),(6,8.5,.18),"steel")
    m.cyl((3,3,height+.85),.45,1.0,"steel",20)
    m.cyl((3,3,height+1.37),.60,.12,"roof",20)
    return m


def control_house(width=24, depth=12, height=5):
    m = Mesh()
    m.box((0,0,height/2),(width,depth,height))
    m.box((0,0,.25),(width+.4,depth+.4,.5),"foundation")
    m.box((0,0,height+.2),(width+.6,depth+.6,.4),"roof")
    for x in range(-int(width/2)+3, int(width/2), 4):
        m.box((x,-depth/2-.05,2.8),(2.4,.12,1.45),"glass")
        m.box((x,-depth/2-.14,2.8),(.07,.12,1.5),"steel")
    m.box((width/2-.06,0,1.4),(.20,1.4,2.8),"red")
    return m


def gantry():
    m = Mesh()
    for x in (-6,6):
        m.box((x,0,.3),(2.1,2.1,.6),"foundation")
        for dx in (-.36,.36):
            for dy in (-.36,.36):
                m.bar((x+dx,dy,.6),(x+dx,dy,12),.095)
        for z in range(1,12,2):
            for dy in (-.36,.36):
                m.bar((x-.36,dy,z),(x+.36,dy,z+2),.05)
                m.bar((x+.36,dy,z),(x-.36,dy,z+2),.05)
            for dx in (-.36,.36):
                m.bar((x+dx,-.36,z),(x+dx,.36,z+2),.05)
                m.bar((x+dx,.36,z),(x+dx,-.36,z+2),.05)
    for y in (-.4,.4):
        for z in (11.2,12.2):
            m.bar((-6.5,y,z),(6.5,y,z),.10)
        for i in range(13):
            m.bar((-6.5+i,y,11.2),(-5.5+i,y,12.2),.05)
            m.bar((-6.5+i,y,12.2),(-5.5+i,y,11.2),.05)
    for x in (-3.8,0,3.8):
        m.insulator(x,0,9.6,1.5)
    return m


def switching_bay():
    m = Mesh()
    # Three phase group, with disconnector and breaker forms along the bay.
    for x in (-3.8,0,3.8):
        for y in (-3,0,3):
            m.box((x,y,.22),(1.5,1.4,.44),"foundation")
            m.box((x,y,1.3),(.18,.18,2.2),"steel")
        for y in (-3,3):
            m.insulator(x,y,2.4,1.3)
        m.bar((x,-3,3.9),(x,-.9,4.15),.065,"conductor")
        m.cyl((x,0,2.5),.35,.8,"steel",16)
        m.insulator(x,0,2.9,1.5)
        m.bar((x,0,4.55),(x,3,3.9),.065,"conductor")
    m.box((0,-.15,.5),(1.0,.8,.8),"steel")
    return m


def busbar_support(m, x=0, y=0):
    for dy in (-3.8,3.8):
        m.box((x,y+dy,.2),(1.4,1.4,.4),"foundation")
        m.box((x,y+dy,2.65),(.24,.24,5.0),"steel")
    m.box((x,y,5.2),(.25,8.6,.28),"steel")
    for dy in (-3.8,0,3.8):
        m.insulator(x,y+dy,5.35,1.1)


def busbar(length=20):
    m = Mesh()
    # A repeated segment owns its start support; the assembly adds one terminal.
    busbar_support(m)
    for y in (-3.8,0,3.8):
        m.bar((0,y,6.62),(length,y,6.62),.09,"conductor",12)
    return m


def transformer():
    m = Mesh()
    m.box((0,0,.25),(12,9,.5),"foundation")
    m.box((0,0,.55),(11,8,.12),"gravel")
    for y in (-4.45,4.45):
        m.box((0,y,.65),(12,.18,.8),"concrete")
    for x in (-5.9,5.9):
        m.box((x,0,.65),(.18,9,.8),"concrete")
    m.box((0,0,2.5),(4.6,5.6,3.5),"steel")
    m.box((0,0,4.35),(4.85,5.85,.2),"roof")
    for x in (-3.35,3.35):
        for i in range(13):
            m.box((x,-2.65+i*.44,2.5),(1.4,.11,2.8),"steel")
        for z in (1.0,4.0):
            m.bar((x,-2.85,z),(x,2.85,z),.16,"steel")
            m.bar((x,0,z),(x*.64,0,z),.14,"steel")
    m.bar((-2.65,2.3,5.25),(2.65,2.3,5.25),.62,"steel",24)
    for x in (-1.5,0,1.5):
        m.insulator(x,-1.65,4.5,2.0)
        m.insulator(x,.35,4.5,.95)
    m.box((2.5,-2.0,2.0),(.45,1.2,1.5),"roof")
    for z in (1,1.7,2.4,3.1,3.8):
        m.bar((2.5,2.0,z),(2.5,2.6,z),.04,"steel",6)
    for y in (2.0,2.6):
        m.bar((2.5,y,.6),(2.5,y,4.3),.05,"steel",6)
    return m


def storage_tank(radius=9, height=22):
    m = Mesh()
    m.cyl((0,0,.35),radius+.5,.7,"foundation",96)
    m.cyl((0,0,height/2+.6),radius,height,"tank",96)
    m.cyl((0,0,height+.72),radius+.05,.24,"roof",96)
    for z in (1.2,5.0,9.0,13.0,17.0,21.5):
        m.cyl((0,0,z),radius+.025,.055,"steel",96)
    for i in range(48):
        a = i*math.tau/48
        m.bar((radius*math.cos(a),radius*math.sin(a),.9),
              (radius*math.cos(a),radius*math.sin(a),height+.5),.016,"steel",4)
    m.ring((0,0,height+1.85),radius-.6,.035)
    m.ring((0,0,height+1.35),radius-.6,.025)
    for i in range(32):
        a=i*math.tau/32
        m.bar(((radius-.6)*math.cos(a),(radius-.6)*math.sin(a),height+.85),
              ((radius-.6)*math.cos(a),(radius-.6)*math.sin(a),height+1.85),.035,"steel",6)
    # Ladder silhouette and intermittent safety hoops.
    for y in (-.38,.38):
        m.bar((radius+.3,y,.7),(radius+.3,y,height+1.7),.045,"steel",6)
    for i in range(int(height/.35)):
        m.bar((radius+.3,-.38,.9+i*.35),(radius+.3,.38,.9+i*.35),.035,"steel",6)
    for z in range(3,int(height)+1,2):
        m.ring((radius+.65,0,z),.65,.035,"steel",16)
    m.cyl((0,0,height+1.0),.55,.25,"steel",24)
    return m


def pipe_rack(length=6):
    m = Mesh()
    for x in (0,):
        for y in (-1.1,1.1):
            m.box((x,y,.2),(.9,.9,.4),"foundation")
            m.box((x,y,2.35),(.2,.2,4.3),"red")
        m.box((x,0,4.5),(.25,2.7,.28),"red")
    for y in (-.65,.65):
        m.bar((0,y,5.0),(length,y,5.0),.38,"steel",20)
    return m


PART_BUILDERS = {
    "architecture.industrial-bay": industrial_bay,
    "architecture.roof-bay": roof_bay,
    "electrical.line-gantry": gantry,
    "electrical.switching-bay": switching_bay,
    "electrical.busbar": busbar,
    "electrical.transformer": transformer,
    "electrical.control-house": control_house,
    "thermal.storage-tank": storage_tank,
    "thermal.pipe-rack": pipe_rack,
}
