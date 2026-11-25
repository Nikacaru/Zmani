"""Build the revised ZMANI investor deck (HTML + PDF) from the founder's original design.

Slides without corrections reuse the original slide renders in deck/assets/.
Corrected slides are rebuilt in HTML in the same style (Arial Bold headlines,
Inter body, #FF4D2D orange, #C8301A labels).

  python3 deck/build_deck.py          # writes deck/ZMANI_Investor_Deck_1.5M_revised.html
  node deck/export_pdf.js             # writes deck/ZMANI_Investor_Deck_1.5M_revised.pdf
"""
import base64
import math
import pathlib

HERE = pathlib.Path(__file__).parent
OUT = HERE / "ZMANI_Investor_Deck_1.5M_revised.html"


def img(name):
    data = base64.b64encode((HERE / "assets" / name).read_bytes()).decode()
    return "data:image/jpeg;base64," + data


def raster(name, overlay=""):
    return f'<section class="slide raster" style="background-image:url({img(name)})">{overlay}</section>'


def slide(label, title, body, foot="", cls=""):
    lab = f'<div class="label">{label}</div>' if label else ""
    tit = f'<h1>{title}</h1>' if title else ""
    ft = f'<div class="foot">{foot}</div>' if foot else ""
    return f'<section class="slide {cls}"><div class="pad">{lab}{tit}{body}</div>{ft}</section>'


def pie(parts):
    """parts: [(value, color, label_html, label_xy)]; returns SVG."""
    total = sum(p[0] for p in parts)
    cx, cy, r = 220, 220, 210
    a = -math.pi / 2
    out = []
    for v, col, _, _ in parts:
        b = a + 2 * math.pi * v / total
        x1, y1 = cx + r * math.cos(a), cy + r * math.sin(a)
        x2, y2 = cx + r * math.cos(b), cy + r * math.sin(b)
        large = 1 if b - a > math.pi else 0
        out.append(f'<path d="M{cx},{cy} L{x1:.1f},{y1:.1f} A{r},{r} 0 {large} 1 {x2:.1f},{y2:.1f} Z" '
                   f'fill="{col}" stroke="#fff" stroke-width="4"/>')
        a = b
    return f'<svg viewBox="0 0 440 440" width="440" height="440">{"".join(out)}</svg>'


S = []

# 1 · Title (unchanged)
S.append(raster("p01.jpg"))

# 2 · Problem
S.append(slide("The problem",
    "Men don’t know how to shop, but they know who they want to dress like.<br>We want to dress like Tony Soprano, Eddie Horniman and Tommy Shelby.",
    """<div class="cards three">
      <div class="card"><div class="big">31%</div><p>of men find buying clothes or putting an outfit together stressful</p><div class="src">Outfittery &amp; GfK consumer survey</div></div>
      <div class="card"><div class="big">5</div><p>items in one look: five searches, five matches, five checkouts</p><div class="src">Example look on zmani.ai, 7 November 2026</div></div>
      <div class="card"><div class="big">39%</div><p>of Georgia’s e-commerce is bought from foreign sites; clothing is a top category</p><div class="src">Galt &amp; Taggart, 2024 data</div></div>
    </div>
    <div class="punch">Shops sell single items. Men want the finished outfit.</div>""", cls="t2"))

# 3 · Solution (unchanged)
S.append(raster("p03.jpg"))

# 4 · Transform (original + honest caption)
S.append(raster("p04.jpg", '<div class="cap">Concept images, AI-generated: they show the idea, not product output.</div>'))

# 5 · Confidence (two slides merged, grammar fixed)
S.append("""<section class="slide orange center"><div>
  <div class="mega dark">We don’t sell clothes.</div>
  <div class="mega cream">We sell confidence:</div>
  <div class="sub dark">we help men show the best version of themselves.</div>
</div></section>""")

