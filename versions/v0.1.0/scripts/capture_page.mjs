#!/usr/bin/env node

import fs from "node:fs/promises";
import path from "node:path";
import process from "node:process";

function usage() {
  console.log(`Capture a webpage at an exact viewport.

Usage:
  node scripts/capture_page.mjs --url <url> --width <px> --height <px> --output <file>

Options:
  --url             Page URL to capture (required)
  --width           Viewport width in CSS pixels (required)
  --height          Viewport height in CSS pixels (required)
  --output          PNG output path (required)
  --full-page       Capture the full scrollable page instead of the viewport
  --wait-ms         Extra wait after load (default: 500)
  --selector        Wait for a selector before capture
  --device-scale    Device scale factor (default: 1)
  --color-scheme    light, dark, or no-preference (default: no-preference)
  --reduced-motion  reduce or no-preference (default: reduce)
  --help            Show this message
`);
}

function parseArgs(argv) {
  const result = {
    fullPage: false,
    waitMs: 500,
    deviceScaleFactor: 1,
    colorScheme: "no-preference",
    reducedMotion: "reduce",
  };

  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    switch (arg) {
      case "--help":
        result.help = true;
        break;
      case "--full-page":
        result.fullPage = true;
        break;
      case "--url":
        result.url = argv[++index];
        break;
      case "--width":
        result.width = Number(argv[++index]);
        break;
      case "--height":
        result.height = Number(argv[++index]);
        break;
      case "--output":
        result.output = argv[++index];
        break;
      case "--wait-ms":
        result.waitMs = Number(argv[++index]);
        break;
      case "--selector":
        result.selector = argv[++index];
        break;
      case "--device-scale":
        result.deviceScaleFactor = Number(argv[++index]);
        break;
      case "--color-scheme":
        result.colorScheme = argv[++index];
        break;
      case "--reduced-motion":
        result.reducedMotion = argv[++index];
        break;
      default:
        throw new Error(`Unknown argument: ${arg}`);
    }
  }
  return result;
}

function validate(options) {
  const missing = ["url", "width", "height", "output"].filter((key) => !options[key]);
  if (missing.length) {
    throw new Error(`Missing required arguments: ${missing.join(", ")}`);
  }
  if (!Number.isInteger(options.width) || options.width < 1) {
    throw new Error("--width must be a positive integer");
  }
  if (!Number.isInteger(options.height) || options.height < 1) {
    throw new Error("--height must be a positive integer");
  }
  if (!Number.isFinite(options.waitMs) || options.waitMs < 0) {
    throw new Error("--wait-ms must be zero or greater");
  }
  if (!Number.isFinite(options.deviceScaleFactor) || options.deviceScaleFactor <= 0) {
    throw new Error("--device-scale must be greater than zero");
  }
}

async function main() {
  let options;
  try {
    options = parseArgs(process.argv.slice(2));
    if (options.help) {
      usage();
      return;
    }
    validate(options);
  } catch (error) {
    console.error(JSON.stringify({ ok: false, error: error.message }, null, 2));
    process.exitCode = 2;
    return;
  }

  await fs.mkdir(path.dirname(path.resolve(options.output)), { recursive: true });

  let chromium;
  try {
    ({ chromium } = await import("playwright"));
  } catch (error) {
    console.error(JSON.stringify({
      ok: false,
      error: "Playwright is not installed. Run: cd scripts && npm install && npx playwright install chromium",
    }, null, 2));
    process.exitCode = 2;
    return;
  }

  const browser = await chromium.launch({ headless: true });

  try {
    const context = await browser.newContext({
      viewport: { width: options.width, height: options.height },
      deviceScaleFactor: options.deviceScaleFactor,
      colorScheme: options.colorScheme,
      reducedMotion: options.reducedMotion,
    });
    const page = await context.newPage();
    await page.goto(options.url, { waitUntil: "networkidle" });
    await page.evaluate(async () => {
      if (document.fonts?.ready) await document.fonts.ready;
    });
    if (options.selector) {
      await page.waitForSelector(options.selector, { state: "visible" });
    }
    if (options.waitMs) {
      await page.waitForTimeout(options.waitMs);
    }
    await page.screenshot({ path: options.output, fullPage: options.fullPage });
    console.log(
      JSON.stringify(
        {
          ok: true,
          url: options.url,
          output: path.resolve(options.output),
          viewport: [options.width, options.height],
          fullPage: options.fullPage,
          deviceScaleFactor: options.deviceScaleFactor,
        },
        null,
        2,
      ),
    );
    await context.close();
  } catch (error) {
    console.error(JSON.stringify({ ok: false, error: error.message }, null, 2));
    process.exitCode = 1;
  } finally {
    await browser.close();
  }
}

await main();
