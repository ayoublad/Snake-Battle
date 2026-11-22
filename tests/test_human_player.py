import pytest

from game.directions import Direction
from game.human_player import HumanPlayer


def test_human_player_uses_player_id():
    player = HumanPlayer("Ayoub", player_id=0)

    assert player.name == "Ayoub"
    assert player.player_id == 0

def fake_input(monkeypatch, inputs: list):
    input_iter = iter(inputs)
    monkeypatch.setattr("builtins.input", lambda prompt="": next(input_iter))

@pytest.fixture
def player():
    return HumanPlayer(name="Ayoub", player_id=0)

@pytest.mark.parametrize("input_value, expected_direction", [
    ("z", Direction.UP),
    ("q", Direction.LEFT),
    ("s", Direction.DOWN),
    ("d", Direction.RIGHT)
])
def test_choose_direction_returns_correct_direction(monkeypatch, player, input_value, expected_direction):
    fake_input(monkeypatch, [input_value])
    assert player.choose_direction() == expected_direction

def test_uppercase_and_spaces_are_ignored(monkeypatch, player):
    fake_input(monkeypatch, ["  Z  "])
    assert player.choose_direction() == Direction.UP

def test_invalid_answer_then_valid_answer(monkeypatch, player):
    fake_input(monkeypatch, ["diagonale", "d"])
    assert player.choose_direction() == Direction.RIGHT
