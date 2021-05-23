from src.io import Connection
from src.player import Player
from src.carte import Carte
from src.gameviz.logger import GameLogger
from src.turn import Turn
connexion = Connection()

password = ["g[B>!&I7C#V;-Y,OW%+/9A5", "ET1j]ZWe(JY)^A4_#@_1.h_J", "0%%IFIJ^&_Ac#_>R,a_YA+'"]

connexion.login("Lyon2", password[1])
connexion.deleteGames()

connexion.newGame('RessourceAI')
connexion.connect()
turn1 = connexion.getMap()
map = Carte(turn1)

logger = GameLogger("game_logs/summon_game.json")
player = Player(map)

if turn1["your_turn"]:
    print("On joue en premier")
    turn_instance = Turn()
    turn = player.play(turn_instance)
    connexion.sendTurn(turn)
else:
    print("On joue en 2e")

for turn_number in range(1001):
    print(f"Tour #{turn_number}")
    
    # Recupere les données du tour
    data = connexion.getTurn()

    # La partie est terminée
    if "your_turn" not in data:
        print("Fin de la partie")
        if data["AIsWinner"] == True:
            print("A a gagné")
        else:
            print("A a perdu")
        break

    player.update(data)

    if data["your_turn"]==False:
        continue

    # On joue
    turn_instance = Turn()
    played = player.play(turn_instance)
    connexion.sendTurn(turn_instance.get_json_turn())
    logger.log_gamestate(player.game_map)

    if turn_number > 10:
        break

connexion.deleteGames(connexion.game_id)
logger.save_logs()
