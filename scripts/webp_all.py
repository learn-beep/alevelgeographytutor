"""Convert every bank image bundle (data/img/*.js) to WebP crops under public/img/<bundle>/, in parallel.
python3 scripts/webp_all.py <bank folder> [<bank folder>...]"""
import sys, re, json, base64, io, pathlib
from multiprocessing import Pool
from PIL import Image
def one(f):
    f = pathlib.Path(f)
    m = re.match(r'QBIMG_LOADED\("([^"]+)",(\{.*\})\);?\s*$', f.read_text(encoding="utf-8"), re.S)
    if not m: return f.stem, 0
    dest = pathlib.Path("public/img") / f.stem; dest.mkdir(parents=True, exist_ok=True); n = 0
    for name, data in json.loads(m.group(2)).items():
        t = dest / (pathlib.Path(name).stem + ".webp")
        im = Image.open(io.BytesIO(base64.b64decode(data.split(",", 1)[1])))
        # bilevel and few-grey PNGs (mark schemes, question text) stay sharp and small as lossless WebP; photos/JPEGs go lossy
        if im.format == "PNG" and im.mode in ("1", "L", "P", "LA"): im.convert("L").save(t, "WEBP", lossless=True, quality=80, method=4)
        else: im.convert("RGB").save(t, "WEBP", quality=72, method=4)
        n += 1
    return f.stem, n
if __name__ == "__main__":
    files = [str(f) for b in sys.argv[1:] for f in sorted(pathlib.Path(b, "data", "img").glob("*.js"))]
    with Pool(8) as p:
        tot = 0
        for stem, n in p.imap_unordered(one, files): tot += n; print(stem, n, flush=True)
    print("images", tot)
