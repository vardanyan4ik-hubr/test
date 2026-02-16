"""Tests for input validators."""

import pytest

from bot.utils.validators import validate_inn, validate_last_name


class TestValidateLastName:
    def test_valid_simple(self):
        result = validate_last_name("Иванов")
        assert result.ok is True

    def test_valid_with_hyphen(self):
        result = validate_last_name("Салтыков-Щедрин")
        assert result.ok is True

    def test_valid_with_spaces_stripped(self):
        result = validate_last_name("  Иванов  ")
        assert result.ok is True

    def test_valid_latin(self):
        result = validate_last_name("Smith")
        assert result.ok is True

    def test_valid_two_chars(self):
        result = validate_last_name("Ли")
        assert result.ok is True

    def test_valid_fifty_chars(self):
        result = validate_last_name("А" * 50)
        assert result.ok is True

    def test_too_short_empty(self):
        result = validate_last_name("")
        assert result.ok is False
        assert result.error_key == "validation_too_short"

    def test_too_short_one_char(self):
        result = validate_last_name("И")
        assert result.ok is False
        assert result.error_key == "validation_too_short"

    def test_too_short_spaces_only(self):
        result = validate_last_name("   ")
        assert result.ok is False
        assert result.error_key == "validation_too_short"

    def test_too_long(self):
        result = validate_last_name("А" * 51)
        assert result.ok is False
        assert result.error_key == "validation_too_long"

    def test_invalid_chars_digits(self):
        result = validate_last_name("Иванов123")
        assert result.ok is False
        assert result.error_key == "validation_invalid_chars"

    def test_invalid_chars_special(self):
        result = validate_last_name("Иванов@!")
        assert result.ok is False
        assert result.error_key == "validation_invalid_chars"

    def test_invalid_chars_underscore(self):
        result = validate_last_name("Иванов_ов")
        assert result.ok is False
        assert result.error_key == "validation_invalid_chars"


class TestValidateInn:
    def test_valid_10_digits(self):
        result = validate_inn("7707083893")
        assert result.ok is True

    def test_valid_12_digits(self):
        result = validate_inn("770708389312")
        assert result.ok is True

    def test_valid_stripped(self):
        result = validate_inn("  7707083893  ")
        assert result.ok is True

    def test_not_digits(self):
        result = validate_inn("77070abc93")
        assert result.ok is False
        assert result.error_key == "validation_inn_digits"

    def test_wrong_length_9(self):
        result = validate_inn("770708389")
        assert result.ok is False
        assert result.error_key == "validation_inn_length"

    def test_wrong_length_11(self):
        result = validate_inn("77070838931")
        assert result.ok is False
        assert result.error_key == "validation_inn_length"

    def test_empty(self):
        result = validate_inn("")
        assert result.ok is False
        assert result.error_key == "validation_inn_digits"