# 6 · Where we are today
S.append(slide("Where we are today", "The product is live. Growth starts with this round.",
    """<div class="stats">
      <div class="stat hot"><div class="big">11</div><p>characters on zmani.ai</p></div>
      <div class="stat"><div class="big">24</div><p>complete looks, each with its items and prices</p></div>
      <div class="stat"><div class="big">~20 sec</div><p>AI try-on on your own photo, as the site states</p></div>
      <div class="stat"><div class="big">2</div><p>languages: Georgian and English</p></div>
      <div class="stat"><div class="big">4</div><p>people today: CEO, CTO, growth, operations</p></div>
      <div class="stat"><div class="big">128K</div><p>subscribers on the founder’s YouTube channel</p></div>
    </div>
    <div class="bar dark">LC Waikiki is in talks; nothing is signed.</div>""",
    "Site facts: zmani.ai, 16 November 2026. YouTube: vidIQ, 4 November 2026. The YouTube audience is a distribution channel, not ZMANI users. No user or sales results are claimed in this deck."))

# 7 · Market
S.append(slide("Market", "A growing home market, a big next one",
    """<div class="mkt">
      <div class="chart">
        <div class="cols">
          <div class="col"><div class="v">GEL 3.5bn</div><div class="b grey" style="height:98px"></div></div>
          <div class="col"><div class="v">GEL 10.7bn</div><div class="b hot" style="height:300px"></div></div>
        </div>
        <div class="axis"><span>2024</span><span>2030 forecast</span></div>
        <div class="cap2">Georgia e-commerce, +20.5% a year</div>
      </div>
      <div class="side">
        <div class="card"><div class="big">~$300M</div><p>men’s clothing spend in Georgia a year: 1.88M men × ~$160 each</p><div class="src">Estimate from Geostat 2024 census and 2025 household spending</div></div>
        <div class="card"><div class="big">€4.8bn</div><p>men’s apparel in Turkey, 2024: the biggest planned next market</p><div class="src">Statista Market Insights</div></div>
      </div>
    </div>""",
    "Sources: Galt &amp; Taggart e-commerce study (2025); Statista Market Insights; Geostat 2024 census and 2025 household spending (via Georgia Today). ~$160 a man a year is our estimate, at GEL 2.62 = $1."))

# 8 · Business model
S.append(slide("Business model", "Users first, then we sell the looks",
    """<div class="phases">
      <div class="ph light"><div class="pill">Phase 1 · 2027 · users</div>
        <div class="duo"><div><div class="big">Free</div><p>looks + item links</p></div><div><div class="big">GEL 0.5</div><p>per AI try-on photo</p></div></div>
        <p class="txt">To win users, we publish the looks with free links to every item. A man finds the look he wants, tries it on, and buys the items he’s missing through each store’s own link.</p></div>
      <div class="arrow">➜</div>
      <div class="ph darkc"><div class="pill hotp">Phase 2 · from late 2027 · pilot sales</div>
        <div class="duo"><div><div class="big">~30%</div><p>target gross margin per look</p></div><div><div class="big">~70%</div><p>of retail to suppliers</p></div></div>
        <p class="txt">If Georgia proves demand, we start selling looks ourselves as a limited pilot, then integrate suppliers in 2028. A women’s line is planned for 2028.</p></div>
    </div>""",
    "Price, margin and timing are plan assumptions. The ~30% is gross margin, before delivery, returns, payment fees and support. No supplier has agreed to 70/30. LC Waikiki is in talks; nothing is signed."))

# 9 · Go to market
S.append(slide("Go to market", "Prove it in Georgia, then expand",
    """<div class="tl">
      <div class="line"></div>
      <div class="node"><div class="yr">2027</div><div class="dot hot"></div><b>Georgia</b><span>Prove demand and the try-on economics</span></div>
      <div class="node"><div class="yr">Late 2027</div><div class="dot"></div><b>Armenia, Azerbaijan<br>Turkey from Q4</b><span>Once Georgia’s numbers work</span></div>
      <div class="node"><div class="yr">2028</div><div class="dot"></div><b>Suppliers</b><span>Integrations · women’s line</span></div>
      <div class="node"><div class="yr">2029–30</div><div class="dot"></div><b>United States</b><span>With a seed round · men’s apparel $116bn</span></div>
    </div>""",
    "Founder’s planned sequence, not committed launch dates: each step starts when the previous market’s numbers work. A look is digital: a new market needs local looks and links."))

