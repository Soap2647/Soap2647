"""Generates the hand-made SVG assets for the GitHub profile README."""
import pathlib
from xml.sax.saxutils import escape

ROOT = pathlib.Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

FONT = "'Segoe UI', Inter, -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif"
MONO = "'JetBrains Mono', 'Cascadia Code', Consolas, 'SF Mono', Menlo, monospace"

BG = "#0a0f1e"
CARD = "#0f172a"
LINE = "#1e293b"
TEXT = "#e2e8f0"
MUTED = "#94a3b8"


def write(name: str, svg: str) -> None:
    (ASSETS / name).write_text(svg.strip() + "\n", encoding="utf-8")


# ─────────────────────────────── header ────────────────────────────────

def neural_net() -> str:
    """Animated feed-forward network drawn on the right side of the banner."""
    layers = [[120, 200, 280], [80, 140, 200, 260, 320], [80, 140, 200, 260, 320], [160, 240]]
    xs = [800, 900, 1000, 1100]
    colors = ["#22d3ee", "#a78bfa", "#c084fc", "#f472b6"]
    edges = "".join(
        f'<line x1="{xs[l]}" y1="{y1}" x2="{xs[l + 1]}" y2="{y2}" stroke="#334155" stroke-width="1" opacity=".55"/>'
        for l in range(3) for y1 in layers[l] for y2 in layers[l + 1]
    )
    # signals travelling input → output along a few fixed routes
    routes = [(0, 1, 2, 0), (1, 3, 1, 1), (2, 0, 3, 1), (1, 2, 4, 0), (0, 4, 2, 1), (2, 1, 0, 0)]
    signals = ""
    for i, route in enumerate(routes):
        pts = [(xs[l], layers[l][n]) for l, n in enumerate(route)]
        d = "M" + " L".join(f"{x} {y}" for x, y in pts)
        col = colors[i % len(colors)]
        signals += (
            f'<path d="{d}" fill="none" stroke="{col}" stroke-width="2" stroke-linecap="round" '
            f'stroke-dasharray="40 400" stroke-dashoffset="440" opacity=".85">'
            f'<animate attributeName="stroke-dashoffset" values="440;0" dur="3s" begin="{i * 0.5}s" repeatCount="indefinite"/></path>'
            f'<circle r="4" fill="{col}"><animateMotion path="{d}" dur="3s" begin="{i * 0.5}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.1;0.9;1" dur="3s" begin="{i * 0.5}s" repeatCount="indefinite"/></circle>'
        )
    nodes = ""
    for l, (x, col) in enumerate(zip(xs, colors)):
        for j, y in enumerate(layers[l]):
            delay = (l * 0.6 + j * 0.25) % 3
            nodes += (
                f'<circle cx="{x}" cy="{y}" r="16" fill="{col}" opacity=".12"/>'
                f'<circle cx="{x}" cy="{y}" r="10" fill="#0f172a" stroke="{col}" stroke-width="2.5"/>'
                f'<circle cx="{x}" cy="{y}" r="4" fill="{col}">'
                f'<animate attributeName="opacity" values=".25;1;.25" dur="3s" begin="{delay:.2f}s" repeatCount="indefinite"/></circle>'
            )
    labels = "".join(
        f'<text x="{x}" y="368" text-anchor="middle" font-family="{MONO}" font-size="14" fill="{MUTED}">{t}</text>'
        for x, t in zip(xs, ["x", "h₁", "h₂", "ŷ"])
    )
    return f"<g>{edges}{signals}{nodes}{labels}</g>"

