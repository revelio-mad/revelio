"""
This file contains tests for the revelio.utils.hashing.hash_dict function.
"""

from __future__ import annotations

from revelio.utils.hashing import hash_dict


def test_empty_dict_hash() -> None:
    """
    Test that hash_dict returns the expected hash with an empty dictionary.
    """
    assert hash_dict({}).hex() == "bbe6a9f5a0146a1f4d0381e9b0ed1ac2f1a979ce9d5ad84e46ff0b58f36b5f46"


def test_dict_keys_ordering_invariance() -> None:
    """
    Test that hash_dict returns the same hash on dictionaries with the same keys, regardless of the keys' order.
    """
    assert hash_dict({"a": 1, "b": 2}) == hash_dict({"b": 2, "a": 1})
