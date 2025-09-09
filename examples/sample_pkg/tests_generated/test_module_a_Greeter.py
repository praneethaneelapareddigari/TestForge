import pytest
from ..module_a import Greeter

def test_Greeter_smoke():
    greeter = Greeter()
    res = greeter.greet()  # call the method of the class
    assert res is not None
