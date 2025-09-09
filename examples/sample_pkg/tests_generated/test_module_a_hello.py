import pytest
from ..module_a import hello

def test_hello_smoke():
    res = hello()
    assert res is not None

