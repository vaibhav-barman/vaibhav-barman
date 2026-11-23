"""Generates every animated SVG in the profile README.

Aesthetic: black, white and liquid chrome. Minimal type, hairlines, real 3D.

GitHub READMEs cannot run JS or WebGL, so every 3D effect here is real
geometry (orthographic spheres, perspective floors, rotating solids) projected
to 2D in Python and baked into SMIL keyframes. Each SVG is self-contained:
no external fonts, images or scripts.

    python scripts/generate_assets.py            # writes ./assets
"""
import math, os, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "assets"
os.makedirs(OUT, exist_ok=True)

# ----------------------------------------------------------------- tokens
BG, PANEL = "#000000", "#050505"
LINE, LINE2 = "#1a1a1a", "#2a2a2a"
DIM, MID, TEXT, WHITE = "#6b6b6b", "#a3a3a3", "#ededed", "#ffffff"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"
SANS = "'Helvetica Neue',Helvetica,Inter,'Segoe UI',Arial,sans-serif"


def n(x):
    s = f"{x:.1f}"
    return s[:-2] if s.endswith(".0") else s


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def write(name, body):
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(body)
    print(f"{name:26} {os.path.getsize(path)/1024:7.1f} KB")


def kt(xs):
    """keyTimes string, forced strictly increasing inside [0, 1]."""
    out, last = [], -1.0
    for x in xs:
        x = min(max(x, 0.0), 1.0)
        if x <= last:
            x = last + 1e-4
        out.append(x)
        last = x
    out[-1] = 1.0
    return ";".join(f"{v:.4f}" for v in out)


# ---------------------------------------------------------- shared defs
def chrome_defs(p=""):
    """Gradients for liquid-chrome objects. Bounding-box units, so they fit any shape."""
    return f'''
<linearGradient id="{p}chl" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#fafafa"/><stop offset=".28" stop-color="#d4d4d4"/>
  <stop offset=".46" stop-color="#5c5c5c"/><stop offset=".5" stop-color="#0b0b0b"/>
  <stop offset=".6" stop-color="#2e2e2e"/><stop offset=".82" stop-color="#bdbdbd"/>
  <stop offset="1" stop-color="#6e6e6e"/></linearGradient>
<radialGradient id="{p}chs" cx=".34" cy=".26" r=".75">
  <stop offset="0" stop-color="#fff" stop-opacity=".95"/><stop offset=".18" stop-color="#fff" stop-opacity=".25"/>
  <stop offset=".55" stop-color="#fff" stop-opacity="0"/></radialGradient>
<radialGradient id="{p}chr" cx=".5" cy=".5" r=".5">
  <stop offset=".62" stop-color="#000" stop-opacity="0"/><stop offset=".9" stop-color="#000" stop-opacity=".55"/>
  <stop offset="1" stop-color="#000" stop-opacity=".9"/></radialGradient>
<linearGradient id="{p}cht" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#7a7a7a"/><stop offset=".22" stop-color="#ffffff"/>
  <stop offset=".45" stop-color="#9c9c9c"/><stop offset=".62" stop-color="#f2f2f2"/>
  <stop offset=".8" stop-color="#6a6a6a"/><stop offset="1" stop-color="#d9d9d9"/></linearGradient>
<linearGradient id="{p}shn" x1="0" y1="0" x2="1" y2="0" gradientUnits="objectBoundingBox">
  <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".46" stop-color="#fff" stop-opacity="0"/>
  <stop offset=".5" stop-color="#fff" stop-opacity=".95"/><stop offset=".54" stop-color="#fff" stop-opacity="0"/>
  <stop offset="1" stop-color="#fff" stop-opacity="0"/>
  <animateTransform attributeName="gradientTransform" type="translate" values="-1 0;1 0;1 0" keyTimes="0;.45;1" dur="6s" repeatCount="indefinite"/></linearGradient>
<radialGradient id="{p}glow"><stop offset="0" stop-color="#fff" stop-opacity=".9"/><stop offset=".35" stop-color="#fff" stop-opacity=".25"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
<radialGradient id="{p}shd"><stop offset="0" stop-color="#fff" stop-opacity=".22"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'''


