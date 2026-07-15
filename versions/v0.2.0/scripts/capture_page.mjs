#!/usr/bin/env node

import fs from "node:fs/promises";
import path from "node:path";
import process from "node:process";

function usage() {
  console.log(`Capture a webpage at an exact viewport with deterministic rendering.

Usage:
  node scripts/capture_page.mjs --url <url> --width <px> --height <px> --output <file>

Options:
  --url                Page URL to capture (required)
  --width              Viewport width in CSS pixels (required)
  --height             Viewport height in CSS pixels (required)
  --output             PNG output path (required)
  --full-page          Capture the full scrollable page instead of the viewport
  --wait-ms            Extra wait after readiness checks (default: 500)
  --timeout-ms         Navigation and selector timeout (default: 30000)
  --selector           Wait for a visible selector before capture
  --scroll-x           Horizontal scroll position (default: 0)
  --scroll-y           Vertical scroll position (default: 0)
  --device-scale       Device scale factor (default: 1)
  --color-scheme       light, dark, or no-preference (default: no-preference)
  --reduced-motion     reduce or no-preference (default: reduce)
  --animation-policy   disable or allow (default: disable)
  --hide-selectors     Comma-separated selectors to hide before capture
  --load-state         domcontentloaded, load, or networkidle (default: networkidle)
  --metadata           Optional JSON path for capture metadata
  --help               Show this message
`);
}

function parseArgs(argv) {
  const result = {
    fullPage: false,
    waitMs: 500,
    timeoutMs: 30000,
    scrollX: 0,
    scrollY: 0,
    deviceScaleFactor: 1,
    colorScheme: "no-preference",
    reducedMotion: "reduce",
    animationPolicy: "disable",
    loadState: "networkidle",
  };

  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    switch (arg) {
      case "--help": result.help = true; break;
      case "--full-page": result.fullPage = true; break;
      case "--url": result.url = argv[++index]; break;
      case "--width": result.width = Number(argv[++index]); break;
      case "--height": result.height = Number(argv[++index]); break;
      case "--output": result.output = argv[++index]; break;
      case "--wait-ms": result.waitMs = Number(argv[++index]); break;
      case "--timeout-ms": result.timeoutMs = Number(argv[++index]); break;
      case "--selector": result.selector = argv[++index]; break;
      case "--scroll-x": result.scrollX = Number(argv[++index]); break;
      case "--scroll-y": result.scrollY = Number(argv[++index]); break;
      case "--device-scale": result.deviceScaleFactor = Number(argv[++index]); break;
      case "--color-scheme": result.colorScheme = argv[++index]; break;
      case "--reduced-motion": result.reducedMotion = argv[++index]; break;
      case "--animation-policy": result.animationPolicy = argv[++index]; break;
      case "--hide-selectors": result.hideSelectors = argv[++index]; break;
      case "--load-state": result.loadState = argv[++index]; break;
      case "--metadata": result.metadata = argv[++index]; break;
      default: throw new Error(`Unknown argument: ${arg}`);
    }
  }
  return result;
}

function validate(options) {
  const missing = ["url", "width", "height", "output"].filter((key) => options[key] === undefined || options[key] === "");
  if (missing.length) throw new Error(`Missing required arguments: ${missing.join(", ")}`);
  if (!Number.isInteger(options.width) || options.width < 1) throw new Error("--width must be a positive integer");
  if (!Number.isInteger(options.height) || options.height < 1) throw new Error("--height must be a positive integer");
  for (const [name, value] of [["--wait-ms", options.waitMs], ["--timeout-ms", options.timeoutMs]]) {
    if (!Number.isFinite(value) || value < 0) throw new Error(`${name} must be zero or greater`);
  }
  for (const [name, value] of [["--scroll-x", options.scrollX], ["--scroll-y", options.scrollY]]) {
    if (!Number.isFinite(value) || value < 0) throw new Error(`${name} must be zero or greater`);
  }
  if (!Number.isFinite(options.deviceScaleFactor) || options.deviceScaleFactor <= 0) throw new Error("--device-scale must be greater than zero");
  if (!["light", "dark", "no-preference"].includes(options.colorScheme)) throw new Error("Invalid --color-scheme");
  if (!["reduce", "no-preference"].includes(options.reducedMotion)) throw new Error("Invalid --reduced-motion");
  if (!["disable", "allow"].includes(options.animationPolicy)) throw new Error("Invalid --animation-policy");
  if (!["domcontentloaded", "load", "networkidle"].includes(options.loadState)) throw new Error("Invalid --load-state");
}

