"""Original A03 facade and electrical refinements, MIT, 2026 Phobos A. D'thorga."""
from shared.prototype_parts import Mesh, transformer, switching_bay


def facade():
    """Six-metre, eighteen-metre facade sample; front faces -Y."""
    m = Mesh()
    for x in (1.1, 4.9):
        m.box((x, 0, .65), (2.2, .58, 1.3), "foundation")
        for z in (2.05, 3.55, 4.8):
            m.box((x, 0, z), (2.2, .50, 1.42 if z < 4 else 1.0))
    m.box((3, 0, 4.42), (1.6, .50, 1.75))
    # Separate upper precast panels leave visible horizontal joints.
    for z in (14.12, 15.55, 16.98):
        m.box((3, 0, z), (5.35, .50, 1.38))
    for x in (.23, 5.77):
        m.box((x, -.34, 9), (.40, .46, 18))
    m.box((3, -.06, 9.4), (5.32, .36, 8.02), "glass")
    for x in (.37, 1.4, 2.44, 3.48, 4.52, 5.63):
        m.box((x, -.32, 9.4), (.075, .16, 8.14), "steel")
    for z in (5.35, 7.38, 9.4, 11.42, 13.45):
        m.box((3, -.34, z), (5.40, .18, .09), "steel")
    for z in (5.22, 13.59, 17.84):
        m.box((3, -.33, z), (6, .32, .19))
    # Original service door, frame, rain hood and hardware.
    m.box((3, -.28, 1.72), (1.58, .12, 3.24), "red")
    for x in (2.15, 3.85):
        m.box((x, -.35, 1.74), (.10, .20, 3.42), "steel")
    m.box((3, -.36, 3.43), (1.8, .22, .12), "steel")
    m.box((3, -.53, 3.56), (2, .72, .08), "roof")
    for z in (.3, .83, 1.36, 1.89, 2.42, 2.95):
        m.box((3, -.36, z), (1.52, .035, .055), "red")
    m.box((3, -.38, 1.72), (.035, .045, 3.1), "steel")
    for x in (2.86, 3.14):
        m.bar((x, -.43, 1.35), (x, -.43, 1.64), .023, "conductor", 8)
    m.box((3, -.42, 3.96), (.58, .035, .24), "roof")
    m.box((3, -.7, .055), (2.15, 1.6, .11), "foundation")
    # A roof-edge slice demonstrates the join, rather than a complete roof.
    m.box((3, .65, 18.10), (6, 2.1, .20), "roof")
    m.box((3, -.48, 18.17), (6, .17, .24), "steel")
    m.bar((5.36, -.67, .18), (5.36, -.67, 17.98), .07, "steel", 12)
    for z in (.7, 5, 9, 13, 17.5):
        m.box((5.36, -.55, z), (.21, .23, .065), "steel")
    m.bar((5.36, -.67, .28), (5.36, -.94, .12), .07, "steel", 12)
    return m


def transformer_sample():
    m = transformer()
    # Conservator supports, inspection cover and modest service fittings.
    for x in (-1.75, 1.75):
        for y in (1.95, 2.65):
            m.bar((x, y, 4.45), (x, 2.3, 5.02), .07, "steel", 8)
    m.bar((2.70, 2.3, 5.25), (2.75, 2.3, 5.25), .26, "roof", 24)
    m.bar((2.76, 2.3, 5.25), (2.78, 2.3, 5.25), .18, "glass", 24)
    for x in (-2.2, 2.2):
        for y in (-2.65, -1.32, 0, 1.32, 2.65):
            m.cyl((x, y, 4.50), .047, .07, "conductor", 6)
    m.box((0, 1.15, 4.48), (1.1, .85, .08), "steel")
    m.bar((-1.65, -2.85, 1.05), (-1.65, -3.22, 1.05), .08, "steel", 12)
    m.bar((-1.65, -3.12, 1.05), (-1.65, -3.12, 1.38), .045, "steel", 8)
    m.ring((-1.65, -3.12, 1.4), .16, .018, "red", 16)
    m.bar((-1.81, -3.12, 1.4), (-1.49, -3.12, 1.4), .014, "red", 6)
    m.bar((-1.65, 2.3, 5.1), (-1.65, 2.3, 3.35), .055, "steel", 10)
    m.cyl((-1.65, 2.3, 3.15), .14, .40, "porcelain", 16)
    m.box((0, -2.83, 2.9), (.78, .04, .38), "roof")
    for x in (-2.15, 2.15):
        m.bar((x, -2.8, 1), (x, -3.4, .64), .025, "conductor", 8)
    # Visible cabinet latch and hinges.
    m.box((2.745, -2.0, 2.0), (.025, .04, .28), "conductor")
    for y in (-2.45, -1.55):
        m.box((2.745, y, 2.0), (.03, .05, .10), "conductor")
    return m


def switching_sample():
    m = switching_bay()
    m.bar((-4.8, -2.65, 1.45), (4.8, -2.65, 1.45), .045, "steel", 8)
    for x in (-3.8, 0, 3.8):
        m.bar((x, -2.65, 1.45), (x, -3, 2.3), .035, "steel", 8)
        m.box((x, -.40, 2.5), (.34, .04, .18), "roof")
        for y in (-3, 0, 3):
            for dx in (-.25, .25):
                m.cyl((x+dx, y, .46), .055, .065, "conductor", 6)
    m.box((-5, -2.4, .18), (1.2, 1.15, .36), "foundation")
    m.box((-5, -2.4, 1.04), (.80, .65, 1.40), "roof")
    m.box((-5, -2.75, 1.06), (.67, .035, 1.18), "steel")
    m.bar((-4.77, -2.79, 1), (-4.77, -2.79, 1.23), .022, "conductor", 8)
    return m


BUILDERS = {
    "hall_bay": (facade, 2048),
    "transformer": (transformer_sample, 2048),
    "switching_group": (switching_sample, 1024),
}
