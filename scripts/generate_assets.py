"""Generates the animated 3D SVG assets for the profile README.

Everything is real 3D geometry projected to 2D per frame and baked into
SMIL keyframes, because GitHub READMEs cannot run JS/WebGL. No external
fonts, images, filters or scripts: each SVG is fully self-contained.
"""
import math, os, random, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "assets"
os.makedirs(OUT, exist_ok=True)

BG0, BG1 = "#060a13", "#0b1022"
CYAN, VIOLET, PINK, GREEN = "#22d3ee", "#a78bfa", "#f472b6", "#34d399"
TEXT, DIM, LINE = "#e2e8f0", "#64748b", "#1e293b"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"
SANS = "'Segoe UI',Inter,'Helvetica Neue',Helvetica,Arial,sans-serif"


def n(x):
    s = f"{x:.1f}"
    return s[:-2] if s.endswith(".0") else s


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def anim(attr, vals, dur, extra=""):
    return (f'<animate attributeName="{attr}" values="{";".join(vals)}" '
            f'dur="{n(dur)}s" repeatCount="indefinite"{extra}/>')


def write(name, body):
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(body)
    print(f"{name:28} {os.path.getsize(path)/1024:7.1f} KB")


# ---------------------------------------------------------------- 3D maths
def rx(p, a):
    x, y, z = p; c, s = math.cos(a), math.sin(a)
    return (x, y * c - z * s, y * s + z * c)


def ry(p, a):
    x, y, z = p; c, s = math.cos(a), math.sin(a)
    return (x * c + z * s, y, -x * s + z * c)


def rz(p, a):
    x, y, z = p; c, s = math.cos(a), math.sin(a)
    return (x * c - y * s, x * s + y * c, z)


def proj(p, cx, cy, R, d=3.4):
    x, y, z = p
    k = d / (d - z)
    return cx + R * x * k, cy - R * y * k


def min_edges(vs, tol=1e-3):
    """Edges of a convex uniform solid = vertex pairs at the minimum distance."""
    best, pairs = 1e9, []
    for i in range(len(vs)):
        for j in range(i + 1, len(vs)):
            dd = math.dist(vs[i], vs[j])
            if dd < best - tol:
                best, pairs = dd, [(i, j)]
            elif abs(dd - best) <= tol:
                pairs.append((i, j))
    return pairs


def normed(vs):
    m = max(math.sqrt(sum(c * c for c in v)) for v in vs)
    return [tuple(c / m for c in v) for v in vs]


PHI = (1 + 5 ** 0.5) / 2


def icosahedron():
    v = []
    for a in (-1, 1):
        for b in (-PHI, PHI):
            v += [(0, a, b), (a, b, 0), (b, 0, a)]
    v = normed(v)
    return v, min_edges(v)


def dodecahedron():
    v = [(a, b, c) for a in (-1, 1) for b in (-1, 1) for c in (-1, 1)]
    for a in (-1 / PHI, 1 / PHI):
        for b in (-PHI, PHI):
            v += [(0, a, b), (a, b, 0), (b, 0, a)]
    v = normed(v)
    return v, min_edges(v)


def stella():
    cube = [(a, b, c) for a in (-1, 1) for b in (-1, 1) for c in (-1, 1)]
    v = normed(cube)
    e = [(i, j) for i in range(8) for j in range(i + 1, 8)
         if sum(1 for k in range(3) if cube[i][k] != cube[j][k]) == 2]
    return v, e


def fib_sphere(k):
    ga = math.pi * (3 - 5 ** 0.5)
    out = []
    for i in range(k):
        y = 1 - 2 * (i + 0.5) / k
        r = math.sqrt(1 - y * y)
        out.append((r * math.cos(ga * i), y, r * math.sin(ga * i)))
    return out


def knn_edges(vs, k=3):
    e = set()
    for i, p in enumerate(vs):
        near = sorted(range(len(vs)), key=lambda j: math.dist(p, vs[j]))[1:k + 1]
        for j in near:
            e.add((min(i, j), max(i, j)))
    return sorted(e)


# ------------------------------------------------------------ shared parts
def defs_common():
    return f'''<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BG0}"/><stop offset="1" stop-color="{BG1}"/></linearGradient>
<linearGradient id="cv" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient>
<linearGradient id="cvp" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}"/><stop offset=".55" stop-color="{VIOLET}"/><stop offset="1" stop-color="{PINK}"/></linearGradient>'''


