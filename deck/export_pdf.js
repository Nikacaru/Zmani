// Exports the revised deck HTML to PDF (one 1440x768 page per slide).
// Optional: pass a folder to also save one PNG preview per slide.
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const dir = __dirname;
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1480, height: 900 } });
  await page.goto('file://' + path.join(dir, 'ZMANI_Investor_Deck_1.5M_revised.html'));
  await page.waitForTimeout(500);
  await page.pdf({
    path: path.join(dir, 'ZMANI_Investor_Deck_1.5M_revised.pdf'),
    width: '1440px', height: '768px', printBackground: true,
  });
  const out = process.argv[2];
  if (out) {
    await page.evaluate(() => document.querySelectorAll('.slide').forEach(x => {
      x.style.transform = 'none'; x.style.marginBottom = '0';
    }));
    const slides = await page.$$('.slide');
    for (let i = 0; i < slides.length; i++) {
      await slides[i].screenshot({ path: path.join(out, `s${String(i + 1).padStart(2, '0')}.png`) });
    }
  }
  await browser.close();
})();
