from game.play import create_game, play_game
from game.prudent_ai_player import PrudentAIPlayer
from game.strategic_ai_player import StrategicAIPlayer

def run_tournament(players, nb_games, width, height, density):
    list_win_counts = [0, 0] #number of wins for each player
    for _ in range(nb_games):
        game = create_game(width=width, height=height, density=density)
        id_winner = play_game(game=game, players=players, display=None)
        list_win_counts[id_winner]+=1
    return list_win_counts

if __name__ == "__main__":
    players = [StrategicAIPlayer(name="Strategic AI 0", player_id=0), StrategicAIPlayer("Strategic AI 1", player_id=1)]
    score_match = run_tournament(players=players, nb_games=200, height=10, width=10, density=0.2)
    print(f"{players[0].name} {score_match[0]} - {score_match[1]} {players[1].name}")