def grid_floor(W, hy, H, vx, cell_dur=1.8, rows=20, max_op=0.55, gid="g"):
    """Perspective floor: fan of lines to a vanishing point + rows that fly toward the camera."""
    A = H - hy
    out = [f'<linearGradient id="{gid}f" x1="0" y1="{hy}" x2="0" y2="{H}" gradientUnits="userSpaceOnUse">'
           f'<stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".25" stop-color="#fff" stop-opacity="{max_op*0.35:.2f}"/>'
           f'<stop offset="1" stop-color="#fff" stop-opacity="{max_op}"/></linearGradient>'
           f'<mask id="{gid}m"><rect x="0" y="{hy}" width="{W}" height="{H-hy}" fill="url(#{gid}f)"/></mask>']
    out.append(f'<g mask="url(#{gid}m)" stroke="url(#cv)" stroke-width="1.1" fill="none">')
    fan = "".join(f"M{vx} {hy}L{n(vx + k * 118 * 1.4)} {n(hy + A * 1.4)}" for k in range(-22, 23))
    out.append(f'<path d="{fan}"/>')
    steps = 6
    for k in range(rows):
        vals = []
        for s in range(steps + 1):
            z = 1 + 0.25 * (k - s / steps)
            vals.append(f"M0 {n(hy + A / z)}H{W}")
        out.append(f'<path d="{vals[0]}">{anim("d", vals, cell_dur)}</path>')
    out.append("</g>")
    out.append(f'<rect x="0" y="{hy-1}" width="{W}" height="2" fill="url(#hz)"/>')
    return "\n".join(out)


