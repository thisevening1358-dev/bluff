"""Build 웹_2안/BLUFF_2안_Products.html from template_products.html.

Inlines the BLUFF logo paths, renders the chip lots and soda cans from the data below,
and copies img/*.webp (+ the painting thumbnails already in ../assets) next to the built file.
Run:  python -E build_products.py
"""
import re
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent

# Product facts come from the brand deck: QUAZIC CHIPS 60 g, 0 kcal, 0 mg sodium, capsaicin 0 %, 2,900 won.
CHIPS = [
    dict(no='01', name='Mona Bluff', kind='QUAZIC CHIPS, Herb', img='bag_mona',
         attrib='허브 향이 진하게 밴 스낵', actual='실제: 향만 진함. 열량과 나트륨은 0',
         prov_img='mona', prov='Leonardo da Vinci, 모나리자', prov_sub='1503-1519, BLUFF 덧칠본',
         notes=[('n-big', '0 kcal', 14, 20, -5), ('n-s', 'herb, by scent only', 30, 58, 3), ('n-m', 'NA 0 MG', 52, 78, -2),
                ('ring', '', 60, 26, 0)]),
    dict(no='02', name='Van Bluff', kind='QUAZIC CHIPS, Blue Cheese', img='bag_van',
         attrib='꼬릿하고 짭짤한 블루치즈 맛', actual='실제: 짠맛 없음. 나트륨 0 mg',
         prov_img='van', prov='Vincent van Gogh, 자화상', prov_sub='1886-1889 연작, BLUFF 덧칠본',
         notes=[('n-big', '0 mg', 56, 22, 4), ('n-s', 'no salt was found', 12, 52, -3), ('n-m', 'SODIUM 0 MG', 46, 76, 2),
                ('ring', '', 16, 18, 0)]),
    dict(no='03', name='David Bluff', kind='QUAZIC CHIPS, Original Hot', img='bag_david',
         attrib='혀가 얼얼하게 매운맛', actual='실제: 얼얼함 없음. 캡사이신 0%',
         prov_img='david', prov='Michelangelo, 다비드', prov_sub='1501-1504, BLUFF 덧칠본',
         notes=[('n-big', '0%', 18, 24, -6), ('n-s', 'hot in name only', 40, 50, 2), ('n-m', 'CAPSAICIN 0%', 20, 78, -3),
                ('ring', '', 58, 60, 0)]),
]
# Soda facts are printed on the cans: 355 ml, 0 kcal, 0 mg sodium.
CANS = ['Cherry Hot Tonic', 'Acid Lime Fizz', 'Blue Cheese Cola', 'Red Sansho Tonic', 'Counterfeit Lime']


def lot_html(c):
    notes = ''.join(
        f'<span class="ring" style="left:{x}%;top:{y}%"></span>' if cls == 'ring' else
        f'<span class="{cls}" style="left:{x}%;top:{y}%;--r:{r}deg">{t}</span>'
        for cls, t, x, y, r in c['notes'])
    return f'''  <section class="lot" data-watch data-lot aria-labelledby="lot{c['no']}">
    <div class="entry">
      <h2 id="lot{c['no']}" class="rise clip">{c['name']}</h2>
      <p class="kind ital rise d1">{c['kind']}</p>
      <dl class="kr rise d2">
        <div><dt>Lot</dt><dd>{c['no']}</dd></div>
        <div><dt>추정</dt><dd class="attrib"><span>{c['attrib']}</span>
          <span class="uv ink" aria-hidden="true"><s>{c['attrib']}</s><b>{c['actual']}</b></span>
          <span class="sr">{c['actual']}</span></dd></div>
        <div><dt>출처</dt><dd class="prov"><img src="{{{{IMG {c['prov_img']}}}}}" alt="" width="52" height="72" loading="lazy">
          <span>{c['prov']}<span class="sub">{c['prov_sub']}</span></span></dd></div>
        <div><dt>낙찰가</dt><dd class="price">₩2,900</dd></div>
      </dl>
    </div>
    <div class="object rise d1" data-certify-zone>
      <div class="pool"></div><div class="floor"></div>
      <img class="pic" src="{{{{IMG {c['img']}}}}}" alt="{c['kind']} 봉지" width="764" height="1036" loading="lazy">
      <div class="uv notes ink" aria-hidden="true">{notes}</div>
      <img class="seal" src="{{{{IMG seal_lime}}}}" alt="">
    </div>
    <div class="report rise d2">
      <h3 class="ital">Condition report<span class="kr">감정서, QUAZIC CHIPS 60 g</span></h3>
      <ol class="kr">
        <li><span class="k">열량</span><span class="v">0<small>kcal</small></span></li>
        <li><span class="k">나트륨</span><span class="v">0<small>mg</small></span></li>
        <li><span class="k">캡사이신</span><span class="v">0<small>%</small></span></li>
      </ol>
      <div class="verdict kr" aria-live="polite">
        <p class="wait">램프를 봉지 위에 잠시 비추면 감정이 끝납니다.</p>
        <p class="done">감정 결과: 내용물 없음.<br>허세만 확인됨.</p>
      </div>
    </div>
  </section>
'''


def can_html(i, name):
    return f'''      <article class="can rise d{min(3, i % 4)}">
        <div class="object" data-certify-zone>
          <div class="pool"></div><div class="floor"></div>
          <img class="pic" src="{{{{IMG can{i + 1}}}}}" alt="BLUFF SODA {name} 캔" width="322" height="724" loading="lazy">
          <div class="uv label ink" aria-hidden="true"><div><strong>0</strong><em>KCAL</em><strong>0</strong><em>MG SODIUM</em></div></div>
        </div>
        <div><h3>{name}</h3><p>Lot {i + 4:02d}<br>355 ml</p></div>
      </article>'''


svg = (HERE.parent / 'source' / 'logo.svg').read_text(encoding='utf-8')
paths = [re.sub(r'\s(fill|id)="[^"]*"', '', p) for p in re.findall(r'<path\b[^>]*/>', svg, flags=re.S)]

html = (HERE / 'template_products.html').read_text(encoding='utf-8')
html = html.replace('{{LOGO_PATHS}}', ''.join(paths))
html = html.replace('{{LOTS}}', ''.join(lot_html(c) for c in CHIPS))
html = html.replace('{{CANS}}', '\n'.join(can_html(i, n) for i, n in enumerate(CANS)))
html = re.sub(r'\{\{IMG (\w+)\}\}', lambda m: 'assets/%s.%s' % (m.group(1), 'jpg' if m.group(1) in ('mona', 'van', 'david') else 'webp'), html)

(OUT / 'assets').mkdir(exist_ok=True)
for f in (HERE / 'img').glob('*.webp'):
    shutil.copyfile(f, OUT / 'assets' / f.name)
(OUT / 'BLUFF_2안_Products.html').write_text(html, encoding='utf-8')
print('built', OUT / 'BLUFF_2안_Products.html')
