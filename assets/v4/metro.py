"""Genere les SVG du theme « Réseau JOCHA » dans le dossier passe en argument."""
import os
import random
import sys
from xml.sax.saxutils import escape as esc

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

SANS = "'Inter','Segoe UI','Helvetica Neue',Arial,sans-serif"
MONO = "'JetBrains Mono','Fira Code',Consolas,'Liberation Mono',monospace"

LINES = {
    "O":  {"color": "#9b5de5", "name": "Ligne O · Odoo"},
    "M":  {"color": "#2ec27e", "name": "Ligne M · Mobile Money"},
    "IA": {"color": "#22b8f0", "name": "Ligne IA · Intelligence artificielle"},
    "F":  {"color": "#f5b700", "name": "Ligne F · Face B"},
}


def bullet(x, y, key, r=16, fs=None):
    c = LINES[key]["color"]
    fs = fs or (r * 1.05 if len(key) == 1 else r * 0.85)
    dark = "#1a1300" if key == "F" else "#ffffff"
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'
            f'<text x="{x}" y="{y + fs * 0.36:.1f}" text-anchor="middle" font-family="{SANS}" '
            f'font-size="{fs:.1f}" font-weight="800" fill="{dark}">{key}</text>')


def write(name, svg):
    with open(os.path.join(OUT, name), "w") as f:
        f.write(svg)


# =============================================================================
# 1. Panneau de station
# =============================================================================
def station():
    W, H = 860, 300
    windows = "".join(f'<rect x="{x}" y="46" width="34" height="16" rx="4" fill="#cfe8ff" fill-opacity=".85"/>'
                      for x in range(28, 400, 46))
    train = f'''<g class="train">
      <rect x="0" y="36" width="420" height="44" rx="18" fill="#e9eef5"/>
      <rect x="0" y="66" width="420" height="5" fill="#008751"/>
      <rect x="0" y="71" width="420" height="3" fill="#fcd116"/>
      <rect x="0" y="74" width="420" height="3" fill="#e8112d"/>
      {windows}
      <path d="M402 36 h0 a18 18 0 0 1 18 18 v8 h-30 z" fill="#0b1f3a" fill-opacity=".85"/>
      <circle cx="410" cy="72" r="3" fill="#fff3b0"/>
      <text x="200" y="31" text-anchor="middle" font-family="{SANS}" font-size="10" font-weight="700" fill="#7f93b3" letter-spacing="3">DIRECTION · LE FUTUR</text>
    </g>'''
    ticks = "".join(
        f'<line x1="0" y1="-38" x2="0" y2="{-32 if i % 3 else -28}" stroke="#0b1f3a" stroke-width="{2 if i % 3 else 3.5}" transform="rotate({i*30})"/>'
        for i in range(12))
    bullets = "".join(bullet(96 + i * 44, 186, k, r=17) for i, k in enumerate(LINES))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Station JOCHA, Cotonou-Centre">
  <style>
    .train {{ animation: pass 9s cubic-bezier(.55,0,.45,1) infinite; }}
    .sec {{ transform-origin: 0 0; animation: spin 60s linear infinite; }}
    .min {{ transform-origin: 0 0; animation: spin 3600s linear infinite; }}
    .lamp {{ animation: lamp 1.6s ease-in-out infinite; }}
    @keyframes pass {{ 0% {{ transform: translateX(-460px); }} 55%, 100% {{ transform: translateX(900px); }} }}
    @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
    @keyframes lamp {{ 50% {{ opacity: .25; }} }}
  </style>
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#07111f"/><stop offset="1" stop-color="#0d1b2e"/>
    </linearGradient>
    <linearGradient id="plate" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#173a6b"/><stop offset="1" stop-color="#0f2a52"/>
    </linearGradient>
    <clipPath id="c"><rect width="{W}" height="{H}" rx="20"/></clipPath>
  </defs>
  <g clip-path="url(#c)">
    <rect width="{W}" height="{H}" fill="url(#sky)"/>
    <!-- tunnel -->
    <rect x="0" y="20" width="{W}" height="76" fill="#0a1626"/>
    {"".join(f'<rect x="{x}" y="20" width="3" height="76" fill="#13243b"/>' for x in range(20, W, 70))}
    <rect x="0" y="84" width="{W}" height="3" fill="#3a4a60"/>
    <rect x="0" y="92" width="{W}" height="3" fill="#3a4a60"/>
    {train}
    <rect x="0" y="96" width="{W}" height="8" fill="#05090f"/>

    <!-- plaque -->
    <rect x="34" y="122" width="{W-68}" height="150" rx="18" fill="url(#plate)" stroke="#f2f5fa" stroke-width="4"/>
    <rect x="44" y="132" width="{W-88}" height="130" rx="12" fill="none" stroke="#f2f5fa" stroke-opacity=".25" stroke-width="1.5"/>
    {bullets}
    <text x="96" y="236" font-family="{MONO}" font-size="11" fill="#9db4d6" letter-spacing="2">4 LIGNES · 1 HUB</text>
    <text x="294" y="204" font-family="{SANS}" font-size="70" font-weight="900" fill="#f8fafc" letter-spacing="6">JOCHA</text>
    <text x="298" y="238" font-family="{SANS}" font-size="16" font-weight="600" fill="#c9d7ee" letter-spacing="1">Cotonou · Centre  ·  Backend · Odoo · IA</text>
    <circle class="lamp" cx="602" cy="160" r="5" fill="#3ddc84"/>
    <text x="614" y="165" font-family="{MONO}" font-size="11" fill="#3ddc84" letter-spacing="2">EN SERVICE</text>

    <!-- horloge -->
    <g transform="translate(748 197)">
      <circle r="50" fill="#0b1f3a"/>
      <circle r="44" fill="#f8fafc"/>
      {ticks}
      <g transform="rotate(84)"><rect x="-2.5" y="-24" width="5" height="26" rx="2.5" fill="#0b1f3a"/></g>
      <g class="min"><rect x="-2" y="-34" width="4" height="36" rx="2" fill="#0b1f3a"/></g>
      <g class="sec"><rect x="-.8" y="-38" width="1.6" height="46" fill="#e8112d"/><circle cy="-30" r="3.5" fill="#e8112d"/></g>
      <circle r="3.5" fill="#0b1f3a"/>
    </g>
  </g>
