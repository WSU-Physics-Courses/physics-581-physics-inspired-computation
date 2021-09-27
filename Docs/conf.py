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
import os.path

# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = "Physics 581: Physics Inspired Computational Techniques"
copyright = "2021, Michael McNeil Forbes"
author = "Michael McNeil Forbes"

# The full version, including alpha/beta/rc tags
release = "0.1"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "myst_nb",
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx.ext.ifconfig",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
    "sphinxcontrib.zopeext.autointerface",
    "matplotlib.sphinxext.plot_directive",
    "sphinxcontrib.bibtex",
    # From jupyterbook
    # "jupyter_book",
    # "sphinx_thebe",
    # "sphinx_comments",
    # "sphinx_external_toc",
    "sphinx_panels",
    "sphinx_book_theme",
    # "recommonmark",
]

source_suffix = {
    # '.ipynb': 'myst-nb',  # Ignore notebooks.
    ".myst": "myst-nb",
    ".md": "myst-nb",
}

# https://myst-parser.readthedocs.io/en/latest/using/syntax-optional.html
# https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#substitutions-with-jinja2
myst_enable_extensions = [
    "amsmath",
    "colon_fence",
    "deflist",
    "dollarmath",
    "html_admonition",
    "html_image",
    # "linkify",
    "replacements",
    "smartquotes",
    "substitution",
    # "tasklist",
]

# https://github.com/mcmtroffaes/sphinxcontrib-bibtex
# BibTeX files
bibtex_bibfiles = [
    # For now, macros.bib must be included in local.bib.  See:
    # https://github.com/mcmtroffaes/sphinxcontrib-bibtex/issues/261
    # Separate files can now be used for sphinxcontrib-bibtex>=2.4.0a0 but we will wait
    # for release before doing this here.
    # "macros.bib",
    "local.bib",
]

bibtex_reference_style = "author_year"

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# Cache notebook output to speed generation.
# https://myst-nb.readthedocs.io/en/latest/use/execute.html
jupyter_execute_notebooks = "cache"

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "alabaster"  # Default Sphinx theme
html_theme = "sphinx_book_theme"  # Theme for JupyterBook
html_logo = "_static/wsu-logo.svg"  # Needed for sidebars

html_theme_options = {
    "repository_url": "https://gitlab.com/wsu-courses/physics-581-physics-inspired-computation",
    "use_repository_button": True,
}

# Override version number in title... not relevant for docs.
html_title = project

# html_sidebars = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    "https://docs.python.org/": None,
    "matplotlib": ("https://matplotlib.org/stable/", None),
}

# Napoleon settings
napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True

######################################################################
# Variables with course information
course_package = "phys_581_2021"

myst_substitutions = {
    "instructor": "Michael McNeil Forbes [`m.forbes+581@wsu.edu`](mailto:m.forbes+581@wsu.edu)",
    "office": "947F Webster, (509) 335-6125",
    "office_hours": "MWF, 1pm - 2pm, Spark 223 (after class) or by appointment",
    "class_name": project,
    "class_homepage": "<https://schedules.wsu.edu/List/Pullman/20213/Phys/581/02>",
    "class_number": "[Phys. 581.02 Fall 2021, Pullman, Class Number 01665]"
    + "(https://www.catalog.wsu.edu/Pullman/Courses/ByList/PHYSICS/581)",
    "class_time": "MWF, 12:10pm - 1pm",
    "class_room": "Spark 223",
    "course_package": course_package,
    "Perusall": "[Perusall](https://app.perusall.com/courses/2021-fall-physics-581-pullm-1-02-01665-adv-topics-in-physics/)",
    "zoom_info": "Zoom Meeting: [957 9571 0263](https://wsu.zoom.us/j/95795710263.). "
    + "(Please use the Canvas link or as the instructor for the password.)",
    "Canvas": "[Canvas](https://wsu.instructure.com/courses/1488567)",
}

math_defs_filename = "_static/math_defs.tex"

html_context = {
    "mathjax_defines": "",
}


def config_inited_handler(app, config):
    """Insert contents of `math_defs_filename` into html_context['mathjax_defines']"""
    global math_defs_filename
    filename = os.path.join(
        "" if os.path.isabs(math_defs_filename) else app.confdir, math_defs_filename
    )

    defines = config.html_context.get("mathjax_defines", "").splitlines()
    try:
        with open(filename, "r") as _f:
            defines.extend(_f.readlines())
    except IOError:
        pass

    config.html_context["mathjax_defines"] = "\n".join(defines)


# Allows us to perform initialization before building the docs.  We use this to install
# the named kernel so we can keep the name in the notebooks.
def setup(app):
    app.connect("config-inited", config_inited_handler)
    import subprocess

    subprocess.check_call(["anaconda-project", "run", "init"])
    # Ignore .ipynb files
    app.registry.source_suffix.pop(".ipynb", None)