def header() -> None:
    w, h = 1200, 400
    network = neural_net()

    # faint dotted grid
    dots = "".join(
        f'<circle cx="{x}" cy="{y}" r="1" fill="#334155" opacity=".55"/>'
        for x in range(30, w, 40)
        for y in range(30, h, 40)
    )
    roles = [
        ("Machine Learning", "#22d3ee"),
        ("Artificial Intelligence", "#a78bfa"),
        ("AI for Healthcare", "#f472b6"),
    ]
    # each role is visible for 3s of a 9s loop, staggered by `begin`
    role_nodes = ""
    for i, (label, color) in enumerate(roles):
        role_nodes += (
            f'<text x="80" y="222" font-family="{MONO}" font-size="24" fill="{color}" opacity="0">'
            f'&gt; {escape(label)}<tspan>'
            f'<animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/>▍</tspan>'
            f'<animate attributeName="opacity" dur="9s" begin="{i * 3}s" repeatCount="indefinite" '
            f'keyTimes="0;0.04;0.3;0.333;1" values="0;1;1;0;0"/></text>'
        )

    svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Mert Yasin Yılmaz — Machine Learning and AI">
  <title>Mert Yasin Yılmaz</title>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#070b16"/>
      <stop offset="1" stop-color="#0d1326"/>
    </linearGradient>
    <radialGradient id="o1"><stop offset="0" stop-color="#22d3ee" stop-opacity=".45"/><stop offset="1" stop-color="#22d3ee" stop-opacity="0"/></radialGradient>
    <radialGradient id="o2"><stop offset="0" stop-color="#a78bfa" stop-opacity=".45"/><stop offset="1" stop-color="#a78bfa" stop-opacity="0"/></radialGradient>
    <radialGradient id="o3"><stop offset="0" stop-color="#f472b6" stop-opacity=".35"/><stop offset="1" stop-color="#f472b6" stop-opacity="0"/></radialGradient>
    <linearGradient id="name" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#e2e8f0"/>
      <stop offset=".55" stop-color="#c4b5fd"/>
      <stop offset="1" stop-color="#67e8f9"/>
    </linearGradient>
    <linearGradient id="ring" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#22d3ee"/>
      <stop offset=".5" stop-color="#a78bfa"/>
      <stop offset="1" stop-color="#f472b6"/>
    </linearGradient>
    <clipPath id="frame"><rect width="{w}" height="{h}" rx="22"/></clipPath>
  </defs>
  <g clip-path="url(#frame)">
    <rect width="{w}" height="{h}" fill="url(#bg)"/>
    {dots}
    <circle cx="180" cy="60" r="260" fill="url(#o1)">
      <animate attributeName="cx" values="180;260;180" dur="14s" repeatCount="indefinite"/>
    </circle>
    <circle cx="1000" cy="380" r="300" fill="url(#o2)">
      <animate attributeName="cy" values="380;320;380" dur="11s" repeatCount="indefinite"/>
    </circle>
    <circle cx="640" cy="-40" r="220" fill="url(#o3)">
      <animate attributeName="cx" values="640;560;640" dur="17s" repeatCount="indefinite"/>
    </circle>

    <text x="78" y="150" font-family="{FONT}" font-size="66" font-weight="800" fill="url(#name)" letter-spacing="-1">Mert Yasin Yılmaz</text>
    {role_nodes}
    <text x="80" y="274" font-family="{FONT}" font-size="19" fill="{MUTED}">Computer Engineering @ Kastamonu University</text>
    <g font-family="{MONO}" font-size="14" fill="{MUTED}">
      <rect x="80" y="298" width="152" height="32" rx="16" fill="#22d3ee" fill-opacity=".1" stroke="#22d3ee" stroke-opacity=".45"/>
      <text x="156" y="319" text-anchor="middle" fill="#67e8f9">📍 Türkiye</text>
    </g>

    {network}
  </g>
  <rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="22" fill="none" stroke="#1e293b"/>