</svg>
'''


# =============================================================================
# 2. Plan du reseau
# =============================================================================
def plan():
    W, H = 860, 540
    HUB = (430, 250)
    routes = {
        "O":  [(60, 100), (280, 100), HUB, (580, 400), (800, 400)],
        "M":  [(60, 400), (280, 400), HUB, (580, 100), (800, 100)],
        "IA": [(60, 250), HUB, (800, 250)],
        "F":  [(430, 34), HUB, (430, 468)],
    }
    # (x, y, label, ancre, dx, dy)
    stations = {
        "O":  [(60, 100, "Odoo 17", "start", -8, -18), (170, 100, "Odoo 18", "middle", 0, -18),
               (280, 100, "Odoo 19", "middle", 0, -18), (355, 175, "OWL", "end", -14, 4),
               (505, 325, "Localisation BJ", "start", 14, 4), (580, 400, "Paie · RH", "middle", 0, 30),
               (690, 400, "Point de vente", "middle", 0, 30), (800, 400, "MECEF", "end", 8, 30)],
        "M":  [(60, 400, "FedaPay", "start", -8, 30), (170, 400, "KkiaPay", "middle", 0, 30),
               (280, 400, "MTN MoMo", "middle", 0, 30), (355, 325, "Odoo Payment", "end", -14, 4),
               (505, 175, "API REST", "start", 14, 4), (580, 100, "jocha-shop", "middle", 0, -18),
               (690, 100, "Vocal fon", "middle", 0, -18), (800, 100, "Commerçants", "end", 8, 30)],
        "IA": [(60, 250, "Python", "start", -8, -18), (150, 250, "scikit-learn", "middle", 0, 30),
               (240, 250, "PyTorch", "middle", 0, -18), (325, 250, "FaceNet", "middle", 0, 30),
               (535, 250, "Anti-usurpation", "middle", 0, 30), (630, 250, "FHIR", "middle", 0, -18),
               (715, 250, "Expo", "middle", 0, 30), (800, 250, "Urgences", "end", 8, -18)],
        "F":  [(430, 34, "Beats", "start", 16, 5), (430, 130, "Studio de nuit", "start", 16, 5),
               (430, 380, "Plateforme musicale", "start", 16, 5), (430, 468, "Face B", "start", 16, 5)],
    }
    terminus = {(60, 100), (800, 400), (60, 400), (800, 100), (60, 250), (800, 250), (430, 34), (430, 468)}

    def d(pts):
        return "M" + " L".join(f"{x} {y}" for x, y in pts)

    out = []
    # grille de fond
    out.append("".join(f'<circle cx="{x}" cy="{y}" r="1" fill="#1f2b40"/>' for x in range(20, W, 30) for y in range(20, H - 60, 30)))
    # fleuve (lagune de Cotonou, stylisee)
    out.append('<path d="M0 470 C 160 430, 260 520, 430 492 S 700 440, 860 486 L860 540 L0 540 Z" fill="#0e2a44" fill-opacity=".55"/>')
    out.append(f'<text x="840" y="520" text-anchor="end" font-family="{SANS}" font-size="11" font-style="italic" fill="#3f6a94" letter-spacing="2">lagune de Cotonou</text>')
    # lignes
    for k, pts in routes.items():
        out.append(f'<path d="{d(pts)}" fill="none" stroke="#0a0f18" stroke-width="16" stroke-linejoin="round" stroke-linecap="round"/>')
    for k, pts in routes.items():
        out.append(f'<path id="r{k}" d="{d(pts)}" fill="none" stroke="{LINES[k]["color"]}" stroke-width="9" stroke-linejoin="round" stroke-linecap="round"/>')
    # stations
    for k, sts in stations.items():
        c = LINES[k]["color"]
        for x, y, lab, anc, dx, dy in sts:
            if (x, y) in terminus:
                out.append(f'<circle cx="{x}" cy="{y}" r="10" fill="#f8fafc" stroke="{c}" stroke-width="5"/>')
            else:
                out.append(f'<circle cx="{x}" cy="{y}" r="6.5" fill="#f8fafc" stroke="#0a0f18" stroke-width="2"/>')
            out.append(f'<text x="{x+dx}" y="{y+dy}" text-anchor="{anc}" font-family="{SANS}" font-size="13" '
                       f'font-weight="{700 if (x, y) in terminus else 500}" fill="#e6edf7" '
                       f'paint-order="stroke" stroke="#0b1220" stroke-width="4" stroke-linejoin="round">{esc(lab)}</text>')
    # rames
    durs = {"O": 14, "M": 16, "IA": 12, "F": 10}
    for k in routes:
        for i, delay in enumerate((0, durs[k] / 2)):
            out.append(f'''<g><rect x="-11" y="-5" width="22" height="10" rx="5" fill="#ffffff" stroke="{LINES[k]["color"]}" stroke-width="2.5"/>
      <animateMotion dur="{durs[k]}s" begin="-{delay}s" repeatCount="indefinite" rotate="auto" keyPoints="0;1;0" keyTimes="0;.5;1" calcMode="linear"><mpath href="#r{k}"/></animateMotion></g>''')
    # pole d'echange
    hx, hy = HUB
    out.append(f'<circle cx="{hx}" cy="{hy}" r="40" fill="#3ddc84" fill-opacity=".12" class="ping"/>')
    out.append(f'<circle cx="{hx}" cy="{hy}" r="30" fill="#f8fafc" stroke="#0a0f18" stroke-width="5"/>')
    out.append(f'<text x="{hx}" y="{hy-2}" text-anchor="middle" font-family="{SANS}" font-size="11.5" font-weight="900" fill="#0b1f3a" letter-spacing="1">JOCHA</text>')
    out.append(f'<text x="{hx}" y="{hy+11}" text-anchor="middle" font-family="{SANS}" font-size="7.5" font-weight="700" fill="#4a5d7a">COTONOU</text>')
    # cartouche titre
    out.append(f'<text x="22" y="34" font-family="{MONO}" font-size="11" fill="#6f84a6" letter-spacing="3">PLAN DU RÉSEAU · ÉDITION 2026</text>')
    # legende
    lx = 22
    leg = []
    for k, v in LINES.items():
        leg.append(bullet(lx + 12, H - 22, k, r=11))
        label = v["name"].split(" · ")[1]
        leg.append(f'<text x="{lx+30}" y="{H-17}" font-family="{SANS}" font-size="12.5" font-weight="600" fill="#c9d7ee">{esc(label)}</text>')
        lx += 52 + len(label) * 7.0
    out.extend(leg)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Plan du réseau JOCHA : lignes Odoo, Mobile Money, IA et Face B">
  <style>
    .ping {{ transform-box: fill-box; transform-origin: center; animation: ping 2.4s ease-out infinite; }}
    @keyframes ping {{ 0% {{ transform: scale(.7); opacity: 1; }} 100% {{ transform: scale(1.6); opacity: 0; }} }}
  </style>
  <defs><clipPath id="c"><rect width="{W}" height="{H}" rx="20"/></clipPath></defs>
  <g clip-path="url(#c)">
    <rect width="{W}" height="{H}" fill="#0b1220"/>
    {"".join(out)}
  </g>
</svg>
'''


