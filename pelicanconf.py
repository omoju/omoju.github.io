AUTHOR = 'Omoju Miller'
SITENAME = 'Omoju Miller'
SITEURL = ""

PATH = "content"

TIMEZONE = 'America/Los_Angeles'

DEFAULT_LANG = 'en'

# Theme
THEME = 'themes/minimalist'

# Static files
STATIC_PATHS = ['images', 'themes/minimalist/static']

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
