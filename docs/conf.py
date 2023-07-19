import os
import sys

# Add all directories that contain Python files to the Python path
sys.path.extend([
    os.path.abspath('../services/acquisition-control'),
    os.path.abspath('../services/device-manager'),
    os.path.abspath('../services/exam-manager'),
    os.path.abspath('../services/mri'),
    os.path.abspath('../services/workflow-manager'),
    os.path.abspath('../services/acquisition-control/app'),
    os.path.abspath('../services/device-manager/app'),
    os.path.abspath('../services/device-manager/app/api'),
    os.path.abspath('../services/device-manager/app/data_lake'),
    os.path.abspath('../services/exam-manager/app'),
    os.path.abspath('../services/exam-manager/app/api'),
    os.path.abspath('../services/exam-manager/app/data_lake'),
    os.path.abspath('../services/mri/recos'),
    os.path.abspath('../services/mri/sequence-manager'),
    os.path.abspath('../services/mri/recos/cartesian-reco-service'),
    os.path.abspath('../services/mri/recos/cartesian-reco-service/app'),
    os.path.abspath('../services/mri/recos/cartesian-reco-service/app/data_lake'),
    os.path.abspath('../services/mri/sequence-manager/app'),
    os.path.abspath('../services/mri/sequence-manager/tests'),
    os.path.abspath('../services/mri/sequence-manager/app/core'),
    os.path.abspath('../services/mri/sequence-manager/app/database'),
    os.path.abspath('../services/mri/sequence-manager/app/endpoints'),
    os.path.abspath('../services/mri/sequence-manager/app/services'),
    os.path.abspath('../services/workflow-manager/app'),
    os.path.abspath('../services/workflow-manager/app/api'),
    os.path.abspath('../services/workflow-manager/app/data_lake'),
])

# -- Project information -----------------------------------------------------

project = 'ScanHub API Documentation'
copyright = '2023, BRAIN-LINK UG'
author = 'Authors of ScanHub'

# The full version, including alpha/beta/rc tags
release = '1.0.0'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
