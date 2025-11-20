from jii_multispeq import measurement as _measurement
import gettext
import json
import matplotlib.pyplot as plt
import numpy as np
import os
import pkgutil
import pprint
import shutil
from string import Template
from tabulate import tabulate
import textwrap
import traceback
from importlib import import_module

import jii_multispeq_protocols.protocols
import jii_multispeq_protocols.validate as validate
import jii_multispeq_protocols.visualize as visualize
from jii_multispeq_protocols.visualize import JII_STYLES

PROTOCOL = """$header

.. automodule:: $package_name.$module_name
  :members:
  :undoc-members:
  :show-inheritance:
  :no-index:
  :no-title:

Basic Usage
-----------

.. code-block:: python
  :caption: *Example:* Import statement for the **$module_name** protocol

  ## Import $module_name
  from $package_name import $module_name as _$module_name

----

Sequence
--------
$flowchart

----

Details
-------
$protocol

----

Analysis
--------
$analysis
"""

PROTOCOL_FLOWCHART = """
.. mermaid::

$code
"""

PROTOCOL_DETAILS = """
$settings

Code
~~~~

.. code-block:: python
   :caption: $caption
   
$code

$validation
"""

PROTOCOL_SETTINGS = """
Settings
~~~~~~~~
$info

$settings

.. collapse:: Settings Code

   .. code-block:: python

$code
"""

PROTOCOL_ANALYSIS = """
$fn

$example
"""

PROTOCOL_FN = """
Usage
~~~~~

.. code-block:: python
  :caption: Analysis Example (requires ``JII-MultispeQ`` package)

  from jii_multispeq import measurement as _measurement
  from $package_name import $module_name as _$module_name

  ## Take a measurement using the MultispeQ
  data, crc32 = _measurement.measure(port="<Selected Port>", protocol=_$module_name, filename=None, notes="")

  ## The analyze function of JII-MultispeQ helps to provide the correct format
  output = _measurement.analyze( data, _$module_name._analyze )

  ## View Analysis output (as table)
  _measurement.view( output )

Function Details
~~~~~~~~~~~~~~~~

.. autofunction:: $package_name.$module_name._analyze
  :no-index:
"""

PROTOCOL_EXAMPLE = """
Example Data
~~~~~~~~~~~~

$table

$graphs
"""

PROTOCOL_GRAPH = """
.. plot::
   :caption: *Figure:* Recorded or calculated trace for $name.

   import matplotlib.pyplot as plt

   plt.style.use('default')

   fig, ax = plt.subplots(figsize=(10, 5))
   ax.plot($y_axis, linewidth=2, color=$color, label="$name")

   # Customize the plot
   ax.grid(True, linestyle='-', axis='y', alpha=0.3)
   ax.set_xlabel('Pulses', fontdict={"size": 15})
   ax.set_ylabel("a.u.", fontdict={"size": 15})
   for spine in ['top', 'right']:
     ax.spines[spine].set_visible(False)
  
   fig.patch.set_alpha(0)
   ax.patch.set_alpha(0)

   # Show Legend
   plt.legend()

   # Use a tight layout
   plt.tight_layout()

   # Show the plot
   plt.show()
"""

def generate_individual_module_rst():
  package = jii_multispeq_protocols.protocols
  package_name = package.__name__
  
  ## Clean up the individual protocol files
  dir_path = os.path.join( os.path.dirname(__file__), '..', 'protocols' )
  shutil.rmtree( dir_path, ignore_errors=True )
  os.makedirs( dir_path, exist_ok=True )

  import_package_recursive(package_name, package)


def import_package_recursive(base_module_name, target_namespace):
  
  try:
    protocol_pkg = import_module(base_module_name)
    
    # Iterate through all modules in protocol package
    for _, name, is_pkg in pkgutil.iter_modules(protocol_pkg.__path__):
      
      # Import each module/subpackage
      module_name = f'{base_module_name}.{name}'
      
      # If it's a subpackage, recurse into it
      if is_pkg:
        try:
          pkg_dir = os.path.join( os.path.dirname(__file__), '..', *protocol_pkg.__name__.split(".")[1:], name )
          os.makedirs( pkg_dir )
        except:
          pass
        import_package_recursive(module_name, target_namespace)
      else:
        module_rst(name, protocol_pkg.__name__, protocol_pkg) # package name
            
  except ImportError as e:
    print(f"Could not import {base_module_name}: {e}")


