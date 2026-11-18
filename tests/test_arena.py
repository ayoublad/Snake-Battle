from game.arena import Arena

WALLS = [(3, 0), (3, 1), (3, 2), (4, 2), (0, 3), (1, 3), (1, 4)]

def build_arena():
    arena = Arena(5, 5, walls=WALLS)
    return arena

def test_corners_are_inside():
    arena = build_arena()
    assert arena.is_inside((0, 0)) 
    assert arena.is_inside((4, 0)) 
    assert arena.is_inside((0, 4)) 
    assert arena.is_inside((4, 4))
    #enleve tous les prints de test pour que le test soit plus propre et plus lisible.

def test_outside_cells():
    arena = build_arena()
    assert not arena.is_inside((-1, 0)) 
    assert not arena.is_inside((5, 0)) 
    assert not arena.is_inside((0, -1)) 
    assert not arena.is_inside((0, 5))

def test_walls():
    arena = build_arena()
    for wall in WALLS:
        assert arena.is_wall(wall)

def test_free_cells():
    arena = build_arena()
    for x in range(arena.width):
        for y in range(arena.height):
            if (x, y) not in WALLS:
                assert not arena.is_wall((x, y))

def test_xy_order():
    arena = build_arena()
    assert arena.is_wall((4,2))
    assert not arena.is_wall((2,4))

def test_walls_are_copied():
    walls = [(1,1), (2, 2), (3, 3)]
    arena = Arena(5, 5, walls=walls)
    walls.append((3, 4))  
    assert not arena.is_wall(walls[-1])

def test_reachable_cells_without_blocked_cells():
    arena = build_arena()
    initial_cell = (1, 1)
    reachable = arena.reachable_cells(initial_cell)
    assert reachable == {
        (0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), 
        (0, 2), (1, 2), (2, 2), (2, 3), (3, 3), (4, 3), 
        (2, 4), (3, 4), (4, 4)
    }

def test_reachable_cells_with_blocked_cells():
    arena = build_arena()
    initial_cell = (1, 1)
    blocked_cells = {(2, 2)}
    reachable = arena.reachable_cells(initial_cell, set_cell_blocked=blocked_cells)
    assert reachable == {(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2)}

def test_reachable_cells_with_initial_cell_blocked():
    arena = build_arena()
    initial_cell = (1, 1)
    reachable = arena.reachable_cells(initial_cell, set_cell_blocked=set([initial_cell]))
    assert reachable == {
        (0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), 
        (0, 2), (1, 2), (2, 2), (2, 3), (3, 3), (4, 3), 
        (2, 4), (3, 4), (4, 4)
    }