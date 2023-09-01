"""
This module contains utility functions related to efficiently hashing dictionaries.
"""

from __future__ import annotations

from typing import Any, Mapping

import blake3
import msgpack


def hash_dict(dictionary: Mapping[str, Any]) -> bytes:
    """
    Deterministically hashes a serializable dictionary.

    The ordering of the keys inside the dictionary does not affect the resulting hash.

    Arguments:
        dictionary: The dictionary to hash.

    Returns:
        A byte sequence representing the hash of the dictionary.

    Raises:
        TypeError: If the dictionary is not serializable.
    """

    sorted_dict = {key: dictionary[key] for key in sorted(dictionary.keys())}
    packed = msgpack.packb(sorted_dict, use_bin_type=True)
    return blake3.blake3(packed).digest()  # pylint: disable=not-callable
