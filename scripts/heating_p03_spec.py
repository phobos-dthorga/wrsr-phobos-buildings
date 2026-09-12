"""Shared P03 geometry/gameplay dimensions. Original Phobos work, MIT, 2026."""
LIFT = .30
OUTLETS = (82, 72, 77, 87, 74.5, 79.5, 84.5, 89.5)
NAME = "Phobos' Electric Heating Works [P03 TEST]"


def access_lift(site_y, pedestrian=False):
    length = 7  # Both ramps start at the pad boundary, site Y=112.
    return LIFT * max(0, min(1, (119-site_y)/length))
