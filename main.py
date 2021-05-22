from src.io import Connection
from src.player import Player
from src.carte import Carte

connexion = Connection()
connexion.login("Lyon1","g[B>!&I7C#V;-Y,OW%+/9A5")
connexion.deleteGames()
connexion.newGame('InactiveAI')
connexion.connect()
turn1 = connexion.getMap()

map = Carte(turn1)

print(map.distance(0,0,1,1))
print(map.distance(0,0,5,0))
print(map.distance(0,0,3,3))

print(map.adjacent(0,0))

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
            print("On a perdu")
        else:
            print("On a gagné")
        break

    if data["your_turn"]==False:
        continue

    # On joue
    played = player.play()
    connexion.sendTurn(played)

