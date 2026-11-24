from game.move_result import MoveResult

def play_game(game, players, display=None):
    while not game.is_over():
        current_player = players[game.current_player]
        if display is not None:
            print(f"Turn {game.turn} - It's up to {current_player.name} to play.\n")
            print(display.render(game))
        direction = current_player.choose_direction(game)
        result_move = game.play(direction)
        while result_move == MoveResult.REFUSED:
            if display is not None:
                print("No U-turns")
            direction = current_player.choose_direction(game)
            result_move = game.play(direction)
        if display is not None:
            print(f"{current_player.name} played direction: {direction.name}\n")
    if display is not None:
        print(display.render(game))
        print(f"Game over! Winner: {players[game.winner].name}")
    return players[game.winner]