import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sample_pkg.module_a import Greeter

def test_greeter_hello():
    greeter = Greeter()
    assert greeter.hello() == "Hello"
