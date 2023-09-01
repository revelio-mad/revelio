"""
Mixin for classes that can be registered and instantiated via a string name.
"""

from __future__ import annotations

from typing import Any, TypeVar

from revelio import registry

RegistrableT_co = TypeVar("RegistrableT_co", bound="RegistrableMixin", covariant=True)


class RegistrableMixin:
    """
    Mixin for classes that can be registered and instantiated via a string name.

    If a class inherits this mixin, it will be registered using the class name, and it must be instantiable.
    Also, its name must be globally unique (case-insensitive).

    Finally, this mixin provides a way of finding and instantiating a class with a given case-insensitive name.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Initializes a registrable object.

        This class cannot be instantiated directly, and must be inherited from.

        Raises:
            TypeError: If the class that called this method is RegistrableMixin itself.
        """
        super().__init__(*args, **kwargs)
        # Being a mixin, we don't want users to be able to instantiate this class directly
        if type(self) is RegistrableMixin:  # pylint: disable=unidiomatic-typecheck
            raise TypeError("ConfigurableMixin cannot be instantiated directly, and must be inherited from.")

    def __init_subclass__(cls) -> None:
        registry.register(cls.__name__, cls)

    @classmethod
    def find(cls: type[RegistrableT_co], name: str) -> type[RegistrableT_co]:
        """
        Finds a class with the given name.

        Arguments:
            name: The name of the class to find.

        Returns:
            The class with the given name.

        Raises:
            KeyError: If no class with the given name is registered.
            TypeError: If the class with the given name is not a subclass of the class that called this method.
        """
        found = registry.get(name)
        if not issubclass(found, cls):
            raise TypeError(f"Class with name '{name}' is not a subclass of {cls.__name__}.")
        return found

    @classmethod
    def instantiate(cls: type[RegistrableT_co], name: str, *args: Any, **kwargs: Any) -> RegistrableT_co:
        """
        Instantiates a class with the given name. All extra arguments will be passed to the class constructor.

        Arguments:
            name: The name of the class to instantiate.

        Returns:
            The instantiated class.

        Raises:
            KeyError: If no class with the given name is registered.
            TypeError: If the class with the given name is not a subclass of the class that called this method.
        """
        found = cls.find(name)
        return found(*args, **kwargs)
