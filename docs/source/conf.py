# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import sys
import shutil
import importlib.util
import errno

from databricks import koalas
sys.path.insert(0, os.path.abspath('.'))

# Remove previously generated rst files. Ignore errors just in case it stops generating whole docs.
shutil.rmtree("%s/reference/api" % os.path.dirname(os.path.abspath(__file__)), ignore_errors=True)
try:
    os.mkdir("%s/reference/api" % os.path.dirname(os.path.abspath(__file__)))
except OSError as e:
    if e.errno != errno.EEXIST:
        raise


def gendoc():
    """Get releases from Github and generate reStructuredText files for release notes."""
    dev_dir = "%s/../../dev" % os.path.dirname(os.path.abspath(__file__))
    spec = importlib.util.spec_from_file_location("gendoc", "%s/gendoc.py" % dev_dir)
    gendoc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gendoc)
    gendoc.download_pandoc_if_needed(dev_dir)
    source_dir = os.path.dirname(os.path.abspath(__file__))
    gendoc.gen_release_notes(source_dir)


gendoc()


# -- Project information -----------------------------------------------------

project = 'Koalas'
copyright = '2019, Databricks'
author = 'The Koalas Team'

# The full version, including alpha/beta/rc tags
release = os.environ.get('RELEASE_VERSION', koalas.__version__)


# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
needs_sphinx = '1.2'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'numpydoc',  # handle NumPy documentation formatted docstrings. Needs to install
    'matplotlib.sphinxext.plot_directive',  # For visualize plot result
    'nbsphinx',  # Converts Jupyter Notebook to reStructuredText files for Sphinx.
    # For ipython directive in reStructuredText files.
    'IPython.sphinxext.ipython_console_highlighting',
]

# matplotlib plot directive
plot_include_source = True
plot_formats = [("png", 90)]
plot_html_show_formats = False
plot_html_show_source_link = False
plot_pre_code = """import numpy as np
import pandas as pd
import databricks.koalas as ks"""

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '**.ipynb_checkpoints']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# The master toctree document.
master_doc = 'index'

numpydoc_show_class_members = False

# -- Options for auto output -------------------------------------------------

autoclass_content = 'both'
autosummary_generate = True


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'nature_with_gtoc'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = []

# Add any paths that contain custom themes here, relative to this directory.
html_theme_path = ['themes']

# If false, no index is generated.
html_use_index = False

# If false, no module index is generated.
html_domain_indices = False


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ('index', 'databricks.koalas', u'databricks.koalas Documentation',
     [u'Author'], 1)
]
