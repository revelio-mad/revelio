"""
The registry keeps track of all the classes that are registered, and can then be instantiated via a string name.

Classes must have globally unique names (case-insensitive) in order to be registered.
"""

from __future__ import annotations

__all__ = (
    "clear",
    "register",
    "get",
)


__revelio_registry__: dict[str, type] = {}


def clear() -> None:
    """
    Clears the registry.
    """
    __revelio_registry__.clear()


def register(name: str, cls: type) -> None:
    """
    Registers a class with the given name.

    Arguments:
        name: The name to register the class with.
        cls: The class to register.

    Raises:
        TypeError: If the name is not a string, or if the class is not a type.
        ValueError: If a class with the given name is already registered.
    """
    if not isinstance(name, str):
        raise TypeError(f"Name must be a string, got {type(name).__name__}.")
    if not isinstance(cls, type):
        raise TypeError(f"Class must be a type, got {type(cls).__name__}.")
    name = _sanitize_name(name)
    if name in __revelio_registry__ and __revelio_registry__[name] is not cls:
        raise ValueError(f"Class with sanitized name '{name}' already registered.")
    __revelio_registry__[name] = cls


def get(name: str) -> type:
    """
    Gets the class with the given name.

    Arguments:
        name: The name of the class to get.

    Returns:
        The class with the given name.

    Raises:
        TypeError: If the name is not a string.
        KeyError: If no class with the given name is registered.
    """
    if not isinstance(name, str):
        raise TypeError(f"Name must be a string, got {type(name).__name__}.")
    name = _sanitize_name(name)
    if name not in __revelio_registry__:
        raise KeyError(f"No class registered with sanitized name '{name}'.")
    return __revelio_registry__[name]


def _sanitize_name(name: str) -> str:
    ignored_chars = (" ", "_", "-")
    return "".join(c for c in name if c not in ignored_chars).lower()