# -------------------------------------------------------------------- hero
def hero():
    W, H = 1200, 440
    hy = 272
    cx, cy, R = 952, 196, 150
    F, DUR = 48, 26

    pts = fib_sphere(36)
    edges = knn_edges(pts, 3)
    core, core_e = icosahedron()

    def frame(f):
        a = 2 * math.pi * f / F
        outer = [rz(rx(ry(p, a), 0.38), -0.22) for p in pts]
        inner = [rz(rx(ry(tuple(c * 0.42 for c in p), -2 * a), 0.5 + a), 0.3) for p in core]
        return outer, inner

    frames = [frame(f) for f in range(F + 1)]
    g = []
    # outer shell edges
    for (i, j) in edges:
        dv, ov = [], []
        for outer, _ in frames:
            x1, y1 = proj(outer[i], cx, cy, R); x2, y2 = proj(outer[j], cx, cy, R)
            dv.append(f"M{n(x1)} {n(y1)}L{n(x2)} {n(y2)}")
            t = ((outer[i][2] + outer[j][2]) / 2 + 1) / 2
            ov.append(f"{0.07 + 0.55 * t * t:.2f}")
        g.append(f'<path d="{dv[0]}" opacity="{ov[0]}">{anim("d", dv, DUR)}{anim("opacity", ov, DUR)}</path>')
    shell_edges = "\n".join(g)
    g = []
    hot = {2, 9, 17, 23, 30}
    for i in range(len(pts)):
        xs, ys, rs, os_ = [], [], [], []
        for outer, _ in frames:
            x, y = proj(outer[i], cx, cy, R)
            t = (outer[i][2] + 1) / 2
            xs.append(n(x)); ys.append(n(y))
            rs.append(n((1.3 + 2.6 * t) * (1.5 if i in hot else 1)))
            os_.append(f"{0.2 + 0.8 * t:.2f}")
        col = PINK if i in hot else (VIOLET if i % 4 == 0 else CYAN)
        g.append(f'<circle cx="{xs[0]}" cy="{ys[0]}" r="{rs[0]}" fill="{col}" opacity="{os_[0]}">'
                 f'{anim("cx", xs, DUR)}{anim("cy", ys, DUR)}{anim("r", rs, DUR)}{anim("opacity", os_, DUR)}</circle>')
    shell_nodes = "\n".join(g)
    # inner core, counter-rotating
    dv = []
    for _, inner in frames:
        d = ""
        for (i, j) in core_e:
            x1, y1 = proj(inner[i], cx, cy, R); x2, y2 = proj(inner[j], cx, cy, R)
            d += f"M{n(x1)} {n(y1)}L{n(x2)} {n(y2)}"
        dv.append(d)
    core_svg = f'<path d="{dv[0]}" stroke="{VIOLET}" stroke-width="1.3" fill="none" opacity=".9">{anim("d", dv, DUR)}</path>'

    # stars
    rnd = random.Random(7)
    stars = []
    for _ in range(46):
        x, y = rnd.uniform(20, W - 20), rnd.uniform(16, hy - 14)
        r = rnd.choice([0.6, 0.8, 1.1])
        d = rnd.uniform(2.5, 6)
        stars.append(f'<circle cx="{n(x)}" cy="{n(y)}" r="{r}" fill="#cbd5e1" opacity=".5">'
                     f'<animate attributeName="opacity" values=".1;.75;.1" dur="{n(d)}s" begin="-{n(rnd.uniform(0, d))}s" repeatCount="indefinite"/></circle>')

    # extruded title
    tx, ty, tl = 62, 168, 640
    tattr = (f'x="{tx}" y="{ty}" font-family="{SANS}" font-weight="900" font-size="78" '
             f'textLength="{tl}" lengthAdjust="spacingAndGlyphs"')
    layers = []
    depth = 11
    for i in range(depth, 0, -1):
        t = i / depth
        r_, g_, b_ = int(76 - 46 * t), int(29 - 12 * t), int(149 - 96 * t)
        layers.append(f'<text {tattr} transform="translate({n(i*0.95)} {n(i*0.95)})" fill="rgb({r_},{g_},{b_})">VAIBHAV BARMAN</text>')
    title = "\n".join(layers) + (
        f'\n<text {tattr} fill="url(#tg)" stroke="#ecfeff" stroke-width=".6">VAIBHAV BARMAN</text>')

    # typed lines
    lines = ["building AI agents that check their own work",
             "LangGraph · MCP · RAG · local LLMs",
             "generate → critique → repair → ship",
             "open to remote AI engineering roles"]
    cw, fs, lx, ly = 10.4, 17, 92, 250
    slot = 5.6
    total = slot * len(lines)
    typed, cursor_events = [], []
    for li, s in enumerate(lines):
        L = len(s); t0 = li * slot
        ev = [(0.0, 0)] if t0 > 0 else []
        t_type = min(2.0, L * 0.05)
        for c in range(1, L + 1):
            ev.append((t0 + 0.15 + t_type * c / L, c))
        t_hold = t0 + slot - 0.75
        er = 8
        for e in range(1, er + 1):
            ev.append((t_hold + 0.45 * e / er, round(L * (1 - e / er))))
        if ev[0][0] != 0:
            ev.insert(0, (0.0, 0))
        cursor_events += [(t, c) for (t, c) in ev if t >= t0 + 0.1 or li == 0]
        vals = [n(c * cw) for _, c in ev]
        kts = [f"{t/total:.4f}" for t, _ in ev]
        typed.append(
            f'<clipPath id="tc{li}"><rect x="{lx}" y="{ly-fs}" width="0" height="{fs+8}">'
            f'<animate attributeName="width" values="{";".join(vals)}" keyTimes="{";".join(kts)}" calcMode="discrete" dur="{n(total)}s" repeatCount="indefinite"/></rect></clipPath>'
            f'<text x="{lx}" y="{ly}" font-family="{MONO}" font-size="{fs}" fill="{TEXT}" textLength="{n(L*cw)}" lengthAdjust="spacing" clip-path="url(#tc{li})">{esc(s)}</text>')
    cursor_events.sort()
    if cursor_events[0][0] != 0:
        cursor_events.insert(0, (0.0, 0))
    cvals = [n(lx + c * cw + 2) for _, c in cursor_events]
    ckts = [f"{t/total:.4f}" for t, _ in cursor_events]
    cursor = (f'<rect x="{lx+2}" y="{ly-fs+2}" width="9" height="{fs+1}" fill="{CYAN}">'
              f'<animate attributeName="x" values="{";".join(cvals)}" keyTimes="{";".join(ckts)}" calcMode="discrete" dur="{n(total)}s" repeatCount="indefinite"/>'
              f'<animate attributeName="opacity" values="1;1;.15;.15" keyTimes="0;.5;.5;1" dur="1s" repeatCount="indefinite"/></rect>')

    ring = lambda rx_, ry_, rot, col, dur, dash: (
        f'<g transform="rotate({rot} {cx} {cy})"><ellipse cx="{cx}" cy="{cy}" rx="{rx_}" ry="{ry_}" fill="none" stroke="{col}" stroke-width="1" stroke-dasharray="{dash}" opacity=".55">'
        f'<animate attributeName="stroke-dashoffset" values="0;-{sum(int(v) for v in dash.split())*6}" dur="{dur}s" repeatCount="indefinite"/></ellipse>'
        f'<circle r="3.2" fill="{col}"><animateMotion dur="{dur}s" repeatCount="indefinite" path="M{cx-rx_},{cy} a{rx_},{ry_} 0 1,1 {2*rx_},0 a{rx_},{ry_} 0 1,1 {-2*rx_},0"/></circle></g>')

    brk = lambda x, y, sx, sy: f'<path d="M{x} {y+sy*22}V{y}H{x+sx*22}" fill="none" stroke="{CYAN}" stroke-width="2" opacity=".8"/>'

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Vaibhav Barman. AI Engineer, agentic systems. A rotating 3D network globe over a perspective grid.">
<title>Vaibhav Barman · AI Engineer · Agentic Systems</title>
<defs>
{defs_common()}
<linearGradient id="tg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset=".5" stop-color="#a5f3fc"/><stop offset="1" stop-color="{CYAN}"/></linearGradient>
<linearGradient id="hz" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset=".5" stop-color="{CYAN}" stop-opacity=".9"/><stop offset=".8" stop-color="{VIOLET}" stop-opacity=".9"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></linearGradient>
<radialGradient id="glow"><stop offset="0" stop-color="{VIOLET}" stop-opacity=".42"/><stop offset=".45" stop-color="{CYAN}" stop-opacity=".12"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>
<radialGradient id="sun"><stop offset="0" stop-color="{CYAN}" stop-opacity=".30"/><stop offset=".5" stop-color="{CYAN}" stop-opacity=".09"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>
<radialGradient id="shd"><stop offset="0" stop-color="{CYAN}" stop-opacity=".30"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>
<linearGradient id="scan" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#a5f3fc" stop-opacity=".07"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<clipPath id="frame"><rect width="{W}" height="{H}" rx="18"/></clipPath>
</defs>
<g clip-path="url(#frame)">
<rect width="{W}" height="{H}" fill="url(#bg)"/>
<ellipse cx="600" cy="{hy}" rx="760" ry="150" fill="url(#sun)"/>
{"".join(stars)}
{grid_floor(W, hy, H, 600)}
<ellipse cx="{cx}" cy="396" rx="170" ry="20" fill="url(#shd)"/>
<circle cx="{cx}" cy="{cy}" r="{R+70}" fill="url(#glow)"/>
{ring(R+34, 46, -18, CYAN, 14, "2 9")}
{ring(R+52, 30, 24, VIOLET, 22, "14 10")}
<g stroke="{CYAN}" stroke-width="1" fill="none" stroke-linecap="round">
{shell_edges}
</g>
{core_svg}
{shell_nodes}
<rect x="0" y="-120" width="{W}" height="120" fill="url(#scan)"><animate attributeName="y" values="-120;{H}" dur="7s" repeatCount="indefinite"/></rect>
<g font-family="{MONO}" font-size="14.5" letter-spacing="1.5">
<circle cx="70" cy="62" r="5" fill="{GREEN}"><animate attributeName="opacity" values="1;.25;1" dur="1.6s" repeatCount="indefinite"/></circle>
<text x="86" y="67" fill="{GREEN}">AGENT ONLINE</text>
<text x="226" y="67" fill="{DIM}">// github.com/vaibhav-barman</text>
<text x="{W-62}" y="67" fill="{DIM}" text-anchor="end">NODES {len(pts)} · EDGES {len(edges)}</text>
<text x="62" y="{H-34}" fill="{DIM}">status: <tspan fill="{CYAN}">open to remote roles</tspan></text>
<text x="{W-62}" y="{H-34}" fill="{DIM}" text-anchor="end">INDIA · UTC+05:30</text>
</g>
{title}
<text x="64" y="216" font-family="{MONO}" font-size="19" font-weight="700" fill="url(#cvp)" letter-spacing="5" textLength="610" lengthAdjust="spacing">AI ENGINEER // AGENTIC SYSTEMS</text>
<text x="64" y="{ly}" font-family="{MONO}" font-size="{fs}" font-weight="700" fill="{CYAN}">&gt;</text>
{"".join(typed)}
{cursor}
{brk(26, 26, 1, 1)}{brk(W-26, 26, -1, 1)}{brk(26, H-26, 1, -1)}{brk(W-26, H-26, -1, -1)}
</g>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="18" fill="none" stroke="{LINE}"/>
</svg>
'''
    write("hero.svg", svg)


# ------------------------------------------------------------ poly icons
def poly_icon(name, color, color2, frames_fn, F=60, dur=16, dots=True, sw=1.6):
    S = 160
    c = S / 2
    fr = [frames_fn(2 * math.pi * f / F) for f in range(F + 1)]
    dv, pv = [], []
    for polylines, verts in fr:
        d = ""
        for pl, closed in polylines:
            d += "M" + "L".join(f"{n(x)} {n(y)}" for x, y in pl) + ("Z" if closed else "")
        dv.append(d)
        pv.append("".join(f"M{n(x)} {n(y)}h0" for x, y in verts))
    dots_svg = (f'<path d="{pv[0]}" stroke="{color2}" stroke-width="5" stroke-linecap="round" fill="none">{anim("d", pv, dur)}</path>'
                if dots else "")
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}" width="{S}" height="{S}" role="img" aria-label="rotating 3D wireframe">
<defs>
<linearGradient id="b" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BG0}"/><stop offset="1" stop-color="{BG1}"/></linearGradient>
<linearGradient id="s" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{color}"/><stop offset="1" stop-color="{color2}"/></linearGradient>
<radialGradient id="g"><stop offset="0" stop-color="{color}" stop-opacity=".30"/><stop offset="1" stop-color="{color}" stop-opacity="0"/></radialGradient>
</defs>
<rect x="1" y="1" width="{S-2}" height="{S-2}" rx="22" fill="url(#b)" stroke="url(#s)" stroke-opacity=".55" stroke-width="1.5"/>
<clipPath id="c"><rect x="4" y="4" width="{S-8}" height="{S-8}" rx="19"/></clipPath>
<circle cx="{c}" cy="{c}" r="66" fill="url(#g)"/>
<ellipse cx="{c}" cy="138" rx="40" ry="5" fill="{color}" opacity=".14"/>
<g clip-path="url(#c)"><path d="{dv[0]}" stroke="url(#s)" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round" fill="none">{anim("d", dv, dur)}</path>
{dots_svg}</g>
<path d="M14 30V14H30M130 14H146V30M146 130V146H130M30 146H14V130" fill="none" stroke="{color}" stroke-width="1.5" opacity=".6"/>
</svg>
'''
    write(name, svg)


