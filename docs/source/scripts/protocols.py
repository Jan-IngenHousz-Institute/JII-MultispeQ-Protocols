import os
import pkgutil
from string import Template
from importlib import import_module

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
.. automodule:: $full_modname
  :members:
  :undoc-members:
  :show-inheritance:

.. rst-class:: inline-list

+ **Details:** :doc:`protocols/$module_path`
+ **Source:** `[view] <_modules/jii_multispeq_protocols/protocols/$module_path.html>`__
+ **Download:** :download:`$module_name.py <../../$package_path/$module_name.py>`
"""

SUBMODULE_HEADER = f"""

$package_display_name
$underline

.. automodule:: $package_module_name
  :members:
  :undoc-members:
  :show-inheritance:
"""

def process_package_recursive(base_module_name, main_modules, submodules_dict, rst_toctree, package_path="", is_root=True):
    try:
        package = import_module(base_module_name)
        
        # Iterate through all modules in the package
        for _, module_name, is_pkg in pkgutil.iter_modules(package.__path__):
            
            # Get full module name
            full_modname = f"{base_module_name}.{module_name}"
            
            # Create paths for different uses
            if package_path:
                module_path = f"{package_path}/{module_name}"
                toctree_path = f"protocols/{package_path}/{module_name}"
            else:
                module_path = module_name
                toctree_path = f"protocols/{module_name}"
            
            # Only add to RST content if it's not a package (i.e., it's a module)
            if not is_pkg:
                protocol_content = Template(PROTOCOL).substitute(
                    full_modname=full_modname,
                    module_name=module_name,
                    module_path=module_path,
                    package_path=base_module_name.replace(".", "/")
                )
                
                if is_root:
                    # Main package modules
                    main_modules.append(protocol_content)
                else:
                    # Subpackage modules - group by package
                    package_display_name = package_path.replace("/", " > ").title()
                    if package_display_name not in submodules_dict:
                        submodules_dict[package_display_name] = {
                            'package_module_name': f"{base_module_name}",
                            'modules': []
                        }
                    submodules_dict[package_display_name]['modules'].append(protocol_content)
                
                # Append module name to toc-tree
                rst_toctree.append(toctree_path)
            
            # If it's a package, recurse into it
            if is_pkg:
                new_package_path = f"{package_path}/{module_name}" if package_path else module_name
                process_package_recursive(full_modname, main_modules, submodules_dict, rst_toctree, new_package_path, False)
                
    except ImportError as e:
        print(f"Could not import {base_module_name}: {e}")

def generate_module_rst():
    package = jii_multispeq_protocols.protocols
    package_name = package.__name__
    
    ## List to create a toc-tree
    rst_toctree = []
    
    ## Lists to separate main modules from submodules
    main_modules = []
    submodules_dict = {}  # Dict to group submodules by package
    
    ## Set up rst content
    rst_content = Template(MAIN).substitute(package_name=package_name)
    
    # Process the main package and all subpackages recursively
    process_package_recursive(package_name, main_modules, submodules_dict, rst_toctree)
    
    # Add main modules first
    rst_content += "\n\n----\n\n".join(main_modules)
    
    # Add submodules grouped by package with headers
    for package_display_name, package_info in submodules_dict.items():
        # Create underline the same length as the header
        underline = "=" * len(package_display_name)
        
        rst_content += Template(SUBMODULE_HEADER).substitute(
            package_display_name=package_display_name,
            underline=underline,
            package_module_name=package_info['package_module_name']
        )
        
        rst_content += "\n\n----\n\n".join(package_info['modules'])
    
    ## Append toc-tree to rst file content
    rst_content += Template(TOCTREE).substitute(
        elements="\n  ".join(rst_toctree)
    )
    
    ## Write out protocols.rst file
    with open(os.path.join(os.path.dirname(__file__), '../protocols.rst'), 'w+') as f:
        f.write(rst_content)