def module_rst(module_name, package_name, target_namespace):
  """
  Build a module page for individual protocols
  """

  ## Initial parameters for templates
  header = module_name
  formatted_code = ".. warning:: Protocol ``_protocol`` not found, check manually."
  flowchart = ".. note:: Flowchart could not be generated, missing ``_protocol``, check manually."
  validation_results = ""
  protocol_settings = ""
  protocol_fn = ".. note:: Analysis could not run, missing ``_analyze`` function, check manually."
  example = ".. note:: No MultispeQ output example found, missing ``_example``, check manually."
  code_caption = "Protocol Code"

  ## Extract header
  if hasattr( getattr(target_namespace, f"{module_name}"), "__doc__"):
    doc = getattr( getattr(target_namespace, f"{module_name}"), "__doc__").split('\n')

    for i in range(len(doc) - 1):
            
      if (doc[i].strip() and doc[i + 1] and 
        len(set(doc[i + 1].strip())) == 1 and 
        doc[i + 1].strip()[0] in '=-~^'):
          
        # Remove the heading
        header = doc[i].strip()
        break
  
  ## Get the protocol dictionary
  if hasattr( getattr(target_namespace, f"{module_name}"), "_protocol"):

    ## Get the protocol code
    protocol_code = getattr( getattr(target_namespace, f"{module_name}"), "_protocol")

    ## Validate protocol code
    if isinstance(protocol_code, (list, dict)):
      is_valid, errors = validate(protocol_code, False)
      
      if not is_valid:
        validation_results = "\n.. warning:: Protocol failed automated validation!\n\n"
        for error in errors:
          validation_results += "  + %s\n" % error

    ## Generate protocol flow chart
    if isinstance(protocol_code, (list, dict)):

      direction = "TD" if len(protocol_code[0].get("_protocol_set_", "")) > 1 else "LR"

      flowchart = Template(PROTOCOL_FLOWCHART).substitute(
        code = '\n'.join('   ' + line for line in visualize.generate(protocol_code, direction, JII_STYLES).splitlines())
      )

    ## Return protocol code block
    if isinstance(protocol_code, (list, dict)):
      formatted_code = pprint.pformat( protocol_code, width=80, indent=3 )
      formatted_code = textwrap.indent(formatted_code, '   ')

  ## Get protocol settings
  if hasattr( getattr(target_namespace, f"{module_name}"), "_settings"):
    settings = getattr( getattr(target_namespace, f"{module_name}"), "_settings")
    
    ## Info paragraph
    settings_info = "This protocol's settings expects **%s** %s.\n\n" % (len(settings), gettext.ngettext('parameter', 'parameters', len(settings)))
    
    ## Available Settings
    settings_list = []
    for key, value in settings.items():
      if "prompt" in value and "default" in value:
        str_prompt = value["prompt"]
        str_default = value["default"]
        settings_list.append( "**%s**\n  Replaces ``%s`` (default: %s)" % (str_prompt, key , str_default) )
      else:
        settings_list.append( "**Unknown Setting**\n  Please check and provide the correct setting including default value and prompt." )
    
      formatted_settings_code = json.dumps( settings, indent=2 )
      formatted_settings_code = textwrap.indent(formatted_settings_code, ' ' * 6)

    ## Settings Code
    protocol_settings = Template(PROTOCOL_SETTINGS).substitute(
      info = settings_info,
      settings = "\n".join(settings_list),
      code = formatted_settings_code
    )

  ## Get the analyze function for the protocol
  if hasattr( getattr(target_namespace, f"{module_name}"), "_analyze"):

    protocol_fn = Template(PROTOCOL_FN).substitute(
      package_name= package_name,
      module_name= module_name
    )

  ## Get the example data and generate analysis output
  if hasattr( getattr(target_namespace, f"{module_name}"), "_example"):
          
    _example = getattr( getattr(target_namespace, f"{module_name}"), "_example")

    _analyzed_data = {}
    table_content = []
    graphs_content = []

    ## Apply calculation function example data
    if hasattr( getattr(target_namespace, f"{module_name}"), "_analyze"):
      _analyze = getattr( getattr(target_namespace, f"{module_name}"), "_analyze")
    else:
      def _analyze( _data ):
        return {}

    try:
      _analyzed_data = _measurement.analyze(_example, _analyze )

      keys = sorted(_analyzed_data.keys(), key=str.lower)

      for key in keys:
        value = _analyzed_data[key]

        if value is None:
          table_content.append([key, 'N/A'])
        elif isinstance(value, ( str, float, int, bool )):
          table_content.append([key, value])
        elif isinstance(value, ( dict )):
          table_content.append([key, value])
        elif isinstance(value, (list, np.ndarray )) and key not in ["protocol", "settings", "order"] and isinstance(value[0], (float, int)):
          
          try:
            graph = Template(PROTOCOL_GRAPH).substitute(
              name = key,
              color = "(0, 0.37, 0.37)",
              y_axis = repr(value.tolist()) if isinstance(value, np.ndarray) else repr(value)
            )

            graphs_content.append(graph)

          except Exception as e:
            print(e)
            traceback.print_exc()
            pass

        else:
          table_content.append([key, value])      
    except Exception as e:
      print(e)
      traceback.print_exc()
      pass

    ## Add table and graphs to example
    if len(table_content) > 0:
      example = Template(PROTOCOL_EXAMPLE).substitute(
        table = tabulate(table_content, headers=['Parameter', 'Value'], tablefmt="rst"),
        graphs = "\n\n".join(graphs_content)
      )


  ## Generate Protocol Details
  protocol = Template(PROTOCOL_DETAILS).substitute(
    settings = protocol_settings,
    validation = validation_results,
    code = formatted_code,
    caption = code_caption
  )

  ## Generate Analysis Output
  analysis = Template(PROTOCOL_ANALYSIS).substitute(
    fn = protocol_fn,
    example = example
  )

  ## Add Generated Content to Template
  rst_content = Template(PROTOCOL).substitute(
    header= "%s\n%s" % (header, ('=' * len(header))),
    package_name = package_name,
    module_name = module_name,
    flowchart = flowchart,
    protocol = protocol,
    analysis = analysis
  )
  
  ## Write rst content to file
  with open( os.path.join( os.path.dirname(__file__), '..', *package_name.split(".")[1:], module_name+'.rst' ), 'w') as f:
    f.write(rst_content)
