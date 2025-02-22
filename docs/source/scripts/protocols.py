import os
import pkgutil
import shutil
import pprint
import jii_multispeq_protocols.protocols
import jii_multispeq_protocols.validate as validate

from string import Template

TOCTREE = f"""
.. toctree::
  :hidden:

  $elements
"""
  
MAIN = f"""MultispeQ Protocols
===================

.. automodule:: $package_name
  :members:
  :undoc-members:
  :show-inheritance:
"""

PROTOCOL = f"""
----

.. automodule:: $full_modname
  :members:
  :undoc-members:
  :show-inheritance:

.. rst-class:: inline-list

+ **Details:** :doc:`protocols/$module_name`
+ **Source:** `[view] <_modules/jii_multispeq_protocols/protocols/$module_name.html>`__
+ **Download:** :download:`$module_name.py <../../$package_name/$module_name.py>`
"""

def generate_module_rst():
  package = jii_multispeq_protocols.protocols
  package_name = package.__name__
  
  rst_toctree = []

  rst_content = Template(MAIN).substitute(
    package_name= package_name
  )
    
  for _, module_name, _ in pkgutil.iter_modules(package.__path__):

      full_modname = f"{package_name}.{module_name}"
      
      rst_content += Template(PROTOCOL).substitute(
        full_modname= full_modname,
        module_name= module_name,
        package_name= package_name.replace(".","/")
      )
      
      rst_toctree.append(f"protocols/{module_name}")

  rst_content += Template(TOCTREE).substitute(
    elements= "\n  ".join(rst_toctree)
  )

  path = os.path.join( os.path.dirname(__file__), '../protocols.rst' )
  if os.path.exists( path ):
    os.remove( path )
  with open( os.path.join( os.path.dirname(__file__), '../protocols.rst' ), 'w+') as f:
      f.write(rst_content)



PROTOCOL_DETAILS = """
.. automodule:: $package_name.$module_name
  :members:
  :undoc-members:
  :show-inheritance:
  :no-index:

.. rubric:: Import

.. code-block:: python
  :caption: *Example:* Import ``$module_name`` into a script

  import jii_multispeq_protocols.$module_name as _$module_name

.. rubric:: Protocol
$error_warning
$protocol_code

.. rubric:: Analysis Function
$fn
"""

PROTOCOL_FN = """
.. autofunction:: $package_name.$module_name._analyze
  :no-index:

.. code-block:: python
  :caption: Analysis Example (requires ``JII-MultispeQ`` package)

  from jii_multispeq import measurement

  ## Take a measurement using the MultispeQ
  data, crc32 = jii_multispeq.measure(port="<Selected Port>", protocol=_$module_name, filename=None, notes="")

  ## The analyze function of JII-MultispeQ helps to provide the correct format
  output = measurement.analyze( data, _$module_name._analzye )

  ## View Analysis output (as table)
  measurement.view( output )

"""


def generate_individual_module_rst():
  package = jii_multispeq_protocols.protocols
  package_name = package.__name__
  
  dir_path = os.path.join( os.path.dirname(__file__), '..', 'protocols' )

  if os.path.exists( dir_path ):
    shutil.rmtree( dir_path )  
  
  os.mkdir( dir_path )

  for _, module_name, _ in pkgutil.iter_modules(package.__path__):

    rst_content = ""
    error_warning = ""
    code = ""
    fn = ""
    
    if hasattr( getattr(jii_multispeq_protocols, f"{module_name}"), "_protocol"):

      protocol_code = getattr( getattr(jii_multispeq_protocols, f"{module_name}"), "_protocol")

      if isinstance(protocol_code, (list, dict)):
        is_valid, errors = validate(protocol_code, False)
        
        if not is_valid:
          error_warning = "\n.. warning:: Protocol failed automated validation!\n\n"
          for error in errors:
            error_warning += "  + %s\n" % error

      if isinstance(protocol_code, (str,list,dict)):

        code += ".. code-block:: python\n\n   "
        code += pprint.pformat( protocol_code, width=80  )
      
    else:
      code = ".. warning:: Protocol ``_protocol`` not found, check manually."

    if hasattr( getattr(jii_multispeq_protocols, f"{module_name}"), "_analyze"):

      fn = Template(PROTOCOL_FN).substitute(
        package_name= package_name,
        module_name= module_name
      )

    else:
      fn = "\n.. warning:: Function ``_analyze`` not found, check manually."
      
    ## Add content to template
    rst_content = Template(PROTOCOL_DETAILS).substitute(
      package_name= package_name,
      module_name= module_name,
      error_warning = error_warning,
      protocol_code= code,
      fn= fn
    )    
      
    with open( os.path.join( os.path.dirname(__file__), '..', 'protocols', module_name+'.rst' ), 'w') as f:
      f.write(rst_content)