async function writeMetadata(target, payload) {
  if (!target) return;
  const resolved = path.resolve(target);
  await fs.mkdir(path.dirname(resolved), { recursive: true });
  await fs.writeFile(resolved, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
}

async function main() {
  let options;
  try {
    options = parseArgs(process.argv.slice(2));
    if (options.help) { usage(); return; }
    validate(options);
  } catch (error) {
    console.error(JSON.stringify({ ok: false, error: error.message }, null, 2));
    process.exitCode = 2;
    return;
  }

  const output = path.resolve(options.output);
  await fs.mkdir(path.dirname(output), { recursive: true });

  let chromium;
  try {
    ({ chromium } = await import("playwright"));
  } catch {
    console.error(JSON.stringify({
      ok: false,
      error: "Playwright is not installed. Run: cd scripts && npm install && npx playwright install chromium",
    }, null, 2));
    process.exitCode = 2;
    return;
  }

  const browser = await chromium.launch({ headless: true });
  const consoleErrors = [];
  const pageErrors = [];
  const failedRequests = [];

  try {
    const context = await browser.newContext({
      viewport: { width: options.width, height: options.height },
      deviceScaleFactor: options.deviceScaleFactor,
      colorScheme: options.colorScheme,
      reducedMotion: options.reducedMotion,
    });
    const page = await context.newPage();
    page.setDefaultTimeout(options.timeoutMs);
    page.on("console", (message) => {
      if (message.type() === "error") consoleErrors.push(message.text());
    });
    page.on("pageerror", (error) => pageErrors.push(error.message));
    page.on("requestfailed", (request) => failedRequests.push({ url: request.url(), error: request.failure()?.errorText ?? "unknown" }));

    await page.goto(options.url, { waitUntil: options.loadState, timeout: options.timeoutMs });

    if (options.animationPolicy === "disable") {
      await page.addStyleTag({ content: `
        *, *::before, *::after {
          animation-delay: 0s !important;
          animation-duration: 0s !important;
          animation-iteration-count: 1 !important;
          transition-delay: 0s !important;
          transition-duration: 0s !important;
          caret-color: transparent !important;
          scroll-behavior: auto !important;
        }
        html { scrollbar-width: none !important; }
        body::-webkit-scrollbar, html::-webkit-scrollbar { display: none !important; }
      ` });
    }

    await page.evaluate(async () => {
      if (document.fonts?.ready) await document.fonts.ready;
      const images = Array.from(document.images);
      await Promise.all(images.map(async (image) => {
        if (image.complete) {
          try { await image.decode?.(); } catch {}
          return;
        }
        await new Promise((resolve) => {
          image.addEventListener("load", resolve, { once: true });
          image.addEventListener("error", resolve, { once: true });
        });
      }));
    });

    if (options.selector) await page.waitForSelector(options.selector, { state: "visible", timeout: options.timeoutMs });

    if (options.hideSelectors) {
      const selectors = options.hideSelectors.split(",").map((value) => value.trim()).filter(Boolean);
      await page.evaluate((items) => {
        for (const selector of items) {
          document.querySelectorAll(selector).forEach((element) => {
            element.style.setProperty("visibility", "hidden", "important");
          });
        }
      }, selectors);
    }

    await page.evaluate(({ x, y }) => window.scrollTo(x, y), { x: options.scrollX, y: options.scrollY });
    if (options.waitMs) await page.waitForTimeout(options.waitMs);

    const pageInfo = await page.evaluate(() => ({
      title: document.title,
      url: location.href,
      scroll: [window.scrollX, window.scrollY],
      documentSize: [document.documentElement.scrollWidth, document.documentElement.scrollHeight],
      viewport: [window.innerWidth, window.innerHeight],
    }));

    await page.screenshot({ path: output, fullPage: options.fullPage, animations: "disabled" });
    const payload = {
      ok: true,
      requestedUrl: options.url,
      finalUrl: pageInfo.url,
      title: pageInfo.title,
      output,
      viewport: [options.width, options.height],
      documentSize: pageInfo.documentSize,
      scroll: pageInfo.scroll,
      fullPage: options.fullPage,
      deviceScaleFactor: options.deviceScaleFactor,
      colorScheme: options.colorScheme,
      reducedMotion: options.reducedMotion,
      animationPolicy: options.animationPolicy,
      consoleErrors,
      pageErrors,
      failedRequests,
    };
    await writeMetadata(options.metadata, payload);
    console.log(JSON.stringify(payload, null, 2));
    await context.close();
  } catch (error) {
    const payload = { ok: false, error: error.message, consoleErrors, pageErrors, failedRequests };
    await writeMetadata(options.metadata, payload);
    console.error(JSON.stringify(payload, null, 2));
    process.exitCode = 1;
  } finally {
    await browser.close();
  }
}

await main();
