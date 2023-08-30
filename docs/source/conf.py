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
import sys

sys.path.insert(0, os.path.abspath(".."))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'services'))
# sys.path.insert(0, basedir)

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'ScanHub'
copyright = '2023, BRAIN-LINK UG (haftungsbeschraenkt)'
author = 'BRAIN-LINK UG (haftungsbeschraenkt)'
release = '0.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinxcontrib.openapi'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'pydata_sphinx_theme'
html_show_sphinx = False


html_theme_options = {
    "external_links": [
        {
            "url": "https://brain-link.de/",
            "name": "BRAIN-LINK"
        }
    ],
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/brain-link/scanhub",
            "icon": "fa-brands fa-github",
        },
        {
            "name": "LinkedIn",
            "url": "https://www.linkedin.com/company/brain-link/",
            "icon": "fa-brands fa-linkedin",
        },
    ],
    "collapse_navigation": True,
    "navigation_depth": 1,
    "show_toc_level": 1,
    "footer_start": ["copyright"],
    "navbar_align": "content",
}

# html_scaled_image_link = False
html_show_sourcelink = True
html_logo = "_static/logo_brainlink.svg"
# html_logo = "_static/logo_scaanhub.png"
html_sidebars = {
    "**": [
        "search-field",
        "sidebar-nav-bs"
    ]
}
pygments_style = "sphinx"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