def ball(cx, cy, r, p=""):
    """A small chrome sphere."""
    return (f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(r)}" fill="url(#{p}chl)"/>'
            f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(r)}" fill="url(#{p}chs)"/>'
            f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(r)}" fill="url(#{p}chr)"/>')


def frame_open(W, H, label, extra_defs=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{esc(label)}">
<title>{esc(label)}</title>
<defs>{chrome_defs()}{extra_defs}
<clipPath id="frame"><rect width="{W}" height="{H}" rx="20"/></clipPath>
</defs>
<g clip-path="url(#frame)">
<rect width="{W}" height="{H}" fill="{BG}"/>'''


def frame_close(W, H):
    return f'''</g>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="20" fill="none" stroke="{LINE2}"/>
<path d="M18 34V18H34M{W-34} 18H{W-18}V34M{W-18} {H-34}V{H-18}H{W-34}M34 {H-18}H18V{H-34}" fill="none" stroke="#3d3d3d" stroke-width="1"/>
</svg>
'''


def dot_grid(W, H, step=24, op=.16, mask=None):
    d = "".join(f"M{x} {y}h0" for x in range(step // 2, W, step) for y in range(step // 2, H, step))
    m = f' mask="url(#{mask})"' if mask else ""
    return f'<path d="{d}" stroke="#fff" stroke-width="1.3" stroke-linecap="round" opacity="{op}"{m}/>'


def persp_floor(W, top, H, vx, rows=14, cols=26, op=.35, gid="pf", dur=2.4):
    """Perspective floor grid: lines to a vanishing point plus rows that drift toward the viewer."""
    A = H - top
    out = [f'<linearGradient id="{gid}" x1="0" y1="{top}" x2="0" y2="{H}" gradientUnits="userSpaceOnUse">'
           f'<stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".35" stop-color="#fff" stop-opacity="{op*.4:.2f}"/>'
           f'<stop offset="1" stop-color="#fff" stop-opacity="{op}"/></linearGradient>']
    d = ""
    for k in range(-cols, cols + 1):
        d += f"M{n(vx)} {top}L{n(vx + k * W / cols * 1.6)} {H}"
    out.append(f'<path d="{d}" stroke="url(#{gid})" stroke-width="1" fill="none"/>')
    for i in range(rows):
        vals = []
        for f in range(13):
            s = (i + f / 12) / rows
            vals.append(n(top + A * s ** 2.6))
        out.append(f'<path d="M0 0H{W}" stroke="url(#{gid})" stroke-width="1"><animateTransform attributeName="transform" type="translate" '
                   f'values="{";".join("0 " + v for v in vals)}" dur="{dur}s" repeatCount="indefinite"/></path>')
    return "".join(out)


# ----------------------------------------------------------------- 3D maths
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


def octahedron():
    v = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
    return v, min_edges(v)


def stella():
    cube = [(a, b, c) for a in (-1, 1) for b in (-1, 1) for c in (-1, 1)]
    v = normed(cube)
    e = [(i, j) for i in range(8) for j in range(i + 1, 8)
         if sum(1 for k in range(3) if cube[i][k] != cube[j][k]) == 2]
    return v, e


# ---------------------------------------------------------- chrome sphere
def chrome_sphere(cx, cy, R, dur=14, meridians=10, uid="cs"):
    """Liquid-chrome sphere with rotating meridian wires (orthographic, vertical axis).

    Every great circle through the poles shows one visible half at a time. Its
    projection is x = R*s*sin(t), y = R*cos(t) with s = sin(phase), so all
    meridians share one keyframe list and differ only by a begin offset.
    """
    F, P = 36, 22
    vals, ops = [], []
    for f in range(F + 1):
        ph = -math.pi / 2 + math.pi * f / F
        s = math.sin(ph)
        pts = [(cx + R * s * math.sin(math.pi * k / P), cy - R * math.cos(math.pi * k / P)) for k in range(P + 1)]
        vals.append("M" + "L".join(f"{n(x)} {n(y)}" for x, y in pts))
        ops.append(f"{0.05 + 0.5 * math.cos(ph) ** 1.5:.2f}")
    wires = "".join(
        f'<path d="{vals[0]}" fill="none" stroke="#fff" stroke-width="1"><animate attributeName="d" values="{";".join(vals)}" '
        f'dur="{dur}s" begin="-{n(dur * k / meridians)}s" repeatCount="indefinite"/><animate attributeName="opacity" values="{";".join(ops)}" '
        f'dur="{dur}s" begin="-{n(dur * k / meridians)}s" repeatCount="indefinite"/></path>'
        for k in range(meridians))
    par = "".join(f'<path d="M{n(cx - R * math.cos(a))} {n(cy - R * math.sin(a))}H{n(cx + R * math.cos(a))}" stroke="#fff" stroke-width="1" opacity=".16"/>'
                  for a in [math.radians(x) for x in (-60, -30, 0, 30, 60)])
    return f'''<g>
<circle cx="{cx}" cy="{cy}" r="{R}" fill="url(#{uid}L)"/>
<g clip-path="url(#{uid}C)" style="mix-blend-mode:screen">{par}{wires}</g>
<circle cx="{cx}" cy="{cy}" r="{R}" fill="url(#chs)"/>
<circle cx="{cx}" cy="{cy}" r="{R}" fill="url(#chr)"/>
<ellipse cx="{n(cx - R*.38)}" cy="{n(cy - R*.52)}" rx="{n(R*.2)}" ry="{n(R*.08)}" fill="url(#glow)" opacity=".9" transform="rotate(-28 {n(cx - R*.38)} {n(cy - R*.52)})"/>
<circle cx="{cx}" cy="{cy}" r="{R - .5}" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width="1"/>
</g>''', f'''
<clipPath id="{uid}C"><circle cx="{cx}" cy="{cy}" r="{R}"/></clipPath>
<linearGradient id="{uid}L" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#fdfdfd"/><stop offset=".22" stop-color="#cfcfcf"/>
  <stop offset=".43" stop-color="#6b6b6b"/><stop offset=".485" stop-color="#151515"/>
  <stop offset=".515" stop-color="#000"/><stop offset=".58" stop-color="#262626"/>
  <stop offset=".78" stop-color="#9a9a9a"/><stop offset=".93" stop-color="#e6e6e6"/>
  <stop offset="1" stop-color="#8a8a8a"/>
  <animate attributeName="y1" values="0;.03;0" dur="7s" repeatCount="indefinite"/>
</linearGradient>'''


def orbit(cx, cy, Rr, tilt, roll, labels, dur, phase0=0.0, F=96):
    """A 3D ring around the sphere. Returns (back layer, front layer)."""
    def P(u):
        p = (Rr * math.cos(u), 0, Rr * math.sin(u))
        return rz(rx(p, tilt), roll)

    K = 120
    back, front = "", ""
    pts = [P(2 * math.pi * k / K) for k in range(K + 1)]
    for k in range(K):
        a, b = pts[k], pts[k + 1]
        seg = f"M{n(cx + a[0])} {n(cy - a[1])}L{n(cx + b[0])} {n(cy - b[1])}"
        if (a[2] + b[2]) / 2 < 0:
            back += seg
        else:
            front += seg
    back_l = [f'<path d="{back}" fill="none" stroke="#fff" stroke-opacity=".18" stroke-width="1" stroke-dasharray="2 5"/>']
    front_l = [f'<path d="{front}" fill="none" stroke="#fff" stroke-opacity=".55" stroke-width="1.1"/>']
    for i, lab in enumerate(labels):
        u0 = phase0 + 2 * math.pi * i / len(labels)
        xs, ys, fo, bo, rs = [], [], [], [], []
        for f in range(F + 1):
            p = P(u0 + 2 * math.pi * f / F)
            xs.append(n(cx + p[0])); ys.append(n(cy - p[1]))
            fr = p[2] >= 0
            fo.append("1" if fr else "0"); bo.append("0" if fr else ".5")
            rs.append(n(5.2 + 2.6 * p[2] / Rr))
        A = lambda attr, v: f'<animate attributeName="{attr}" values="{";".join(v)}" dur="{dur}s" repeatCount="indefinite"/>'
        D = lambda attr, v: f'<animate attributeName="{attr}" values="{";".join(v)}" dur="{dur}s" calcMode="discrete" repeatCount="indefinite"/>'
        node = lambda: (f'<circle r="{rs[0]}" fill="url(#chl)">{A("cx", xs)}{A("cy", ys)}{A("r", rs)}</circle>'
                        f'<circle r="{rs[0]}" fill="url(#chs)">{A("cx", xs)}{A("cy", ys)}{A("r", rs)}</circle>')
        back_l.append(f'<g opacity="0">{node()}{D("opacity", bo)}</g>')
        lx = [n(float(x) + 12) for x in xs]
        ly = [n(float(y) - 10) for y in ys]
        front_l.append(f'<g opacity="0"><circle r="16" fill="url(#glow)" opacity=".35">{A("cx", xs)}{A("cy", ys)}</circle>{node()}'
                       f'<text font-family="{MONO}" font-size="12" fill="{TEXT}" letter-spacing="1">{A("x", lx)}{A("y", ly)}{esc(lab)}</text>'
                       f'{D("opacity", fo)}</g>')
    return "".join(back_l), "".join(front_l)


# --------------------------------------------------------------------- hero
def hero():
    W, H = 1200, 600
    cx, cy, R = 858, 262, 132
    sph, sph_defs = chrome_sphere(cx, cy, R, dur=16, uid="hs")
    b1, f1 = orbit(cx, cy, R * 1.45, math.radians(20), math.radians(-13),
                   ["retrieve()", "grade()", "reflect()", "generate()"], 22)
    b2, f2 = orbit(cx, cy, R * 1.95, math.radians(-7), math.radians(24),
                   ["mcp://tools", "rewrite()", "critic"], 34, phase0=2.2)
    # reflection: the sphere mirrored under the floor line, faded
    floor_y = cy + R + 54
    phrases = [
        "building agents that check their own work",
        "self-rag  ·  corrective-rag  ·  multi-agent writers",
        "langgraph state machines with bounded retries",
        "local models via ollama, frontier models via api",
        "deterministic checks > model opinion",
    ]
    T = 3.6 * len(phrases)
    typ = []
    for i, ph in enumerate(phrases):
        a, b = i / len(phrases), (i + 1) / len(phrases)
        w = len(ph) * 9.05 + 4
        typ.append(f'<clipPath id="tp{i}"><rect x="96" y="452" height="28" width="0">'
                   f'<animate attributeName="width" values="0;0;{n(w)};{n(w)};0;0" keyTimes="{kt([0, a, a + (b - a) * .45, b - .012, b, 1])}" dur="{n(T)}s" repeatCount="indefinite"/></rect></clipPath>'
                   f'<text x="96" y="472" font-family="{MONO}" font-size="15" fill="{TEXT}" clip-path="url(#tp{i})" letter-spacing=".2">{esc(ph)}</text>')
        typ.append(f'<rect x="96" y="459" width="9" height="17" fill="#fff"><animate attributeName="x" values="96;96;{n(96 + w)};{n(96 + w)};96;96" keyTimes="{kt([0, a, a + (b - a) * .45, b - .012, b, 1])}" dur="{n(T)}s" repeatCount="indefinite"/>'
                   f'<animate attributeName="opacity" values="1;0;1" dur="1s" calcMode="discrete" repeatCount="indefinite"/></rect>' if i == 0 else "")
    # one shared caret driven by all phrases
    xs_caret, kts = [], []
    for i, ph in enumerate(phrases):
        a, b = i / len(phrases), (i + 1) / len(phrases)
        w = len(ph) * 9.05 + 4
        xs_caret += ["96", n(96 + w), n(96 + w), "96"]
        kts += [a, a + (b - a) * .45, b - .012, b - .001]
    typ = [t for t in typ if not t.startswith("<rect")]
    typ.append(f'<rect x="96" y="459" width="9" height="17" fill="#fff"><animate attributeName="x" values="{";".join(xs_caret + ["96"])}" keyTimes="{kt(kts + [1])}" dur="{n(T)}s" repeatCount="indefinite"/>'
               f'<animate attributeName="opacity" values="1;0" dur="1s" calcMode="discrete" repeatCount="indefinite"/></rect>')

    ticks = "".join(f'<path d="M{x} 548v{6 if x % 100 == 0 else 3}" stroke="#fff" stroke-opacity=".35"/>' for x in range(72, 1130, 20))
    extra = sph_defs + f'''
<radialGradient id="vig" cx=".5" cy=".45" r=".75"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".85"/></radialGradient>
<radialGradient id="dm" cx=".7" cy=".42" r=".55"><stop offset="0" stop-color="#fff" stop-opacity=".9"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
<mask id="dmask"><rect width="{W}" height="{H}" fill="url(#dm)"/></mask>
<linearGradient id="rf" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".28"/><stop offset=".55" stop-color="#fff" stop-opacity="0"/></linearGradient>
<linearGradient id="flg" x1="0" y1="0" x2="1" y2="0"><stop offset=".42" stop-color="#000"/><stop offset=".62" stop-color="#fff"/></linearGradient>
<mask id="flm"><rect width="{W}" height="{H}" fill="url(#flg)"/></mask>
<mask id="rmask"><rect x="0" y="{floor_y}" width="{W}" height="{H - floor_y}" fill="url(#rf)"/></mask>
<radialGradient id="halo" cx=".5" cy=".5" r=".5"><stop offset=".55" stop-color="#fff" stop-opacity=".10"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'''
    svg = frame_open(W, H, "Vaibhav Barman. AI engineer building agentic systems. A liquid-chrome sphere with agents orbiting it.", extra)
    svg += f'''
{dot_grid(W, H, 26, .22, "dmask")}
<g mask="url(#flm)">{persp_floor(W, floor_y, H, cx, rows=12, cols=22, op=.28, gid="hf", dur=3)}
<rect x="0" y="{floor_y}" width="{W}" height="1" fill="#fff" opacity=".3"/></g>
<circle cx="{cx}" cy="{cy}" r="{n(R * 2.25)}" fill="url(#halo)"/>
<g mask="url(#rmask)"><g transform="translate(0 {n(2 * floor_y)}) scale(1 -1)">{sph}</g></g>
<ellipse cx="{cx}" cy="{floor_y + 2}" rx="{n(R * .95)}" ry="10" fill="url(#shd)"/>
{b2}{b1}
{sph}
{f1}{f2}
<rect width="{W}" height="{H}" fill="url(#vig)"/>

<g font-family="{MONO}" font-size="12" letter-spacing="3" fill="{DIM}">
  <text x="96" y="92">VB — 2026</text>
  <text x="250" y="92">AGENTIC SYSTEMS</text>
  <circle cx="440" cy="88" r="3.5" fill="#fff"><animate attributeName="opacity" values="1;.15;1" dur="2s" repeatCount="indefinite"/></circle>
  <text x="452" y="92" fill="{TEXT}">ONLINE · OPEN TO REMOTE ROLES</text>
</g>
<text x="92" y="214" font-family="{SANS}" font-weight="200" font-size="96" letter-spacing="14" fill="url(#cht)">VAIBHAV</text>
<text x="92" y="214" font-family="{SANS}" font-weight="200" font-size="96" letter-spacing="14" fill="url(#shn)">VAIBHAV</text>
<text x="92" y="314" font-family="{SANS}" font-weight="800" font-size="96" letter-spacing="6" fill="url(#cht)">BARMAN</text>
<text x="92" y="314" font-family="{SANS}" font-weight="800" font-size="96" letter-spacing="6" fill="url(#shn)" style="animation-delay:1s">BARMAN</text>
<path d="M96 360H560" stroke="#fff" stroke-opacity=".3"/>
<rect x="96" y="358.5" width="60" height="3" fill="#fff"><animate attributeName="x" values="96;500;96" dur="7s" repeatCount="indefinite" calcMode="spline" keySplines=".6 0 .4 1;.6 0 .4 1"/></rect>
<text x="96" y="396" font-family="{MONO}" font-size="14" letter-spacing="4" fill="{MID}">AI ENGINEER  /  AGENTS  /  RAG  /  MCP</text>
<text x="96" y="434" font-family="{MONO}" font-size="12" letter-spacing="3" fill="{DIM}">STDOUT</text>
<text x="76" y="472" font-family="{MONO}" font-size="15" fill="{DIM}">›</text>
{"".join(typ)}
{ticks}
<g font-family="{MONO}" font-size="11" letter-spacing="2.5" fill="{DIM}">
  <text x="72" y="576">LANGGRAPH · LANGCHAIN · FASTMCP · OLLAMA · GROQ · GEMINI · FASTAPI · POSTGRES</text>
  <text x="{W - 72}" y="576" text-anchor="end">IST +05:30 · BITS PILANI</text>
</g>
<text x="{cx}" y="{n(cy - R * 2.02)}" text-anchor="middle" font-family="{MONO}" font-size="11" letter-spacing="4" fill="{DIM}">CORE · ORCHESTRATOR</text>
'''
    svg += frame_close(W, H)
    write("hero.svg", svg)


# ----------------------------------------------------- pipeline renderer
class Scene:
    """Nodes floating over a perspective floor, with packets running the graph on a timeline."""

    def __init__(self, W, H, gx, hy=96, f=560, D=6.0, camH=3.0, T=15.0, p="", h=0.75):
        self.W, self.H, self.gx, self.hy, self.f, self.D, self.camH, self.T = W, H, gx, hy, f, D, camH, T
        self.p, self.h = p, h
        self.nodes, self.edges, self.events = {}, {}, []
        self.arrivals = {}

    def scr(self, x, z, h=0.0):
        d = z + self.D
        return self.gx + self.f * x / d, self.hy + self.f * (self.camH - h) / d

    def node(self, key, x, z, label, sub="", kind="ball"):
        self.nodes[key] = dict(x=x, z=z, label=label, sub=sub, kind=kind)

    def node_s(self, key, sx, sy, label, sub="", kind="ball"):
        """Place a node by where its ball should appear on screen; solve for world x, z."""
        d = self.f * (self.camH - self.h) / (sy - self.hy)
        self.node(key, (sx - self.gx) * d / self.f, d - self.D, label, sub, kind)

    def pos(self, key):
        nd = self.nodes[key]
        return self.scr(nd["x"], nd["z"], self.h)

    def edge(self, a, b, bend=0.0, dashed=False):
        self.edges[(a, b)] = dict(bend=bend, dashed=dashed)

    def path(self, a, b):
        (x0, y0), (x1, y1) = self.pos(a), self.pos(b)
        bend = self.edges[(a, b)]["bend"]
        if not bend:
            return f"M{n(x0)} {n(y0)}L{n(x1)} {n(y1)}", math.dist((x0, y0), (x1, y1))
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        L = math.dist((x0, y0), (x1, y1)) or 1
        nx, ny = -(y1 - y0) / L, (x1 - x0) / L
        qx, qy = mx + nx * bend, my + ny * bend
        length, prev = 0.0, (x0, y0)
        for k in range(1, 41):
            t = k / 40
            pt = ((1 - t) ** 2 * x0 + 2 * (1 - t) * t * qx + t * t * x1, (1 - t) ** 2 * y0 + 2 * (1 - t) * t * qy + t * t * y1)
            length += math.dist(prev, pt); prev = pt
        return f"M{n(x0)} {n(y0)}Q{n(qx)} {n(qy)} {n(x1)} {n(y1)}", length

    def run(self, seq, t0, step=0.55):
        """A packet walks the node sequence starting at t0 seconds. Returns end time."""
        t = t0
        for a, b in zip(seq, seq[1:]):
            self.events.append((a, b, t, t + step))
            self.arrivals.setdefault(b, []).append(t + step)
            t += step
        self.arrivals.setdefault(seq[0], []).append(t0)
        return t

    def render_floor(self, x0, x1):
        p = self.p
        out = []
        # floor grid in world space
        d = ""
        for gx in range(-8, 9):
            (ax, ay), (bx, by) = self.scr(gx * .75, -0.8), self.scr(gx * .75, 9)
            d += f"M{n(ax)} {n(ay)}L{n(bx)} {n(by)}"
        for gz in range(0, 13):
            z = -0.8 + gz * .82
            (ax, ay), (bx, by) = self.scr(-6.5, z), self.scr(6.5, z)
            d += f"M{n(ax)} {n(ay)}L{n(bx)} {n(by)}"
        out.append(f'<path d="{d}" stroke="#fff" stroke-width="1" fill="none" opacity=".13" mask="url(#{p}fm)"/>')
        return "".join(out)

    def render(self):
        p, T = self.p, self.T
        out = []
        # shadows + stems
        for k, nd in self.nodes.items():
            fx, fy = self.scr(nd["x"], nd["z"], 0)
            bx, by = self.pos(k)
            s = self.f / (nd["z"] + self.D)
            out.append(f'<ellipse cx="{n(fx)}" cy="{n(fy)}" rx="{n(s * .32)}" ry="{n(s * .07)}" fill="url(#shd)"/>'
                       f'<path d="M{n(fx)} {n(fy)}L{n(bx)} {n(by)}" stroke="#fff" stroke-opacity=".14" stroke-dasharray="1 3"/>')
        # base edges
        for (a, b), e in self.edges.items():
            d, _ = self.path(a, b)
            dash = ' stroke-dasharray="3 5"' if e["dashed"] else ""
            out.append(f'<path d="{d}" fill="none" stroke="#fff" stroke-opacity=".22" stroke-width="1.2"{dash}/>')
        # comets
        for a, b, t0, t1 in self.events:
            d, L = self.path(a, b)
            A, B = t0 / T, t1 / T
            tail = min(70, L * .6)
            C = min(B + (B - A) * tail / max(L, 1), .9999)
            out.append(f'<path d="{d}" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-dasharray="{n(tail)} {n(L + tail + 10)}" stroke-dashoffset="{n(tail)}">'
                       f'<animate attributeName="stroke-dashoffset" values="{n(tail)};{n(tail)};{n(tail - L)};{n(-L - 2)};{n(-L - 2)}" keyTimes="{kt([0, A, B, C, 1])}" dur="{n(T)}s" repeatCount="indefinite"/></path>'
                       f'<g opacity="0"><circle r="11" fill="url(#{p}glow)"/><circle r="3.2" fill="#fff"/>'
                       f'<animateMotion path="{d}" keyPoints="0;0;1;1" keyTimes="{kt([0, A, B, 1])}" calcMode="linear" dur="{n(T)}s" repeatCount="indefinite"/>'
                       f'<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="{kt([0, A, A + .002, B - .002, B, 1])}" dur="{n(T)}s" repeatCount="indefinite"/></g>')
        # nodes, far to near
        for k, nd in sorted(self.nodes.items(), key=lambda kv: -kv[1]["z"]):
            bx, by = self.pos(k)
            s = self.f / (nd["z"] + self.D)
            r = s * (.16 if nd["kind"] == "ball" else .11)
            pulse = ""
            arr = sorted(set(round(t, 3) for t in self.arrivals.get(k, [])))
            if arr:
                vals, kts, last = ["0"], [0.0], 0.0
                for t in arr:
                    a = t / T
                    if a - .004 <= last:
                        continue
                    vals += ["0", "1", "0"]; kts += [a - .004, a, min(a + .07, .999)]
                    last = kts[-1]
                vals.append("0"); kts.append(1)
                pulse = (f'<circle cx="{n(bx)}" cy="{n(by)}" r="{n(r * 2.4)}" fill="url(#{p}glow)" opacity="0">'
                         f'<animate attributeName="opacity" values="{";".join(vals)}" keyTimes="{kt(kts)}" dur="{n(T)}s" repeatCount="indefinite"/></circle>'
                         f'<circle cx="{n(bx)}" cy="{n(by)}" r="{n(r * 1.9)}" fill="none" stroke="#fff" stroke-width="1" opacity="0">'
                         f'<animate attributeName="opacity" values="{";".join(vals)}" keyTimes="{kt(kts)}" dur="{n(T)}s" repeatCount="indefinite"/></circle>')
            if nd["kind"] == "ring":
                body = (f'<circle cx="{n(bx)}" cy="{n(by)}" r="{n(r * 1.35)}" fill="{BG}" stroke="#fff" stroke-width="1.3"/>'
                        f'<circle cx="{n(bx)}" cy="{n(by)}" r="{n(r * .45)}" fill="#fff"/>')
            else:
                body = ball(bx, by, r, p)
            fs = 12.5 if s > 80 else 11.5
            lab = (f'<text x="{n(bx)}" y="{n(by - r - 10)}" text-anchor="middle" font-family="{MONO}" font-size="{fs}" fill="{TEXT}" letter-spacing=".5">{esc(nd["label"])}</text>')
            if nd["sub"]:
                lab += f'<text x="{n(bx)}" y="{n(by + r + 17)}" text-anchor="middle" font-family="{MONO}" font-size="10.5" fill="{DIM}" letter-spacing=".5">{esc(nd["sub"])}</text>'
            out.append(f'{pulse}{body}{lab}')
        return "".join(out)

    def window_text(self, x, y, items, size=12, anchor="start", fill=TEXT, ls="2"):
        """Text that swaps by time window: items = [(t0, t1, text), ...]"""
        T, out = self.T, []
        for t0, t1, txt in items:
            A, B = t0 / T, t1 / T
            out.append(f'<text x="{n(x)}" y="{n(y)}" text-anchor="{anchor}" font-family="{MONO}" font-size="{size}" fill="{fill}" letter-spacing="{ls}" opacity="0">{esc(txt)}'
                       f'<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="{kt([0, A, A + .01, B - .01, B, 1])}" dur="{n(T)}s" repeatCount="indefinite"/></text>')
        return "".join(out)


def wrap(text, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > width and cur:
            lines.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    return lines


def info_column(x, idx, tag, title, blurb, specs, chips, repo):
    out = [f'<text x="{x}" y="66" font-family="{MONO}" font-size="12" letter-spacing="3" fill="{DIM}">{esc(idx)}</text>']
    tw = len(tag) * 8.4 + 24
    out.append(f'<rect x="{x + 70}" y="51" width="{n(tw)}" height="22" rx="11" fill="none" stroke="#fff" stroke-opacity=".5"/>'
               f'<text x="{n(x + 70 + tw / 2)}" y="66" text-anchor="middle" font-family="{MONO}" font-size="11" letter-spacing="2.5" fill="{TEXT}">{esc(tag)}</text>')
    y = 118
    for line in title:
        out.append(f'<text x="{x - 2}" y="{y}" font-family="{SANS}" font-weight="300" font-size="40" letter-spacing="1" fill="url(#cht)">{esc(line)}</text>'
                   f'<text x="{x - 2}" y="{y}" font-family="{SANS}" font-weight="300" font-size="40" letter-spacing="1" fill="url(#shn)">{esc(line)}</text>')
        y += 46
    y += 6
    for line in wrap(blurb, 46):
        out.append(f'<text x="{x}" y="{y}" font-family="{SANS}" font-size="15" fill="{MID}">{esc(line)}</text>')
        y += 22
    y += 14
    out.append(f'<path d="M{x} {y - 12}H{x + 380}" stroke="#fff" stroke-opacity=".15"/>')
    for k, v in specs:
        out.append(f'<text x="{x}" y="{y + 8}" font-family="{MONO}" font-size="12" fill="{DIM}" letter-spacing="1">{esc(k)}</text>'
                   f'<text x="{x + 96}" y="{y + 8}" font-family="{MONO}" font-size="12.5" fill="{TEXT}">{esc(v)}</text>')
        y += 23
    y += 12
    cx_ = x
    for c in chips:
        w = len(c) * 7.6 + 18
        if cx_ + w > x + 390:
            cx_ = x; y += 30
        out.append(f'<rect x="{n(cx_)}" y="{y}" width="{n(w)}" height="22" rx="4" fill="#0c0c0c" stroke="#fff" stroke-opacity=".22"/>'
                   f'<text x="{n(cx_ + w / 2)}" y="{y + 15}" text-anchor="middle" font-family="{MONO}" font-size="11.5" fill="{TEXT}">{esc(c)}</text>')
        cx_ += w + 8
    out.append(f'<text x="{x}" y="472" font-family="{MONO}" font-size="12.5" letter-spacing="1" fill="{TEXT}">github.com/vaibhav-barman/{esc(repo)}'
               f'<tspan fill="{MID}"> →</tspan></text>')
    return "".join(out)


def panel(fname, label, scene, info, overlay=""):
    W, H = scene.W, scene.H
    p = scene.p
    extra = f'''
<linearGradient id="{p}fg" x1="0" y1="{scene.hy + 40}" x2="0" y2="{H}" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".4" stop-color="#fff" stop-opacity=".8"/><stop offset="1" stop-color="#fff" stop-opacity="1"/></linearGradient>
<linearGradient id="{p}fx" x1="0" y1="0" x2="{scene.W}" y2="0" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#000"/><stop offset=".06" stop-color="#fff"/><stop offset=".55" stop-color="#fff"/><stop offset=".64" stop-color="#000"/></linearGradient>
<mask id="{p}fm"><rect width="{W}" height="{H}" fill="url(#{p}fg)"/></mask>
<mask id="{p}gm"><rect width="{W}" height="{H}" fill="url(#{p}fx)"/></mask>
<linearGradient id="{p}sep" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".25"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'''
    svg = frame_open(W, H, label, extra)
    svg += f'''
<g mask="url(#{p}gm)">{scene.render_floor(0, 0)}</g>
{scene.render()}
{overlay}
<rect x="748" y="30" width="1" height="{H - 60}" fill="url(#{p}sep)"/>
{info}'''
    svg += frame_close(W, H)
    write(fname, svg)


# ------------------------------------------------------- featured: blog
def fx_blog():
    T = 14.0
    s = Scene(1200, 500, gx=380, hy=72, f=400, D=4.0, camH=3.8, T=T, h=.75)
    s.node_s("topic", 78, 365, "topic", "cli · streamlit", kind="ring")
    s.node_s("router", 175, 268, "router", "closed/hybrid/open")
    s.node_s("research", 260, 392, "research", "tavily · no llm")
    s.node_s("orch", 345, 290, "orchestrator", "plans 4–6 sections")
    for i, sy in enumerate([228, 280, 336, 398]):
        s.node_s(f"w{i}", 488 + (i % 2) * 14, sy, f"worker_{i + 1}", "")
    s.node_s("reduce", 610, 300, "reducer", "order · cite · save")
    s.node_s("md", 690, 392, "blogs/*.md", "", kind="ring")
    s.edge("topic", "router"); s.edge("router", "research", dashed=True); s.edge("research", "orch")
    s.edge("router", "orch")
    for i in range(4):
        s.edge("orch", f"w{i}"); s.edge(f"w{i}", "reduce")
    s.edge("reduce", "md")
    st = .5
    # pass 1: closed book, no research
    t = s.run(["topic", "router", "orch"], 0.4, st)
    for i in range(4):
        e = s.run(["orch", f"w{i}", "reduce"], t, st * 1.4)
    s.run(["reduce", "md"], e, st)
    # pass 2: open book, research first
    t = s.run(["topic", "router", "research", "orch"], 7.4, st)
    for i in range(4):
        e = s.run(["orch", f"w{i}", "reduce"], t, st * 1.4)
    s.run(["reduce", "md"], e, st)
    ov = (f'<text x="48" y="66" font-family="{MONO}" font-size="12" letter-spacing="3" fill="{DIM}">RUN</text>'
          + s.window_text(92, 66, [(0, 7, "closed_book · timeless topic · research skipped"),
                                    (7, 14, "open_book · time-sensitive · tavily research first")], 12, fill=TEXT, ls="1")
          + f'<text x="48" y="472" font-family="{MONO}" font-size="11.5" letter-spacing="1" fill="{DIM}">Send() fans out one worker per section · unsupported links stripped</text>')
    info = info_column(784, "P / 01", "MULTI-AGENT", ["Blog Writing Agent"],
                       "Give it a topic. It decides whether the web is needed, plans the post, writes every section in parallel and saves Markdown with real sources only.",
                       [("graph", "LangGraph · Send fan-out"), ("model", "Gemini · structured output"),
                        ("budget", "20 req/day, every call metered"), ("guards", "no invented links, honest gaps")],
                       ["LangGraph", "Gemini", "Tavily", "Pydantic", "Streamlit", "uv"], "blog-wriring-agent")
    panel("fx-blog.svg", "Blog Writing Agent: router, optional research, orchestrator, parallel section workers, reducer.", s, info, ov)


# --------------------------------------------------- featured: self-rag
def fx_selfrag():
    T = 18.0
    s = Scene(1200, 500, gx=380, hy=72, f=400, D=4.0, camH=3.8, T=T, h=.75)
    s.node_s("q", 66, 352, "question", "", kind="ring")
    s.node_s("dec", 150, 262, "RETRIEVE?", "decide")
    s.node_s("direct", 330, 206, "direct", "no retrieval")
    s.node_s("ret", 232, 352, "retrieve", "chroma top-4")
    s.node_s("rel", 318, 270, "ISREL", "grade chunks")
    s.node_s("gen", 398, 352, "generate", "per chunk")
    s.node_s("sup", 482, 268, "ISSUP", "grounded?")
    s.node_s("rev", 548, 206, "revise", "≤ 2 rounds")
    s.node_s("use", 590, 352, "ISUSE", "useful?")
    s.node_s("rw", 404, 428, "rewrite", "", kind="ball")
    s.node_s("ans", 692, 272, "answer", "+ cited chunk", kind="ring")
    s.edge("q", "dec"); s.edge("dec", "direct"); s.edge("direct", "use", bend=-40, dashed=True)
    s.edge("dec", "ret"); s.edge("ret", "rel"); s.edge("rel", "gen"); s.edge("gen", "sup")
    s.edge("sup", "rev", bend=18); s.edge("rev", "sup", bend=18); s.edge("sup", "use"); s.edge("use", "ans")
    s.edge("use", "rw", bend=-20); s.edge("rw", "ret", bend=-20)
    st = .5
    s.run(["q", "dec", "direct", "use", "ans"], 0.3, st)
    s.run(["q", "dec", "ret", "rel", "gen", "sup", "rev", "sup", "use", "ans"], 3.6, st)
    s.run(["q", "dec", "ret", "rel", "gen", "sup", "use", "rw", "ret", "rel", "gen", "sup", "use", "ans"], 10.0, st)
    ov = (f'<text x="48" y="58" font-family="{MONO}" font-size="12" letter-spacing="3" fill="{DIM}">PATH</text>'
          + s.window_text(100, 58, [(0, 3.4, "A · no retrieval needed → answer directly"),
                                     (3.4, 9.8, "B · not fully supported → revise until grounded"),
                                     (9.8, 18, "C · not useful → rewrite query, retrieve again")], 12, fill=TEXT, ls="1")
          + f'<text x="48" y="472" font-family="{MONO}" font-size="11.5" letter-spacing="1" fill="{DIM}">pydantic judgements · bounded retries + revisions, so it always halts</text>')
    info = info_column(784, "P / 02", "REFLECTIVE RAG", ["Self-RAG"],
                       "Decides whether to retrieve, grades each chunk, checks that its answer is grounded and useful, and rewrites the query when it is not.",
                       [("graph", "LangGraph · 11 nodes"), ("llm", "Groq gpt-oss-20b → 120b"),
                        ("embed", "Ollama mxbai-embed-large"), ("store", "Chroma, local")],
                       ["LangGraph", "Groq", "Ollama", "Chroma", "Pydantic", "Streamlit"], "self-rag")
    panel("fx-selfrag.svg", "Self-RAG: decide retrieval, grade relevance, check support and usefulness, revise or rewrite.", s, info, ov)


# ------------------------------------------------------- featured: crag
def fx_crag():
    T = 18.0
    s = Scene(1200, 500, gx=380, hy=72, f=400, D=4.0, camH=3.8, T=T, h=.75)
    s.node_s("q", 66, 362, "question", "", kind="ring")
    s.node_s("ret", 168, 276, "retrieve", "pinecone top-4")
    s.node_s("ev", 268, 366, "evaluate", "score 0 → 1")
    s.node_s("rw", 336, 238, "rewrite", "keyword query")
    s.node_s("web", 470, 226, "web_search", "tavily")
    s.node_s("ref", 448, 392, "refine", "strip · filter")
    s.node_s("gen", 576, 298, "generate", "cited answer")
    s.node_s("ans", 690, 372, "answer", "", kind="ring")
    s.edge("q", "ret"); s.edge("ret", "ev"); s.edge("ev", "ref"); s.edge("ev", "rw")
    s.edge("rw", "web"); s.edge("web", "ref"); s.edge("ref", "gen"); s.edge("gen", "ans")
    st = .55
    s.run(["q", "ret", "ev", "ref", "gen", "ans"], 0.4, st)
    t = s.run(["q", "ret", "ev"], 6.4, st)
    s.run(["ev", "ref"], t, st * 3.2)
    s.run(["ev", "rw", "web", "ref", "gen", "ans"], t, st)
    t = s.run(["q", "ret", "ev"], 12.4, st)
    s.run(["ev", "rw", "web", "ref", "gen", "ans"], t, st)
    # score bars
    phases = [(0, 6, "CORRECT", [.88, .64, .33, .12]),
              (6, 12, "AMBIGUOUS", [.58, .47, .36, .21]),
              (12, 18, "INCORRECT", [.24, .15, .09, .05])]
    bx, by, bw = 470, 92, 200
    ov = [f'<text x="48" y="58" font-family="{MONO}" font-size="12" letter-spacing="3" fill="{DIM}">VERDICT</text>',
          s.window_text(132, 58, [(a, b, f"{v}  ·  " + {"CORRECT": "a chunk > 0.7 → use the books",
                                                          "AMBIGUOUS": "in between → books + web",
                                                          "INCORRECT": "all < 0.3 → ignore, search web"}[v]) for a, b, v, _ in phases], 12, fill=TEXT, ls="1"),
          f'<text x="{bx}" y="{by - 12}" font-family="{MONO}" font-size="10.5" letter-spacing="2" fill="{DIM}">CHUNK SCORES</text>']
    for thr in (.3, .7):
        x = bx + 26 + bw * thr
        ov.append(f'<path d="M{n(x)} {by - 4}V{by + 66}" stroke="#fff" stroke-opacity=".35" stroke-dasharray="2 3"/>'
                  f'<text x="{n(x)}" y="{by + 80}" text-anchor="middle" font-family="{MONO}" font-size="10" fill="{DIM}">{thr}</text>')
    for i in range(4):
        y = by + i * 16
        vals, kts = [], []
        for a, b, _, sc in phases:
            w = n(bw * sc[i])
            vals += [w, w]; kts += [a / T + .015, b / T]
        vals = [vals[-1]] + vals; kts = [0] + kts
        ov.append(f'<text x="{bx}" y="{y + 8}" font-family="{MONO}" font-size="10" fill="{DIM}">c{i + 1}</text>'
                  f'<rect x="{bx + 26}" y="{y}" width="{bw}" height="9" rx="2" fill="#fff" fill-opacity=".06"/>'
                  f'<rect x="{bx + 26}" y="{y}" width="{vals[0]}" height="9" rx="2" fill="url(#cht)">'
                  f'<animate attributeName="width" values="{";".join(vals)}" keyTimes="{kt(kts)}" dur="{n(T)}s" repeatCount="indefinite" calcMode="spline" keySplines="{";".join([".5 0 .2 1"] * (len(vals) - 1))}"/></rect>')
    ov.append(f'<text x="48" y="472" font-family="{MONO}" font-size="11.5" letter-spacing="1" fill="{DIM}">answers only from refined context · cites file.pdf p.N or url</text>')
    info = info_column(784, "P / 03", "CORRECTIVE RAG", ["Corrective RAG"],
                       "Grades what the retriever returns before trusting it. Good chunks are refined into strips, weak ones trigger a rewritten web search.",
                       [("graph", "LangGraph · conditional edges"), ("llm", "Gemini flash-lite → flash"),
                        ("embed", "Ollama nomic-embed-text"), ("store", "Pinecone serverless")],
                       ["LangGraph", "Gemini", "Ollama", "Pinecone", "Tavily", "Streamlit"], "corrective-rag")
    panel("fx-crag.svg", "Corrective RAG: retrieve, score each chunk, route correct / ambiguous / incorrect, refine, generate.", s, info, "".join(ov))


# ---------------------------------------------------- how I build (loop)
def agent_loop():
    T = 12.0
    s = Scene(1200, 400, gx=600, hy=14, f=480, D=4.0, camH=3.6, T=T, p="", h=.8)
    names = [("task", "doc · diff · prompt"), ("plan", "langgraph state"), ("act", "tools · mcp · rag"),
             ("observe", "run · lint · retrieve"), ("critic", "rules · grounding"), ("ship", "you confirm")]
    spots = [(120, 270), (305, 170), (500, 262), (700, 170), (890, 262), (1080, 174)]
    keys = []
    for i, ((nm, sub), (sx, sy)) in enumerate(zip(names, spots)):
        k = f"n{i}"; keys.append(k)
        s.node_s(k, sx, sy, nm, sub, kind="ring" if i in (0, 5) else "ball")
    for a, b in zip(keys, keys[1:]):
        s.edge(a, b)
    s.edge("n4", "n1", bend=-250, dashed=True)
    st = .6
    t = s.run(keys[:5], 0.3, st)
    t = s.run(["n4", "n1"], t, st * 1.6)
    t = s.run(keys[1:5], t, st)
    s.run(["n4", "n5"], t, st)
    ov = (f'<text x="48" y="44" font-family="{MONO}" font-size="12" letter-spacing="3" fill="{DIM}">AGENT_LOOP.RUN()</text>'
          + s.window_text(1152, 44, [(0, 2.7, "draft"), (2.7, 3.7, "✗ rejected · revise with findings"), (3.7, 6.3, "redraft"), (6.3, 12, "✓ passed · ship")], 12, "end", TEXT, "2")
          + f'<text x="600" y="376" text-anchor="middle" font-family="{MONO}" font-size="12.5" letter-spacing="1" fill="{DIM}">pass / fail comes from exit codes, linters, rules and retrieval checks, <tspan fill="{TEXT}">not from the model grading itself</tspan></text>')
    W, H = s.W, s.H
    extra = f'''
<linearGradient id="fg" x1="0" y1="90" x2="0" y2="{H}" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".9"/><stop offset="1" stop-color="#fff" stop-opacity=".2"/></linearGradient>
<mask id="fm"><rect width="{W}" height="{H}" fill="url(#fg)"/></mask>'''
    svg = frame_open(W, H, "Agent loop: task, plan, act, observe, critic, ship. Rejected drafts go back from critic to plan.", extra)
    svg += s.render_floor(0, 0) + s.render() + ov + frame_close(W, H)
    write("agent-loop.svg", svg)


# ------------------------------------------------------------ poly icons
def poly_icon(name, frames_fn, F=60, dur=16, dots=True, sw=1.4):
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
    dots_svg = (f'<path d="{pv[0]}" stroke="#fff" stroke-width="4.5" stroke-linecap="round" fill="none"><animate attributeName="d" values="{";".join(pv)}" dur="{dur}s" repeatCount="indefinite"/></path>'
                if dots else "")
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}" width="{S}" height="{S}" role="img" aria-label="rotating 3D wireframe">
<defs>{chrome_defs()}
<linearGradient id="s" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff"/><stop offset=".5" stop-color="#8a8a8a"/><stop offset="1" stop-color="#e5e5e5"/></linearGradient>
<clipPath id="c"><rect x="4" y="4" width="{S - 8}" height="{S - 8}" rx="19"/></clipPath>
</defs>
<rect x="1" y="1" width="{S - 2}" height="{S - 2}" rx="22" fill="#000" stroke="#fff" stroke-opacity=".28" stroke-width="1.2"/>
<circle cx="{c}" cy="{c}" r="62" fill="url(#glow)" opacity=".16"/>
<ellipse cx="{c}" cy="140" rx="38" ry="4" fill="url(#shd)"/>
<g clip-path="url(#c)"><path d="{dv[0]}" stroke="url(#s)" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round" fill="none"><animate attributeName="d" values="{";".join(dv)}" dur="{dur}s" repeatCount="indefinite"/></path>
{dots_svg}</g>
<path d="M14 30V14H30M130 14H146V30M146 130V146H130M30 146H14V130" fill="none" stroke="#fff" stroke-opacity=".4" stroke-width="1"/>
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
            x, w = x * c - w * s, x * s + w * c
            y, z = y * c - z * s, y * s + z * c
            k = 2.6 / (2.6 - w)
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
                v = 2 * math.pi * j / N + a
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
        for li in range(layers):
            y = -0.72 + 1.44 * li / (layers - 1)
            sq = [(0.8 * sx, y, 0.8 * sz) for sx, sz in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
            off = a * (1 if li % 2 == 0 else -1)
            sq = [rx(ry(p, off + 0.4), 0.48) for p in sq]
            pp = [proj(p, 80, 78, R, 3.4) for p in sq]
            pls.append((pp, True)); verts += pp
        axis = [proj(rx((0, y, 0), 0.48), 80, 78, R, 3.4) for y in (-0.95, 0.95)]
        pls.append((axis, False))
        return pls, verts
    return fn


def icons():
    v, e = icosahedron()
    poly_icon("poly-commit.svg", solid_frames(v, e, 52), dur=18)
    poly_icon("poly-forge.svg", tesseract_frames(50), dur=14)
    poly_icon("poly-glossa.svg", stack_frames(42), dur=20)
    poly_icon("poly-recovery.svg", torus_frames(58), dur=16, dots=False, sw=1.1)
    v, e = stella()
    poly_icon("poly-mcp.svg", solid_frames(v, e, 54, spin=(1, 2)), dur=18)
    v, e = dodecahedron()
    poly_icon("poly-odyssey.svg", solid_frames(v, e, 52, spin=(1, -1)), dur=22)


# --------------------------------------------------------- section bars
def header(fname, idx, label, note):
    W, H = 1200, 84
    v, e = octahedron()
    F, dur = 48, 12
    vals = []
    for f in range(F + 1):
        a = 2 * math.pi * f / F
        pts = [rx(ry(p, a), .45) for p in v]
        pp = [proj(p, W - 62, 42, 17, 3.0) for p in pts]
        vals.append("".join(f"M{n(pp[i][0])} {n(pp[i][1])}L{n(pp[j][0])} {n(pp[j][1])}" for i, j in e))
    lw = len(label) * 15.5
    x1 = 146 + lw + 28
    x2 = W - 110 - len(note) * 7.6 - 24
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{esc(idx)} {esc(label)}">
<defs>{chrome_defs()}
<linearGradient id="ln" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity=".55"/><stop offset="1" stop-color="#fff" stop-opacity=".05"/></linearGradient>
</defs>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" fill="#000" stroke="{LINE2}"/>
<text x="30" y="58" font-family="{SANS}" font-weight="200" font-size="46" fill="url(#cht)">{esc(idx)}</text>
<text x="30" y="58" font-family="{SANS}" font-weight="200" font-size="46" fill="url(#shn)">{esc(idx)}</text>
<path d="M118 24V60" stroke="#fff" stroke-opacity=".25"/>
<text x="146" y="50" font-family="{MONO}" font-size="20" letter-spacing="5" fill="{TEXT}">{esc(label)}</text>
<path d="M{n(x1)} 43H{n(x2)}" stroke="url(#ln)" stroke-width="1"/>
<circle cx="{n(x1)}" cy="43" r="2.5" fill="#fff"><animate attributeName="cx" values="{n(x1)};{n(x2)}" dur="4.5s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.1;.85;1" dur="4.5s" repeatCount="indefinite"/></circle>
<text x="{W - 110}" y="48" text-anchor="end" font-family="{MONO}" font-size="12.5" letter-spacing="1.5" fill="{DIM}">{esc(note)}</text>
<path d="{vals[0]}" fill="none" stroke="#fff" stroke-opacity=".85" stroke-width="1.1" stroke-linejoin="round"><animate attributeName="d" values="{";".join(vals)}" dur="{dur}s" repeatCount="indefinite"/></path>
</svg>
'''
    write(fname, svg)


def footer():
    W, H = 1200, 220
    cx, cy, R = 600, 92, 42
    sph, sd = chrome_sphere(cx, cy, R, dur=12, meridians=8, uid="fs")
    b, f = orbit(cx, cy, R * 1.9, math.radians(78), math.radians(-12), ["eof"], 14)
    svg = frame_open(W, H, "End of transmission", sd)
    svg += f'''
{persp_floor(W, 150, H, 600, rows=8, cols=24, op=.3, gid="ff", dur=3)}
<ellipse cx="{cx}" cy="150" rx="46" ry="5" fill="url(#shd)"/>
{b}{sph}{f}
<text x="96" y="98" font-family="{MONO}" font-size="12" letter-spacing="4" fill="{DIM}">SESSION.CLOSE()</text>
<text x="{W - 96}" y="98" text-anchor="end" font-family="{MONO}" font-size="12" letter-spacing="4" fill="{DIM}">END OF TRANSMISSION</text>
<text x="600" y="194" text-anchor="middle" font-family="{MONO}" font-size="12" letter-spacing="3" fill="{TEXT}">thanks for scrolling · vaibhav-barman.github.io</text>
'''
    svg += frame_close(W, H)
    write("footer.svg", svg)


if __name__ == "__main__":
    hero()
    fx_blog()
    fx_selfrag()
    fx_crag()
    agent_loop()
    icons()
    header("h-whoami.svg", "01", "WHOAMI", "identity.load()")
    header("h-flagship.svg", "02", "FLAGSHIP BUILDS", "three agentic pipelines")
    header("h-loop.svg", "03", "HOW I BUILD", "agent_loop.run()")
    header("h-builds.svg", "04", "MORE BUILDS", "ls ./agents ./rag ./mcp")
    header("h-lab.svg", "05", "LAB NOTEBOOK", "ls ./experiments")
    header("h-stack.svg", "06", "STACK", "pip freeze | grep signal")
    header("h-telemetry.svg", "07", "TELEMETRY", "contributions in 3d")
    header("h-creds.svg", "08", "TRAINING DATA", "education + credentials")
    header("h-connect.svg", "09", "OPEN A CHANNEL", "handshake()")
    footer()
