"""Build 웹_2안/BLUFF_2안_Brand.html from template.html.

Inlines the BLUFF logo paths (fill attributes stripped so <use fill> can recolour them)
inlines the shared footer (../shared/footer.html) and points the paintings at ./assets/*.jpg next to the built file.
Run:  python -E build.py
"""
import re
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent

svg = (HERE / 'logo.svg').read_text(encoding='utf-8')
paths = re.findall(r'<path\b[^>]*/>', svg, flags=re.S)
paths = [re.sub(r'\s(fill|id)="[^"]*"', '', p) for p in paths]

html = (HERE / 'template.html').read_text(encoding='utf-8')
html = html.replace('{{LOGO_PATHS}}', ''.join(paths))
html = html.replace('{{FOOTER}}', (HERE.parent / 'shared' / 'footer.html').read_text(encoding='utf-8'))
for key, name in [('MONA', 'mona'), ('VAN', 'van'), ('DAVID', 'david')]:
    html = html.replace('{{IMG_%s}}' % key, 'assets/%s.jpg' % name)

(OUT / 'assets').mkdir(exist_ok=True)
for name in ('mona', 'van', 'david'):
    shutil.copyfile(HERE / ('%s.jpg' % name), OUT / 'assets' / ('%s.jpg' % name))
(OUT / 'BLUFF_2안_Brand.html').write_text(html, encoding='utf-8')
print('built', OUT / 'BLUFF_2안_Brand.html', len(paths), 'logo paths')
