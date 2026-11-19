// main.ts for the gta6-meme-x-01 entry (Node 22, standard library only).
// The entry is an X post, so this program only has to hand POST.json over:
// it copies POST.json from the repository root to the output directory,
// validates that it parses as JSON and carries a url field, and logs a
// short self-check line. It exits non-zero on any failure.
import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

const botDir = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const source = join(botDir, "POST.json");

const raw = readFileSync(source, "utf8");
if (raw.length > 16384) {
  throw new Error("POST.json exceeds 16384 bytes");
}
const post = JSON.parse(raw) as unknown;

if (typeof post !== "object" || post === null || !("url" in post)) {
  throw new Error("POST.json must be a JSON object with a url field");
}
const url = (post as { url: unknown }).url;
if (typeof url !== "string" || !url.startsWith("https://")) {
  throw new Error("POST.json url must be an https URL string");
}
// The gate only accepts an X post address, so reject anything else early.
const xPost = /^https:\/\/(www\.|mobile\.)?(x\.com|twitter\.com)\/\w+\/status\/\d+$/;
const bare = url.split(/[?#]/)[0];
if (!xPost.test(bare)) {
  throw new Error(`POST.json url is not an X post address: ${url}`);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(source, join(outDir, "POST.json"));
console.log(`gta6-meme-x-01: POST.json copied to ${outDir} (${url})`);
