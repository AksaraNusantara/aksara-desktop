"""
===============================================================================

Aksara Nusantara

Module:
    core.exceptions

Module Type:
    Foundation Module

Purpose:
    Defines the exception hierarchy used by the Aksara Nusantara Core Engine.

Supports:
    AN-STD-001
    Section 14 - Script Validation

References:
    docs/standards/SCRIPTPACK_INTERFACE_SPECIFICATION.md
    docs/development/TRACEABILITY.md

Copyright (c) Aksara Nusantara Project

SPDX-License-Identifier: GPL-3.0-or-later

Support Module:
    Core Exception Hierarchy
===============================================================================
"""

class CoreEngineError(Exception):
    """
    Base exception for all Core Engine related errors.
    """
    pass


class ValidationError(CoreEngineError):
    """
    Raised when a ScriptPack fails validation.
    """
    pass


class RegistryError(CoreEngineError):
    """
    Raised when a ScriptPack registry operation fails.
    """
    pass


class LoaderError(CoreEngineError):
    """
    Raised when loading a ScriptPack fails.
    """
    pass


class EngineError(CoreEngineError):
    """
    Raised when the Core Engine encounters an unrecoverable error.
    """
    pass


class TransliterationError(EngineError):
    """
    Raised when a transliteration request cannot be dispatched, for example
    when no ScriptPack is selected or the ScriptPack does not provide
    transliteration support.
    """
    pass


class AudioServiceError(CoreEngineError):
    """
    Raised when an audio service operation fails.
    """
    pass