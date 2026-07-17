# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
# 
# Configuration file for the ScanHub's Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import shutil
import sys

sys.path.insert(0, os.path.abspath(".."))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'services'))
sys.path.insert(0, basedir)

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'ScanHub'
copyright = 'David Schote, Christoph Dinh and Johannes Behrens'
author = 'David Schote, Christoph Dinh and Johannes Behrens'
release = '0.0.1'   # import this from scanhub package
version = '0.0.1'   # import this from scanhub package

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration


# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
source_suffix = {".rst": "restructuredtext", ".txt": "restructuredtext", ".md": "markdown"}

extensions = [
    'autoapi.extension',
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',  # support numpy and google style docstrings (at the moment only openapi)
    'sphinx.ext.todo',
    'sphinxcontrib.openapi',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.autosummary',
    'myst_parser',
    'sphinx_design',
]

autoclass_content = "class"
add_module_names = True
autosectionlabel_prefix_document = True
# Limit label generation to top-level page headings. Without this, every
# repeated "Parameters"/"Returns" heading emitted per-endpoint by the
# openapi:: directive collides with the others in the same document.
autosectionlabel_maxdepth = 2

suppress_warnings = [
    # introduction/demo.rst includes a README.md fragment that intentionally
    # starts at H3 (it's spliced under an existing RST title), not a real issue.
    'myst.header',
]


# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for AutoAPI -----------------------------------------------------

# AutoAPI names each generated page by walking up from a source file through
# consecutive directories that contain an __init__.py, stopping at the first
# one that doesn't - independent of which `autoapi_dirs` entry was configured.
# Several services all name their top-level package "app" (or "orchestrator" /
# "scanhub_libraries" are the exceptions), so scanning services/ directly makes
# AutoAPI collapse device-manager, protocol-manager, user-login-manager and
# patient-manager into a single "app" output tree, silently merging them.
#
# To keep each service's docs distinct, stage a copy of each service's package
# under a uniquely-named directory before AutoAPI scans it, and point AutoAPI
# at that staging directory instead of services/ directly.
_services_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'services'))
_autoapi_stage_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '_autoapi_src'))

_autoapi_sources = {
    'device_manager': os.path.join(_services_root, 'device-manager', 'app'),
    'protocol_manager': os.path.join(_services_root, 'protocol-manager', 'app'),
    'orchestration_engine': os.path.join(_services_root, 'orchestration-engine', 'orchestrator'),
    'user_login_manager': os.path.join(_services_root, 'user-login-manager', 'app'),
    'patient_manager': os.path.join(_services_root, 'patient-manager', 'app'),
    'shared_libraries': os.path.join(_services_root, 'base', 'shared_libs', 'src', 'scanhub_libraries'),
}

if os.path.isdir(_autoapi_stage_dir):
    shutil.rmtree(_autoapi_stage_dir)
os.makedirs(_autoapi_stage_dir)
for _alias, _source_path in _autoapi_sources.items():
    shutil.copytree(
        _source_path,
        os.path.join(_autoapi_stage_dir, _alias),
        ignore=shutil.ignore_patterns('__pycache__', '*.pyc'),
    )

autoapi_dirs = [_autoapi_stage_dir]

autoapi_ignore = [
    '*/.mypy_cache/*', '*/.ruff_cache/*', '*/__pycache__/*',
    '*/tests/*', '*/data_lake/*', '*/dist/*', '*/build/*',
]

autoapi_template_dir = '_templates/autoapi'
autoapi_add_toctree_entry = False

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.

html_theme = 'pydata_sphinx_theme'
html_show_sphinx = False
html_scaled_image_link = False
html_show_sourcelink = True
html_favicon = "_static/scanhub_favicon/favicon-32x32.png"

html_context = {
    "github_user": "scanhub-os",
    "github_repo": "scanhub",
    "github_version": "dev",
    "doc_path": "docs/",
    "conf_py_path": "/docs/",
    "VERSION": version,
}

html_sidebars = {
    "index": [],
    # "**": ["search-field", "sidebar-nav-bs"]
    "**": ["sidebar-nav-bs"],
}

html_theme_options = {
    "logo": {
        "image_light": "_static/images/logo.png",
        "image_dark": "_static/images/logo.png",
        "text": "ScanHub Documentation",
    },
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/brain-link/scanhub",
            "icon": "fa-brands fa-github",
        },
    ],
    "collapse_navigation": True,
    "navigation_depth": 1,
    "show_nav_level": 1,
    "show_toc_level": 2,
    "footer_start": ["copyright"],
    "footer_end": [],
    "navbar_align": "content",
    "header_links_before_dropdown": 4,
    "pygments_light_style": "default",
    "pygments_dark_style": "github-dark",
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static/css']
html_css_files = ["custom.css"]
html_title = "ScanHub Documentation"
