"""Tests for state management."""

from bot.state import StateManager, UserState


class TestStateManager:
    def test_new_user_is_idle(self):
        sm = StateManager()
        session = sm.get("user1")
        assert session.state == UserState.IDLE

    def test_set_state(self):
        sm = StateManager()
        sm.set_state("user1", UserState.AUTHORIZED)
        assert sm.get("user1").state == UserState.AUTHORIZED

    def test_set_data(self):
        sm = StateManager()
        sm.set_data("user1", "page", 3)
        assert sm.get_data("user1", "page") == 3

    def test_get_data_default(self):
        sm = StateManager()
        assert sm.get_data("user1", "missing", "default") == "default"

    def test_reset(self):
        sm = StateManager()
        sm.set_state("user1", UserState.SEARCH_EMPLOYEE)
        sm.reset("user1")
        session = sm.get("user1")
        assert session.state == UserState.IDLE

    def test_independent_users(self):
        sm = StateManager()
        sm.set_state("user1", UserState.AUTHORIZED)
        sm.set_state("user2", UserState.SEARCH_EMPLOYEE)
        assert sm.get("user1").state == UserState.AUTHORIZED
        assert sm.get("user2").state == UserState.SEARCH_EMPLOYEE
