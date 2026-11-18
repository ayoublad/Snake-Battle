from game.directions import Direction, next_cell

START_CELL = (3, 5)

def test_next_cell_in_the_right_direction():
    assert next_cell(START_CELL, Direction.UP) == (3, 4)
    assert next_cell(START_CELL, Direction.DOWN) == (3, 6)
    assert next_cell(START_CELL, Direction.LEFT) == (2, 5)
    assert next_cell(START_CELL, Direction.RIGHT) == (4, 5)

def test_next_cell_ignore_area_boundaries():
    assert next_cell((0, 0), Direction.UP) == (0, -1)
    assert next_cell((0, 0), Direction.LEFT) == (-1, 0)

def test_opposite_directions_cancel_out():
    after_up = next_cell(START_CELL, Direction.UP) 
    assert next_cell(after_up, Direction.DOWN) == START_CELL
    after_left = next_cell(START_CELL, Direction.LEFT)
    assert next_cell(after_left, Direction.RIGHT) == START_CELL

def test_exactly_four_directions():
    assert set(Direction.__members__.keys()) == {"UP", "DOWN", "LEFT", "RIGHT"}

def test_each_direction_moves_exactly_one_cell_without_diagonal():
    for direction in Direction:
        dx, dy = direction.value
        assert abs(dx) + abs(dy) == 1, f"Direction {direction.name} is not a single-cell move"

def test_next_cell_returns_a_tuple():
    for direction in Direction:
        result = next_cell(START_CELL, direction)
        assert isinstance(result, tuple), f"next_cell returned {result} which is not a tuple"
        assert result in {result}