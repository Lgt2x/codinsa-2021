import src.util

import json


class Player:
    def __init__(self, game_map):
        self.game_map = game_map

    def play(self, turn):

        print("Commence notre tour")

        self.move = {}
        self.attack = {}
        self.mine = {}
        self.build = {}
        self.summon = {}

        # On joue avec les ingés
        self.ingenieurs()

        # On joue avec les PPA

        # On calcule les summons
        self.compute_all_summonings()

        # Conversions des summons dans le format de sortie

        final_summon = {}
        for location, unit in self.summon.items():
            key = str(list(self.game_map.convToDown(*location))).lower()
            final_summon[json.dumps(self.game_map.convToDown(*location))] = unit
            turn.summon(location, unit)

        for unite in self.game_map.listeUnites:
            if unite.appartenance:
                voisins_unite = self.game_map.adjacent(*unite.position)
                for voisin_unite in voisins_unite:
                    if self.game_map.estConstructible(*voisin_unite) and self.game_map.estVide(*voisin_unite):
                        turn.build(unite.position, voisin_unite, "C")
        # On renvoie à l'IO les bonnes infos
        return {
            "move": self.move,
            "attack": self.attack,
            "mine": self.mine,
            "build": self.build,
            "summon": final_summon,
        }

    def ingenieurs(self):
        """
        détermine le comportement et les sorties des ingénieurs
        """

        for unite in self.game_map.listeUnites:
            # Check si inge
            if unite.identifiant == "V" and unite.appartenance == 1:

                # Si le déplacement est fini
                if unite.role == 1 and unite.position == unite.target:
                    # On l'assigne au minage
                    unite.role = 2
                    unite.target = None

                # Si il est en train de miner
                if unite.role == 2:
                    # On mine
                    posRessource = src.util.miner(unite, self.game_map)

                    """
                    voisins = self.game_map.adjacent(unite.position.x,unite.position.y)
                    for v in voisins:
                        if self.game_map.terrain[v[0],v[1]] == 3:
                            # On ajoute à la liste de minage
                            self.mine[str(self.game_map.position_serial_to_UD(unite.position[0], unite.position[1]))] = self.game_map.position_serial_to_UD(v[0], v[1])
                            break
                    """

                # Si il se déplace vers la ressource
                if unite.role == 1:
                    # continuer déplacement
                    moves = src.util.nextPositions(
                        (unite.position[0], unite.position[1]),
                        self.game_map,
                        (unite.target[0], unite.target[1])
                        , unite.pointMouvement
                    )
                    """
                    turn.move(unite.position, moves)
                    """

                # TODO PLUS TARD
                # Si il se déplace pour construire un amphi
                # if unite.role == 3:
                # si sur case target
                # construire
                # Réaffecter a rôle = 0
                # else se déplace vers target

                # Si il n'a pas de role
                if unite.role == 0:

                    # TODO PLUS TARD
                    # si gold > 250 + x
                    # Affecter a rôle 3
                    # Donne les coordonnees de la target

                    # Trouve la ressource libre la plus proche
                    posLibreRessource = src.util.closestAvailableRessource(
                        unite, self.game_map
                    )
                    unite.target = posLibreRessource
                    # on save que cette position est prise
                    self.game_map.target[posLibreRessource[0]][
                        posLibreRessource[1]
                    ] = True
                    # on deplace
                    deplacementUnite = src.util.nextPositions(
                        unite.position,
                        self.game_map,
                        unite.target,
                        unite.pointMouvement,
                    )
                    """turn.move(unite,deplacementUnite)"""
                    # on passe au role "se deplacer vers ress"
                    unite.role = 1

                    # affecter a role 1 et trouver la ressource libre la plus proche

        # Summon le max d'ingés (autour du spawn)
        # Mise à jour de la liste d'ingés

    def PPA(self, move, attack):
        pass

    def compute_all_summonings(self):
        for i in range(len(self.game_map.batiments)):
            for j in range(len(self.game_map.batiments[0])):
                if self.game_map.batiments[i][j] == None:
                    continue
                if (
                    self.game_map.batiments[i][j].identifiant == "S"
                    and self.game_map.batiments[i][j].appartenance == 1
                ):
                    voisins = self.game_map.adjacent(i, j)
                    # print(voisins)
                    for v in voisins:
                        if v != None:
                            if self.game_map.unites[v[0]][v[1]] == None and (
                                self.game_map.terrain[v[0]][v[1]] == "F"
                                or self.game_map.terrain[v[0]][v[1]] == "M"
                            ):  # Case vide
                                self.summon[tuple(v)] = "V"
                                break

                if (
                    self.game_map.batiments[i][j].identifiant == "C"
                    and self.game_map.batiments[i][j].appartenance == 1
                ):
                    voisins = self.game_map.adjacent(i, j)
                    for v in voisins:
                        if v != None:
                            if self.game_map.unites[v[0]][v[1]] == None and (
                                self.game_map.terrain[v[0]][v[1]] == 0
                                or self.game_map.terrain[v[0]][v[1]] == 1
                            ):  # Case vide
                                self.summon[tuple(v)] = "L"
                                break

    def update(self, data):
        self.game_map.update(data)
