"""
This module contains utility functions related to typing.
"""

from __future__ import annotations

from typing import TypeVar, get_args, get_origin


def resolve_type_arguments(query_type: type, target_type: type) -> tuple[type | TypeVar, ...]:
    """
    Resolves the type arguments of the query type as supplied by the target type of any of its bases.

    Operates in a tail-recursive fashion, and drills through the hierarchy of generic base types
    breadth-first in left-to-right order to correctly identify the type arguments that need to be supplied
    to the next recursive call.

    Arguments:
        query_type: The type whose type arguments are to be resolved.
            Must be supplied without type arguments (e.g. Mapping, not Mapping[KT, VT]).
        target_type: The type whose type arguments are to be used to resolve the type arguments of the query type.
            Must be supplied with type arguments (e.g. Mapping[KT, VT], not Mapping).

    Returns:
        A tuple of the arguments given via target_type for the type parameters of for the query_type,
        if it has any parameters, otherwise an empty tuple. These arguments may themselves be TypeVars.

    Raises:
        TypeError: If the target type is not an instance of the query type.
    """

    # Taken from https://stackoverflow.com/a/69862817

    target_origin = get_origin(target_type)
    if target_origin is None:
        if target_type is query_type:
            return getattr(target_type, "__parameters__", ())
        else:
            target_origin = target_type
            supplied_args = None
    else:
        supplied_args = get_args(target_type)
        if target_origin is query_type:
            return supplied_args
    param_set = set()
    param_list = []
    for each_base in target_origin.__orig_bases__:  # type: ignore[union-attr]
        each_origin = get_origin(each_base)
        if each_origin is not None:
            for each_param in each_base.__parameters__:
                if each_param not in param_set:
                    param_set.add(each_param)
                    param_list.append(each_param)
            if issubclass(each_origin, query_type):
                if supplied_args is not None and len(supplied_args) > 0:
                    params_to_args = {key: value for (key, value) in zip(param_list, supplied_args)}
                    resolved_args = tuple(params_to_args[each] for each in each_base.__parameters__)
                    return resolve_type_arguments(query_type, each_base[resolved_args])
                else:
                    return resolve_type_arguments(query_type, each_base)
        elif issubclass(each_base, query_type):
            return resolve_type_arguments(query_type, each_base)
    if not issubclass(target_origin, query_type):
        raise ValueError(f"{target_type} is not a subclass of {query_type}")
    else:
        return ()
