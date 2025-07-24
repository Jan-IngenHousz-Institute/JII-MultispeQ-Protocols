import os
import pkgutil
from string import Template

import jii_multispeq_protocols.protocols

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
  
  ## List to create a toc-tree
  rst_toctree = []

  ## Set up rst content
  rst_content = Template(MAIN).substitute(
    package_name= package_name
  )
  
  for _, module_name, _ in pkgutil.iter_modules(package.__path__):

      ## Get full module name aka protocol
      full_modname = f"{package_name}.{module_name}"
      
      ## Append protocol to rst content
      rst_content += Template(PROTOCOL).substitute(
        full_modname= full_modname,
        module_name= module_name,
        package_name= package_name.replace(".","/")
      )
      
      ## Append module name to toc-tree
      rst_toctree.append(f"protocols/{module_name}")

  ## Append toc-tree to rst file content
  rst_content += Template(TOCTREE).substitute(
    elements= "\n  ".join(rst_toctree)
  )

  ## Write out protocols.rst file
  with open( os.path.join( os.path.dirname(__file__), '../protocols.rst' ), 'w+') as f:
    f.write(rst_content)
