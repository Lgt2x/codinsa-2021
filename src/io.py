import json
import socket

import requests


class Connection:
    def __init__(self, token=""):
        self.game_started = False
        self.token = token

    def login(self, username: str, password: str):
        resp = requests.post(
            "http://codinsa.insa-rennes.fr/init",
            data=json.dumps({"username": username, "password": password}),
            headers={"Content-Type": "application/json"},
        )
        self.token = resp.headers["Set-Cookie"].split(";")[0].split("=")[1]

        with open('token', 'w') as f:
            f.write(self.token)

        print(f"Connexion établie, token {self.token}")

    def newGame(self, type: str):
        res = requests.get(
            f"http://codinsa.insa-rennes.fr/game/new?ai={type}",
            headers={"Cookie": f"session={self.token}"},
        )
        self.game_id = json.loads(res.text)["game_id"]
        self.password = json.loads(res.text)["password"]
        self.port = json.loads(res.text)["port"]

        print(f"Rejoint la nouvelle partie id {self.game_id}, pwd {self.password}, port {self.port}")

    def current(self):
        resp = requests.get('http://codinsa.insa-rennes.fr/current', headers={'Cookie': f'session={self.token}'})
        return json.loads(resp.text)['games']

    def deleteGames(self, game=""):
        # Supprime une partie si l'argument est précisé, vire tout sinon

        if game:
            requests.delete(f'http://codinsa.insa-rennes.fr/game/{game}', headers={'Cookie': f'session={self.token}'})
            print(f"Deleted game {game}")
        else:
            resp = requests.get('http://codinsa.insa-rennes.fr/current', headers={'Cookie': f'session={self.token}'})
            games = json.loads(resp.text)['games']

            print(f"Liste des parties en cours qui vont être supprimées: {games}")

            for g in games:
                requests.delete(f'http://codinsa.insa-rennes.fr/game/{g}', headers={'Cookie': f'session={self.token}'})

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(('193.52.94.158', self.port))

    def getMap(self):
        """
        Reçoit le premier tour, avec la map
        """
        data = self.socket.recv(2048)
        data = data.decode()
        print(data)

        while data[-2] != "}":
            data2 = self.socket.recv(2048)
            data2 = data2.decode()
            print(data2)
            data += data2

        return json.loads(data)

    def sendTurn(self, data):
        """
        Envoie le tour passé en argument au serveur
        """

        data['token'] = self.password
        print(str(data).replace("'", '"'))
        d = str(data).replace("'", '"') + "\n"
        self.socket.send(d.encode())

        print("Tour envoyé")
        print(data)

    def getTurn(self):
        """
        Reçoit le tour envoyé au serveur, et le renvoie
        """

        data = self.socket.recv(1024).decode()

        while data[-2] != "}":
            data2 = self.socket.recv(1024)
            data2 = data2.decode()
            data += data2

        print("Tour reçu")
        print(data)
        parsed = json.loads(data)

        if "errors" in parsed:
            print(parsed["errors"])

        return parsed
