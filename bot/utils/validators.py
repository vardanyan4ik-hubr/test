"""Input validation utilities."""

from __future__ import annotations

import re
from dataclasses import dataclass


LAST_NAME_PATTERN = re.compile(r"^[а-яА-ЯёЁa-zA-Z\s\-]+$")
INN_PATTERN = re.compile(r"^\d+$")


@dataclass
class ValidationResult:
    ok: bool
    error_key: str = ""


def validate_last_name(raw: str) -> ValidationResult:
    """Validate a last name string.

    Rules:
      - strip whitespace
      - length 2..50 (after strip)
      - only letters, spaces, hyphens
    """
    name = raw.strip()

    if len(name) < 2:
        return ValidationResult(ok=False, error_key="validation_too_short")
    if len(name) > 50:
        return ValidationResult(ok=False, error_key="validation_too_long")
    if not LAST_NAME_PATTERN.match(name):
        return ValidationResult(ok=False, error_key="validation_invalid_chars")

    return ValidationResult(ok=True)


def validate_inn(raw: str) -> ValidationResult:
    """Validate an INN (taxpayer identification number).

    Rules:
      - strip whitespace
      - digits only
      - exactly 10 or 12 digits
    """
    inn = raw.strip()

    if not INN_PATTERN.match(inn):
        return ValidationResult(ok=False, error_key="validation_inn_digits")
    if len(inn) not in (10, 12):
        return ValidationResult(ok=False, error_key="validation_inn_length")

    return ValidationResult(ok=True)
