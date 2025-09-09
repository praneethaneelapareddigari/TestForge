import pytest
from ..module_a import Greeter  # relative import from the package

def test_Greeter_smoke():
    greeter = Greeter()         # create an instance
    res = greeter.greet()       # call the greet() method
    assert res is not None       # simple smoke test

