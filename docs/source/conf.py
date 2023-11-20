import pathlib
import sys

# isort: off
sys.path.insert(0, str(pathlib.Path("..", "..").absolute()))

from recsys_metrics_polars import __version__  # noqa: E402
# isort: on


def autodoc_process_docstring(app, what, name, obj, options, lines):
    for i in range(len(lines)):
        lines[i] = lines[i].replace("np.", "numpy.").replace("pl.", "polars.")


def setup(app):
    app.connect("autodoc-process-docstring", autodoc_process_docstring)


def format_type_hints(annotation, config):
    if annotation.__module__ == "polars.dataframe.frame" and annotation.__name__ == "DataFrame":
        return ":external+polars:doc:`reference/dataframe/index`"
    return None


# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
project = "recsys-metrics-polars"
version = __version__
copyright = "2023, KernelA"
author = "KernelA"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.imgmath",
    "sphinx.ext.viewcode",
    "sphinx.ext.autosummary",
    "sphinx.ext.githubpages",
    "sphinx.ext.intersphinx",
    "sphinx_autodoc_typehints",
]

templates_path = ["_templates"]
exclude_patterns = ["_build"]

typehints_formatter = format_type_hints
autosummary_generate = True
autoclass_content = "both"
autodoc_typehints = "both"
imgmath_image_format = "svg"
autodoc_default_options = {"members": True, "member-order": "bysource", "undoc-members": True, "show-inheritance": True}

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "packaging": ("https://packaging.pypa.io/en/latest", None),
    "polars": ("https://pola-rs.github.io/polars/py-polars/html", None),
}
imgmath_latex = "xelatex"
imgmath_latex_args = ["-no-pdf"]
imgmath_latex_preamble = """\\usepackage{amsmath}"""

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
html_theme = "furo"
html_static_path = ["_static"]