</svg>"""
    write("hero.svg", svg)


# ─────────────────────────────── cards ─────────────────────────────────
def wrap(text: str, max_chars: int) -> list[str]:
    words, lines, cur = text.split(), [], ""
    for wd in words:
        if len(cur) + len(wd) + 1 > max_chars and cur:
            lines.append(cur)
            cur = wd
        else:
            cur = f"{cur} {wd}".strip()
    if cur:
        lines.append(cur)
    return lines


CARDS = [
    dict(
        slug="fisilti", title="Fısıltı", kicker="AI · BIOINFORMATICS · R&D",
        accent=("#22d3ee", "#34d399"),
        desc="Multi-omics, AI-driven discovery of a blood-based biomarker panel for early-stage pancreatic cancer (PDAC I/II).",
        metric="8-protein panel · external tissue AUC 0.87 – 0.95",
        tags=["Python", "PyTorch", "MOFA+", "XGBoost", "SHAP"],
    ),
    dict(
        slug="mertos", title="MertOS", kicker="OPERATING SYSTEM · x86_64",
        accent=("#a78bfa", "#6366f1"),
        desc="A 64-bit hobby OS written from scratch: paging, heap, processes & context switching, VFS and a windowed desktop.",
        metric="Boots on QEMU via GRUB · Multiboot2",
        tags=["C++17", "NASM", "GRUB", "QEMU"],
    ),
    dict(
        slug="doruk", title="DORUK + Mert Studio", kicker="PROGRAMMING LANGUAGE · IDE",
        accent=("#f472b6", "#a78bfa"),
        desc="A programming language with Turkish keywords: lexer, parser, semantic analyzer and interpreter, plus its own Qt IDE.",
        metric='eğer (x > y) { yazdır("merhaba") }',
        tags=["C++17", "Qt 6", "CMake", "Electron"],
    ),
    dict(
        slug="opcode", title="Binary Opcode Analyzer", kicker="REVERSE ENGINEERING · DESKTOP",
        accent=("#fbbf24", "#f97316"),
        desc="Looks inside PE executables and raw binaries: x86 opcode categories, Shannon entropy for packed code, side-by-side diff.",
        metric="CSV / HTML reports · IEEE-style paper",
        tags=["C++17", "Qt Charts", "CMake"],
    ),
    dict(
        slug="talentguard", title="TalentGuard HR", kicker="MACHINE LEARNING · FULL-STACK",
        accent=("#34d399", "#22d3ee"),
        desc="Employee-churn prediction platform with explainable risk factors, role-based access and an audited 3NF database.",
        metric="XGBoost + SHAP · model registry",
        tags=["FastAPI", "React", "PostgreSQL", "XGBoost"],
    ),
    dict(
        slug="noshow", title="Hospital No-Show", kicker="HEALTHCARE · CLEAN ARCHITECTURE",
        accent=("#60a5fa", "#a78bfa"),
        desc="Appointment platform that scores each patient's no-show risk and re-weights it from SMS reminder responses.",
        metric="Admin · Doctor · Patient panels",
        tags=[".NET 10", "Blazor WASM", "EF Core", "JWT"],
    ),
]


def card(c: dict) -> str:
    w, h = 580, 250
    a1, a2 = c["accent"]
    lines = wrap(c["desc"], 62)
    desc = "".join(
        f'<text x="32" y="{112 + i * 24}" font-family="{FONT}" font-size="15.5" fill="{MUTED}">{escape(l)}</text>'
        for i, l in enumerate(lines[:3])
    )
    x, pills = 32, ""
    for t in c["tags"]:
        tw = int(len(t) * 7.6 + 24)
        pills += (
            f'<rect x="{x}" y="200" width="{tw}" height="26" rx="13" fill="{a1}" fill-opacity=".1" stroke="{a1}" stroke-opacity=".35"/>'
            f'<text x="{x + tw / 2}" y="217.5" text-anchor="middle" font-family="{MONO}" font-size="12.5" fill="{a1}">{escape(t)}</text>'
        )
        x += tw + 8
    sid = c["slug"]
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(c['title'])}">
  <title>{escape(c['title'])}</title>
  <defs>
    <linearGradient id="g{sid}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{a1}"/><stop offset="1" stop-color="{a2}"/></linearGradient>
    <radialGradient id="r{sid}" cx="1" cy="0" r="1"><stop offset="0" stop-color="{a1}" stop-opacity=".18"/><stop offset=".6" stop-color="{a1}" stop-opacity="0"/></radialGradient>
    <clipPath id="c{sid}"><rect width="{w}" height="{h}" rx="18"/></clipPath>
  </defs>
  <g clip-path="url(#c{sid})">
    <rect width="{w}" height="{h}" fill="{CARD}"/>
    <rect width="{w}" height="{h}" fill="url(#r{sid})"/>
    <rect width="{w}" height="4" fill="url(#g{sid})"/>
    <text x="32" y="44" font-family="{MONO}" font-size="12" letter-spacing="2" fill="{a1}">{escape(c['kicker'])}</text>
    <text x="32" y="80" font-family="{FONT}" font-size="27" font-weight="700" fill="{TEXT}">{escape(c['title'])}</text>
    <g transform="translate({w - 52} 36)" stroke="{MUTED}" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round" opacity=".8">
      <path d="M4 16 L16 4 M7 4 H16 V13"/>
    </g>
    {desc}
    <text x="32" y="{112 + min(len(lines), 3) * 24 + 8}" font-family="{MONO}" font-size="13" fill="{TEXT}" opacity=".9">▸ {escape(c['metric'])}</text>
    {pills}
  </g>
  <rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="18" fill="none" stroke="{LINE}"/>
</svg>"""


