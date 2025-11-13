"""
JII-MultispeQ-Protocols
"""

from pkgutil import iter_modules
from importlib import import_module, invalidate_caches
from importlib.metadata import version, PackageNotFoundError
import sys

import jii_multispeq_protocols
from jii_multispeq_protocols.validate import validate
from jii_multispeq_protocols.visualize import generate

try:
    __version__ = version("jii_multispeq_protocols")
except PackageNotFoundError:
    # package is not installed
    pass

# Make sure to expose __version__ at package level
__all__ = ['__version__']

# Not sure if this needs to be here...
invalidate_caches()

def import_package_recursive(base_module_name, target_namespace):
    try:
        protocol_pkg = import_module(base_module_name)
        
        # Iterate through all modules in protocol package
        for _, name, is_pkg in iter_modules(protocol_pkg.__path__):
            
            # Import each module/subpackage
            module_name = f'{base_module_name}.{name}'
            
            if module_name not in sys.modules:
                try:
                    module = import_module(module_name)
                except ImportError:
                    continue
            else:
                module = sys.modules[module_name]
            
            # Add the module to namespace
            setattr(target_namespace, name, module)
            
            # If it's a subpackage, recurse into it
            if is_pkg:
                import_package_recursive(module_name, target_namespace)
                
    except ImportError as e:
        print(f"Could not import {base_module_name}: {e}")

import_package_recursive('jii_multispeq_protocols.protocols', jii_multispeq_protocols)
