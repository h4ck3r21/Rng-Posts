"""Unit tests for tooch typing game."""
import touch_typing_game


def test_santize_removes_non_ascii():
    """Given a paragraph with non-ascii characters, should remove the character"""
    em_dash = "\N{EM DASH}"
    start_string = "hello there "
    end_string = " blah"
    assert touch_typing_game.sanitise_paragraph(
        start_string + em_dash + end_string) == start_string + end_string
