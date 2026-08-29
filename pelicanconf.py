import hashlib as _hashlib
import pathlib as _pathlib

AUTHOR = 'Omoju Miller'
SITENAME = 'Omoju Miller'
SITEURL = ""

PATH = "content"

TIMEZONE = 'America/Los_Angeles'

DEFAULT_LANG = 'en'

# Theme
THEME = 'themes/minimalist'

# Static files
# 'themes/...' resolved against content/ and never existed; dropping it also
# silences the dev server's watch warning. The CV PDF is served from the site
# root so the CV page can point at it as the full record.
STATIC_PATHS = ['images', 'Omoju_Miller_MasterCV.pdf']
EXTRA_PATH_METADATA = {
    'Omoju_Miller_MasterCV.pdf': {'path': 'Omoju_Miller_CV.pdf'},
}

# Used for share metadata (<meta description>, Open Graph, Twitter cards) on
# any page that is not a single article or page. SITEIMAGE is the fallback
# preview image; set it to a path under content/images and posts can override
# it with an "Image:" metadata line. Left empty, previews render as text-only
# summary cards rather than large-image ones.
SITEDESCRIPTION = (
    "I think about how people learn to build things, who gets to build them, "
    "and what we are actually making when we make software."
)
SITEIMAGE = "images/og-card.jpg"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = ()

# Social widget
SOCIAL = ()

DEFAULT_PAGINATION = 8

# Posts keep the date-first shape of the original blog: /2016/11/24/slug/
ARTICLE_URL = "{date:%Y}/{date:%m}/{date:%d}/{slug}/"
ARTICLE_SAVE_AS = "{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html"
DRAFT_URL = "drafts/{slug}/"
DRAFT_SAVE_AS = "drafts/{slug}/index.html"

# The CV page is the landing page (see content/pages/cv.md), so the article
# listing that normally lives at / moves to /blog.html.
# The landing page is content/pages/home.md, so there is no paginated index.
# /writing/ is the full year-grouped archive.
INDEX_SAVE_AS = ""
ARCHIVES_SAVE_AS = "writing/index.html"
ARCHIVES_URL = "writing/"

# Keep the old /pages/cv.html URL alive as a redirect to the new homepage.
TEMPLATE_PAGES = {
    "cv-redirect.html": "pages/cv.html",
    "about-redirect.html": "pages/about.html",
    "blog-redirect.html": "blog.html",
}
IGNORE_FILES = ["cv-redirect.html", "about-redirect.html", "blog-redirect.html"]

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True


# Cache-busting: the stylesheet URL carries a hash of its contents, so a deploy
# with changed CSS is picked up instead of served from a stale browser cache.
_css = _pathlib.Path(__file__).parent / "themes/minimalist/static/css/style.css"
CSS_VERSION = _hashlib.md5(_css.read_bytes()).hexdigest()[:8] if _css.exists() else "0"
