const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  const browser = await chromium.launch({
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  const context = await browser.newContext({
    viewport: { width: 1280, height: 800 }
  });
  const page = await context.newPage();

  const filePath = 'file://' + path.resolve('theme.xml');
  console.log('Navigating to:', filePath);
  await page.goto(filePath, { waitUntil: 'networkidle' });

  fs.mkdirSync('/home/jules/verification/screenshots', { recursive: true });
  await page.screenshot({ path: '/home/jules/verification/screenshots/verification.png', fullPage: false });
  console.log('Screenshot taken!');

  await browser.close();
})();
