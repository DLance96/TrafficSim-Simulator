import pytest


def func(x):
    return 3


def test_func():
    assert func(3) == 3