def solid_frames(verts, edges, R=50, spin=(1, 1), tilt=0.3, d=3.2):
    def fn(a):
        pts = [rz(rx(ry(p, spin[0] * a), tilt + spin[1] * a), 0.15) for p in verts]
        pp = [proj(p, 80, 78, R, d) for p in pts]
        return [([pp[i], pp[j]], False) for i, j in edges], pp
    return fn


def tesseract_frames(R=50):
    v4 = [(a, b, c, d) for a in (-1, 1) for b in (-1, 1) for c in (-1, 1) for d in (-1, 1)]
    e = [(i, j) for i in range(16) for j in range(i + 1, 16)
         if sum(1 for k in range(4) if v4[i][k] != v4[j][k]) == 1]

    def fn(a):
        out = []
        for (x, y, z, w) in v4:
            c, s = math.cos(a), math.sin(a)
            x, w = x * c - w * s, x * s + w * c          # XW rotation (4D)
            c, s = math.cos(a), math.sin(a)
            y, z = y * c - z * s, y * s + z * c          # YZ rotation
            k = 2.6 / (2.6 - w)                           # 4D -> 3D
            out.append(rx(ry((x * k * 0.4, y * k * 0.4, z * k * 0.4), 0.5), 0.35))
        pp = [proj(p, 80, 78, R, 4.0) for p in out]
        return [([pp[i], pp[j]], False) for i, j in e], pp
    return fn


