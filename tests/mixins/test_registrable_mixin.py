"""
This file contains tests for revelio.mixins.configurable_mixin.RegistrableMixin.
"""

from __future__ import annotations

from typing import Generator

import pytest

from revelio import registry
from revelio.mixins.registrable_mixin import RegistrableMixin


@pytest.fixture(autouse=True)
def cleanup_registry() -> Generator:
    """
    A fixture that clears the registry before and after each test.
    """
    registry.clear()
    yield


def test_instantiation() -> None:
    """
    Test that RegistrableMixin cannot be instantiated directly.
    """
    with pytest.raises(TypeError):
        RegistrableMixin()


def test_find() -> None:
    """
    Test that RegistrableMixin.find finds the correct class under the correct namespace.
    """

    class MyBaseClass(RegistrableMixin, namespace="global"):  # pylint: disable=missing-class-docstring
        pass

    class MyClass1(MyBaseClass):  # pylint: disable=missing-class-docstring
        pass

    class MyOtherBaseClass(RegistrableMixin, namespace="other"):  # pylint: disable=missing-class-docstring
        pass

    class MyOtherClass1(MyOtherBaseClass):  # pylint: disable=missing-class-docstring
        pass

    assert MyBaseClass.find("MyClass1") is MyClass1
    assert MyBaseClass.find("myclass1") is MyClass1
    assert MyBaseClass.find("my-class1") is MyClass1
    assert MyBaseClass.find("my_class1") is MyClass1
    assert MyOtherBaseClass.find("MyOtherClass1") is MyOtherClass1
    assert MyOtherBaseClass.find("myotherclass1") is MyOtherClass1
    assert MyOtherBaseClass.find("my-other-class1") is MyOtherClass1
    assert MyOtherBaseClass.find("my_other_class1") is MyOtherClass1
    with pytest.raises(KeyError):
        MyBaseClass.find("MyOtherClass1")
    with pytest.raises(KeyError):
        MyOtherBaseClass.find("MyClass1")


def test_namespace_inheritance() -> None:
    """
    Test that RegistrableMixin inherits the namespace of its superclass according to the MRO.
    """

    class ClassA(RegistrableMixin, namespace="global"):  # pylint: disable=missing-class-docstring
        pass

    class ClassB(ClassA):  # pylint: disable=missing-class-docstring
        pass

    class ClassC(ClassA, namespace="other"):  # pylint: disable=missing-class-docstring
        pass

    class ClassD(ClassB, ClassC):  # pylint: disable=missing-class-docstring
        pass

    class ClassE(ClassC, ClassB):  # pylint: disable=missing-class-docstring
        pass

    assert ClassA.__revelio_namespace__ == "global"
    assert ClassB.__revelio_namespace__ == "global"
    assert ClassC.__revelio_namespace__ == "other"
    assert ClassD.__revelio_namespace__ == "global"
    assert ClassE.__revelio_namespace__ == "other"


def test_find_not_subclass() -> None:
    """
    Test that RegistrableMixin.find raises a TypeError when the found class is not a subclass
    of the class that called this method.
    """

    class MyBaseClass(RegistrableMixin, namespace="global"):  # pylint: disable=missing-class-docstring
        pass

    class MyClass1(MyBaseClass):  # pylint: disable=missing-class-docstring,unused-variable
        pass

    class MyOtherBaseClass(RegistrableMixin, namespace="global"):  # pylint: disable=missing-class-docstring
        pass

    class MyOtherClass1(MyOtherBaseClass):  # pylint: disable=missing-class-docstring,unused-variable
        pass

    with pytest.raises(TypeError):
        MyBaseClass.find("MyOtherClass1")

    with pytest.raises(TypeError):
        MyOtherBaseClass.find("MyClass1")


def test_instantiate() -> None:
    """
    Test that RegistrableMixin.instantiate instantiates the correct class.
    """

    class MyBaseClass(RegistrableMixin, namespace="global"):  # pylint: disable=missing-class-docstring
        pass

    class MyClass1(MyBaseClass):  # pylint: disable=missing-class-docstring
        def __init__(self, param1: int, *, param2: str) -> None:
            super().__init__()
            self.param1 = param1
            self.param2 = param2

    obj = MyBaseClass.instantiate("MyClass1", param1=1, param2="test")
    assert isinstance(obj, MyClass1)
    assert obj.param1 == 1
    assert obj.param2 == "test"

    obj = MyBaseClass.instantiate("myclass1", 1, param2="test")
    assert isinstance(obj, MyClass1)
    assert obj.param1 == 1
    assert obj.param2 == "test"
