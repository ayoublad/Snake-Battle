from game.directions import DIRECTIONS, next_cell

START_CELL = (3, 5)

def test_next_cell_in_the_right_direction():
    assert next_cell(START_CELL, DIRECTIONS["UP"]) == (3, 4)
    assert next_cell(START_CELL, DIRECTIONS["DOWN"]) == (3, 6)
    assert next_cell(START_CELL, DIRECTIONS["LEFT"]) == (2, 5)
    assert next_cell(START_CELL, DIRECTIONS["RIGHT"]) == (4, 5)

def test_next_cell_ignore_area_boundaries():
    assert next_cell((0, 0), DIRECTIONS["UP"]) == (0, -1)
    assert next_cell((0, 0), DIRECTIONS["LEFT"]) == (-1, 0)

def test_opposite_directions_cancel_out():
    after_up = next_cell(START_CELL, DIRECTIONS["UP"]) 
    assert next_cell(after_up, DIRECTIONS["DOWN"]) == START_CELL

def test_exactly_four_directions():
    assert set(DIRECTIONS.keys()) == {"UP", "DOWN", "LEFT", "RIGHT"}

def test_each_direction_moves_exactly_one_cell_without_diagonal():
    for name, (dx, dy) in DIRECTIONS.items():
        assert abs(dx) + abs(dy) == 1, f"Direction {name} is not a single-cell move"

def test_next_cell_returns_a_tuple():
    for direction in DIRECTIONS.values():
        result = next_cell(START_CELL, direction)
        assert isinstance(result, tuple), f"next_cell returned {result} which is not a tuple"
        assert result in {result}