def torus_frames(R=50, M=10, N=6, r1=0.68, r2=0.3):
    def fn(a):
        grid = [[None] * N for _ in range(M)]
        for i in range(M):
            u = 2 * math.pi * i / M
            for j in range(N):
                v = 2 * math.pi * j / N + a          # minor circles roll: one full turn per loop
                p = ((r1 + r2 * math.cos(v)) * math.cos(u), r2 * math.sin(v), (r1 + r2 * math.cos(v)) * math.sin(u))
                p = rz(rx(ry(p, a), 1.05), 0.25)
                grid[i][j] = proj(p, 80, 78, R, 3.2)
        pls = [([grid[i][j] for j in range(N)], True) for i in range(M)]
        pls += [([grid[i][j] for i in range(M)], True) for j in range(N)]
        return pls, []
    return fn


def stack_frames(R=50, layers=4):
    def fn(a):
        pls, verts = [], []
        cols = []
        for li in range(layers):
            y = -0.72 + 1.44 * li / (layers - 1)
            sq = [(0.8 * sx, y, 0.8 * sz) for sx, sz in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
            off = a * (1 if li % 2 == 0 else -1)      # alternate layers counter-rotate
            sq = [rx(ry(p, off + 0.4), 0.48) for p in sq]
            pp = [proj(p, 80, 78, R, 3.4) for p in sq]
            pls.append((pp, True)); verts += pp; cols.append(pp)
        axis = [proj(rx((0, y, 0), 0.48), 80, 78, R, 3.4) for y in (-0.95, 0.95)]
        pls.append((axis, False))
        return pls, verts
    return fn


def icons():
    v, e = icosahedron()
    poly_icon("poly-commit.svg", CYAN, VIOLET, solid_frames(v, e, 52), dur=18)
    poly_icon("poly-forge.svg", VIOLET, PINK, tesseract_frames(50), dur=14)
    poly_icon("poly-glossa.svg", CYAN, GREEN, stack_frames(42), dur=20)
    poly_icon("poly-recovery.svg", PINK, VIOLET, torus_frames(58), dur=16, dots=False, sw=1.2)
    v, e = stella()
    poly_icon("poly-mcp.svg", GREEN, CYAN, solid_frames(v, e, 54, spin=(1, 2)), dur=18)
    v, e = dodecahedron()
    poly_icon("poly-odyssey.svg", VIOLET, CYAN, solid_frames(v, e, 52, spin=(1, -1)), dur=22)


# ------------------------------------------------------- isometric loop
def agent_loop():
    W, H = 1200, 400
    u = 46
    C30, S30 = math.cos(math.radians(30)), 0.5
    fy = 236
    stages = [("TASK", "diff · doc · prompt", "#94a3b8"),
              ("PLAN", "LangGraph state", CYAN),
              ("ACT", "tools · MCP · RAG", CYAN),
              ("OBSERVE", "run · lint · retrieve", CYAN),
              ("CRITIC", "rules + faithfulness", VIOLET),
              ("SHIP", "you confirm", GREEN)]
    xs = [150 + 180 * k for k in range(6)]

    def iso(cx, gx, gy, gz):
        return cx + (gx - gy) * C30 * u, fy + (gx + gy) * S30 * u - gz * u

    def poly(pts, **kw):
        a = " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in kw.items())
        return f'<polygon points="{" ".join(f"{n(x)},{n(y)}" for x, y in pts)}" {a}/>'

    out = []
    # faint isometric floor
    fl = ""
    for k in range(-30, 60):
        x0 = k * 2 * C30 * u * 0.75
        fl += f"M{n(x0)} 0L{n(x0 + H / math.tan(math.radians(30)))} {H}M{n(x0)} {H}L{n(x0 + H / math.tan(math.radians(30)))} 0"
    out.append(f'<path d="{fl}" stroke="{CYAN}" stroke-width="1" opacity=".055" fill="none" mask="url(#fm)"/>')

    # conduits
    half = 1.5 / 2 * 2 * C30 * u / 1  # screen half-width of a 1.5 pad
    for k in range(5):
        col = GREEN if k == 4 else CYAN
        x1, x2 = xs[k] + half + 6, xs[k + 1] - half - 6
        out.append(f'<path d="M{n(x1)} {fy}H{n(x2)}" stroke="{col}" stroke-width="2" opacity=".55" stroke-dasharray="5 6">'
                   f'<animate attributeName="stroke-dashoffset" values="22;0" dur="1.1s" repeatCount="indefinite"/></path>'
                   f'<path d="M{n(x2-7)} {fy-6}L{n(x2)} {fy}L{n(x2-7)} {fy+6}" fill="none" stroke="{col}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
    # return loop (critic -> plan)
    y0 = fy + 0.75 * u + 24
    ret = f"M{xs[4]} {n(y0)}C{xs[4]} 352 {xs[1]} 352 {xs[1]} {n(y0 + 6)}"
    out.append(f'<path id="ret" d="{ret}" fill="none" stroke="{PINK}" stroke-width="2" stroke-dasharray="6 7" opacity=".8">'
               f'<animate attributeName="stroke-dashoffset" values="0;26" dur="1.2s" repeatCount="indefinite"/></path>'
               f'<path d="M{xs[1]-7} {n(y0+15)}L{xs[1]} {n(y0+5)}L{xs[1]+7} {n(y0+15)}" fill="none" stroke="{PINK}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
    out.append(f'<rect x="440" y="316" width="320" height="30" rx="15" fill="{BG0}" stroke="{PINK}" stroke-opacity=".5"/>'
               f'<text x="600" y="336" text-anchor="middle" font-family="{MONO}" font-size="14.5" fill="{PINK}">✗ rejected → revise with findings</text>')
    out.append(f'<text x="{(xs[4]+xs[5])//2}" y="{fy-14}" text-anchor="middle" font-family="{MONO}" font-size="13.5" fill="{GREEN}">✓ pass</text>')

    # pads + cubes
    for k, (name, sub, col) in enumerate(stages):
        cx = xs[k]
        pad = [iso(cx, a, b, 0) for a, b in ((-.75, -.75), (.75, -.75), (.75, .75), (-.75, .75))]
        pad2 = [iso(cx, a, b, 0) for a, b in ((-.5, -.5), (.5, -.5), (.5, .5), (-.5, .5))]
        out.append(poly(pad, fill=col, fill_opacity=".07", stroke=col, stroke_width="1.4", stroke_opacity=".7"))
        out.append(f'<g>{poly(pad2, fill=col, fill_opacity=".22", stroke="none")}'
                   f'<animate attributeName="opacity" values=".25;1;.25" dur="3s" begin="-{k*0.5}s" repeatCount="indefinite"/></g>')
        h0, h1 = 0.42, 1.42
        s = 0.5
        top = [iso(cx, a, b, h1) for a, b in ((-s, -s), (s, -s), (s, s), (-s, s))]
        left = [iso(cx, -s, s, h1), iso(cx, s, s, h1), iso(cx, s, s, h0), iso(cx, -s, s, h0)]
        right = [iso(cx, s, -s, h1), iso(cx, s, s, h1), iso(cx, s, s, h0), iso(cx, s, -s, h0)]
        beam = [iso(cx, -s, s, h0), iso(cx, s, s, h0), iso(cx, s, -s, h0), pad2[1], pad2[2], pad2[3]]
        emb = [iso(cx, a, b, h1) for a, b in ((-.24, -.24), (.24, -.24), (.24, .24), (-.24, .24))]
        cube = (poly(beam, fill=f"url(#beam{k})", stroke="none")
                + poly(left, fill=col, fill_opacity=".30", stroke=col, stroke_width="1.5", stroke_linejoin="round")
                + poly(right, fill=col, fill_opacity=".14", stroke=col, stroke_width="1.5", stroke_linejoin="round")
                + poly(top, fill=col, fill_opacity=".55", stroke="#f8fafc", stroke_opacity=".85", stroke_width="1.5", stroke_linejoin="round")
                + poly(emb, fill="#f8fafc", fill_opacity=".85", stroke="none"))
        out.append(f'<linearGradient id="beam{k}" x1="0" y1="{n(fy-h0*u)}" x2="0" y2="{n(fy+0.5*u)}" gradientUnits="userSpaceOnUse">'
                   f'<stop offset="0" stop-color="{col}" stop-opacity=".30"/><stop offset="1" stop-color="{col}" stop-opacity="0"/></linearGradient>')
        out.append(f'<g>{cube}<animateTransform attributeName="transform" type="translate" values="0 0;0 -8;0 0" keyTimes="0;.5;1" '
                   f'calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1" dur="4.2s" begin="-{k*0.7:.1f}s" repeatCount="indefinite"/></g>')
        out.append(f'<text x="{cx}" y="96" text-anchor="middle" font-family="{MONO}" font-size="19" font-weight="700" fill="{TEXT}" letter-spacing="2">{name}</text>'
                   f'<text x="{cx}" y="117" text-anchor="middle" font-family="{MONO}" font-size="13.2" fill="{col}">{esc(sub)}</text>'
                   f'<text x="{cx}" y="{n(fy+0.75*u+17)}" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{DIM}">0{k+1}</text>')

    # packets
    out.append(f'<circle r="5" fill="#ecfeff"><animateMotion dur="5s" repeatCount="indefinite" path="M{xs[0]} {fy}H{xs[4]}"/>'
               f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.06;.94;1" dur="5s" repeatCount="indefinite"/></circle>')
    out.append(f'<circle r="9" fill="{CYAN}" opacity=".25"><animateMotion dur="5s" repeatCount="indefinite" path="M{xs[0]} {fy}H{xs[4]}"/></circle>')
    out.append(f'<circle r="4.5" fill="{PINK}"><animateMotion dur="3.2s" begin="-1s" repeatCount="indefinite"><mpath href="#ret"/></animateMotion>'
               f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.1;.9;1" dur="3.2s" begin="-1s" repeatCount="indefinite"/></circle>')
    out.append(f'<circle r="4.5" fill="{GREEN}"><animateMotion dur="2.4s" repeatCount="indefinite" path="M{xs[4]} {fy}H{xs[5]}"/>'
               f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.1;.9;1" dur="2.4s" repeatCount="indefinite"/></circle>')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Isometric 3D diagram of an agent loop: task, plan, act, observe, critic, ship. Rejected drafts loop from critic back to plan.">
<title>Agent loop: task → plan → act → observe → critic → ship, with a repair loop</title>
<defs>
{defs_common()}
<linearGradient id="ff" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".55" stop-color="#fff" stop-opacity="1"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<mask id="fm"><rect width="{W}" height="{H}" fill="url(#ff)"/></mask>
<clipPath id="frame"><rect width="{W}" height="{H}" rx="18"/></clipPath>
</defs>
<g clip-path="url(#frame)">
<rect width="{W}" height="{H}" fill="url(#bg)"/>
<text x="40" y="44" font-family="{MONO}" font-size="14.5" fill="{DIM}" letter-spacing="1"><tspan fill="{CYAN}">agent_loop.run()</tspan> // the pattern behind most things I build</text>
<text x="{W-40}" y="44" text-anchor="end" font-family="{MONO}" font-size="14.5" fill="{DIM}" letter-spacing="1">ISOMETRIC · LIVE</text>
{"".join(out)}
<text x="600" y="{H-22}" text-anchor="middle" font-family="{MONO}" font-size="14.5" fill="{DIM}">pass / fail comes from exit codes, linters and rules, <tspan fill="{TEXT}">not from the model grading itself</tspan></text>
</g>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="18" fill="none" stroke="{LINE}"/>
</svg>
'''
    write("agent-loop.svg", svg)


# --------------------------------------------------------- section bars
def header(fname, idx, label, note):
    W, H = 1200, 62
    x0 = 28
    layers = "".join(
        f'<text x="{x0}" y="42" transform="translate({n(i*0.8)} {n(i*0.8)})" font-family="{SANS}" font-weight="900" font-size="34" fill="rgb({int(76-40*i/6)},{int(29-10*i/6)},{int(149-80*i/6)})">{idx}</text>'
        for i in range(6, 0, -1))
    lw = len(label) * 15.2
    lx = 92
    x1 = lx + lw + 26
    x2 = W - 30 - len(note) * 8.2 - 22
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{esc(label)}">
<defs>{defs_common()}
<linearGradient id="ln" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}" stop-opacity=".9"/><stop offset="1" stop-color="{VIOLET}" stop-opacity=".15"/></linearGradient>
</defs>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="url(#bg)" stroke="{LINE}"/>
{layers}
<text x="{x0}" y="42" font-family="{SANS}" font-weight="900" font-size="34" fill="#ecfeff">{idx}</text>
<text x="{lx}" y="40" font-family="{MONO}" font-weight="700" font-size="22" fill="url(#cvp)" letter-spacing="2" textLength="{n(lw)}" lengthAdjust="spacing">{esc(label)}</text>
<path d="M{n(x1)} 32H{n(x2)}" stroke="url(#ln)" stroke-width="1.5"/>
<rect x="{n(x1)}" y="29" width="46" height="6" rx="3" fill="{CYAN}"><animate attributeName="x" values="{n(x1)};{n(x2-46)}" dur="3.6s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.1;.85;1" dur="3.6s" repeatCount="indefinite"/></rect>
<text x="{W-30}" y="37" text-anchor="end" font-family="{MONO}" font-size="13.5" fill="{DIM}">{esc(note)}</text>
</svg>
'''
    write(fname, svg)


def footer():
    W, H = 1200, 170
    hy = 58
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="End of transmission">
<defs>
{defs_common()}
<linearGradient id="hz" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset=".5" stop-color="{CYAN}" stop-opacity=".9"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></linearGradient>
<clipPath id="frame"><rect width="{W}" height="{H}" rx="18"/></clipPath>
</defs>
<g clip-path="url(#frame)">
<rect width="{W}" height="{H}" fill="url(#bg)"/>
{grid_floor(W, hy, H, 600, cell_dur=2.2, rows=16, max_op=0.5)}
<text x="600" y="36" text-anchor="middle" font-family="{MONO}" font-size="14" fill="{DIM}" letter-spacing="2"><tspan fill="{CYAN}">&gt; session.close()</tspan>  // thanks for scrolling · vaibhav-barman.github.io<tspan fill="{CYAN}"> ▌<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1s" repeatCount="indefinite"/></tspan></text>
</g>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="18" fill="none" stroke="{LINE}"/>
</svg>
'''
    write("footer.svg", svg)


if __name__ == "__main__":
    hero()
    icons()
    agent_loop()
    header("h-whoami.svg", "01", "WHOAMI", "identity.load()")
    header("h-loop.svg", "02", "HOW I BUILD", "agent_loop.run()")
    header("h-builds.svg", "03", "FEATURED BUILDS", "ls ./agents ./rag ./mcp")
    header("h-lab.svg", "04", "LAB NOTEBOOK", "ls ./experiments")
    header("h-stack.svg", "05", "STACK", "pip freeze | grep signal")
    header("h-telemetry.svg", "06", "TELEMETRY", "contributions in 3D")
    header("h-creds.svg", "07", "TRAINING DATA", "education + credentials")
    header("h-connect.svg", "08", "OPEN A CHANNEL", "handshake()")
    footer()
