"""
This file contains tests for revelio.mixins.configurable_mixin.ConfigurableMixin.
"""

from __future__ import annotations

from typing import TypeVar, Union

import pytest

from revelio.config.base import BaseConfig
from revelio.mixins.configurable_mixin import ConfigurableMixin


def test_init_baseconfig() -> None:
    """
    Test initialization with a valid configuration object that inherits from BaseConfig.
    """

    class MyConfig(BaseConfig):  # pylint: disable=missing-class-docstring
        param1: int
        param2: str

    class MyConfigurableClass(ConfigurableMixin[MyConfig]):  # pylint: disable=missing-class-docstring
        pass

    config = MyConfig(param1=1, param2="test")
    obj = MyConfigurableClass(config=config)
    assert obj.config == config
    assert obj.config.param1 == 1
    assert obj.config.param2 == "test"
    assert obj.config_class is MyConfig


def test_init_dict() -> None:
    """
    Test initialization with a valid configuration object that is a dict.
    """

    class MyConfigurableClass(ConfigurableMixin[dict]):  # pylint: disable=missing-class-docstring
        pass

    config = {"param1": 1, "param2": "test"}
    obj = MyConfigurableClass(config=config)
    assert obj.config == config
    assert obj.config["param1"] == 1
    assert obj.config["param2"] == "test"
    assert obj.config_class is dict


def test_init_none() -> None:
    """
    Test initialization with a valid configuration object that is None.
    """

    class MyConfigurableClass(ConfigurableMixin[None]):  # pylint: disable=missing-class-docstring
        pass

    obj = MyConfigurableClass()
    assert obj.config is None
    assert obj.config_class is type(None)


def test_init_without_config() -> None:
    """
    Test initialization with no configuration object, when one was expected.
    """

    class MyConfig(BaseConfig):  # pylint: disable=missing-class-docstring
        param1: int
        param2: str

    class MyConfigurableClass(ConfigurableMixin[MyConfig]):  # pylint: disable=missing-class-docstring
        pass

    with pytest.raises(TypeError):
        MyConfigurableClass()


def test_init_invalid_config() -> None:
    """
    Test initialization with an invalid config object.
    """

    class MyConfig(BaseConfig):  # pylint: disable=missing-class-docstring
        param1: int
        param2: str

    class MyConfigurableClass(ConfigurableMixin[MyConfig]):  # pylint: disable=missing-class-docstring
        pass

    with pytest.raises(TypeError):
        MyConfigurableClass(config="invalid")


def test_instantiation() -> None:
    """
    Test instantiation of ConfigurableMixin.
    """
    with pytest.raises(TypeError):
        ConfigurableMixin()


def test_without_type_argument() -> None:
    """
    Test that ConfigurableMixin cannot be used without a type argument.
    """
    with pytest.raises(TypeError):

        class InvalidConfigurableClass(ConfigurableMixin):  # pylint: disable=missing-class-docstring,unused-variable
            pass


def test_inheritance_with_unbound_type_argument() -> None:
    """
    Test that ConfigurableMixin cannot be used with an unbound type argument.
    """
    T = TypeVar("T", bound=Union[BaseConfig, None])

    with pytest.raises(TypeError):

        class GenericClass(ConfigurableMixin[T]):  # pylint: disable=missing-class-docstring
            pass

        class InvalidConfigurableClass(GenericClass):  # pylint: disable=missing-class-docstring
            pass

        InvalidConfigurableClass()
