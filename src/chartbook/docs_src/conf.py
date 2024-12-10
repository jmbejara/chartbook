# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#

# Needed for sphinx-autodoc (but not autodoc2)
# sys.path.insert(0, os.path.abspath("../src/"))


# -- Project information -----------------------------------------------------

project = "ChartBook"
copyright = "2024, Jeremiah Bejarano"
author = "Jeremiah Bejarano"

# The full version, including alpha/beta/rc tags
release = "0.1"


# -- General configuration ---------------------------------------------------
external_toc_exclude_missing = True
# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    # "myst_parser",
    # "autodoc2",
    "sphinx.ext.intersphinx",
    # "numpydoc",
    "myst_nb",
    "ablog",
    "sphinx_design",
    "sphinx_copybutton",
    # "sphinxext.opengraph",
    # "sphinxext.rediraffe",
]

## Use autodoc2 to generate documentation from the source code
# Here are some reasons why: https://sphinx-autodoc2.readthedocs.io/en/latest/autodoc_diff.html
# autodoc2_packages = [
#     # "../src",
#     "../src/misc_tools.py",
# ]
# Use MyST by default for all docstrings
# https://sphinx-autodoc2.readthedocs.io/en/latest/quickstart.html#using-markdown-myst-docstrings
# autodoc2_render_plugin = "myst"

myst_enable_extensions = [
    "amsmath",
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "html_admonition",
    "html_image",
    "linkify",
    "replacements",
    "smartquotes",
    "strikethrough",
    "substitution",
    "tasklist",
]
myst_url_schemes = ["mailto", "http", "https"]
nb_execution_allow_errors = False
nb_execution_cache_path = ""
nb_execution_excludepatterns = []
nb_execution_in_temp = False
nb_execution_mode = "off"
nb_execution_timeout = 30
nb_output_stderr = "show"
numfig = True
pygments_style = "sphinx"
suppress_warnings = ["myst.domains"]
use_jupyterbook_latex = True
use_multitoc_numbering = True
comments_config = {"hypothesis": False, "utterances": False}
bibtex_bibfiles = ["../reports/bibliography.bib"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    "**.ipynb_checkpoints",
    ".DS_Store",
    "Thumbs.db",
    "_build",
]


## For including date and time in MyST
# https://myst-parser.readthedocs.io/en/latest/syntax/roles-and-directives.html#insert-the-date-and-reading-time
# today_fmt = '%b %d, %Y'
today_fmt = "%c"  # Locale’s appropriate date and time representation.


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = "sphinx_book_theme"
html_theme = "pydata_sphinx_theme"

# html_theme_options = {
#     "navigation_with_keys": True,
#     "search_bar_text": "Search this book...",
#     "launch_buttons": {
#         "notebook_interface": "classic",
#         "binderhub_url": "",
#         "jupyterhub_url": "",
#         "thebe": False,
#         "colab_url": "",
#     },
#     "path_to_docs": "docs_src",
#     "repository_url": "https://github.com/jmbejara/blank_project",
#     "repository_branch": "master",
#     "extra_footer": "",
#     "home_page_in_toc": True,
#     "announcement": "",
#     "analytics": {"google_analytics_id": ""},
#     "use_repository_button": True,
#     "use_edit_page_button": False,
#     "use_issues_button": True,
# }


