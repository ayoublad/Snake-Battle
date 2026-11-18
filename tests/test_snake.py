from collections import deque
from game.snake import Snake
from game.directions import Direction, next_cell

def build_abc():
    """Construit le serpent A – B – C de notre exemple : A(0,0), B(1,0), C(2,0), tête en C."""
    snake = Snake((0, 0))                    # A
    snake.move_forward((1, 0), growth=True)  # + B
    snake.move_forward((2, 0), growth=True)  # + C
    return snake


def test_initial_state():
    snake = Snake((3, 5))
    assert snake.body == deque([(3, 5)])
    assert snake.head() == (3, 5)
    assert snake.tail() == (3, 5)        # une seule case : la tête est aussi la queue
    assert snake.neck() is None          # pas encore de cou

def test_turn_zero_growth():
    snake = Snake((3, 5))
    snake.move_forward((3, 6), growth=True)
    assert snake.body == deque([(3, 5), (3, 6)])
    assert snake.head() == (3, 6)
    assert snake.neck() == (3, 5)
    assert snake.tail() == (3, 5)

def test_normal_move_abc_to_bcd():
    snake = build_abc()
    snake.move_forward((3, 0), growth=False)              # vers D
    assert snake.body == deque([(1, 0), (2, 0), (3, 0)])   # B – C – D
    assert not snake.is_cell_occupied((0, 0))             # A a été libérée

def test_growth_move_abc_to_abcd():
    snake = build_abc()
    snake.move_forward((3, 0), growth=True)                       # vers D
    assert snake.body == deque([(0, 0), (1, 0), (2, 0), (3, 0)])   # A – B – C – D
    assert snake.is_cell_occupied((0, 0))                         # A est toujours là

def test_coiled_snake_enters_its_tail():
    # Q(0,0) B(1,0) C(1,1) T(0,1) : la tête vise (0,0), la case de sa propre queue
    snake = Snake((0, 0))
    snake.move_forward((1, 0), growth=True)
    snake.move_forward((1, 1), growth=True)
    snake.move_forward((0, 1), growth=True)
    snake.move_forward((0, 0), growth=False)
    assert snake.body == deque([(1, 0), (1, 1), (0, 1), (0, 0)])
    assert snake.head() == (0, 0)
    assert snake.tail() == (1, 0)

def test_length_over_20_turns():
    start = (3, 5)                       # volontairement pas (0, 0)
    snake = Snake(start)
    for turn in range(20):
        growth = turn % 5 == 0
        destination = next_cell(snake.head(), Direction.DOWN)   # calculée depuis la tête
        snake.move_forward(destination, growth)

        expected_length = 2 + turn // 5   # 1 case au départ + croissances aux tours 0, 5, 10…
        assert len(snake.body) == expected_length, f"tour {turn} : longueur {len(snake.body)}, attendu {expected_length}"
        assert snake.head() == (3, 5 + turn + 1), f"tour {turn} : tête en {snake.head()}"