# 10 · Growth engine
S.append(slide("Growth engine", "Humor brings men in, ads scale what works",
    """<div class="cards three g">
      <div class="card"><div class="ico hot">▶</div><h3>Funny TikTok series</h3><p>Red flags, famous men’s looks of the week, looks to copy</p></div>
      <div class="card"><div class="ico">⬆</div><h3>Boosted on Facebook</h3><p>The best videos and look posts, on Facebook and Instagram</p></div>
      <div class="card"><div class="ico">★</div><h3>Known faces</h3><p>Men share their favourite looks; women pick the one they’d date</p></div>
    </div>
    <div class="funnel"><span class="hot">Watch a video</span><i>➜</i><span>Open the look</span><i>➜</i><span>Item links</span><i>➜</i><span>Try it on · GEL 0.5</span><i>➜</i><span>Confirmed purchase</span><i>➜</i><span>Comes back</span></div>""",
    "Channel plan, not measured results: no CAC is proven and no known faces are signed yet. We measure every step above. A link click is not a sale: purchases are confirmed with partner data or by the user."))

# 11 · Unit economics
wf = [("Price", 0.50, 0, "k"), ("VAT 18%", -0.08, 0.42, "g"), ("Net", 0.42, 0, "k"),
      ("AI compute", -0.16, 0.26, "g"), ("Card fees", -0.01, 0.25, "g"), ("Support", -0.01, 0.24, "g"),
      ("We keep", 0.24, 0, "h")]
bars = []
for name, v, base, c in wf:
    h = abs(v) * 640
    b = base * 640
    lab = f"{v:+.2f}".replace("+", "") if v > 0 else f"−{abs(v):.2f}"
    bars.append(f'<div class="wcol"><div class="wbar {c}" style="height:{max(h,4):.0f}px;margin-bottom:{b:.0f}px">'
                f'<em>{lab}</em></div><div class="wl">{name}</div></div>')
S.append(slide("Unit economics · Georgia · plan", "Every GEL 0.5 photo leaves about GEL 0.24",
    f"""<div class="ue"><div class="wf">{''.join(bars)}</div>
      <div class="val"><h3>To prove in Georgia</h3>
        <ul><li>The AI provider’s real cost per photo</li><li>Re-generations and failed attempts</li>
        <li>Top-up size and real card fees</li><li>Support load per paying user</li></ul>
        <p class="muted">GEL 0.24 is before the cost of winning a user and fixed costs. Lifetime value and CAC will come from the first cohorts.</p></div></div>""",
    "Planning estimates, rounded, in GEL. GEL 2.62 = $1; photos are bought as credit top-ups."))

# 12 · Team
S.append(slide("Team", "Led by a founder who has done it before",
    """<div class="team">
      <div class="left">
        <div class="founder"><div class="role">Founder &amp; CEO</div><div class="nm">Nika Abashidze</div>
          <div class="fstat"><b>8 yrs</b><span>founder &amp; CEO of caru.ge, a Georgian car marketplace</span></div>
          <p>500 Startups · TechCrunch Disrupt 2022 · GITA grant · Forbes Georgia 30 Under 30 · YouTube 128K</p></div>
        <div class="mates">
          <div><b>Rezi</b><span>CTO &amp; software developer</span></div>
          <div><b>Levani</b><span>Growth &amp; paid ads</span></div>
          <div><b>Giorgi</b><span>Operations</span></div>
        </div>
      </div>
      <div class="right"><h3>The budget allows up to 13, hired in stages</h3>
        <div class="row"><div class="ico hot">✦</div><div class="n">5</div><div><b>Product &amp; AI</b><span>developers, product designer</span></div></div>
        <div class="row"><div class="ico">▶</div><div class="n">4</div><div><b>Content</b><span>camera &amp; editing, actor, scriptwriter, look builder</span></div></div>
        <div class="row"><div class="ico">⬆</div><div class="n">2</div><div><b>Growth</b><span>ads manager, social media and support</span></div></div>
        <div class="row"><div class="ico">⛟</div><div class="n">1</div><div><b>Operations</b><span>logistics manager</span></div></div>
        <div class="row"><div class="ico">♛</div><div class="n">1</div><div><b>Leadership</b><span>director</span></div></div>
      </div>
    </div>""",
    "Hiring follows test results: each role is added when the numbers justify it. Today’s team is 4."))

