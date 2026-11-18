from random import seed
import pytest
from game.arena import generate_arena   
from game.directions import DIRECTIONS, next_cell 

def check_arena(arena, width, height, density):
    assert arena.width == width
    assert arena.height == height
    assert len(arena.walls) == int(width * height * density)

    for wall in arena.walls:
        assert arena.is_inside(wall)

    assert not arena.is_wall((2, height // 2)) 
    assert not arena.is_wall((width - 3, height // 2))

    neighbor_cells_for_human = set()
    neighbor_cells_for_ai = set()

    for directions in DIRECTIONS.values():
        neighbor_cells_for_human.add(next_cell((2, height // 2), directions))
        neighbor_cells_for_ai.add(next_cell((width - 3, height // 2), directions))

    for cell_human in neighbor_cells_for_human:
        assert not arena.is_wall(cell_human)

    for cell_ai in neighbor_cells_for_ai:
        assert not arena.is_wall(cell_ai)

    set_visited = arena.reachable_cells((2, height // 2))
    assert (width - 3, height // 2) in set_visited

@pytest.mark.parametrize("width, height, density", [
    (15, 10, 0.15),
    (10, 11, 0.25),
    (20, 20, 0.20),
    (17, 13, 0.18),
    (10, 15, 0.18)
])
@pytest.mark.parametrize("random_seed", range(100))
def test_generate_arena(width, height, density, random_seed):
    seed(random_seed)
    arena = generate_arena(width, height, density, 1000)
    check_arena(arena, width, height, density)

def test_invalid_width():
    with pytest.raises(ValueError):
        generate_arena(9, 10, 0.2)

def test_invalid_height():
    with pytest.raises(ValueError):
        generate_arena(10, 9, 0.2)

def test_invalid_density_low():
    with pytest.raises(ValueError):
        generate_arena(10, 10, 0.1)

def test_invalid_density_high():
    with pytest.raises(ValueError):
        generate_arena(10, 10, 0.3)

def test_zero_max_attempts():
    with pytest.raises(RuntimeError):
        generate_arena(10, 10, 0.2, max_attempts=0)