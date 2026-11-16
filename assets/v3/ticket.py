"""Genere assets/v3/ticket.svg : le profil sous forme de ticket de caisse thermique."""
import random
import sys
from xml.sax.saxutils import escape

sys.path.insert(0, sys.argv[2])
from qr import encode  # noqa: E402

OUT = sys.argv[1]
CONTRIB = sys.argv[3]

W = 520
PX, PW = 46, 428          # papier
L, R = PX + 22, PX + PW - 22
CX = W // 2
INK = "#1f1d1a"
SOFT = "#6d675d"

body = []
y = 150


def t(txt, x=None, size=13, anchor="start", weight=400, fill=INK, cls="m", extra=""):
    x = L if x is None else x
    body.append(f'<text x="{x}" y="{y}" class="{cls}" font-size="{size}" text-anchor="{anchor}" '
                f'font-weight="{weight}" fill="{fill}" {extra}>{escape(txt)}</text>')


def row(left, right, size=13, weight=400, fill=INK):
    t(left, size=size, weight=weight, fill=fill)
    t(right, x=R, size=size, anchor="end", weight=weight, fill=fill)


def sep(ch="-"):
    global y
    body.append(f'<line x1="{L}" y1="{y}" x2="{R}" y2="{y}" stroke="{INK}" stroke-width="1.2" '
                f'stroke-dasharray="{"5 4" if ch == "-" else "none"}"/>')
    if ch == "=":
        body.append(f'<line x1="{L}" y1="{y+4}" x2="{R}" y2="{y+4}" stroke="{INK}" stroke-width="1.2"/>')


def gap(n):
    global y
    y += n


# --- en-tete -----------------------------------------------------------------
owl = f'''<g transform="translate({CX} {y+18})" fill="{INK}">
  <path d="M-22 -14 L-15 -30 L-8 -18 Z M22 -14 L15 -30 L8 -18 Z"/>
  <ellipse cx="0" cy="0" rx="24" ry="26"/>
  <circle cx="-9" cy="-6" r="8" fill="#fbf8f1"/><circle cx="9" cy="-6" r="8" fill="#fbf8f1"/>
  <circle cx="-8" cy="-5" r="3.6"/><circle cx="10" cy="-5" r="3.6"/>
  <path d="M-3 3 L0 9 L3 3 Z" fill="#fbf8f1"/>
</g>'''
body.append(owl)
gap(80)
t("J O C H A", x=CX, size=34, anchor="middle", weight=800, cls="d")
gap(24)
t("ATELIER LOGICIEL · COTONOU · BÉNIN", x=CX, size=12, anchor="middle", fill=SOFT)
gap(18)
t("github.com/jocha28", x=CX, size=12, anchor="middle", fill=SOFT)
gap(22); sep("="); gap(30)

row("TICKET N° 028-2026", "16/11/26  03:28")
gap(20); row("CAISSIER", "José HOUNNAHO")
gap(20); row("CLIENT", "toi, visiteur 👀")
gap(18); sep(); gap(26)

t("QTÉ  ARTICLE", size=12, weight=700)
t("PRIX", x=R, size=12, anchor="end", weight=700)
gap(10); sep(); gap(24)

items = [
    ("1", "Module Odoo sur mesure", "12 cafés"),
    ("1", "Intégration Mobile Money", "8 cafés"),
    ("1", "Facture normalisée MECEF", "15 cafés"),
    ("1", "Driver Go, boîtier fiscal", "6 cafés"),
    ("1", "Biométrie faciale, urgences", "21 cafés"),
    ("1", "Chatbot français ⇄ fongbè", "9 cafés"),
    ("7", "Nuits blanches", "OFFERT"),
    ("1", "Face B rap / trap tech 🎧", "OFFERT"),
]
items_top = y
for q, name, price in items:
    t(q, size=13)
    t(name, x=L + 38, size=13)
    t(price, x=R, size=13, anchor="end", weight=700 if price == "OFFERT" else 400)
    gap(24)
