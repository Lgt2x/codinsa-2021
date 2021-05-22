from src.io import Connection
from src.player import Player
from src.carte import Carte

connexion = Connection()

password = ["g[B>!&I7C#V;-Y,OW%+/9A5", "ET1j]ZWe(JY)^A4_#@_1.h_J", "0%%IFIJ^&_Ac#_>R,a_YA+'"]

connexion.login("Lyon3", password[2])
connexion.newGame('RessourceAI')
connexion.connect()
turn1 = connexion.getMap()

map = Carte(turn1)

player = Player(map)

if turn1["your_turn"]:
    print("On joue en premier")
    turn = player.play()
    connexion.sendTurn(turn)
else:
    print("On joue en 2e")

for turn_number in range(1001):
    print(f"Tour #{turn_number}")
    
    # Récupère les données du tour
    data = connexion.getTurn()
    player.update(data)

    if "your_turn" not in data:
        print("Fin de la partie")
        if data["AIsWinner"] == True:
            print("A a gagné")
        else:
            print("A a perdu")
        break

    if data["your_turn"]==False:
        continue

    # On joue
    played = player.play()
    connexion.sendTurn(played)

connexion.deleteGames(connexion.game_id)
