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

# Get protocol package
protocol_pkg = import_module('jii_multispeq_protocols.protocols')

# Iterate through all modules in protocol package
for loader, name, is_pkg in iter_modules(protocol_pkg.__path__):
    
    # Import each module
    module_name = f'jii_multispeq_protocols.protocols.{name}'

    if module_name not in sys.modules:
        # Import module only if not already imported
        module = import_module(module_name)
    else:
        # Use existing module if already imported
        module = sys.modules[module_name]
    
    # Add the module to jii_multispeq_protocols namespace
    setattr(jii_multispeq_protocols, name, module)
