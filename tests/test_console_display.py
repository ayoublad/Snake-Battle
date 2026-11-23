import pytest
from game.console_display import ConsoleDisplay
from game.arena import Arena
from game.game import Game
from game.snake import Snake

@pytest.fixture
def game():
    arena = Arena(4, 3, [(3, 0)])
    snake_human = Snake((0, 0))
    snake_human.move_forward(destination=(1, 0), growth=True)
    snake_ai = Snake((3, 2))
    snake_ai.move_forward(destination=(2, 2), growth=True)
    game = Game(arena=arena, snake_human=snake_human, snake_ai=snake_ai, first_player=0, turn=5)
    return game

def test_situation_arena(game):
    display = ConsoleDisplay()
    assert display.render(game=game) == "hH.#\n....\n..Ii"

@pytest.mark.parametrize("case, expected_symbol", [
    ((1, 0), "H"),
    ((0, 0), "h"),
    ((2, 2), "I"),
    ((3, 2), "i"),
    ((3, 0), "#"),
    ((1, 1), ".")
])
def test_cell_symbol(game, case, expected_symbol):
    display = ConsoleDisplay()
    assert display.cell_symbol(game, cell=case) == expected_symbol

def test_dimensions_of_rendered_arena(game):
    display = ConsoleDisplay()
    rendered_arena = display.render(game=game)
    lines = rendered_arena.split("\n")
    assert len(lines) == game.arena.height
    for line in lines:
        assert len(line) == game.arena.width
    