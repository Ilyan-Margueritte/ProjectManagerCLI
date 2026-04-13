"""
Commands package.

We automatically import all modules in this directory so their COMMAND
definitions get registered.
"""

import os
import pkgutil
import importlib

# Automatically import all modules in this package so they register their commands
package_name = __name__

for _, module_name, _ in pkgutil.iter_modules([os.path.dirname(__file__)]):
    # This imports the module, which executes its top-level code (command registration)
    importlib.import_module(f"{package_name}.{module_name}")
