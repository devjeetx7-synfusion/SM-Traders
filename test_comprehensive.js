const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  const browser = await chromium.launch({
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const filePath = 'file://' + path.resolve('theme.xml');
  fs.mkdirSync('/home/jules/verification/screenshots', { recursive: true });

  const viewports = [
    { name: 'mobile_320', width: 320, height: 568 },
    { name: 'mobile_390', width: 390, height: 844 },
    { name: 'mobile_412', width: 412, height: 915 },
    { name: 'desktop_1280', width: 1280, height: 720 },
  ];

  let hasOverflow = false;

  for (const vp of viewports) {
    console.log(`\nTesting viewport: ${vp.name} (${vp.width}x${vp.height})`);
    const context = await browser.newContext({ viewport: { width: vp.width, height: vp.height } });
    const page = await context.newPage();

    const errors = [];
    page.on('pageerror', error => errors.push(error.message));

    await page.goto(filePath, { waitUntil: 'networkidle' });

    // Check for overflow
    const overflowInfo = await page.evaluate(() => {
      const isOverflowing = document.documentElement.scrollWidth > document.documentElement.clientWidth;
      const offenders = [...document.querySelectorAll('*')]
        .filter(el => el.getBoundingClientRect().right > window.innerWidth + 1)
        .map(el => ({
          tag: el.tagName,
          class: el.className,
          right: el.getBoundingClientRect().right,
          windowWidth: window.innerWidth
        }));
      return { isOverflowing, offenders };
    });

    if (overflowInfo.isOverflowing || overflowInfo.offenders.length > 0) {
      console.log(`[!] OVERFLOW DETECTED on ${vp.name}`);
      console.log(overflowInfo.offenders);
      hasOverflow = true;
    } else {
      console.log(`[✓] No horizontal overflow.`);
    }

    if (errors.length > 0) {
      console.log(`[!] JS ERRORS DETECTED:`, errors);
    } else {
      console.log(`[✓] No JS errors.`);
    }

    await page.screenshot({ path: `/home/jules/verification/screenshots/full_${vp.name}.png`, fullPage: true });
    await page.screenshot({ path: `/home/jules/verification/screenshots/hero_${vp.name}.png` });

    if (vp.name === 'mobile_390') {
      console.log('Testing mobile interactions...');
      const burger = page.locator('#smBurger');
      if (await burger.isVisible()) {
        await burger.click();
        await page.waitForTimeout(500);
        await page.screenshot({ path: `/home/jules/verification/screenshots/menu_open.png` });
        const close = page.locator('#smClose');
        if (await close.isVisible()) {
          await close.click();
        }
      }
    }

    await context.close();
  }

  await browser.close();

  if (hasOverflow) {
    process.exit(1);
  }
})();
