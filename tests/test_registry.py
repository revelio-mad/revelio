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
    Test that `register` registers a class with the given namespace and name, and `get` gets it back.
    """

    class MyClass:  # pylint: disable=missing-class-docstring
        pass

    registry.register("global", "MyClass", MyClass)
    assert registry.get("global", "MyClass") is MyClass
    assert registry.get("global", "myclass") is MyClass
    assert registry.get("global", "my-class") is MyClass
    assert registry.get("global", "my_class") is MyClass
    with pytest.raises(KeyError):
        registry.get("other", "MyClass")


def test_register_incorrect_types() -> None:
    """
    Test that `register` raises a TypeError when given incorrect types.
    """

    class MyClass:  # pylint: disable=missing-class-docstring
        pass

    with pytest.raises(TypeError):
        registry.register("global", "test", "fail")
    with pytest.raises(TypeError):
        registry.register("global", 0, MyClass)
    with pytest.raises(TypeError):
        registry.register(0, "test", MyClass)


def test_register_two_classes_same_namespace_same_name() -> None:
    """
    Test that `register` raises a ValueError when registering two classes with the same name under the same namespace.
    """

    class MyClass1:  # pylint: disable=missing-class-docstring
        pass

    class MyClass2:  # pylint: disable=missing-class-docstring
        pass

    registry.register("global", "MyClass", MyClass1)
    with pytest.raises(ValueError):
        registry.register("global", "MyClass", MyClass2)


def test_register_two_classes_different_namespace_same_name() -> None:
    """
    Test that `register` completes successfully when registering two classes with the same name
    under different namespaces.
    """

    class MyClass1:  # pylint: disable=missing-class-docstring
        pass

    class MyClass2:  # pylint: disable=missing-class-docstring
        pass

    registry.register("global", "MyClass", MyClass1)
    registry.register("other", "MyClass", MyClass2)
    assert registry.get("global", "MyClass") is MyClass1
    assert registry.get("other", "MyClass") is MyClass2


def test_get_incorrect_types() -> None:
    """
    Test that `get` raises a TypeError when given incorrect types.
    """
    with pytest.raises(TypeError):
        registry.get("global", 0)
    with pytest.raises(TypeError):
        registry.get(0, "test")


def test_get_not_existing() -> None:
    """
    Test that `get` raises a KeyError when given a name that does not exist.
    """
    with pytest.raises(KeyError):
        registry.get("global", "not_existing")


def test_clear() -> None:
    """
    Test that `clear` clears the registry or a single namespace.
    """

    class MyClass1:  # pylint: disable=missing-class-docstring
        pass

    class MyClass2:  # pylint: disable=missing-class-docstring
        pass

    registry.register("global", "MyClass", MyClass1)
    registry.register("other", "MyClass", MyClass2)
    assert registry.get("global", "MyClass") is MyClass1
    assert registry.get("other", "MyClass") is MyClass2
    registry.clear("global")
    with pytest.raises(KeyError):
        registry.get("global", "MyClass")
    assert registry.get("other", "MyClass") is MyClass2
    registry.register("global", "MyClass", MyClass1)
    registry.clear()
    with pytest.raises(KeyError):
        registry.get("global", "MyClass")
    with pytest.raises(KeyError):
        registry.get("other", "MyClass")
