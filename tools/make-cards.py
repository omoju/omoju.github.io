#!/usr/bin/env python
"""Generate a share card per article, from that article's own title and description.

Each card is 1200x630 (the Open Graph large-image ratio) and is typeset in the
site's own palette and fonts, so a shared link looks like the essay it points at
rather than like a generic site card.

Cards land in content/images/cards/<slug>.jpg. The <slug> convention is what
themes/minimalist/templates/base.html relies on to build og:image for articles,
so a card must exist for every article -- this script regenerates all of them.

Run from the repo root, with the project virtualenv:

    ./new_pelican_env/bin/python tools/make-cards.py

Rendering is batched: cards are stacked into tall pages and captured in one
browser pass each, then sliced. One browser launch per card would take minutes.
"""

import glob
import html
import os
import shutil
import subprocess
import sys
import tempfile

from pelican.readers import MarkdownReader
from pelican.settings import read_settings
from pelican.utils import slugify

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT_DIR = "content/images/cards"
W, H = 1200, 630
BATCH = 16          # keeps each captured page well inside Chrome's height limit
PAD = 40            # see render(): keeps the final slice off the bottom edge
JPEG_QUALITY = 88

CARD_CSS = """
  *{margin:0;padding:0;box-sizing:border-box}
  body{background:#fff;font-family:'EB Garamond',Georgia,serif}
  .card{width:1200px;height:630px;background:#fdfdfa;color:#211f1b;
        display:flex;flex-direction:column;padding:88px 96px 64px;position:relative}
  h1{font-weight:500;font-variant-caps:small-caps;letter-spacing:.045em;line-height:1.08}
  .rule{width:110px;height:2px;background:#cdc8bd;margin:32px 0}
  p{font-size:31px;line-height:1.5;color:#3d3931;max-width:960px}
  .byline{margin-top:auto;font-size:22px;color:#56514a;letter-spacing:.06em;
          font-variant-caps:small-caps}
"""


def dimensions(path):
    out = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", path],
                         check=True, capture_output=True, text=True).stdout
    vals = [int(l.split(":")[1]) for l in out.splitlines() if ":" in l and l.split(":")[0].strip()
            in ("pixelWidth", "pixelHeight")]
    return tuple(vals)


def font_size(title):
    """Long titles need to step down so they never wrap past three lines."""
    n = len(title)
    if n <= 24:
        return 84
    if n <= 40:
        return 72
    if n <= 60:
        return 60
    return 50


def truncate(text, limit=165):
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit(" ", 1)[0]
    return cut.rstrip(".,;:") + "…"


def collect():
    settings = read_settings("publishconf.py")
    reader = MarkdownReader(settings)
    subs = settings.get("SLUG_REGEX_SUBSTITUTIONS", [])
    out = []
    for path in sorted(glob.glob("content/*.md")):
        try:
            _, meta = reader.read(path)
        except Exception as exc:                      # malformed post: skip, don't fail the run
            print(f"  skip {os.path.basename(path)}: {exc}", file=sys.stderr)
            continue
        title = (meta.get("title") or "").strip()
        if not title:
            continue
        slug = meta.get("slug") or slugify(title, subs)
        desc = (meta.get("description") or "").strip()
        out.append((slug, title, desc))
    return out


def render(batch, workdir, index):
    """Stack a batch of cards into one page, capture it, and slice it up."""
    cards = []
    for _, title, desc in batch:
        body = f"<p>{html.escape(truncate(desc))}</p>" if desc else ""
        cards.append(
            f'<div class="card">'
            f'<h1 style="font-size:{font_size(title)}px">{html.escape(title)}</h1>'
            f'<div class="rule"></div>{body}'
            f'<div class="byline">Omoju Miller &nbsp;·&nbsp; omojumiller.com</div>'
            f"</div>"
        )
    page = os.path.join(workdir, f"page{index}.html")
    with open(page, "w") as fh:
        fh.write(
            "<!doctype html><meta charset='utf-8'>"
            "<link href='https://fonts.googleapis.com/css2?"
            "family=EB+Garamond:wght@400;500&display=swap' rel='stylesheet'>"
            f"<style>{CARD_CSS}</style>" + "".join(cards)
        )
    shot = os.path.join(workdir, f"page{index}.png")
    # PAD matters: sips silently returns the *whole* image, exit code 0, when a
    # crop region ends flush with the bottom edge. Padding the page keeps the
    # last slice off that boundary.
    subprocess.run(
        [CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
         f"--window-size={W},{H * len(batch) + PAD}", f"--screenshot={shot}",
         "--virtual-time-budget=15000", f"file://{os.path.abspath(page)}"],
        check=True, capture_output=True,
    )
    for i, (slug, _, _) in enumerate(batch):
        crop = os.path.join(workdir, f"{slug}.png")
        subprocess.run(["sips", "-c", str(H), str(W), "--cropOffset", str(i * H), "0",
                        shot, "--out", crop], check=True, capture_output=True)
        out = os.path.join(OUT_DIR, f"{slug}.jpg")
        subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions",
                        str(JPEG_QUALITY), crop, "--out", out],
                       check=True, capture_output=True)
        got = dimensions(out)
        if got != (W, H):
            sys.exit(f"{slug}: expected {W}x{H}, got {got[0]}x{got[1]}")


def main():
    if not os.path.exists(CHROME):
        sys.exit(f"Chrome not found at {CHROME}")
    articles = collect()
    print(f"{len(articles)} articles, {sum(1 for a in articles if a[2])} with descriptions")

    shutil.rmtree(OUT_DIR, ignore_errors=True)       # stale cards would silently ship
    os.makedirs(OUT_DIR, exist_ok=True)

    with tempfile.TemporaryDirectory() as workdir:
        for i in range(0, len(articles), BATCH):
            batch = articles[i:i + BATCH]
            print(f"  rendering {i + 1}-{i + len(batch)}...")
            render(batch, workdir, i)

    made = sorted(glob.glob(f"{OUT_DIR}/*.jpg"))
    total = sum(os.path.getsize(f) for f in made)
    print(f"wrote {len(made)} cards, {total / 1024:.0f} KB total")
    if len(made) != len(articles):
        sys.exit(f"expected {len(articles)} cards, got {len(made)}")


if __name__ == "__main__":
    main()