html_theme_options = {
    "navigation_with_keys": True,
    "header_links_before_dropdown": 5,
    "icon_links": [
        # {
        #     "name": "Twitter",
        #     "url": "https://twitter.com/PyData",
        #     "icon": "fa-brands fa-twitter",
        # },
        # {
        #     "name": "GitHub",
        #     "url": "https://github.com/jmbejara/chartbook",
        #     "icon": "fa-brands fa-github",
        # },
        # {
        #     "name": "ChartBook Code Repo",
        #     "url": "https://github.com/jmbejara/chartbook",
        #     "icon": "fa-solid fa-code",
        # },
        # {
        #     "name": "Browse ChartBook Directories",
        #     "url": "https://github.com/jmbejara/chartbook",
        #     "icon": "fa-solid fa-folder-tree",
        # },
        # {
        #     "name": "PyData",
        #     "url": "https://pydata.org",
        #     "icon": "fa-custom fa-pydata",
        # },
    ],
    # alternative way to set twitter and github header icons
    # "github_url": "https://github.com/pydata/pydata-sphinx-theme",
    # "twitter_url": "https://twitter.com/PyData",
    "logo": {
        "text": "ChartBook",
        # "image_dark": "_static/logo-dark.svg",
    },
    "use_edit_page_button": False,
    "show_toc_level": 1,
    "navbar_align": "left",  # [left, content, right] For testing that the navbar items align properly
    # "show_nav_level": 2,
    "announcement": None,
    "show_version_warning_banner": False,
    "navbar_center": ["navbar-nav"],
    # "navbar_start": ["navbar-logo"],
    # "navbar_end": ["theme-switcher", "navbar-icon-links"],
    # "navbar_persistent": ["search-button"],
    # "primary_sidebar_end": ["custom-template", "sidebar-ethical-ads"],
    # "article_footer_items": ["test", "test"],
    # "content_footer_items": ["test", "test"],
    "footer_start": ["copyright"],
    "footer_center": ["sphinx-version"],
    "secondary_sidebar_items": {
        "**/*": ["page-toc", "sourcelink"],
        # "pipelines": ["page-toc", "sourcelink", ],
    },
    # "switcher": {
    #     "json_url": json_url,
    #     "version_match": version_match,
    # },
    # "back_to_top_button": False,
}


html_logo = "../assets/logo.svg"
html_favicon = "../assets/logo.svg"
html_title = "ChartBook"
html_sourcelink_suffix = ""
html_last_updated_fmt = "%c"  # to reveal the build date in the pages meta


# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

html_js_files = [
    "https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.4/require.min.js",
]

# -- Ablog options -----------------------------------------------------------
blog_path = "charts/index"
blog_post_pattern = [
    # "_notebook_build/*.ipynb",
    "charts/*.md",
]

# html_sidebars = {
#     "**": [
#         # sphinx book theme default html sidebar elements: https://sphinx-book-theme.readthedocs.io/en/stable/sections/sidebar-primary.html
#         "navbar-logo.html",
#         "icon-links.html",
#         "search-button-field.html",
#         "sbt-sidebar-nav.html",
#         # ablog html sidebar elements
#         # "ablog/postcard.html",
#         # "ablog/recentposts.html",
#         "ablog/categories.html",
#         "ablog/tagcloud.html",
#         # "ablog/archives.html",
#     ]
# }

html_sidebars = {
    # "community/index": [
    #     "sidebar-nav-bs",
    #     "custom-template",
    # ],  # This ensures we test for custom sidebars
    # "examples/no-sidebar": [],  # Test what page looks like with no sidebar items
    # "examples/persistent-search-field": ["search-field"],
    ## Blog sidebars
    # ref: https://ablog.readthedocs.io/manual/ablog-configuration-options/#blog-sidebars
    "charts/*": [
        "ablog/categories.html",
        "ablog/tagcloud.html",
        # "ablog/postcard.html",
        # "ablog/recentposts.html",
        # "ablog/authors.html",
        # "ablog/languages.html",
        # "ablog/locations.html",
        # "ablog/archives.html",
    ],
    "charts": [
        "ablog/categories.html",
        "ablog/tagcloud.html",
        # "ablog/postcard.html",
        # "ablog/recentposts.html",
        # "ablog/authors.html",
        # "ablog/languages.html",
        # "ablog/locations.html",
        # "ablog/archives.html",
    ],
    # "pipelines": [
    # ],
    # "index": [
    #     "navbar-logo.html",
    # ],
}
