"""
This file contains tests for the revelio.utils.typing.resolve_type_arguments function.
"""

# pylint: disable=too-few-public-methods,missing-class-docstring
from __future__ import annotations

from typing import Generic, TypeVar

import pytest

from revelio.utils.typing import resolve_type_arguments


def test_self_not_generic() -> None:
    """
    Test that resolve_type_arguments returns an empty tuple when the type has no generic parameters
    and it is queried against itself.
    """

    class NoParams:
        pass

    assert resolve_type_arguments(NoParams, NoParams) == ()


def test_self_generic() -> None:
    """
    Test that resolve_type_arguments returns the type's generic parameters when queried against itself.
    """

    T = TypeVar("T")
    U = TypeVar("U")

    class GenericA(Generic[T, U]):
        pass

    assert resolve_type_arguments(GenericA, GenericA[int, str]) == (int, str)


def test_self_generic_with_different_typevars() -> None:
    """
    Test that resolve_type_arguments returns the type's generic parameters when queried against itself,
    even if the type variables are different.
    """

    T = TypeVar("T")
    U = TypeVar("U")

    X = TypeVar("X")
    Y = TypeVar("Y")

    class GenericA(Generic[T, U]):
        pass

    assert resolve_type_arguments(GenericA, GenericA[X, Y]) == (X, Y)


def test_nested_generics() -> None:
    """
    Test that resolve_type_arguments returns the type's generic parameters when queried against a complex type
    that contains nested generics.
    """

    T = TypeVar("T")
    U = TypeVar("U")
    Q = TypeVar("Q")
    R = TypeVar("R")

    class NoParams:
        pass

    class GenericA(Generic[T, U, Q, R]):
        pass

    class NestedA(Generic[T, U, Q]):
        pass

    class NestedB(Generic[T]):
        pass

    class GenericB(NoParams, NestedA[U, Q, U], GenericA[int, NestedA[Q, Q, Q], Q, U], NestedB[R]):
        pass

    assert resolve_type_arguments(GenericA, GenericB) == (int, NestedA[Q, Q, Q], Q, U)


def test_fully_bound_generics() -> None:
    pass


def test_unrelated_types_raises_exception() -> None:
    """
    Test that resolve_type_arguments raises a ValueError when the target type is not an instance of the query type.
    """

    T = TypeVar("T")
    U = TypeVar("U")
    Q = TypeVar("Q")
    R = TypeVar("R")

    class GenericA(Generic[T, U, Q, R]):
        pass

    class GenericB(Generic[T, U, Q, R]):
        pass

    with pytest.raises(ValueError):
        resolve_type_arguments(GenericA, GenericB)
