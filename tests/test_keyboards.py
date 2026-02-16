"""Tests for keyboard builders."""

from bot.utils.keyboards import (
    main_menu_keyboard,
    resources_keyboard,
    resources_total_pages,
    search_prompt_keyboard,
    start_keyboard,
)


class TestStartKeyboard:
    def test_has_one_row(self):
        kb = start_keyboard()
        assert len(kb) == 1

    def test_button_text(self):
        kb = start_keyboard()
        assert kb[0][0]["text"] == "Начать"
        assert kb[0][0]["callbackData"] == "start"


class TestMainMenu:
    def test_has_nine_buttons(self):
        kb = main_menu_keyboard()
        assert len(kb) == 9

    def test_first_button(self):
        kb = main_menu_keyboard()
        assert "Поиск сотрудников" in kb[0][0]["text"]

    def test_all_callbacks(self):
        kb = main_menu_keyboard()
        for row in kb:
            for btn in row:
                assert "callbackData" in btn


class TestResourcesKeyboard:
    def test_first_page(self):
        kb = resources_keyboard(1)
        total = resources_total_pages()
        has_next = any(
            btn.get("callbackData", "").startswith("resources:2")
            for row in kb
            for btn in row
        )
        has_prev = any(
            "Предыдущая" in btn.get("text", "")
            for row in kb
            for btn in row
        )
        if total > 1:
            assert has_next
        assert not has_prev

    def test_last_page(self):
        total = resources_total_pages()
        kb = resources_keyboard(total)
        has_next = any(
            "Следующая" in btn.get("text", "")
            for row in kb
            for btn in row
        )
        has_prev = any(
            "Предыдущая" in btn.get("text", "")
            for row in kb
            for btn in row
        )
        assert not has_next
        if total > 1:
            assert has_prev

    def test_middle_page(self):
        total = resources_total_pages()
        if total < 3:
            return  # not enough pages to test
        kb = resources_keyboard(2)
        texts = [btn.get("text", "") for row in kb for btn in row]
        assert any("Предыдущая" in t for t in texts)
        assert any("Следующая" in t for t in texts)

    def test_has_home_button(self):
        kb = resources_keyboard(1)
        last_row = kb[-1]
        assert any("Главное меню" in btn.get("text", "") for btn in last_row)

    def test_five_resources_per_page(self):
        kb = resources_keyboard(1)
        url_buttons = [
            btn
            for row in kb
            for btn in row
            if btn.get("type") == "url"
        ]
        assert len(url_buttons) == 5


class TestSearchPrompt:
    def test_has_home_button(self):
        kb = search_prompt_keyboard()
        assert len(kb) == 1
        assert "Главное меню" in kb[0][0]["text"]