# =============================================================================
# 3. Tableau des departs (afficheur a palettes)
# =============================================================================
def tableau():
    W = 860
    rows = [
        ("03:28", "O",  "Facture normalisée MECEF", "17", "À L'HEURE",    "#3ddc84", ""),
        ("04:12", "M",  "Mobile Money partout",     "18", "EMBARQUEMENT", "#ffb000", "blink"),
        ("05:40", "IA", "Urgences biométriques",    "19", "EN COURS",     "#22b8f0", ""),
        ("06:00", "O",  "Driver Go · boîtier CC300", "28", "ARRIVÉ",       "#7d8796", ""),
        ("22:00", "M",  "Boutiques · assistant fon", "2",  "EN COURS",     "#22b8f0", ""),
        ("23:30", "IA", "Chatbot français ⇄ fongbè", "4",  "À L'HEURE",    "#3ddc84", ""),
        ("23:59", "F",  "Face B · rap / trap tech",  "∞",  "NOCTURNE",     "#c77dff", ""),
    ]
    top, rh = 112, 50
    H = top + len(rows) * rh + 40
    rnd = random.Random(28)
    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    cols = {"h": 34, "l": 138, "d": 186, "v": 600, "s": 664}
    widths = {"h": 82, "d": 398, "v": 50, "s": 166}
    out = []

    def cell(x, y, w):
        return (f'<rect x="{x}" y="{y-26}" width="{w}" height="36" rx="4" fill="#151515"/>'
                f'<rect x="{x}" y="{y-8.5}" width="{w}" height="1.5" fill="#050505"/>')

    def flip(x, y, txt, fill, delay, size=19, weight=700, cls=""):
        scr = "".join(rnd.choice(alpha) if ch not in " ·⇄∞'" else ch for ch in txt.upper())
        return (f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
                f'class="scr" style="animation-delay:{delay:.2f}s">{esc(scr)}</text>'
                f'<g class="{cls}"><text x="{x}" y="{y}" font-family="{MONO}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
                f'class="fin" style="animation-delay:{delay:.2f}s">{esc(txt)}</text></g>')

    for i, (h, ln, dest, voie, stat, sc, cls) in enumerate(rows):
        y = top + i * rh + 20
        base = 0.3 + i * 0.25
        if i % 2 == 0:
            out.append(f'<rect x="18" y="{y-32}" width="{W-36}" height="{rh-2}" fill="#ffffff" fill-opacity=".018"/>')
        out.append(cell(cols["h"] - 8, y, widths["h"]))
        out.append(flip(cols["h"], y, h, "#ffb000", base))
        out.append(bullet(cols["l"] + 14, y - 8, ln, r=14))
        out.append(cell(cols["d"] - 8, y, widths["d"]))
        out.append(flip(cols["d"], y, dest, "#f2f2f2", base + .1, size=17, weight=600))
        out.append(cell(cols["v"] - 8, y, widths["v"]))
        out.append(flip(cols["v"] + 17, y, voie, "#ffb000", base + .15))
        out.append(cell(cols["s"] - 8, y, widths["s"]))
        out.append(flip(cols["s"], y, stat, sc, base + .2, size=15, cls=cls))

    head = (f'<text x="34" y="44" font-family="{SANS}" font-size="22" font-weight="900" fill="#ffb000" letter-spacing="3">PROCHAINS DÉPARTS</text>'
            f'<text x="34" y="64" font-family="{SANS}" font-size="12" font-style="italic" fill="#8a7a55" letter-spacing="2">Departures · Départs</text>'
            f'<text x="{W-34}" y="44" text-anchor="end" font-family="{MONO}" font-size="12" fill="#8a8a8a" letter-spacing="2">GARE JOCHA · COTONOU</text>'
            f'<g class="blink"><circle cx="{W-124}" cy="60" r="4" fill="#e8112d"/></g>'
            f'<text x="{W-34}" y="64" text-anchor="end" font-family="{MONO}" font-size="11" fill="#e8112d" letter-spacing="2">EN DIRECT</text>')
    labels = "".join(f'<text x="{x}" y="96" font-family="{MONO}" font-size="10.5" fill="#6a6a6a" letter-spacing="2">{t}</text>'
                     for x, t in ((cols["h"], "HEURE"), (cols["l"], "LIGNE"), (cols["d"], "DESTINATION"), (cols["v"], "VOIE"), (cols["s"], "STATUT")))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Tableau des prochains départs : les projets de JOCHA">
  <style>
    .scr {{ animation: scr .9s steps(1) forwards; }}
    .fin {{ opacity: 0; animation: fin .9s steps(1) forwards; }}
    .blink {{ animation: blink 1.1s steps(1) infinite; }}
    @keyframes scr {{ 0% {{ opacity: 1; }} 100% {{ opacity: 0; }} }}
    @keyframes fin {{ 0% {{ opacity: 0; }} 100% {{ opacity: 1; }} }}
    @keyframes blink {{ 50% {{ opacity: .15; }} }}
  </style>
  <defs><clipPath id="c"><rect width="{W}" height="{H}" rx="20"/></clipPath></defs>
  <g clip-path="url(#c)">
    <rect width="{W}" height="{H}" fill="#0a0a0a"/>
    <rect x="6" y="6" width="{W-12}" height="{H-12}" rx="16" fill="none" stroke="#1f1f1f" stroke-width="3"/>
    {head}
    <rect x="34" y="78" width="{W-68}" height="1" fill="#2a2a2a"/>
    {labels}
    {"".join(out)}
    <text x="{W/2}" y="{H-14}" text-anchor="middle" font-family="{MONO}" font-size="10.5" fill="#5a5a5a" letter-spacing="2">LES HORAIRES PEUVENT ÊTRE MODIFIÉS PAR UNE BONNE IDÉE À 3 H DU MATIN</text>
  </g>
