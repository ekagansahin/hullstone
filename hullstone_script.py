# Hullstone, script version -> STL. Edit the points, run: python hullstone_script.py
import numpy as np, struct
from scipy.spatial import ConvexHull

# Base (z=0), mm
base = [(0,0,0),(45,-5,0),(60,20,0),(40,45,0),(-20,25,0)]
# Upper vertices (x, y, z) - tilted pentagon top + ridge
top = [(30,0,22),(48,15,30),(38,38,34),(15,35,30),(8,15,26),
       (-18,25,2)]   # sharp low tip on the left

pts = np.array(base + top, float)
hull = ConvexHull(pts)

def write_stl(fn, pts, hull):
    c = pts.mean(0)
    with open(fn, "wb") as f:
        f.write(b"\0"*80); f.write(struct.pack("<I", len(hull.simplices)))
        for s in hull.simplices:
            a, b, d = pts[s]
            n = np.cross(b-a, d-a)
            if np.dot(n, a-c) < 0: b, d = d, b; n = -n   # outward normal
            n /= np.linalg.norm(n)
            f.write(struct.pack("<12fH", *n, *a, *b, *d, 0))

write_stl("hullstone.stl", pts, hull)
print(len(hull.simplices), "triangles, volume %.0f mm3" % hull.volume)
