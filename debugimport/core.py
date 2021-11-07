"""
The main module with the function to import.
"""
import sys
import os
import importlib.util


def debug_import(module_name: str, path: str, is_debug: bool):
	"""
	Load a module from a path or import it normally.

	The importing module must have an `__init__.py` in a root directory 
	to create a module spec object.
	:param module_name: A name of a module.
	:param path: A path to module sources.
	:param is_debug: If `True` then load a module from the `path`
	otherwise import module normally by `module_name`.
	"""
	if module_name in sys.modules:
		module = sys.modules[module_name]
	elif is_debug:
		spec_path = os.path.join(path, module_name, '__init__.py')
		spec = importlib.util.spec_from_file_location(module_name, spec_path)
		module = importlib.util.module_from_spec(spec)
		sys.modules[module_name] = module
		spec.loader.exec_module(module)
	else:
		module = __import__(module_name)
	return module
