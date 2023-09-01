"""
This file contains tests for the revelio.registry module.
"""

from __future__ import annotations

from typing import Generator

import pytest

from revelio import registry


@pytest.fixture(autouse=True)
def cleanup_registry() -> Generator:
    """
    A fixture that clears the registry before and after each test.
    """
    registry.clear()
    yield


def test_register_get() -> None:
    """
    Test that `register` registers a class with the given name, and `get` gets it back.
    """

    class MyClass:  # pylint: disable=missing-class-docstring
        pass

    registry.register("MyClass", MyClass)
    assert registry.get("MyClass") is MyClass
    assert registry.get("myclass") is MyClass
    assert registry.get("my-class") is MyClass
    assert registry.get("my_class") is MyClass


def test_register_incorrect_types() -> None:
    """
    Test that `register` raises a TypeError when given incorrect types.
    """

    class MyClass:  # pylint: disable=missing-class-docstring
        pass

    with pytest.raises(TypeError):
        registry.register("test", "fail")

    with pytest.raises(TypeError):
        registry.register(0, MyClass)


def test_register_two_classes_same_name() -> None:
    """
    Test that `register` raises a ValueError when registering two classes with the same name.
    """

    class MyClass1:  # pylint: disable=missing-class-docstring
        pass

    class MyClass2:  # pylint: disable=missing-class-docstring
        pass

    registry.register("MyClass", MyClass1)
    with pytest.raises(ValueError):
        registry.register("MyClass", MyClass2)


def test_get_incorrect_types() -> None:
    """
    Test that `get` raises a TypeError when given incorrect types.
    """
    with pytest.raises(TypeError):
        registry.get(0)


def test_get_not_existing() -> None:
    """
    Test that `get` raises a KeyError when given a name that does not exist.
    """
    with pytest.raises(KeyError):
        registry.get("not_existing")


def test_clear() -> None:
    """
    Test that `clear` clears the registry.
    """

    class MyClass:  # pylint: disable=missing-class-docstring
        pass

    registry.register("MyClass", MyClass)
    assert registry.get("MyClass") is MyClass
    registry.clear()
    with pytest.raises(KeyError):
        registry.get("MyClass")
