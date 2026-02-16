"""Tests for data loader."""

from bot.utils.data_loader import (
    clear_cache,
    load_employees,
    load_messages,
    load_resources,
    load_wifi,
)


class TestLoadMessages:
    def setup_method(self):
        clear_cache()

    def test_returns_dict(self):
        msgs = load_messages()
        assert isinstance(msgs, dict)

    def test_has_welcome(self):
        msgs = load_messages()
        assert "welcome" in msgs

    def test_has_main_menu(self):
        msgs = load_messages()
        assert "main_menu" in msgs


class TestLoadResources:
    def setup_method(self):
        clear_cache()

    def test_returns_list(self):
        res = load_resources()
        assert isinstance(res, list)

    def test_not_empty(self):
        res = load_resources()
        assert len(res) > 0

    def test_resource_has_fields(self):
        res = load_resources()
        for r in res:
            assert "title" in r
            assert "url" in r


class TestLoadEmployees:
    def setup_method(self):
        clear_cache()

    def test_returns_list(self):
        emp = load_employees()
        assert isinstance(emp, list)

    def test_not_empty(self):
        emp = load_employees()
        assert len(emp) > 0

    def test_employee_has_fields(self):
        emp = load_employees()
        for e in emp:
            assert "last_name" in e
            assert "first_name" in e
            assert "email" in e


class TestLoadWifi:
    def setup_method(self):
        clear_cache()

    def test_returns_dict(self):
        wifi = load_wifi()
        assert isinstance(wifi, dict)

    def test_has_password(self):
        wifi = load_wifi()
        assert "password" in wifi
        assert "network_name" in wifi
