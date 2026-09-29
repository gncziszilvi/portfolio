#!/usr/bin/env python3
"""Generates every project page. Edit PROJECTS below, then run:  python3 build.py

Images expected in /images:
  <slug>.jpg                    thumbnail (home page + "You may also like")
  <slug>-hero.jpg                big image at the top of the project page
  <slug>-patterns/01.jpg ...     one full-width image per pattern, in order

Each project's "patterns" list gives the number and name shown under each
full-width pattern image, e.g. ("01", "Whispering Sedge").
"""
from html import escape

FONT = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..800&display=swap" rel="stylesheet">')
ARROW = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3" '
         'stroke-linecap="round" stroke-linejoin="round"><path d="M12 20V4M5 11l7-7 7 7"/></svg>')

DEFAULTS = dict(
    statement="ONE-LINE PROJECT STATEMENT GOES HERE",
    lead="Short intro line goes here.",
    description="Project description goes here.",
    bar_color="#4a4a42",   # hero caption-bar background; Adobe Portfolio tints this from the hero image
    patterns=[],           # list of (number_str, name) tuples, e.g. [("01","Whispering Sedge"), ...]
    related=None,          # list of 3 slugs; None = first 3 other projects
)

PROJECTS = [
    dict(slug="garden-memories", title="Garden Memories", year=2026),
    dict(slug="veil-of-fog", title="Veil of Fog", year=2025,
         bar_color="#a3936f",
         statement="THE FOUNDATION OF MY PROJECT IS THE MYSTERIOUS ATMOSPHERE OF THE SWAMP",
         lead="A projektem alapjául az „Ahol a folyami rákok énekelnek” című film szolgált, "
              "amelynek sejtelmes mocsári atmoszféráját fogalmaztam meg.",
         description="During the pattern design process, my aim was to capture the lush flora and mysterious "
                     "atmosphere of the wetlands. I achieved the enigmatic, misty mood seen in the film by playing "
                     "with layering and opacity. The density within the patterns and the intertwining motifs reflect "
                     "the organic growth of nature and the vibrant wildlife of the swamp. The color palette was drawn "
                     "directly from the visual world of the film, dominated by deep greens, earth tones, and "
                     "watery bluish-grays.",
         patterns=[("01","Whispering Sedge"),("02","Mire Veins"),("03","Mud Gems"),("04","Raw Wild"),
                   ("05","Mossy Canopy"),("06","Flock Over Marsh"),("07","Lush Canopy"),("08","Woven Reeds"),
                   ("09","Midnight Flora"),("10","Mayfly Mist"),("11","Blossoming Mire"),("12","Shadow Lotus"),
                   ("13","Velvet Mire"),("14","Beetle Drift"),("15","Golden Roots"),("16","Swamp Thistle")],
         related=["surface-echoes", "golden-east", "street-sounds"]),
    dict(slug="street-sounds", title="Street Sounds", year=2025),
    dict(slug="surface-echoes", title="Surface Echoes", year=2025),
    dict(slug="golden-east", title="Golden East", year=2024),
    dict(slug="poppy-rhythm", title="Poppy Rhythm", year=2024),
    dict(slug="water-line", title="Water Line", year=2024),
]
BY_SLUG = {p["slug"]: p for p in PROJECTS}


def page(p):
    p = {**DEFAULTS, **p}
    t, slug = p["title"], p["slug"]
    up = escape(t.upper())
    first, _, rest = t.upper().partition(" ")
    h1 = escape(first) + ("<br>" + escape(rest) if rest else "")

    blocks = []
    for num, name in p["patterns"]:
        blocks.append(
            f'      <figure class="pattern-block">\n'
            f'        <img src="images/{slug}-patterns/{num}.jpg" alt="{escape(name)}" loading="lazy">\n'
            f'        <figcaption><span class="p-num">({num})</span>'
            f'<span class="p-name">{escape(name)}</span>'
            f'<span class="p-tag">DIGITAL PATTERN</span></figcaption>\n'
            f'      </figure>'
        )
    pattern_html = "\n".join(blocks)

    rel = p["related"] or [q["slug"] for q in PROJECTS if q["slug"] != slug][:3]
    cards = "\n".join(
        f'      <a class="rel-card" href="{r}.html"><img src="images/{r}.jpg" alt="{escape(BY_SLUG[r]["title"])}" loading="lazy">'
        f'<strong>{escape(BY_SLUG[r]["title"].upper())}</strong><span>{BY_SLUG[r]["year"]}</span></a>'
        for r in rel)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(t)} – Szilvi Gönczi</title>
  {FONT}
  <link rel="stylesheet" href="style.css">
</head>
<body class="project-page">
  <header class="p-header">
    <a class="p-nav" href="index.html">Work</a>
    <div class="p-title">{up}</div>
  </header>

  <main>
    <div class="hero">
      <img src="images/{slug}-hero.jpg" alt="{escape(t)}">
      <div class="hero-caption" style="background:{p['bar_color']}"><span>{up}</span><i>|</i><span>{p['year']}</span></div>
    </div>

    <section class="p-intro">
      <div class="statement-row">
        <p class="statement">{escape(p["statement"])}</p>
        <span class="vr"></span>
        <span class="p-year">{p["year"]}</span>
      </div>
      <h1 class="p-h1">{h1}</h1>
      <hr class="short-rule">
      <p class="p-lead">{escape(p["lead"])}</p>
      <p class="p-desc">{escape(p["description"])}</p>
    </section>

    <section class="collection">
      <div class="section-label"><span>PATTERN COLLECTION</span><i></i><b></b></div>
      <div class="tiles">
{"".join(f'''        <img src="images/{slug}-patterns/{num}.jpg" alt="{escape(name)}" loading="lazy">
''' for num, name in p["patterns"])}      </div>
    </section>

    <section class="showcase">
      <div class="showcase-caption"><strong>{up}</strong><span>| PATTERN COLLECTION</span></div>
{pattern_html}
    </section>

    <section class="related">
      <h2>You may also like</h2>
      <div class="rel-grid">
{cards}
      </div>
    </section>
  </main>

  <footer class="site-footer">© Szilvi Gönczi</footer>
  <a class="to-top" href="#" aria-label="Back to top">{ARROW}</a>
</body>
</html>
'''

for proj in PROJECTS:
    open(f'{proj["slug"]}.html', "w", encoding="utf-8").write(page(proj))
print("Built", len(PROJECTS), "project pages")