# 13 · The ask
parts = [(484, "#FF4D2D", "", ""), (333, "#2F76D2", "", ""), (133, "#A3A3A3", "", ""),
         (281, "#1DAF7A", "", ""), (269, "#EBA100", "", "")]
S.append(slide("The ask", "",
    f"""<div class="ask">
      <div class="l"><div class="huge">$1.5M</div><div class="pre">Pre-seed at a $10M pre-money valuation</div>
        <div class="duo2"><div class="box g"><div class="big">13%</div><p>for new investors,<br>$11.5M post-money</p></div>
        <div class="box h"><div class="big">20</div><p>months of runway at the full<br>planned budget, before any sales</p></div></div></div>
      <div class="r"><h3>Use of funds</h3><div class="pie">{pie(parts)}</div>
        <ul class="legend">
          <li><i style="background:#FF4D2D"></i><b>$484K</b> Product &amp; AI</li>
          <li><i style="background:#2F76D2"></i><b>$333K</b> Leadership, ops &amp; admin</li>
          <li><i style="background:#1DAF7A"></i><b>$281K</b> Content &amp; production</li>
          <li><i style="background:#EBA100"></i><b>$269K</b> Marketing &amp; growth</li>
          <li><i style="background:#A3A3A3"></i><b>$133K</b> Reserve (8.9%)</li>
        </ul></div>
    </div>""",
    "$1.5M covers $38K of set-up costs and about 20 months of the planned $72.8K a month, before any sales. Hiring in stages makes the real burn lower. GEL 2.62 = $1."))

# 14 · What the round proves
S.append(slide("What the $1.5M proves", "Three things, in Georgia first",
    """<div class="cards three tall">
      <div class="card"><div class="num hot">1</div><h3>Demand</h3><p>Men open looks, click items, pay for try-on and come back. Measured as a funnel and in monthly cohorts.</p></div>
      <div class="card"><div class="num">2</div><h3>Commerce</h3><p>Written supplier terms, the basket after men untick what they own, and the cost of delivery and partial returns in a pilot.</p></div>
      <div class="card"><div class="num">3</div><h3>Repeatable growth</h3><p>The full cost of winning a user, content and team included, paid back by purchases and repeat use.</p></div>
    </div>
    <div class="bar dark">Then a seed round, sized on these results, to scale into new markets.</div>""",
    "Funnel targets are set from the first months of data. No user, revenue or sales results are claimed yet."))

# 15 · Let's talk (unchanged)
S.append(raster("p18.jpg"))

# Appendix A1 · Why now (unchanged)
S.append(raster("p09.jpg", '<div class="apx">Appendix</div>'))

# Appendix A2 · Long-term ambition
rev = [("2027", 0.20), ("2028", 5.57), ("2029", 15.30), ("2030", 30.80), ("2031", 50.70)]
cols = "".join(f'<div class="col"><div class="v">${v:.2f}M</div><div class="b hot" style="height:{max(v/50.7*250,4):.0f}px"></div><div class="yl">{y}</div></div>' for y, v in rev)
S.append(slide("Appendix · Long-term ambition · USD", "The founder’s revenue target to 2031",
    f'<div class="rev">{cols}</div><div class="bar dark">A top-down target, not a forecast built from demand data.</div>',
    "Founder’s net revenue targets. The earlier users, GMV, EBITDA and cash figures were derived from them and are being rebuilt from real data. Covers Georgia, Armenia, Azerbaijan, Turkey and a women’s line from 2028; not the US."))

# Appendix A3 · Assumptions
S.append(slide("Appendix · Behind the plan", "What the plan assumes",
    """<div class="stats">
      <div class="stat hot"><div class="big">~30%</div><p>target gross margin per look sold; suppliers get about 70% (not yet agreed)</p></div>
      <div class="stat"><div class="big">20%</div><p>of orders assumed to be returned; the share of value returned is modelled separately</p></div>
      <div class="stat"><div class="big">$225</div><p>average order in Georgia in 2027, rising 5% a year</p></div>
      <div class="stat"><div class="big">1–18%</div><p>of active users buy looks, rising from 2027 to 2031</p></div>
      <div class="stat"><div class="big">12–22%</div><p>of active users pay for try-on photos, 8 to 16 a year</p></div>
      <div class="stat"><div class="big">GEL 2.62</div><p>= $1, the planning rate used throughout the deck</p></div>
    </div>
    <div class="bar dark">Assumptions to test, not measured results.</div>""",
    "Definitions of an active user and the split by country are still to be fixed."))

