import json
import sys

from src.io import Connection
from src.player import Player
from src.carte import Carte
from src.gameviz.logger import GameLogger

if len(sys.argv) != 4:
    print("3 args, cf readme")

password = ["", "g[B>!&I7C#V;-Y,OW%+/9A5", "ET1j]ZWe(JY)^A4_#@_1.h_J", "0%%IFIJ^&_Ac#_>R,a_YA+'"]
account = int(sys.argv[1])
mode = sys.argv[2]

from src.turn import Turn
connexion = Connection()
# connexion.login("Lyon3", password[3])
connexion.login(f"Lyon{account}", password[account])

if mode == "ai":
    print(f"Nouvelle partie AI avec l'IA {sys.argv[3]}")
    connexion.newGame(sys.argv[3])
elif mode == "pvp_create":
    print(f"Nouvelle partie PVP salle {sys.argv[3]}")
    connexion.newGameMJ(sys.argv[3])
elif mode == "pvp_join":
    print(f"Rejoint la salle PVP {sys.argv[3]}")
    connexion.joinGame(sys.argv[3])


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

for turn_number in range(10000):
    print(f"Tour #{turn_number}")

    # Recupere les données du tour
    data = connexion.getTurn()
    data = [json.loads(d) for d in data.split("\n")[:-1]]

    # Si on reçoit plusieurs tours, on les traite 1 par 1
    for d in data:
        if "errors" in d:
            print("Erreurs !")
            print(d["errors"])

        # La partie est terminée
        if "your_turn" not in d:
            print("Fin de la partie")
            if d["AIsWinner"] == True:
                print("A a gagné")
            else:
                print("A a perdu")
            break

        player.update(d)

    print(data)
    if len(data) == 2:
        break

    if data[-1]["your_turn"] == False:
        continue

    # On joue
    turn_instance = Turn()
    played = player.play(turn_instance)
    connexion.sendTurn(turn_instance.get_json_turn())
    logger.log_gamestate(player)

    if turn_number >50:
        break

connexion.deleteGames(connexion.game_id)
logger.save_logs()
