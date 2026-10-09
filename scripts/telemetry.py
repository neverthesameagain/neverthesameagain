"""Redraws assets/telemetry.svg from live GitHub data. Run daily by .github/workflows/telemetry.yml.

Needs GITHUB_TOKEN (or GH_TOKEN) in the environment. Locally: GH_TOKEN=$(gh auth token) python3 scripts/telemetry.py
"""
import datetime as dt
import json
import os
import urllib.request

from aryanos import (BUILD, DIM, FAINT, INK, INSET, LAB, LINE, LINE_STRONG, RAISED, SIGNAL,
                     frame, measure, svg, t, write)

LOGIN = "neverthesameagain"
# Notebook output and generated HTML swamp the byte counts, so they don't count as languages here.
SKIP_LANGS = {"Jupyter Notebook", "HTML", "CSS"}

QUERY = """
query($login: String!) {
  user(login: $login) {
    followers { totalCount }
    repositories(ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC, first: 100) {
      totalCount
      nodes {
        stargazerCount
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name color } } }
      }
    }
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}"""


def fetch():
    token = os.environ.get("GITHUB_TOKEN") or os.environ["GH_TOKEN"]
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": LOGIN}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as resp:
        data = json.load(resp)
    if "errors" in data:
        raise SystemExit(data["errors"])
    return data["data"]["user"]


def streaks(days):
    longest = run = 0
    for d in days:
        run = run + 1 if d["contributionCount"] else 0
        longest = max(longest, run)
    current = 0
    for i, d in enumerate(reversed(days)):
        if d["contributionCount"]:
            current += 1
        elif i > 0:  # today with nothing yet doesn't break the streak
            break
    return current, longest


def main():
    user = fetch()
    repos = user["repositories"]
    cal = user["contributionsCollection"]["contributionCalendar"]
    days = [d for w in cal["weeks"] for d in w["contributionDays"]]
    weeks = [sum(d["contributionCount"] for d in w["contributionDays"]) for w in cal["weeks"]]
    current, longest = streaks(days)
    stars = sum(r["stargazerCount"] for r in repos["nodes"])
    langs = {}
    for r in repos["nodes"]:
        for e in r["languages"]["edges"]:
            name = e["node"]["name"]
            if name in SKIP_LANGS:
                continue
            langs[name] = langs.get(name, 0) + e["size"]
    total = sum(langs.values()) or 1
    top = sorted(langs.items(), key=lambda kv: -kv[1])[:6]

    W, H = 1000, 330
    back, front = frame(W, H, glow=LAB, glow_at=(0.0, 0.0))
    stamp = dt.datetime.now(dt.timezone(dt.timedelta(hours=5, minutes=30))).strftime("%Y-%m-%d %H:%M IST")
    out = [f'<text x="32" y="44" class="mono" font-size="12.5" fill="{FAINT}" letter-spacing="1.5">$ <tspan fill="{INK}">telemetry --user {LOGIN}</tspan></text>',
           f'<circle cx="{W - 40 - measure("LIVE · " + stamp, "mono", 11.5, 1.2) - 10:.1f}" cy="40" r="4" fill="{LAB}" class="pulse"/>',
           f'<text x="{W - 32}" y="44" text-anchor="end" class="mono" font-size="11.5" fill="{FAINT}" letter-spacing="1.2"><tspan fill="{LAB}">LIVE</tspan> · {stamp}</text>']

    counters = [(f"{cal['totalContributions']:,}", "CONTRIBUTIONS", "last 12 months"),
                (f"{current}d", "CURRENT STREAK", f"longest {longest}d"),
                (str(repos["totalCount"]), "PUBLIC REPOS", f"★ {stars} stars"),
                (str(user["followers"]["totalCount"]), "FOLLOWERS", "say hi ↗")]
    cw = (W - 64 - 3 * 16) / 4
    for i, (big, label, sub) in enumerate(counters):
        x = 32 + i * (cw + 16)
        out.append(f'<rect x="{x:.1f}" y="66" width="{cw:.1f}" height="104" rx="12" fill="{RAISED}" stroke="{LINE_STRONG}"/>'
                   f'<text x="{x + 18:.1f}" y="92" class="mono" font-size="11" fill="{LAB}" letter-spacing="1.8">{label}</text>'
                   f'<text x="{x + 16:.1f}" y="138" class="display" font-size="40" fill="{INK}" letter-spacing="-1.2">{t(big)}</text>'
                   f'<text x="{x + 18:.1f}" y="158" class="mono" font-size="11.5" fill="{FAINT}">{t(sub)}</text>')

    # Weekly contributions as a bar sparkline.
    bx, by, bw, bh = 32, 196, 520, 100
    out.append(f'<text x="{bx}" y="{by + 8}" class="mono" font-size="11" fill="{FAINT}" letter-spacing="1.8">WEEKLY COMMITS · 52W</text>')
    peak = max(weeks) or 1
    gap = 2
    step = bw / len(weeks)
    for i, n in enumerate(weeks):
        h = max(2, (n / peak) * (bh - 24))
        col = SIGNAL if i >= len(weeks) - 4 else (LAB if n else INSET)
        out.append(f'<rect x="{bx + i * step:.1f}" y="{by + bh - h:.1f}" width="{step - gap:.1f}" height="{h:.1f}" rx="1.5" fill="{col}" opacity="{0.95 if n else 1}" class="bar" style="animation-delay:{i * 0.012:.3f}s"/>')
    out.append(f'<line x1="{bx}" y1="{by + bh + 0.5}" x2="{bx + bw}" y2="{by + bh + 0.5}" stroke="{LINE_STRONG}"/>')

    # Languages: one stacked bar plus a legend.
    lx, lw = 590, W - 32 - 590
    out.append(f'<text x="{lx}" y="{by + 8}" class="mono" font-size="11" fill="{FAINT}" letter-spacing="1.8">LANGUAGES · BY BYTES</text>')
    palette = [SIGNAL, LAB, BUILD, "#f3c14b", "#c792ea", INK]
    cx = lx
    for i, (name, size) in enumerate(top):
        w = lw * size / sum(s for _, s in top)
        out.append(f'<rect x="{cx:.1f}" y="{by + 24}" width="{max(w - 2, 1):.1f}" height="10" rx="3" fill="{palette[i]}"/>')
        cx += w
    for i, (name, size) in enumerate(top):
        col_x = lx + (i % 2) * (lw / 2)
        row_y = by + 62 + (i // 2) * 22
        out.append(f'<circle cx="{col_x + 4:.1f}" cy="{row_y - 4}" r="4" fill="{palette[i]}"/>'
                   f'<text x="{col_x + 14:.1f}" y="{row_y}" class="mono" font-size="12.5" fill="{INK}">{t(name)}</text>'
                   f'<text x="{col_x + lw / 2 - 16:.1f}" y="{row_y}" text-anchor="end" class="mono" font-size="12" fill="{DIM}">{100 * size / total:.1f}%</text>')

    style = """.pulse{animation:p 2s ease-in-out infinite;}@keyframes p{50%{opacity:.3}}
.bar{transform-box:fill-box;transform-origin:bottom;animation:grow .7s cubic-bezier(.2,.7,.2,1) both;}
@keyframes grow{from{transform:scaleY(0)}to{transform:scaleY(1)}}"""
    write("telemetry.svg", svg(W, H, back + "".join(out) + front, ["display", "mono"], style, "Live GitHub telemetry"))


if __name__ == "__main__":
    main()