# Appendix A4 · Runway math
S.append(slide("Appendix · Runway", "How far $1.5M goes",
    """<div class="math">
      <div class="eq"><span>($1,500,000 − $38,000 set-up)</span><span>÷ $72,800 a month</span><b>≈ 20 months</b></div>
      <div class="eq"><span>24 months at the full budget</span><span>≈ $1.785M</span><b>≈ $285K short</b></div>
    </div>
    <div class="cards two">
      <div class="card"><h3>The levers</h3><p>Hire in stages as tests pass, so the real burn starts well under $72.8K a month. Try-on revenue and pilot sales extend the runway further.</p></div>
      <div class="card"><h3>What we don’t claim</h3><p>That $1.5M covers all of 2027–2028 without sales. The calendar runway also depends on when the round closes and spending starts.</p></div>
    </div>""",
    "$72.8K a month is the planned budget for a team of up to 13, not today’s spend."))

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#2a2a2a}
body{font-family:Inter,system-ui,sans-serif;color:#111}
.deck{display:flex;flex-direction:column;align-items:center;gap:24px;padding:24px 0}
.slide{width:1440px;height:768px;position:relative;background:#fff;overflow:hidden;flex:none}
.raster{background-size:cover;background-position:center}
.pad{padding:86px 128px 0}
.label{color:#C8301A;font-weight:700;letter-spacing:.08em;text-transform:uppercase;font-size:17px;margin-bottom:22px}
h1{font-family:Arial,'Liberation Sans',sans-serif;font-weight:700;font-size:40px;line-height:1.2;letter-spacing:-.01em}
.t2 h1{font-size:31px}
.foot{position:absolute;left:128px;right:128px;bottom:44px;color:#6b6b6b;font-size:14px;line-height:1.45}
.big{font-family:Arial,'Liberation Sans',sans-serif;font-weight:700;font-size:60px;line-height:1;letter-spacing:-.02em}
.cards{display:grid;gap:22px;margin-top:56px}
.cards.three{grid-template-columns:repeat(3,1fr)}.cards.two{grid-template-columns:1fr 1fr;margin-top:30px}
.card{border:1.5px solid #111;border-radius:10px;padding:34px 34px 30px}
.card p{font-size:19px;line-height:1.45;margin-top:12px;color:#222}
.card .src{font-size:14px;color:#777;margin-top:14px}
.card h3{font-size:24px;margin-top:6px}
.punch{font-weight:700;font-size:22px;margin-top:40px}
.cap{position:absolute;left:0;right:0;bottom:22px;text-align:center;color:#bdbdbd;font-size:15px}
.apx{position:absolute;top:30px;right:40px;background:#111;color:#fff;font-size:13px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;padding:6px 12px;border-radius:6px}
.orange{background:#FF4D2D}.center{display:flex;align-items:center;justify-content:center;text-align:center}
.mega{font-family:Arial,'Liberation Sans',sans-serif;font-weight:700;font-size:74px;line-height:1.25}
.sub{font-family:Arial,'Liberation Sans',sans-serif;font-weight:700;font-size:36px;margin-top:34px}
.dark{color:#111}.cream{color:#FFF8F0}
.stats{display:grid;grid-template-columns:repeat(3,1fr);column-gap:22px;row-gap:34px;margin-top:44px}
.stat{border-top:3px solid #111;padding-top:24px}.stat.hot{border-color:#FF4D2D}
.stat p{color:#6b6b6b;font-size:17px;margin-top:10px;line-height:1.4}
.bar{margin-top:36px;border-radius:10px;padding:18px;text-align:center;font-weight:700;font-size:21px}
.bar.dark{background:#111;color:#fff}
.mkt{display:grid;grid-template-columns:1.25fr 1fr;gap:70px;margin-top:20px;align-items:end}
.chart .cols{display:flex;justify-content:space-around;align-items:flex-end;height:340px;border-bottom:1.5px solid #111}
.col{display:flex;flex-direction:column;align-items:center}
.col .v{font-weight:700;font-size:21px;margin-bottom:14px}
.b{width:190px;border-radius:3px 3px 0 0}.b.grey{background:#E3E3DF}.b.hot,.hot.b{background:#FF4D2D}
.axis{display:flex;justify-content:space-around;font-weight:700;font-size:16px;margin-top:10px}
.cap2{font-weight:700;font-size:21px;margin-top:20px}
.side{display:flex;flex-direction:column;gap:18px}.side .card{padding:24px 30px}.side .big{font-size:52px}
.side .card p{font-size:17px;margin-top:8px}
.phases{display:grid;grid-template-columns:1fr 70px 1fr;align-items:center;margin-top:46px}
.ph{border-radius:12px;padding:38px 40px;height:380px}.ph.light{background:#F2F2F0}.ph.darkc{background:#111;color:#fff}
.pill{display:inline-block;background:#fff;color:#111;font-weight:700;font-size:18px;padding:10px 20px;border-radius:30px}
.pill.hotp{background:#FF4D2D;color:#111}
.duo{display:flex;gap:56px;margin-top:34px}.duo p{font-size:17px;color:#777;margin-top:6px}.darkc .duo p{color:#bbb}
.ph .txt{font-size:17px;line-height:1.5;color:#666;margin-top:26px}.darkc .txt{color:#bbb}
.arrow{color:#FF4D2D;font-size:44px;text-align:center}
.tl{position:relative;display:grid;grid-template-columns:repeat(4,1fr);margin-top:120px;text-align:center}
.tl .line{position:absolute;left:12.5%;right:12.5%;top:104px;height:3px;background:#111}
.node{display:flex;flex-direction:column;align-items:center;position:relative}
.yr{font-family:Arial,'Liberation Sans',sans-serif;font-weight:700;font-size:40px;height:66px}
.dot{width:34px;height:34px;border-radius:50%;border:3px solid #111;background:#fff;margin:12px 0 26px;z-index:1}.dot.hot{background:#FF4D2D;border-color:#FF4D2D}
.node b{font-size:22px;line-height:1.25}.node span{color:#6b6b6b;font-size:17px;margin-top:8px;max-width:270px}
.g .card{padding:34px}.ico{width:72px;height:72px;border-radius:50%;background:#F2F2F0;display:flex;align-items:center;justify-content:center;font-size:28px;margin-bottom:22px}
.ico.hot{background:#FF4D2D;color:#fff}
.g .card p{color:#777;font-size:18px}
.funnel{display:flex;align-items:center;gap:8px;margin-top:34px}
.funnel span{flex:1;background:#F2F2F0;border-radius:8px;text-align:center;font-weight:700;font-size:15.5px;padding:15px 6px}
.funnel span.hot{background:#FF4D2D}.funnel i{font-style:normal;font-size:18px}
.ue{display:grid;grid-template-columns:1.5fr 1fr;gap:70px;margin-top:30px}
.wf{display:flex;align-items:flex-end;gap:16px;height:420px;border-bottom:1.5px solid #111}
.wcol{flex:1;display:flex;flex-direction:column;justify-content:flex-end;height:100%;position:relative}
.wbar{position:relative;border-radius:2px}.wbar.k{background:#141414}.wbar.g{background:#D8D8D4}.wbar.h{background:#FF4D2D}
.wbar em{position:absolute;top:-30px;left:0;right:0;text-align:center;font-style:normal;font-weight:700;font-size:17px}
.wl{position:absolute;bottom:-34px;left:-10px;right:-10px;text-align:center;font-size:15px;color:#555}
.val h3{font-size:24px;margin-top:40px}.val ul{margin:18px 0 0 22px;font-size:19px;line-height:1.75}
.muted{color:#777;font-size:16px;line-height:1.5;margin-top:20px}
.team{display:grid;grid-template-columns:1fr 1fr;gap:60px;margin-top:34px}
.founder{background:#111;color:#fff;border-radius:12px;padding:32px 36px}
.founder .role{color:#FF4D2D;font-weight:700;font-size:18px}.founder .nm{font-family:Arial,'Liberation Sans',sans-serif;font-weight:700;font-size:40px;margin:14px 0 16px}
.fstat{display:flex;gap:16px;align-items:baseline}.fstat b{font-family:Arial,'Liberation Sans',sans-serif;font-size:36px}.fstat span{color:#bbb;font-size:16px;max-width:300px}
.founder p{color:#aaa;font-size:15px;line-height:1.5;margin-top:16px}
.mates{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:14px}
.mates div{background:#F2F2F0;border-radius:10px;padding:16px 18px}.mates b{display:block;font-size:19px}.mates span{font-size:14px;color:#666}
.right h3{font-size:24px;margin-bottom:18px}
.row{display:grid;grid-template-columns:64px 44px 1fr;align-items:center;margin-bottom:12px}
.row .ico{width:54px;height:54px;font-size:20px;margin:0}.row .n{font-family:Arial,'Liberation Sans',sans-serif;font-weight:700;font-size:32px}
.row b{display:block;font-size:18px}.row span{color:#6b6b6b;font-size:16px}
.ask{display:grid;grid-template-columns:.95fr 1.15fr;gap:24px;margin-top:10px}
.huge{font-family:Arial,'Liberation Sans',sans-serif;font-weight:700;font-size:150px;letter-spacing:-.03em;line-height:1}
.pre{font-weight:700;font-size:24px;margin:22px 0 36px}
.duo2{display:flex;gap:18px}.box{border-radius:10px;padding:26px 28px;width:290px}.box.g{background:#F2F2F0}.box.h{background:#FF4D2D}
.box .big{font-size:52px}.box p{font-size:16px;margin-top:10px;line-height:1.4}.box.g p{color:#666}
.r h3{font-size:24px;text-align:center;margin-bottom:14px}.r{display:grid;grid-template-columns:auto 1fr;grid-template-rows:auto 1fr;column-gap:20px}
.r h3{grid-column:1/3}.pie svg{width:290px;height:290px}
.legend{list-style:none;align-self:center}.legend li{font-size:17px;margin:12px 0;white-space:nowrap;display:flex;align-items:center;gap:10px}
.legend i{width:16px;height:16px;border-radius:3px;display:inline-block}.legend b{min-width:62px}
.tall .card{padding:34px 34px 38px}.num{width:52px;height:52px;border-radius:50%;background:#F2F2F0;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:22px;margin-bottom:18px}
.num.hot{background:#FF4D2D}
.rev{display:flex;justify-content:space-around;align-items:flex-end;height:320px;border-bottom:1.5px solid #111;margin-top:10px;position:relative}
.rev .col{position:relative}.rev .b{width:150px}.rev .yl{position:absolute;bottom:-34px;font-weight:700;font-size:20px}
.rev + .bar{margin-top:56px}
.math{display:flex;flex-direction:column;gap:16px;margin-top:40px}
.eq{display:grid;grid-template-columns:1.3fr 1fr .8fr;align-items:baseline;border-top:3px solid #111;padding-top:18px;font-size:24px}
.eq b{font-family:Arial,'Liberation Sans',sans-serif;font-size:40px;color:#FF4D2D;text-align:right}
.nav{display:none;position:fixed;bottom:14px;right:18px;background:rgba(0,0,0,.6);color:#fff;font:13px Inter,sans-serif;padding:6px 10px;border-radius:6px}
@media screen{.deck .slide{transform-origin:top center}}
@media print{@page{size:1440px 768px;margin:0}html,body{background:#fff}.deck{display:block;padding:0}.slide{page-break-after:always;break-after:page}.nav{display:none}}
"""

JS = """
const sl=[...document.querySelectorAll('.slide')];
function fit(){const s=Math.min(1,(window.innerWidth-40)/1440);sl.forEach(x=>{x.style.transform=`scale(${s})`;x.style.marginBottom=`${(s-1)*768}px`});}
addEventListener('resize',fit);fit();
"""

html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>ZMANI Investor Deck</title>
<style>{CSS}</style></head><body><main class="deck">{''.join(S)}</main>
<div class="nav">{len(S)} slides · scroll · Ctrl/Cmd+P for PDF</div><script>{JS}</script></body></html>"""
OUT.write_text(html, encoding="utf-8")
print(f"Wrote {OUT} ({len(S)} slides, {OUT.stat().st_size/1e6:.1f} MB)")
