# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
import toml
from sphinx.ext.autodoc import ModuleDocumenter
import traceback

# from setuptools_scm import get_version
# from importlib.metadata import version as get_version

# sys.path.insert(0, os.path.abspath('../../src/jii_multispeq'))
# sys.path.insert(0, os.path.abspath('../../jii_multispeq_protocols'))
sys.path.insert(0, os.path.abspath('../..'))


# sys.path.append(os.path.abspath('.'))

config = toml.load("../../pyproject.toml")

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = config["tool"]["sphinx"]["project"]
copyright = "%Y - "  + config["tool"]["sphinx"]["copyright"]
author = config["tool"]["sphinx"]["author"]
# release = get_version(root=os.path.dirname(__file__), relative_to=__file__)
# release = get_version(root='../../', relative_to=__file__)
# release = get_version(root='./', relative_to=__file__)
# release = get_version("jii_multispeq")
release = "0.0.2"
version = ".".join(release.split('.')[:2])

# Open graph parameters
ogp_site_url = 'https://docs.example.org/'
ogp_image = "_static/images/jan-ingenhousz-institute-logo-header.webp"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
  "sphinx.ext.autodoc",
  'sphinx.ext.autosummary',
  'sphinx.ext.duration',
  "sphinx.ext.napoleon",
  "sphinx.ext.viewcode",
  "sphinx_toolbox.collapse",
  "sphinx_copybutton",
  "myst_parser",
  "matplotlib.sphinxext.plot_directive",
  "sphinxext.opengraph",
  "sphinxcontrib.mermaid"
]

templates_path = ["_templates"]
exclude_patterns = ["Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_title = "JII - MultispeQ Protocols"
html_short_title = "JII MQP"
html_logo = "_static/images/jan-ingenhousz-institute-logo.webp"
html_favicon = "_static/images/favicon.png"
html_theme_options = {
    # 'logo_only': True, # Not available for furo
    # 'display_version': True, # Not available for furo
}
html_css_files = [
  'css/custom.css',
]

plot_include_source = False
plot_html_show_source_link = False

html_static_path = ["_static"]
source_suffix = {
  ".rst": "restructuredtext", 
  ".md": "markdown"
}

# -- Options for autodoc -------------------------------------------------

autodoc_member_order = "bysource"
autodoc_special_members = "__init__"
autodoc_undoc_members = True
autodoc_exclude_members = "__weakref__"

add_module_names = False


# -- Pre-Build content generation ----------------------------------------
sys.path.insert(0, os.path.abspath('./scripts'))

# Import your scripts
import protocols
import protocol
import schema

def setup(app):
  """Set up the Sphinx extension."""
  # Register callback to run before builder initialization
  app.connect('config-inited', run_pre_build)

  app.connect('autodoc-process-docstring', process_docstring)
  
  # Register the custom option for modules
  ModuleDocumenter.option_spec['no-title'] = lambda x: True
  
  return {
      'version': '1.0',
      'parallel_read_safe': True,
      'parallel_write_safe': True,
  }

def run_pre_build(app, config):
  """Execute pre-build scripts."""
  # Run your scripts
  protocols.generate_module_rst()
  try:
    protocol.generate_individual_module_rst()
  except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()
  schema.schema_to_rst()


def process_docstring(app, what, name, obj, options, lines):
  if what == 'module' and 'no-title' in options:
    # Remove only the first heading found
    for i in range(len(lines) - 1):
      current_line = lines[i]
      next_line = lines[i + 1]
      
      if (current_line.strip() and next_line and 
        len(set(next_line.strip())) == 1 and 
        next_line.strip()[0] in '=-~^'):
        
        # Remove the heading
        lines.pop(i + 1)  # Remove underline
        lines.pop(i)      # Remove title
        
        # Clean up extra empty lines
        while i < len(lines) and not lines[i].strip():
          lines.pop(i)
        break