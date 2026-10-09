"""Builds every static ARYAN.OS asset in assets/. Edit the data here and run `python3 scripts/build.py`.

The live stats card is not built here - scripts/telemetry.py does that, on a schedule (.github/workflows).
"""
from aryanos import (BG, BUILD, DIM, FAINT, INK, INSET, LAB, LINE, LINE_STRONG, RAISED, SIGNAL,
                     L_BUILD, L_DIM, L_INK, L_LAB, L_LINE, L_SIGNAL,
                     chip, chips, frame, measure, svg, t, write)

W = 1000


def wrap(text, face, size, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if cur and measure(trial, face, size) > max_w:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    return lines + ([cur] if cur else [])


def text_block(x, y, lines, face, size, fill, lh, extra=""):
    spans = "".join(f'<tspan x="{x}" dy="{0 if i == 0 else lh}">{t(l)}</tspan>' for i, l in enumerate(lines))
    return f'<text x="{x}" y="{y}" class="{face}" font-size="{size}" fill="{fill}" {extra}>{spans}</text>'


def flow(x, y, steps, color, size=13, active_cls="node"):
    """Architecture chips joined by arrows, each lighting up in turn."""
    out, cx = [], x
    for i, step in enumerate(steps):
        w = measure(step, "mono", size) + 24
        out.append(f'<g class="{active_cls}" style="animation-delay:{i * 0.6:.1f}s">'
                   f'<rect x="{cx:.1f}" y="{y}" width="{w:.1f}" height="30" rx="8" fill="{INSET}" stroke="{LINE_STRONG}"/>'
                   f'<rect x="{cx:.1f}" y="{y}" width="{w:.1f}" height="30" rx="8" fill="none" stroke="{color}" class="lit" style="animation-delay:{i * 0.6:.1f}s"/>'
                   f'<text x="{cx + 12:.1f}" y="{y + 19.5}" class="mono" font-size="{size}" fill="{INK}">{t(step)}</text></g>')
        cx += w
        if i < len(steps) - 1:
            out.append(f'<path d="M{cx + 6:.1f} {y + 15}h14m-5 -4l5 4l-5 4" fill="none" stroke="{FAINT}" stroke-width="1.4"/>')
            cx += 26
    return "".join(out), cx


LIT_STYLE = """
.lit{opacity:0;animation:lit %(cycle)ss ease-in-out infinite;}
@keyframes lit{0%%{opacity:0}6%%{opacity:1}22%%{opacity:0}100%%{opacity:0}}
"""


# ── hero ──────────────────────────────────────────────────────────────────────

def hero():
    H = 540
    back, front = frame(W, H, glow=SIGNAL, glow_at=(0.05, 1.05))
    boot = [
        ("ARYAN.OS — build 2026.10 · kernel: identity.sys", None),
        ("mounting /experience ................", "OK"),
        ("mounting /research ...................", "OK"),
        ("mounting /leadership .................", "OK"),
        ("mounting /projects ...................", "OK"),
        ("resolving identity: Aryan Mathur", None),
        ("role: engineer · operator · researcher · builder", None),
        ("boot complete.", None),
    ]
    log = []
    for i, (line, ok) in enumerate(boot):
        y = 84 + i * 22
        last = i == len(boot) - 1
        tail = f'<tspan fill="{LAB}"> {ok}</tspan>' if ok else ""
        log.append(f'<g class="boot" style="animation-delay:{0.25 + i * 0.22:.2f}s">'
                   f'<text x="32" y="{y}" class="mono" font-size="14"><tspan fill="{SIGNAL}">›</tspan>'
                   f'<tspan dx="8" fill="{INK if last else DIM}">{t(line)}</tspan>{tail}</text></g>')
    cursor_x = 32 + measure("›", "mono", 14) + 8 + measure("boot complete.", "mono", 14) + 6
    log.append(f'<rect x="{cursor_x:.1f}" y="{84 + 7 * 22 - 12}" width="8" height="15" fill="{SIGNAL}" class="cursor"/>')

    name_w = measure("Aryan Mathur", "display", 92, -2.5)
    identity = f"""<g class="rise">
<text x="32" y="300" class="mono" font-size="13" fill="{SIGNAL}" letter-spacing="2">› WHOAMI</text>
<text x="28" y="384" class="display" font-size="92" fill="{INK}" letter-spacing="-2.5">Aryan Mathur</text>
<circle cx="{28 + name_w + 14:.1f}" cy="374" r="9" fill="{SIGNAL}" class="pulse-dot"/>
<text x="32" y="428" class="body" font-size="22" fill="{DIM}">I build systems, run programs, and ship under ambiguity.</text>
<text x="32" y="466" class="mono" font-size="13.5" fill="{FAINT}"><tspan fill="{INK}">AI Native Software Engineer</tspan> @ Accenture  ·  prev. Mercor  ·  IIT Palakkad</text>
</g>"""

    # The electron from the old bio, still exploring infinity.
    cx, cy = 845, 160
    orbits = "".join(
        f'<ellipse cx="{cx}" cy="{cy}" rx="104" ry="34" fill="none" stroke="{LINE_STRONG}" transform="rotate({a} {cx} {cy})"/>'
        for a in (0, 60, 120))
    path = f"M{cx - 104} {cy} a104 34 0 1 0 208 0 a104 34 0 1 0 -208 0"
    atom = f"""<g class="fade-in">
{orbits}
<circle cx="{cx}" cy="{cy}" r="5" fill="{INK}"/>
<circle cx="{cx}" cy="{cy}" r="14" fill="none" stroke="{INK}" stroke-opacity="0.25"/>
<g transform="rotate(60 {cx} {cy})"><circle r="5.5" fill="{SIGNAL}"><animateMotion dur="3.2s" repeatCount="indefinite" path="{path}"/></circle>
<circle r="11" fill="{SIGNAL}" opacity="0.25"><animateMotion dur="3.2s" repeatCount="indefinite" path="{path}"/></circle></g>
<g transform="rotate(120 {cx} {cy})"><circle r="3.5" fill="{LAB}"><animateMotion dur="4.6s" repeatCount="indefinite" path="{path}"/></circle></g>
<g><circle r="3.5" fill="{BUILD}"><animateMotion dur="5.8s" repeatCount="indefinite" path="{path}" begin="-2s"/></circle></g>
<text x="{cx}" y="{cy + 92}" text-anchor="middle" class="mono" font-size="11.5" fill="{FAINT}" letter-spacing="1.5">AN EXCITED ELECTRON, EXPLORING ∞</text>
</g>"""

    stats = [("3", "PUBLICATIONS", "arXiv · CV, RL, XAI"),
             ("0.9%", "TOP · AMAZON ML", "251 / 27.6k teams"),
             ("2×", "HACKATHON FINALS", "Meta · Paytm, 2026")]
    stat_svg = [f'<line x1="724" y1="300" x2="724" y2="470" stroke="{LINE_STRONG}"/>']
    for i, (big, label, sub) in enumerate(stats):
        y = 318 + i * 60
        stat_svg.append(f'<g class="rise" style="animation-delay:{2.7 + i * 0.15:.2f}s">'
                        f'<text x="748" y="{y + 16}" class="display" font-size="30" fill="{INK}" letter-spacing="-0.5">{t(big)}</text>'
                        f'<text x="{748 + measure(big, "display", 30, -0.5) + 12:.1f}" y="{y + 1}" class="mono" font-size="11" fill="{SIGNAL}" letter-spacing="1.5">{t(label)}</text>'
                        f'<text x="{748 + measure(big, "display", 30, -0.5) + 12:.1f}" y="{y + 16}" class="mono" font-size="11.5" fill="{FAINT}">{t(sub)}</text></g>')

    chrome = f"""<text x="32" y="28" class="mono" font-size="11.5" fill="{FAINT}" letter-spacing="2.5">SYSTEM BOOT</text>
<circle cx="{W - 32 - measure('running · ARYAN.OS v2026.10', 'mono', 11.5, 1.5) - 14:.1f}" cy="24" r="4" fill="{SIGNAL}" class="pulse-dot"/>
<text x="{W - 32}" y="28" text-anchor="end" class="mono" font-size="11.5" fill="{FAINT}" letter-spacing="1.5"><tspan fill="{INK}">running</tspan> · ARYAN.OS v2026.10</text>
<line x1="0" y1="44" x2="{W}" y2="44" stroke="{LINE}"/>
<line x1="0" y1="{H - 44}" x2="{W}" y2="{H - 44}" stroke="{LINE}"/>
<g><rect x="32" y="{H - 33}" width="{measure('scroll to explore the system ↓', 'mono', 11.5, 1.2) + 28:.1f}" height="22" rx="11" fill="none" stroke="{LINE_STRONG}"/>
<text x="46" y="{H - 18}" class="mono" font-size="11.5" fill="{DIM}" letter-spacing="1.2">scroll to explore the system ↓</text></g>
<text x="{W - 32}" y="{H - 18}" text-anchor="end" class="mono" font-size="11.5" fill="{FAINT}" letter-spacing="1.5">GURGAON, IN · IIT PALAKKAD '26</text>"""

    style = """
.boot{opacity:0;animation:boot .35s ease-out forwards;}
@keyframes boot{from{opacity:0;transform:translateX(-6px)}to{opacity:1;transform:none}}
.rise{opacity:0;animation:rise .9s cubic-bezier(.2,.7,.2,1) 2.3s forwards;}
@keyframes rise{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
.fade-in{opacity:0;animation:fade 1.4s ease 1s forwards;}
@keyframes fade{to{opacity:1}}
.cursor{animation:blink 1.1s steps(2,start) infinite;}
@keyframes blink{to{visibility:hidden}}
.pulse-dot{animation:pd 2.4s ease-in-out infinite;transform-box:fill-box;transform-origin:center;}
@keyframes pd{0%,100%{opacity:1}50%{opacity:.35}}
"""
    body = back + chrome + "".join(log) + identity + atom + "".join(stat_svg) + front
    write("hero.svg", svg(W, H, body, ["display", "mono", "body"], style, "ARYAN.OS — Aryan Mathur"))


# ── section headers (dark + light, transparent background) ────────────────────

SECTIONS = [
    ("work", "01 / WORK", "Experience", "Paid engineering work, in order. Production systems, not coursework.", "signal"),
    ("build", "02 / BUILD", "Featured work", "What I build when nobody is paying me to.", "build"),
    ("lab", "03 / LAB", "Lab notes", "Three publications across vision, reinforcement learning and explainable AI. Real metrics, no rounding up.", "lab"),
    ("missions", "04 / MISSIONS", "Hackathon war room", "What actually got built, not just the leaderboard result.", "signal"),
    ("command", "05 / PM-CORE", "Command center", "Programs and teams I didn't get to hand-pick, with real budgets on the line.", "signal"),
    ("stack", "06 / STACK", "Skills", "The tools that show up in the work above.", "build"),
    ("telemetry", "07 / TELEMETRY", "Live signals", "Regenerated every day by a GitHub Action in this repo.", "lab"),
    ("contact", "08 / CONNECT", "Let's talk", "Hiring for backend, AI product engineering or technical program management?", "signal"),
]


def section(key, kicker, title, sub, accent, theme):
    H = 132
    dark = theme == "dark"
    ink, dim, line = (INK, DIM, LINE_STRONG) if dark else (L_INK, L_DIM, L_LINE)
    color = {"signal": SIGNAL if dark else L_SIGNAL, "lab": LAB if dark else L_LAB,
             "build": BUILD if dark else L_BUILD}[accent]
    tw = measure(title, "title", 44, -1)
    dot_x = 4 + tw + 6
    rule_x = dot_x + 34
    body = f"""<text x="4" y="30" class="mono" font-size="13" fill="{color}" letter-spacing="2.5">{t(kicker)}</text>
<text x="2" y="84" class="title" font-size="44" fill="{ink}" letter-spacing="-1">{t(title)}</text>
<circle cx="{dot_x + 4:.1f}" cy="78" r="5.5" fill="{SIGNAL if dark else L_SIGNAL}"/>
<line x1="{rule_x:.1f}" y1="70" x2="{W - 4}" y2="70" stroke="{line}"/>
<rect x="{rule_x:.1f}" y="69" width="80" height="2" fill="{color}" class="sweep"/>
<text x="4" y="116" class="body" font-size="17" fill="{dim}">{t(sub)}</text>"""
    span = W - 4 - rule_x - 80
    style = f""".sweep{{animation:sweep 4.5s cubic-bezier(.6,0,.3,1) infinite;}}
@keyframes sweep{{0%{{transform:translateX(0);opacity:0}}10%{{opacity:1}}80%{{opacity:1}}100%{{transform:translateX({span:.0f}px);opacity:0}}}}"""
    write(f"sections/{key}-{theme}.svg", svg(W, H, body, ["title", "mono", "body"], style, title))


# ── experience timeline ───────────────────────────────────────────────────────

def experience():
    H = 330
    back, front = frame(W, H, glow=SIGNAL, glow_at=(0.0, 0.0))
    jobs = [
        ("NOW · JUL 2026 —", "AI Native Software Engineer", "Accenture · Gurgaon",
         "Backend services and data pipelines that automate enterprise workflows.", True),
        ("JAN — JUL 2026", "Software Engineering Expert", "Mercor · SF, remote",
         "Features and fixes across large production Go and Python codebases.", False),
        ("MAY — JUL 2025", "Advanced Application Engineering Intern", "Accenture · Mumbai",
         "Cloud-native services and AWS pipelines on SageMaker, S3, EC2 and Lambda.", False),
        ("MAY — AUG 2024", "AI/ML Intern", "EasyAlgo · New Delhi",
         "Time-series models and NLP sentiment over financial news and market data.", False),
    ]
    axis_y = 92
    col = (W - 64) / 4
    out = [f'<text x="32" y="44" class="mono" font-size="12.5" fill="{FAINT}" letter-spacing="1.5">$ <tspan fill="{INK}">git log --career --reverse=false</tspan></text>',
           f'<line x1="32" y1="{axis_y}" x2="{W - 32}" y2="{axis_y}" stroke="{LINE_STRONG}"/>',
           f'<rect x="32" y="{axis_y - 1}" width="60" height="2" fill="{SIGNAL}" class="packet"/>']
    for i, (when, role, org, what, now) in enumerate(jobs):
        x = 32 + i * col
        color = SIGNAL if now else INK
        if now:
            out.append(f'<circle cx="{x + 7}" cy="{axis_y}" r="7" fill="{SIGNAL}" class="ring"/>')
        out.append(f'<circle cx="{x + 7}" cy="{axis_y}" r="6" fill="{BG}" stroke="{color}" stroke-width="2"/>')
        if now:
            out.append(f'<circle cx="{x + 7}" cy="{axis_y}" r="2.5" fill="{SIGNAL}"/>')
        out.append(f'<text x="{x}" y="{axis_y + 40}" class="mono" font-size="12" fill="{SIGNAL if now else FAINT}" letter-spacing="1.5">{t(when)}</text>')
        rl = wrap(role, "title", 20, col - 24)
        out.append(text_block(x, axis_y + 72, rl, "title", 20, INK, 24, 'letter-spacing="-0.3"'))
        oy = axis_y + 72 + (len(rl) - 1) * 24 + 26
        out.append(f'<text x="{x}" y="{oy}" class="mono" font-size="12.5" fill="{DIM}">{t(org)}</text>')
        out.append(text_block(x, oy + 30, wrap(what, "body", 14.5, col - 28), "body", 14.5, FAINT, 21))
    span = W - 64 - 60
    style = f""".packet{{animation:pk 6s linear infinite;}}
@keyframes pk{{from{{transform:translateX({span}px)}}to{{transform:translateX(0)}}}}
.ring{{transform-box:fill-box;transform-origin:center;animation:ring 2.2s ease-out infinite;}}
@keyframes ring{{from{{transform:scale(1);opacity:.6}}to{{transform:scale(3.2);opacity:0}}}}"""
    write("experience.svg", svg(W, H, back + "".join(out) + front, ["title", "mono", "body"], style, "Experience"))


# ── Jozzo ─────────────────────────────────────────────────────────────────────

def jozzo():
    H = 400
    back, front = frame(W, H, glow=BUILD, glow_at=(1.0, 0.0))
    left = [f'<text x="40" y="58" class="mono" font-size="12.5" fill="{BUILD}" letter-spacing="2.5">FLAGSHIP · AFTER HOURS · LIVE</text>',
            f'<text x="36" y="134" class="display" font-size="72" fill="{INK}" letter-spacing="-2">Jozzo</text>',
            f'<circle cx="{36 + measure("Jozzo", "display", 72, -2) + 10:.1f}" cy="124" r="8" fill="{SIGNAL}"/>']
    tag = ("Shared group state for friends and flatmates: habits, shopping lists, split bills and "
           "running tabs with the milkman, all driven by one escalating nudge engine.")
    left.append(text_block(40, 176, wrap(tag, "body", 17, 420), "body", 17, DIM, 25))
    c, _ = chips(40, 268, ["web · Next.js PWA", "android · Compose", "ios · SwiftUI"], size=12.5, h=28, pad=11, color=INK)
    left.append(c)
    left.append(f'<text x="40" y="330" class="mono" font-size="12.5" fill="{FAINT}">Next.js 15 · Drizzle · Neon Postgres · Inngest · Kotlin · Swift</text>')
    left.append(f'<text x="40" y="362" class="mono-med" font-size="14" fill="{SIGNAL}">jozzo.in ↗</text>')

    # Diagram: four pillars feed one nudges table, which climbs one escalation ladder.
    px, pw, ph = 528, 112, 38
    pillars = [("Habits", LAB), ("Lists", BUILD), ("Money", SIGNAL), ("Tally", INK)]
    hub_x, hub_y, hub_w, hub_h = 696, 172, 112, 56
    d = [f'<text x="{px}" y="58" class="mono" font-size="11.5" fill="{FAINT}" letter-spacing="1.5">ONE ENGINE, EVERY OBJECT</text>']
    for i, (label, col) in enumerate(pillars):
        y = 82 + i * 62
        d.append(f'<rect x="{px}" y="{y}" width="{pw}" height="{ph}" rx="10" fill="{INSET}" stroke="{LINE_STRONG}"/>'
                 f'<circle cx="{px + 16}" cy="{y + ph / 2}" r="4" fill="{col}"/>'
                 f'<text x="{px + 30}" y="{y + 24}" class="mono" font-size="13" fill="{INK}">{label}</text>')
        sx, sy = px + pw, y + ph / 2
        ex, ey = hub_x, hub_y + hub_h / 2
        p = f"M{sx} {sy} C{sx + 34} {sy} {ex - 34} {ey} {ex} {ey}"
        d.append(f'<path d="{p}" fill="none" stroke="{LINE_STRONG}"/>'
                 f'<circle r="3" fill="{col}"><animateMotion dur="2.4s" begin="{i * 0.6}s" repeatCount="indefinite" path="{p}"/></circle>')
    d.append(f'<rect x="{hub_x}" y="{hub_y}" width="{hub_w}" height="{hub_h}" rx="12" fill="{RAISED}" stroke="{SIGNAL}"/>'
             f'<text x="{hub_x + hub_w / 2}" y="{hub_y + 25}" text-anchor="middle" class="mono-med" font-size="13" fill="{INK}">nudges</text>'
             f'<text x="{hub_x + hub_w / 2}" y="{hub_y + 42}" text-anchor="middle" class="mono" font-size="10.5" fill="{FAINT}">one table</text>')
    rungs = [("day 0", "created"), ("day 1", "gentle ping"), ("day 3", "space sees it"), ("day 6", "louder, every 3d")]
    lx = 836
    d.append(f'<path d="M{hub_x + hub_w} {hub_y + hub_h / 2} H{lx - 6}" stroke="{LINE_STRONG}"/>')
    for i, (day, what) in enumerate(rungs):
        y = 300 - i * 62
        heat = [INK, LAB, BUILD, SIGNAL][i]
        d.append(f'<g><rect x="{lx}" y="{y}" width="132" height="44" rx="10" fill="{INSET}" stroke="{LINE_STRONG}"/>'
                 f'<rect x="{lx}" y="{y}" width="132" height="44" rx="10" fill="none" stroke="{heat}" class="lit" style="animation-delay:{i * 0.7:.1f}s"/>'
                 f'<text x="{lx + 14}" y="{y + 19}" class="mono-med" font-size="12" fill="{heat}">{day}</text>'
                 f'<text x="{lx + 14}" y="{y + 35}" class="mono" font-size="11" fill="{DIM}">{what}</text></g>')
    d.append(f'<path d="M{lx - 6} 344 V{300 - 3 * 62 + 22}" stroke="{LINE_STRONG}" stroke-dasharray="3 4"/>')
    d.append(f'<text x="{lx + 66}" y="368" text-anchor="middle" class="mono" font-size="10.5" fill="{FAINT}" letter-spacing="1.2">ESCALATION LADDER</text>')
    style = LIT_STYLE % {"cycle": 2.8}
    write("jozzo.svg", svg(W, H, back + "".join(left) + "".join(d) + front, ["display", "mono", "mono-med", "body"], style, "Jozzo"))


# ── build cards ───────────────────────────────────────────────────────────────

PROJECTS = [
    ("isitevenhuman", "isitevenHuman",
     "A stylometric AI-text detector. Paste anything and see, sentence by sentence, whether a person or a model wrote it.",
     "114 stylometric features · per-sentence verdicts", ["Python", "FastAPI", "XGBoost", "spaCy"]),
    ("eie", "EIE",
     "Economic Intelligence Engine: a live multi-agent economy where plain-language events reshape the world and agents adapt.",
     "Meta OpenEnv finalist · 7 adaptive agents", ["Python", "multi-agent RL", "Groq", "Gradio"]),
    ("modest", "modest",
     "Content moderation as an environment: toxicity spreads through threads, users carry trust, and bans cost real reward.",
     "OpenEnv-compatible RL env for LLM agents", ["Python", "FastAPI", "Docker", "HF Spaces"]),
    ("spectrumharmony", "SpectrumHarmony",
     "A digital twin of enterprise Wi-Fi across a multi-floor building, for testing self-optimising radio resource control.",
     "RL-driven RRM · interference-aware sim", ["Python", "simulation", "RL", "networking"]),
    ("recurlens", "RecurLens",
     "A multimodal assistant that thinks before it answers: it critiques and refines its own understanding before acting.",
     "input → understand → self-critique → act", ["TypeScript", "Gemini", "multimodal"]),
    ("ackermann", "Ackermann Explorer",
     "A fully autonomous exploration stack for a car-like robot: maps the unknown, picks frontiers, plans and tracks paths.",
     "frontier exploration · A* · pure pursuit", ["Python", "robotics", "path planning"]),
]


def build_card(i, key, title, desc, metric, tags):
    CW, H = 490, 290
    back, front = frame(CW, H, r=16, glow=BUILD, glow_at=(1.0, 0.0))
    idx = f"{i + 1:02d}"
    body = [f'<text x="{CW - 22}" y="{H - 22}" text-anchor="end" class="display" font-size="120" fill="{INK}" opacity="0.045" letter-spacing="-4">{idx}</text>',
            f'<text x="26" y="38" class="mono" font-size="12" fill="{FAINT}" letter-spacing="1"><tspan fill="{BUILD}">~/build/</tspan>{t(key)}</text>',
            f'<text x="{CW - 26}" y="38" text-anchor="end" class="mono" font-size="14" fill="{DIM}">↗</text>',
            f'<line x1="0" y1="56" x2="{CW}" y2="56" stroke="{LINE}"/>',
            f'<text x="24" y="102" class="title" font-size="28" fill="{INK}" letter-spacing="-0.6">{t(title)}</text>']
    body.append(text_block(26, 136, wrap(desc, "body", 15, CW - 56), "body", 15, DIM, 22))
    body.append(f'<text x="26" y="222" class="mono" font-size="12.5" fill="{BUILD}"><tspan fill="{SIGNAL}">›</tspan> {t(metric)}</text>')
    c, _ = chips(26, 240, tags, size=11.5, h=26, pad=10, color=DIM, max_x=CW - 26)
    body.append(c)
    write(f"build/{key}.svg", svg(CW, H, back + "".join(body) + front, ["display", "title", "mono", "body"], "", title))


# ── research ──────────────────────────────────────────────────────────────────

PAPERS = [
    ("violence", "COMPUTER VISION · SEQUENCE MODELING",
     "Violence Detection in Visual Media for Movie Highlight Generation",
     ["frames", "CNN encoder", "BiLSTM", "attention pool", "highlights"],
     [("93.5%", "ACCURACY")], "arXiv:2406.05152"),
    ("pdit", "REINFORCEMENT LEARNING · TRANSFORMERS",
     "Adapting Interleaved Encoders with PPO for Language-Guided RL in BabyAI",
     ["grid + mission", "PDiT encoder", "PPO actor-critic", "BabyAI"],
     [("−42%", "REWARD VARIANCE"), ("+20%", "CONVERGENCE SPEED")], "arXiv:2510.23148"),
    ("xai", "EXPLAINABLE AI · VISION-LANGUAGE · EDGE",
     "Explainable Detection of AI-Generated Images with Artifact Localization",
     ["image", "Faster-Than-Lies CNN", "artifact map", "Qwen2-VL-7B"],
     [("96.5%", "ACCURACY"), ("175ms", "ON A CPU")], "arXiv:2510.23775"),
]


def paper(i, key, kicker, title, steps, metrics, ref):
    H = 236
    back, front = frame(W, H, glow=LAB, glow_at=(1.0, 1.0))
    body = [f'<text x="36" y="46" class="mono" font-size="12" fill="{LAB}" letter-spacing="2">PAPER {i + 1:02d} · {t(kicker)}</text>']
    tl = wrap(title, "title", 25, 610)
    body.append(text_block(34, 88, tl, "title", 25, INK, 31, 'letter-spacing="-0.5"'))
    fy = 88 + (len(tl) - 1) * 31 + 34
    f, _ = flow(36, fy, steps, LAB, size=12.5)
    body.append(f)
    body.append(f'<text x="36" y="{H - 26}" class="mono" font-size="12.5" fill="{FAINT}">{t(ref)} <tspan fill="{LAB}">↗</tspan></text>')
    body.append(f'<line x1="700" y1="30" x2="700" y2="{H - 30}" stroke="{LINE_STRONG}"/>')
    n = len(metrics)
    for j, (big, label) in enumerate(metrics):
        y = (H / 2 + 18) if n == 1 else (98 + j * 82)
        body.append(f'<text x="730" y="{y}" class="display" font-size="{56 if n == 1 else 46}" fill="{LAB}" letter-spacing="-1.5">{t(big)}</text>'
                    f'<text x="732" y="{y + 24}" class="mono" font-size="11.5" fill="{FAINT}" letter-spacing="1.8">{t(label)}</text>')
    style = LIT_STYLE % {"cycle": len(steps) * 0.6 + 1.6}
    write(f"lab/{key}.svg", svg(W, H, back + "".join(body) + front, ["display", "title", "mono", "body"], style, title))


# ── missions ──────────────────────────────────────────────────────────────────

MISSIONS = [
    ("2026", "Meta OpenEnv Hackathon", "FINALIST", "EIE · 7 adaptive agents in a live economy"),
    ("2026", "Paytm GeekRoom Grand Prix", "FINALIST", "CrowdShield · −67% dangerous-density time"),
    ("2025", "Amazon ML Challenge", "TOP 0.9%", "LossLess · 251 of 27,600+ teams, text-only"),
    ("2025", "Flipkart GRiD 7.0", "NATIONAL SEMI-FINALIST", "pure DSA at every elimination round"),
    ("2024", "Adobe AI Challenge · Inter IIT", "9TH OF ALL IITs", "explainable AI-image detection"),
]


def missions():
    rh = 62
    H = 70 + rh * len(MISSIONS) + 22
    back, front = frame(W, H, glow=SIGNAL, glow_at=(1.0, 1.0))
    cols = [(36, "YEAR"), (110, "MISSION"), (430, "RESULT"), (640, "WHAT GOT BUILT")]
    body = [f'<text x="{x}" y="48" class="mono" font-size="11" fill="{FAINT}" letter-spacing="2">{h}</text>' for x, h in cols]
    body.append(f'<line x1="24" y1="66" x2="{W - 24}" y2="66" stroke="{LINE_STRONG}"/>')
    for i, (year, event, result, built) in enumerate(MISSIONS):
        y = 66 + i * rh
        body.append(f'<g class="row" style="animation-delay:{i * 0.12:.2f}s">'
                    f'<rect x="24" y="{y + 8}" width="3" height="{rh - 16}" rx="1.5" fill="{SIGNAL}" opacity="{1 - i * 0.16:.2f}"/>'
                    f'<text x="36" y="{y + 38}" class="mono" font-size="13" fill="{DIM}">{year}</text>'
                    f'<text x="110" y="{y + 39}" class="title" font-size="19" fill="{INK}" letter-spacing="-0.2">{t(event)}</text>')
        w = measure(result, "mono-med", 11.5, 1) + 22
        body.append(f'<rect x="430" y="{y + 19}" width="{w:.1f}" height="26" rx="13" fill="rgba(255,90,54,0.12)" stroke="rgba(255,90,54,0.45)"/>'
                    f'<text x="441" y="{y + 36}" class="mono-med" font-size="11.5" fill="{SIGNAL}" letter-spacing="1">{t(result)}</text>'
                    f'<text x="640" y="{y + 37}" class="body" font-size="14.5" fill="{DIM}">{t(built)}</text></g>')
        if i < len(MISSIONS) - 1:
            body.append(f'<line x1="36" y1="{y + rh}" x2="{W - 36}" y2="{y + rh}" stroke="{LINE}"/>')
    style = """.row{opacity:0;animation:row .5s ease-out forwards;}
@keyframes row{from{opacity:0;transform:translateX(-8px)}to{opacity:1;transform:none}}"""
    write("missions.svg", svg(W, H, back + "".join(body) + front, ["title", "mono", "mono-med", "body"], style, "Hackathon war room"))


# ── command center ────────────────────────────────────────────────────────────

PROGRAMS = [
    ("200", "team", "₹26L budget · 11 mo", "Assistant Fest Coordinator", "Petrichor '24 · IIT Palakkad"),
    ("93", "contingent", "₹8L spend · 7 mo", "Contingent Leader", "Inter IIT Tech Meet 13.0"),
    ("01", "founder", "2024 — 2025", "Founder & President", "E-Cell · IIT Palakkad"),
    ("12", "months", "2025 — 2026", "Placement Coordinator", "Career Development Centre"),
]


def command():
    H = 274
    back, front = frame(W, H, glow=SIGNAL, glow_at=(0.0, 1.0))
    body = [f'<text x="32" y="44" class="mono" font-size="12.5" fill="{FAINT}" letter-spacing="1.5">$ <tspan fill="{INK}">status --all-programs</tspan></text>',
            f'<text x="{W - 32}" y="44" text-anchor="end" class="mono" font-size="12" fill="{SIGNAL}" letter-spacing="1.5">● 4 PROGRAMS SHIPPED</text>']
    tw = (W - 64 - 3 * 16) / 4
    for i, (big, unit, meta, role, org) in enumerate(PROGRAMS):
        x = 32 + i * (tw + 16)
        body.append(f'<rect x="{x:.1f}" y="66" width="{tw:.1f}" height="178" rx="12" fill="{RAISED}" stroke="{LINE_STRONG}"/>')
        big_face = "display"
        body.append(f'<text x="{x + 18:.1f}" y="124" class="{big_face}" font-size="46" fill="{INK}" letter-spacing="-1.5">{t(big)}</text>'
                    f'<text x="{x + 22 + measure(big, "display", 46, -1.5):.1f}" y="124" class="mono" font-size="12" fill="{SIGNAL}">{unit}</text>'
                    f'<text x="{x + 18:.1f}" y="150" class="mono" font-size="11.5" fill="{FAINT}">{t(meta)}</text>'
                    f'<line x1="{x + 18:.1f}" y1="166" x2="{x + tw - 18:.1f}" y2="166" stroke="{LINE}"/>')
        body.append(text_block(round(x + 18, 1), 192, wrap(role, "title", 16, tw - 36), "title", 16, INK, 20))
        body.append(f'<text x="{x + 18:.1f}" y="{216 if len(wrap(role, "title", 16, tw - 36)) == 1 else 234}" class="mono" font-size="11" fill="{DIM}">{t(org)}</text>')
    write("command.svg", svg(W, H, back + "".join(body) + front, ["display", "title", "mono", "mono-med"], "", "Command center"))


# ── stack ─────────────────────────────────────────────────────────────────────

STACK = [
    ("LANGUAGES", ["Python", "TypeScript", "Go", "SQL", "Java", "Scala", "C++", "Kotlin", "Swift", "MATLAB"]),
    ("AI / GENAI", ["PyTorch", "TensorFlow", "LLMs", "RAG", "Transformers", "Vision-Language", "Reinforcement Learning", "Computer Vision", "NLP"]),
    ("DATA / BACKEND", ["PostgreSQL", "MongoDB", "Spark", "Hadoop", "FastAPI", "Node.js", "Next.js", "React", "REST APIs"]),
    ("CLOUD / DEVOPS", ["AWS", "SageMaker", "Azure DevOps", "Docker", "Kubernetes", "CI/CD", "Vercel", "Linux", "Git"]),
    ("HARDWARE", ["ESP32", "Arduino", "Embedded C", "IoT sensors", "MATLAB Robotics"]),
]
CORE = {"Python", "TypeScript", "Go", "PyTorch", "LLMs", "RAG", "Reinforcement Learning", "PostgreSQL", "FastAPI", "Next.js", "AWS", "Docker"}


def stack():
    out, y = [], 40
    for label, items in STACK:
        out.append(f'<text x="32" y="{y + 19}" class="mono" font-size="11.5" fill="{FAINT}" letter-spacing="2">{label}</text>')
        x = 190
        rows_y = y
        for item in items:
            core = item in CORE
            w = measure(item, "mono", 12.5) + 22 + (14 if core else 0)
            if x + w > W - 32:
                x, rows_y = 190, rows_y + 38
            out.append(f'<rect x="{x:.1f}" y="{rows_y}" width="{w:.1f}" height="28" rx="14" fill="{INSET}" stroke="{SIGNAL if core else LINE_STRONG}" stroke-opacity="{0.6 if core else 1}"/>')
            tx = x + 11
            if core:
                out.append(f'<circle cx="{x + 14:.1f}" cy="{rows_y + 14}" r="3" fill="{SIGNAL}"/>')
                tx += 14
            out.append(f'<text x="{tx:.1f}" y="{rows_y + 18.5}" class="mono" font-size="12.5" fill="{INK if core else DIM}">{t(item)}</text>')
            x += w + 8
        y = rows_y + 38 + 18
        out.append(f'<line x1="32" y1="{y - 10}" x2="{W - 32}" y2="{y - 10}" stroke="{LINE}"/>')
    out.pop()
    H = y + 30
    out.append(f'<circle cx="36" cy="{H - 26}" r="3" fill="{SIGNAL}"/><text x="46" y="{H - 22}" class="mono" font-size="11" fill="{FAINT}">daily drivers</text>')
    back, front = frame(W, H, glow=BUILD, glow_at=(1.0, 0.0))
    write("stack.svg", svg(W, H, back + "".join(out) + front, ["mono"], "", "Skills"))


# ── contact buttons + footer ──────────────────────────────────────────────────

BUTTONS = [
    ("email", "aryannmathur@gmail.com", "✉", SIGNAL),
    ("linkedin", "linkedin", "↗", INK),
    ("portfolio", "ARYAN.OS portfolio", "↗", INK),
    ("scholar", "google scholar", "↗", INK),
]


def buttons():
    for key, label, glyph, accent in BUTTONS:
        size = 14
        w = measure(label, "mono", size) + 64
        H = 46
        primary = key == "email"
        body = (f'<rect x="1" y="1" width="{w - 2:.1f}" height="{H - 2}" rx="{H / 2 - 1}" fill="{SIGNAL if primary else BG}" stroke="{SIGNAL if primary else LINE_STRONG}"/>'
                f'<text x="22" y="{H / 2 + 5}" class="mono" font-size="{size}" fill="{BG if primary else INK}">{t(label)}</text>'
                f'<text x="{w - 22:.1f}" y="{H / 2 + 5}" text-anchor="end" class="mono" font-size="{size}" fill="{BG if primary else accent}">{glyph}</text>')
        write(f"buttons/{key}.svg", svg(round(w), H, body, ["mono"], "", label))


def footer():
    H = 150
    back, front = frame(W, H, glow=SIGNAL, glow_at=(0.5, 1.4))
    msg = "ARYAN.OS — phase 1 build. more modules compiling."
    cx = 32 + measure(msg, "mono", 14) + 6
    body = f"""<text x="32" y="56" class="mono" font-size="14" fill="{DIM}"><tspan fill="{SIGNAL}">›</tspan> {t(msg)}</text>
<rect x="{cx + 8:.1f}" y="44" width="8" height="15" fill="{SIGNAL}" class="cursor"/>
<rect x="32" y="82" width="{W - 64}" height="4" rx="2" fill="{INSET}"/>
<rect x="32" y="82" width="{W - 64}" height="4" rx="2" fill="{SIGNAL}" class="bar"/>
<text x="32" y="122" class="mono" font-size="11.5" fill="{FAINT}" letter-spacing="1.5">NEVER THE SAME AGAIN</text>
<text x="{W - 32}" y="122" text-anchor="end" class="mono" font-size="11.5" fill="{FAINT}" letter-spacing="1.5">© 2026 ARYAN MATHUR</text>"""
    style = """.cursor{animation:blink 1.1s steps(2,start) infinite;}
@keyframes blink{to{visibility:hidden}}
.bar{transform-box:fill-box;transform-origin:left;animation:bar 5s cubic-bezier(.7,0,.2,1) infinite;}
@keyframes bar{0%{transform:scaleX(0)}70%{transform:scaleX(.93)}85%{transform:scaleX(.93);opacity:1}100%{transform:scaleX(1);opacity:0}}"""
    write("footer.svg", svg(W, H, back + body + front, ["mono"], style, "ARYAN.OS"))


if __name__ == "__main__":
    hero()
    for s in SECTIONS:
        for theme in ("dark", "light"):
            section(*s, theme)
    experience()
    jozzo()
    for i, p in enumerate(PROJECTS):
        build_card(i, *p)
    for i, p in enumerate(PAPERS):
        paper(i, *p)
    missions()
    command()
    stack()
    buttons()
    footer()