gap(-8); sep(); gap(26)

row("SOUS-TOTAL", "71 cafés")
gap(20); row("TVA (passion)", "100 % incluse")
gap(16); sep("="); gap(40)
row("TOTAL", f"{CONTRIB} commits", size=24, weight=800)
gap(20)
t("contributions GitHub sur 12 mois", x=R, size=11, anchor="end", fill=SOFT)
gap(18); sep("="); gap(30)

t("MOYENS DE PAIEMENT ACCEPTÉS", x=CX, size=12, anchor="middle", weight=700)
gap(22)
for line in ["Python · Go · TypeScript · JavaScript · PHP",
             "Odoo · FastAPI · Django · PostgreSQL · Docker",
             "PyTorch · TensorFlow · React · Three.js · Linux"]:
    t(line, x=CX, size=12, anchor="middle")
    gap(19)
gap(4); sep(); gap(26)

row("STATUT", "en ligne, surtout la nuit")
gap(20); row("LANGUES", "français · fɔngbè · anglais")
gap(20); row("BASE", "Cotonou, Bénin 🇧🇯")
gap(18); sep(); gap(30)

# --- code-barres ---------------------------------------------------------------
rnd = random.Random(28)
bx = L + 24
bars = []
while bx < R - 24:
    w = rnd.choice([1.5, 1.5, 3, 4.5])
    bars.append(f'<rect x="{bx:.1f}" y="{y}" width="{w}" height="54" fill="{INK}"/>')
    bx += w + rnd.choice([1.5, 3, 3])
body.extend(bars)
gap(72)
t("J O C H A  2 8  0 0 1 6  6 9 4 0", x=CX, size=12, anchor="middle", fill=SOFT)
gap(30)

# --- QR code -------------------------------------------------------------------
M = encode("https://github.com/jocha28")
n = len(M)
cell = 4.4
qs = n * cell
qx, qy = CX - qs / 2, y
d = []
for r in range(n):
    for c in range(n):
        if M[r][c]:
            d.append(f"M{qx + c*cell:.1f} {qy + r*cell:.1f}h{cell}v{cell}h-{cell}z")
body.append(f'<rect x="{qx-4*cell:.1f}" y="{qy-4*cell:.1f}" width="{qs+8*cell:.1f}" height="{qs+8*cell:.1f}" fill="#fbf8f1"/>')
body.append(f'<path d="{"".join(d)}" fill="{INK}" shape-rendering="crispEdges"/>')
stamp_y = int(qy + qs / 2)
stamp_x = int((qx + qs + R) / 2) - 4
y = int(qy + qs + 30)
t("SCANNE-MOI, JE NE MORDS PAS", x=CX, size=12, anchor="middle", weight=700)
gap(24); sep(); gap(30)

t("MERCI DE VOTRE VISITE", x=CX, size=16, anchor="middle", weight=800, cls="d")
gap(22)
t("à bientôt dans les commits", x=CX, size=12, anchor="middle", fill=SOFT)
gap(28)
t("🦉 ✕ 🐾", x=CX, size=18, anchor="middle")
gap(22)
t("ticket non fiscal · imprimé avec amour", x=CX, size=10, anchor="middle", fill=SOFT)
gap(26)

PAPER_BOTTOM = y
H = PAPER_BOTTOM + 40

# bord dechire
zig = [f"M{PX} 96"]
zig.append(f"L{PX+PW} 96 L{PX+PW} {PAPER_BOTTOM}")
step = PW / 30
for i in range(30):
    xa = PX + PW - (i + 0.5) * step
    xb = PX + PW - (i + 1) * step
    zig.append(f"L{xa:.1f} {PAPER_BOTTOM + 9} L{xb:.1f} {PAPER_BOTTOM}")
