"""
Mixins for classes that can be configured using a type-checked configuration object.

Two mixins are available:
    ConfigurableMixin: for classes that can be configured using a single configuration object (e.g. a pipeline step).
    ConfigurableModelMixin: for models, that must be configured with two distinct configuration objects,
        one for the model's module, and the other for the model's trainer.
"""

from __future__ import annotations

from typing import Any, Generic, TypeVar, Union

from revelio.config.base import BaseConfig
from revelio.utils.hashing import hash_dict
from revelio.utils.typing import resolve_type_arguments

ConfigT = TypeVar("ConfigT", bound=Union[dict, BaseConfig, None])


class ConfigurableMixin(Generic[ConfigT]):
    """
    Mixin for classes that can be configured using a single configuration object (e.g. a pipeline step).

    If a class inherits this mixin, it must bind the ConfigT type argument to a dict, a subclass of BaseConfig, or None.
    The chosen type will be the type of the configuration object that the class expects to receive at initialization.
    If None is chosen, that means that the inheriting class is not configurable.

    Finally, this mixin provides a way of getting a hash of the configuration object, which can be used to
    uniquely identify the configuration of a class instance. This is useful for caching, for example.

    Attributes:
        config: The provided configuration object at initialization.
        config_hash: A hash of the configuration object.
        config_class: The type of the configuration object.
    """

    __revelio_config__: ConfigT
    __revelio_config_hash__: bytes
    __revelio_config_cls__: type[ConfigT]

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        type_args = resolve_type_arguments(ConfigurableMixin, cls)
        if len(type_args) != 1:
            raise TypeError(
                f"{cls.__name__} must inherit from ConfigurableMixin using a dict, a subclass of BaseConfig, or None."
            )
        tconfig_cls = type_args[0]
        if not isinstance(tconfig_cls, TypeVar) and issubclass(tconfig_cls, (dict, BaseConfig, type(None))):
            cls.__revelio_config_cls__ = tconfig_cls

    def __init__(self, *args: Any, config: ConfigT | None = None, **kwargs: Any) -> None:
        """
        Initializes a configurable object.

        This class cannot be instantiated directly, and must be inherited from.

        Arguments:
            config: The configuration object to use.

        Raises:
            TypeError: If the provided config object is not of the expected type specified by the generic type argument.
        """
        super().__init__(*args, **kwargs)
        # Being a mixin, we don't want users to be able to instantiate this class directly
        if type(self) is ConfigurableMixin:  # pylint: disable=unidiomatic-typecheck
            raise TypeError("ConfigurableMixin cannot be instantiated directly, and must be inherited from.")
        if not hasattr(self, "__revelio_config_cls__"):
            raise TypeError(
                f"{type(self).__name__} must inherit from ConfigurableMixin using "
                "a dict, a subclass of BaseConfig, or None."
            )
        if not isinstance(config, self.__revelio_config_cls__):
            raise TypeError(f"config must be of type {self.__revelio_config_cls__}")
        self.__revelio_config__ = config
        # Precompute the hash of the config object
        if isinstance(config, BaseConfig):
            config_dict = config.model_dump(mode="json")
        elif isinstance(config, dict):
            config_dict = config
        elif config is None:
            config_dict = {}
        else:
            raise TypeError("config must be of type dict, BaseConfig, or None")
        self.__revelio_config_hash__ = hash_dict(config_dict)

    @property
    def config(self) -> ConfigT:
        """
        The configuration object used to initialize the class instance.
        """
        return self.__revelio_config__

    @property
    def config_hash(self) -> bytes:
        """
        A hash of the configuration object used to initialize the class instance.
        """
        return self.__revelio_config_hash__

    @property
    def config_class(self) -> type[ConfigT]:
        """
        The type of the configuration object used to initialize the class instance.
        """
        return self.__revelio_config_cls__
