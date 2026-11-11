# alevelgeographytutor.com

Static Astro site for A-level Geography on two exam boards, deployed on Netlify:
- **AQA** A level 7037 / AS 7036 at `/aqa/`
- **Pearson Edexcel** A level 9GE0 / AS 8GE0 at `/edexcel/`

Shared pages at the root: the board chooser, tutors (Lauren and Glenda), about, privacy, terms, report a mistake, thank-you.
Built from the Sociology/Economics sites with the `subject-revision-site` skill.

## Run locally
    npm install
    npm run build      # node scripts/build.mjs: builds every board and the shared pages into dist/
    npx astro dev      # one board at a time: whatever is in src/data (AQA after a build)

## How the two-board build works
`scripts/build.mjs` copies one board's files from `boards/<board>/` into `src/data/` (questions, papers, topics, spec,
weighting, board.json, exams.json, boundaries.json), runs `astro build` into `.build/<board>`, then moves the output under
`dist/<board>/` and prefixes that board's internal links (`/questions/...` becomes `/aqa/questions/...`). A third build with
`board.id = null` gives the root pages. `public/` (crops in `public/img/<paper>/`, tutor photos, forms) is copied once.
It also writes the sitemap (`/sitemap-index.xml`).

Everything that differs between the boards is in `boards/<board>/board.json`: topic groups and where each is examined,
paper names, question-type pages, the level bands for self-marking, the mock-paper shapes and options, and the notes on
the past-papers page.

Set `CROPS=off` in Netlify's environment to replace every crop with a link to the board's past-paper page.

## Data
`python3 scripts/export.py --bank "<Question Bank folder>" --topics boards/<board>/topics.json --config boards/<board>/config.json --out boards/<board>/data`
reads a question bank export (`data/index.js`) and writes the board's data files. `python3 scripts/webp_all.py <bank> [<bank>]`
converts the image bundles to WebP crops in `public/img/`. `scripts/make_topics.py <AQA bank> <Edexcel bank>` writes the
two `topics.json` files (AQA: 45 topics from the spec subsections; Edexcel: 39 topics, one per enquiry question).

Banks: `Dropbox\Teaching\Geography\AQA\Question Bank` and `Dropbox\Teaching\Geography\Edexcel\Question Bank`.

## Facts to update each year
- `boards/<board>/exams.json`: AQA key dates and Pearson's final timetable (summer 2027 entered November 2026).
- `boards/<board>/boundaries.json`: AQA out of 300 (Papers 1 and 2 out of 120, NEA 60); Pearson out of 350 (Papers 1 and 2 out of 105, Paper 3 and NEA 70), AS out of 180.
- New papers: rebuild the banks, re-export, rerun `webp_all.py`.

## Content to be checked by a tutor
- The level bands used for self-marking (`levels` in each board.json), summarised by the site.
- Tutor profiles in `src/data/tutors.json` (Glenda has no photo yet: add `public/tutors/glenda.webp`, 320×320, and set `photo`).
