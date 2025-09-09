import pytest
from ..module_a import add

def test_add_smoke():
    res = add()
    assert res is not None