zig.append("Z")
paper_path = " ".join(zig)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Ticket de caisse JOCHA : compétences, total {CONTRIB} contributions, QR code vers github.com/jocha28">
  <style>
    .m {{ font-family: 'JetBrains Mono','Fira Code','SFMono-Regular',Consolas,'Liberation Mono','Courier New',monospace; }}
    .d {{ font-family: 'JetBrains Mono','Courier New',monospace; letter-spacing: 1px; }}
    .stamp {{ transform-box: fill-box; transform-origin: center; opacity: 0;
              animation: slam .35s cubic-bezier(.2,1.6,.4,1) 6.4s forwards; }}
    .busy {{ animation: blink .25s steps(1) 0s 25; }}
    .ready {{ opacity: 0; animation: on .01s 6.3s forwards; }}
    @keyframes slam {{ 0% {{ opacity: 0; transform: rotate(-14deg) scale(2.4); }} 100% {{ opacity: .85; transform: rotate(-14deg) scale(1); }} }}
    @keyframes blink {{ 50% {{ opacity: 0; }} }}
    @keyframes on {{ to {{ opacity: 1; }} }}
  </style>
  <defs>
    <clipPath id="roll">
      <rect x="0" y="96" width="{W}" height="0">
        <animate attributeName="height" from="0" to="{H}" dur="6s" begin="0.4s" fill="freeze" calcMode="spline" keySplines=".4 0 .6 1"/>
      </rect>
    </clipPath>
    <filter id="sh" x="-10%" y="-2%" width="120%" height="104%">
      <feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="#000" flood-opacity=".25"/>
    </filter>
    <linearGradient id="curl" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#000" stop-opacity=".18"/><stop offset="1" stop-color="#000" stop-opacity="0"/>
    </linearGradient>
  </defs>

  <!-- papier -->
  <g clip-path="url(#roll)">
    <path d="{paper_path}" fill="#fbf8f1" filter="url(#sh)"/>
    <rect x="{PX}" y="96" width="{PW}" height="26" fill="url(#curl)"/>
    {"".join(body)}
    <g class="stamp">
      <rect x="{stamp_x-62}" y="{stamp_y-26}" width="124" height="52" rx="8" fill="none" stroke="#d7263d" stroke-width="3.5"/>
      <text x="{stamp_x}" y="{stamp_y+4}" text-anchor="middle" class="d" font-size="21" font-weight="900" fill="#d7263d" letter-spacing="3">VALIDÉ</text>
      <text x="{stamp_x}" y="{stamp_y+18}" text-anchor="middle" class="m" font-size="7.5" fill="#d7263d" letter-spacing="2">PAR LE HIBOU</text>
    </g>
  </g>

  <!-- imprimante -->
  <g>
    <rect x="16" y="8" width="{W-32}" height="96" rx="22" fill="#1b2130"/>
    <rect x="16" y="8" width="{W-32}" height="48" rx="22" fill="#232b3d"/>
    <rect x="16" y="40" width="{W-32}" height="16" fill="#232b3d"/>
    <text x="44" y="42" class="m" font-size="12" font-weight="700" fill="#9aa6bb" letter-spacing="4">JOCHA·PRINT</text>
    <text x="44" y="60" class="m" font-size="9" fill="#5d6a82" letter-spacing="2">MODÈLE CC-28 · THERMIQUE</text>
    <circle class="busy" cx="{W-56}" cy="38" r="6" fill="#ffb020"/>
    <circle class="ready" cx="{W-56}" cy="38" r="6" fill="#3ddc84"/>
    <circle class="ready" cx="{W-56}" cy="38" r="11" fill="#3ddc84" fill-opacity=".2"/>
    <rect x="{W-110}" y="31" width="30" height="14" rx="7" fill="#11151f"/>
    <rect x="{PX-10}" y="84" width="{PW+20}" height="12" rx="6" fill="#0a0d14"/>
    <rect x="{PX-4}" y="90" width="{PW+8}" height="3" rx="1.5" fill="#000"/>
    <rect x="{CX-90}" y="64" width="180" height="4" rx="2" fill="#2c3549"/>
  </g>
</svg>
'''
open(OUT, "w").write(svg)
print("hauteur", H)
