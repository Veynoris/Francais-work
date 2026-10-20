// Imprime une liste de fichiers HTML en PDF avec Chromium (Playwright).
// Usage : node src/render_pdf.mjs build/jobs.json   (jobs = [{html, pdf}, ...])
import { readFileSync } from "node:fs";
import { createRequire } from "node:module";
import { pathToFileURL } from "node:url";

const require = createRequire(import.meta.url);
let playwright;
try {
  playwright = require("playwright");
} catch {
  playwright = require("/opt/node22/lib/node_modules/playwright");
}

const jobs = JSON.parse(readFileSync(process.argv[2], "utf8"));
const browser = await playwright.chromium.launch();
const page = await browser.newPage();
for (const job of jobs) {
  await page.goto(pathToFileURL(job.html).href, { waitUntil: "load" });
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({ path: job.pdf, preferCSSPageSize: true, printBackground: true });
}
await browser.close();
