import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sample_pkg.module_a import add

def test_add():
    assert add(2, 3) == 5