# ─────────────────────────────── awards ────────────────────────────────
AWARDS = [
    ("2025", "Genç AI Ideathon", "1st Place · Team Captain", "Samsun Metropolitan Municipality × Kastamonu Univ. Technopark — incubation award", "#fbbf24"),
    ("2025", "TEKNOFEST Efficiency Challenge", "Software Team Captain", "Electromobile category · TÜBİTAK & T3 Foundation — finalist support", "#f472b6"),
    ("2025", "UDHAM 4th Term R&D Ideas", "Incentive Award · Project Lead", "Ministry of Transport and Infrastructure of Türkiye", "#22d3ee"),
    ("2025", "UDHAM 3rd Term R&D Ideas", "Incentive Award · Team Member", "Ministry of Transport and Infrastructure of Türkiye", "#22d3ee"),
    ("2025–26", "ÜNİDES 5th & 6th Term", "Grant-funded projects · Core Team", "Ministry of Youth and Sports — “Bir Kod İki Şehir”, “Geleceğin Rotası”", "#a78bfa"),
    ("2026", "Fısıltı · AR-GE Project Market", "Principal Investigator", "Kastamonu University R&D Project Market & Showcase Days", "#34d399"),
]


def awards() -> None:
    w, row = 1200, 92
    h = 40 + row * len(AWARDS)
    items = ""
    for i, (year, title, role, org, col) in enumerate(AWARDS):
        y = 30 + i * row
        items += f"""
    <g>
      <circle cx="170" cy="{y + 32}" r="8" fill="{BG}" stroke="{col}" stroke-width="3"/>
      <circle cx="170" cy="{y + 32}" r="16" fill="{col}" opacity=".12"/>
      <text x="140" y="{y + 38}" text-anchor="end" font-family="{MONO}" font-size="15" fill="{col}">{escape(year)}</text>
      <rect x="200" y="{y}" width="960" height="70" rx="14" fill="{CARD}" stroke="{LINE}"/>
      <rect x="200" y="{y}" width="4" height="70" rx="2" fill="{col}"/>
      <text x="226" y="{y + 30}" font-family="{FONT}" font-size="19" font-weight="700" fill="{TEXT}">{escape(title)}</text>
      <text x="1136" y="{y + 30}" text-anchor="end" font-family="{MONO}" font-size="13.5" fill="{col}">{escape(role)}</text>
      <text x="226" y="{y + 54}" font-family="{FONT}" font-size="14.5" fill="{MUTED}">{escape(org)}</text>
    </g>"""
    svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Awards and projects timeline">
  <title>Awards &amp; grant-funded projects</title>
  <defs>
    <linearGradient id="tl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fbbf24"/><stop offset=".5" stop-color="#22d3ee"/><stop offset="1" stop-color="#34d399"/></linearGradient>
  </defs>
  <rect x="168.5" y="40" width="3" height="{h - 80}" rx="1.5" fill="url(#tl)" opacity=".5"/>
  {items}
</svg>"""
    write("awards.svg", svg)


# ───────────────────────────── divider ─────────────────────────────────
def divider() -> None:
    svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="24" viewBox="0 0 1200 24">
  <defs><linearGradient id="d" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#22d3ee" stop-opacity="0"/><stop offset=".25" stop-color="#22d3ee"/>
    <stop offset=".5" stop-color="#a78bfa"/><stop offset=".75" stop-color="#f472b6"/>
    <stop offset="1" stop-color="#f472b6" stop-opacity="0"/></linearGradient></defs>
  <rect x="0" y="11" width="1200" height="2" fill="url(#d)" opacity=".7"/>
  <circle cx="600" cy="12" r="5" fill="#a78bfa"><animate attributeName="cx" values="300;900;300" dur="8s" repeatCount="indefinite"/></circle>
</svg>"""
    write("divider.svg", svg)


if __name__ == "__main__":
    header()
    divider()
    print("ok")
