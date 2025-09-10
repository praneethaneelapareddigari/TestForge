# Ensures "from module_a import ..." works during pytest collection
import os
import sys

# Points to: examples/sample_pkg
pkg_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

if pkg_dir not in sys.path:
    sys.path.insert(0, pkg_dir)