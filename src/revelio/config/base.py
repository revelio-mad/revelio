"""
This module contains the base configuration class that all Revelio configuration elements must inherit from.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class BaseConfig(BaseModel):
    """
    This is the base class that all Revelio configuration elements must inherit from.
    """

    model_config = ConfigDict(frozen=True)
