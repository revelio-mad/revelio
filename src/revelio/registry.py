"""
The registry keeps track of all the classes that are registered, and can then be instantiated via a string name.

Classes must have namespace-wise unique names (case-insensitive) in order to be registered.
"""

from __future__ import annotations

__all__ = (
    "clear",
    "register",
    "get",
)


__revelio_registry__: dict[str, dict[str, type]] = {}


def clear(namespace: str | None = None) -> None:
    """
    Clears a namespace in the registry, or the entire registry if no namespace is given.

    Arguments:
        namespace: The namespace to clear. If None, the entire registry is cleared.

    Raises:
        TypeError: If the namespace is not a string, or None.
    """
    if namespace is None:
        __revelio_registry__.clear()
    elif isinstance(namespace, str):
        del __revelio_registry__[namespace]
    else:
        raise TypeError(f"Namespace must be a string or None, got {type(namespace).__name__}.")


def register(namespace: str, name: str, cls: type) -> None:
    """
    Registers a class with the given name under the given namespace.

    Arguments:
        namespace: The namespace to register the class under.
        name: The name to register the class with.
        cls: The class to register.

    Raises:
        TypeError: If the namespace or the name is not a string, or if the class is not a type.
        ValueError: If a class with the given name is already registered.
    """
    if not isinstance(namespace, str):
        raise TypeError(f"Namespace must be a string, got {type(namespace).__name__}.")
    if not isinstance(name, str):
        raise TypeError(f"Name must be a string, got {type(name).__name__}.")
    if not isinstance(cls, type):
        raise TypeError(f"Class must be a type, got {type(cls).__name__}.")
    name = _sanitize_name(name)
    namespace_registry = __revelio_registry__.get(namespace, {})
    if name in namespace_registry and namespace_registry[name] is not cls:
        raise ValueError(
            f"A class with the sanitized name '{name}' is already registered in the '{namespace}' namespace."
        )
    namespace_registry[name] = cls
    __revelio_registry__[namespace] = namespace_registry


def get(namespace: str, name: str) -> type:
    """
    Gets the class with the given name from the given namespace.

    Arguments:
        namespace: The namespace to get the class from.
        name: The name of the class to get.

    Returns:
        The class with the given name.

    Raises:
        TypeError: If the namespace or the name is not a string.
        KeyError: If no class with the given name is registered.
    """
    if not isinstance(namespace, str):
        raise TypeError(f"Namespace must be a string, got {type(namespace).__name__}.")
    if not isinstance(name, str):
        raise TypeError(f"Name must be a string, got {type(name).__name__}.")
    name = _sanitize_name(name)
    namespace_registry = __revelio_registry__.get(namespace, {})
    if name not in namespace_registry:
        raise KeyError(f"Could not find a class with the sanitized name '{name}' in the '{namespace}' namespace.")
    return namespace_registry[name]


def _sanitize_name(name: str) -> str:
    ignored_chars = (" ", "_", "-")
    return "".join(c for c in name if c not in ignored_chars).lower()
