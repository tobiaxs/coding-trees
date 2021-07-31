"""Configuration file for the Sphinx documentation builder."""


# -- Project information -----------------------------------------------------

import sys
from pathlib import Path

project = "Coding Trees"
copyright = "2021, tobias"
author = "tobias"

current_dir = Path(__file__).parent.absolute()
base_dir = current_dir.parents[1]
code_dir = base_dir / "server"

sys.path.insert(0, str(code_dir))

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.coverage",
    "sphinx.ext.napoleon",
    "autoapi.extension",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
source_suffix = [".rst"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = "alabaster"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# Include only folder with Django app.
autoapi_dirs = [code_dir]

# Ignore migrations and tests.
autoapi_ignore = ["*/migration*.py", "*/test_*.py"]
