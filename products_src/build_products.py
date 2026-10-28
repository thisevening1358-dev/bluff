"""Build 웹_2안/BLUFF_2안_Products.html from template_products.html.

Inlines the BLUFF logo paths and the shared footer (../shared/footer.html), renders the five soda cans,
and copies img/*.webp next to the built file (the painting thumbnails already live in ../assets).
Run:  python -E build_products.py
"""
import re
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent

# Soda facts are printed on the cans: 355 ml, 0 kcal, 0 mg sodium.
CANS = ['Cherry Hot Tonic', 'Acid Lime Fizz', 'Blue Cheese Cola', 'Red Sansho Tonic', 'Counterfeit Lime']


def can_html(i, name):
    return f'''    <article class="can" data-light tabindex="0" aria-label="BLUFF SODA {name}, 0 kcal, 나트륨 0 mg" style="left: calc(var(--u) * {120 + i * 345})">
      <div class="spot"></div><div class="floor"></div>
      <img class="pic" src="{{{{IMG can{i + 1}}}}}" alt="" width="322" height="724" loading="lazy"><div class="lightc"></div>
      <h3>{name}</h3><p class="meta">LOT {i + 4:02d}   355 ML</p>
      <p class="ink"><b>0 kcal   0 mg</b><i>SODIUM</i></p>
    </article>'''


svg = (HERE.parent / 'source' / 'logo.svg').read_text(encoding='utf-8')
paths = [re.sub(r'\s(fill|id)="[^"]*"', '', p) for p in re.findall(r'<path\b[^>]*/>', svg, flags=re.S)]

html = (HERE / 'template_products.html').read_text(encoding='utf-8')
html = html.replace('{{LOGO_PATHS}}', ''.join(paths))
html = html.replace('{{FOOTER}}', (HERE.parent / 'shared' / 'footer.html').read_text(encoding='utf-8'))
html = html.replace('{{CANS}}', '\n'.join(can_html(i, n) for i, n in enumerate(CANS)))
html = re.sub(r'\{\{IMG (\w+)\}\}', lambda m: 'assets/%s.%s' % (m.group(1), 'jpg' if m.group(1) in ('mona', 'van', 'david') else 'webp'), html)

(OUT / 'assets').mkdir(exist_ok=True)
for f in (HERE / 'img').glob('*.webp'):
    if f.stem.startswith('seal'):        # the 虛勢 seal is retired
        continue
    shutil.copyfile(f, OUT / 'assets' / f.name)
(OUT / 'BLUFF_2안_Products.html').write_text(html, encoding='utf-8')
print('built', OUT / 'BLUFF_2안_Products.html')
