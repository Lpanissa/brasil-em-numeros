"""Converte o GeoJSON dos estados (geodata-br-states, licença MIT) em caminhos SVG leves: mapa-br.json."""
import json, math, sys
src, out = sys.argv[1], sys.argv[2]
d = json.load(open(src))
K, COS = 15.0, math.cos(math.radians(15))
proj = lambda lon, lat: ((lon + 74.2) * K * COS, (5.6 - lat) * K)

def rdp(pts, eps):
    if len(pts) < 3: return pts
    (x1, y1), (x2, y2) = pts[0], pts[-1]
    dx, dy = x2 - x1, y2 - y1; L = math.hypot(dx, dy) or 1e-9
    i_max, dmax = 0, -1
    for i in range(1, len(pts) - 1):
        x, y = pts[i]; dist = abs(dy * x - dx * y + x2 * y1 - y2 * x1) / L
        if dist > dmax: i_max, dmax = i, dist
    if dmax > eps:
        return rdp(pts[:i_max + 1], eps)[:-1] + rdp(pts[i_max:], eps)
    return [pts[0], pts[-1]]

def area(r): return abs(sum(r[i][0]*r[i-1][1]-r[i-1][0]*r[i][1] for i in range(len(r))))/2
def centro(r):
    a = 0; cx = cy = 0
    for i in range(len(r)):
        x0, y0 = r[i-1]; x1, y1 = r[i]; c = x0*y1 - x1*y0; a += c; cx += (x0+x1)*c; cy += (y0+y1)*c
    a /= 2; return (cx/(6*a), cy/(6*a)) if a else r[0]

res = {}
for f in d["features"]:
    uf = f["properties"]["SIGLA"]; g = f["geometry"]
    polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
    partes, maior = [], None
    for poly in polys:
        ring = [proj(*p[:2]) for p in poly[0]]
        if area(ring) < 4: continue
        h = len(ring) // 2
        s = rdp(ring[:h + 1], 0.45)[:-1] + rdp(ring[h:], 0.45)
        if len(s) < 4: continue
        partes.append("M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in s) + "Z")
        if maior is None or area(ring) > area(maior): maior = ring
    cx, cy = centro(maior)
    res[uf] = {"d": "".join(partes), "cx": round(cx, 1), "cy": round(cy, 1)}
xs = [float(v) for p in res.values() for v in __import__("re").findall(r"[ML]([\d.]+),", p["d"])]
ys = [float(v) for p in res.values() for v in __import__("re").findall(r",([\d.]+)", p["d"])]
json.dump({"w": round(max(xs)+4), "h": round(max(ys)+4), "ufs": res}, open(out, "w"), separators=(",", ":"))
print(len(res), "estados", round(max(xs)), "x", round(max(ys)))
