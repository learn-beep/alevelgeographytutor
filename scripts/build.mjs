// Builds the two-board site: one Astro build per board (AQA at /aqa/, Edexcel at /edexcel/) plus a shared build for the
// root pages (board chooser, tutors, about, legal, forms), merged into dist/ with the board pages' links prefixed.
// Usage: node scripts/build.mjs        (Netlify runs this via `npm run build`)
import { execSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const DATA = path.join(root, 'src/data');
const DIST = path.join(root, 'dist');
const BUILD = path.join(root, '.build');
const BOARDS = ['aqa', 'edexcel'];
const SHARED_PAGES = ['index.html', '404.html', 'tutors', 'about', 'privacy', 'terms', 'thank-you', 'report'];
const DOMAIN = 'https://www.alevelgeographytutor.com';
const FILES = ['questions', 'papers', 'topics', 'spec', 'weighting'];

function useBoard(b) {
  const src = path.join(root, 'boards', b);
  for (const f of FILES) fs.copyFileSync(path.join(src, 'data', f + '.json'), path.join(DATA, f + '.json'));
  for (const f of ['board', 'exams', 'boundaries']) fs.copyFileSync(path.join(src, f + '.json'), path.join(DATA, f + '.json'));
}
function useShared() {
  useBoard('aqa'); // the shared pages need some data to import; they do not show it
  const aqa = JSON.parse(fs.readFileSync(path.join(DATA, 'board.json'), 'utf8'));
  fs.writeFileSync(path.join(DATA, 'board.json'), JSON.stringify({ ...aqa, id: null, short: '', full: 'A-level Geography', store: 'geo' }));
}
function astro(out) {
  fs.rmSync(out, { recursive: true, force: true });
  execSync('npx astro build', { cwd: root, stdio: 'inherit', env: { ...process.env, OUT_DIR: out, NO_PUBLIC: '1' } });
}
const walk = (d) => fs.readdirSync(d, { withFileTypes: true }).flatMap((e) => (e.isDirectory() ? walk(path.join(d, e.name)) : [path.join(d, e.name)]));

fs.rmSync(DIST, { recursive: true, force: true });
fs.mkdirSync(DIST, { recursive: true });

// 1. shared root pages
useShared();
astro(path.join(BUILD, 'shared'));
for (const name of [...SHARED_PAGES, '_astro']) {
  const p = path.join(BUILD, 'shared', name);
  if (fs.existsSync(p)) fs.cpSync(p, path.join(DIST, name), { recursive: true });
}

// 2. one build per board, moved under /<board>/ with its internal links prefixed
for (const b of BOARDS) {
  useBoard(b);
  const out = path.join(BUILD, b);
  astro(out);
  const routes = fs.readdirSync(out, { withFileTypes: true }).filter((e) => e.isDirectory() && !SHARED_PAGES.includes(e.name)).map((e) => e.name);
  const alt = routes.map((r) => r.replace(/[-_]/g, (c) => '\\' + c)).join('|');
  const rx = new RegExp(`(["'\`(=]|${DOMAIN.replace(/[.:/]/g, (c) => '\\' + c)})/(${alt})(?=[/"'?#\`)])`, 'g');
  for (const f of walk(out)) {
    const rel = path.relative(out, f);
    const top = rel.split(path.sep)[0];
    if ((SHARED_PAGES.includes(top) && rel !== 'index.html') || /^sitemap/.test(rel)) continue;
    const dest = path.join(DIST, b, rel);
    fs.mkdirSync(path.dirname(dest), { recursive: true });
    if (/\.(html|js|json|css|xml)$/.test(f)) fs.writeFileSync(dest, fs.readFileSync(f, 'utf8').replace(rx, (m, pre, r) => `${pre}/${b}/${r}`));
    else fs.copyFileSync(f, dest);
  }
  console.log(`${b}: ${routes.length} routes prefixed`);
}

// 3. public/ once (crops, tutor photos, favicon, forms)
fs.cpSync(path.join(root, 'public'), DIST, { recursive: true });

// 4. one sitemap for the whole site
const pages = walk(DIST).filter((f) => f.endsWith('index.html')).map((f) => '/' + path.relative(DIST, path.dirname(f)).split(path.sep).join('/'))
  .map((u) => (u === '/' ? '/' : u + '/')).filter((u) => !/\/(print|data|thank-you)\//.test(u)).sort();
fs.writeFileSync(path.join(DIST, 'sitemap-0.xml'), `<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">${pages.map((u) => `<url><loc>${DOMAIN}${u}</loc></url>`).join('')}</urlset>`);
fs.writeFileSync(path.join(DIST, 'sitemap-index.xml'), `<?xml version="1.0" encoding="UTF-8"?><sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><sitemap><loc>${DOMAIN}/sitemap-0.xml</loc></sitemap></sitemapindex>`);
console.log(`sitemap: ${pages.length} pages`);

// leave the AQA data in src/data for `astro dev`
useBoard('aqa');
fs.rmSync(BUILD, { recursive: true, force: true });