</svg>
'''


# =============================================================================
# 4. Quai (pied de page)
# =============================================================================
def quai():
    W, H = 860, 190
    msg = ("ATTENTION À LA MARCHE EN DESCENDANT DU PROFIL  ·  SERVICE DE NUIT ASSURÉ PAR LE HIBOU  ·  "
           "PROCHAIN COMMIT DANS 3 MIN  ·  MERCI D'AVOIR VOYAGÉ SUR LE RÉSEAU JOCHA  ·  ")
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="2.6" fill="#b88a00"/>' for x in range(12, W, 14) for y in (134, 148, 162))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Quai : attention à la marche en descendant du profil">
  <style>
    .mq {{ animation: mq 40s linear infinite; }}
    @keyframes mq {{ to {{ transform: translateX(-50%); }} }}
  </style>
  <defs>
    <pattern id="led" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="4" fill="#000" fill-opacity=".55"/><rect width="3" height="3" fill="#000" fill-opacity="0"/></pattern>
    <clipPath id="c"><rect width="{W}" height="{H}" rx="20"/></clipPath>
    <clipPath id="screen"><rect x="40" y="28" width="{W-80}" height="44" rx="6"/></clipPath>
  </defs>
  <g clip-path="url(#c)">
    <rect width="{W}" height="{H}" fill="#0d1117"/>
    <!-- bandeau lumineux -->
    <rect x="34" y="22" width="{W-68}" height="56" rx="10" fill="#1a1a1a"/>
    <rect x="40" y="28" width="{W-80}" height="44" rx="6" fill="#050505"/>
    <g clip-path="url(#screen)">
      <g class="mq">
        <text x="40" y="58" font-family="{MONO}" font-size="20" font-weight="700" fill="#ff8c1a" letter-spacing="2" xml:space="preserve">{esc(msg * 2)}</text>
      </g>
    </g>
    <rect x="40" y="28" width="{W-80}" height="44" rx="6" fill="url(#led)" opacity=".35"/>
    <!-- quai -->
    <rect x="0" y="100" width="{W}" height="20" fill="#2a2f38"/>
    <rect x="0" y="120" width="{W}" height="54" fill="#f5b700"/>
    {dots}
    <rect x="0" y="174" width="{W}" height="16" fill="#3a3f48"/>
    <rect x="0" y="174" width="{W}" height="3" fill="#ffffff" fill-opacity=".5"/>
    <text x="{W-24}" y="114" text-anchor="end" font-family="{SANS}" font-size="10" font-weight="700" fill="#8892a2" letter-spacing="3">TERMINUS · TOUT LE MONDE DESCEND · 🦉 ✕ 🐾</text>
    <text x="24" y="114" font-family="{SANS}" font-size="10" font-weight="700" fill="#8892a2" letter-spacing="3">QUAI 28</text>
  </g>
</svg>
'''


write("station.svg", station())
write("plan.svg", plan())
write("tableau.svg", tableau())
write("quai.svg", quai())
print("ok")
