// The World in One Day — Monday, 23 November 2026.
//
// Entry program (Node 22, standard library only). It copies the finished
// front page, entry.png, into the grader's output directory. The image is
// built ahead of time by compose.py; this program does no drawing, no
// network access and no randomness, so both grader runs write identical
// bytes.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const repoRoot = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const source = join(repoRoot, "entry.png");
const target = join(outDir, "entry.png");

mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);
const bytes = statSync(target).size;
console.log(`copied entry.png to ${target} (${bytes} bytes)`);
