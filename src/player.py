import src.util

import json

import src.turn


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
        self.ingenieurs(turn)

        # On joue avec les PPA

        # On calcule les summons
        self.compute_all_summonings(turn)

        """# Conversions des summons dans le format de sortie

        final_summon = {}
        for location, unit in self.summon.items():
            key = str(list(self.game_map.convToDown(*location))).lower()
            final_summon[json.dumps(self.game_map.convToDown(*location))] = unit
            turn.summon(location, unit)"""

        # for unite in self.game_map.listeUnites:
        #     if unite.appartenance:
        #         voisins_unite = self.game_map.adjacent(*unite.position)
        #         for voisin_unite in voisins_unite:
        #             if self.game_map.estConstructible(*voisin_unite) and self.game_map.estVide(*voisin_unite):
        #                 turn.build(unite.position, voisin_unite, "C")
        # On renvoie à l'IO les bonnes infos
        

    def ingenieurs(self, turn):
        """
        détermine le comportement et les sorties des ingénieurs
        """
        caserne_construite = False
        for unite in self.game_map.listeUnites:
            # Check si inge
            if unite.identifiant == "V" and unite.appartenance == 1:

                # Si le déplacement est fini
                if unite.role == 1 and unite.position[0] == unite.target[0] and unite.position[1] == unite.target[1]:
                    # On l'assigne au minage
                    print("MINER")
                    unite.role = 2
                    self.game_map.target[unite.target[0]][unite.target[1]] = False
                    unite.target = None


                # Si il est en train de miner
                if unite.role == 2:
                    # On mine
                    posRessource = src.util.miner(unite, self.game_map)
                    print("POS RESSOURCE: ",posRessource)
                    print("POS UNITE: ", unite.position)
                    if len(posRessource)>0:
                        print("F")
                        turn.mine(unite.position,posRessource)
                    # else:
                        # unite.role=0

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

                    if len(moves )> 0:
                        turn.deplacer_unite(unite.position, moves)
                    else:
                        unite.role = 0
                        self.game_map.target[unite.target[0]][unite.target[1]]=False


                # TODO PLUS TARD
                # Il se déplace pour construire un amphi
                if unite.role == 3:
                    pass


                # si sur case target
                # construire
                # Réaffecter a rôle = 0
                # else se déplace vers target

                # Si il n'a pas de role

                if unite.role == 0:
                    print("Position: ",unite.position)

                    # Si on a assez de gold, on crée une caserne pour former des PPA
                    if self.game_map.balance > 350 and self.game_map.nombreCasernes() == 0 and not caserne_construite:
                        #Ordre de construction de la caserne a cote du larbin
                        voisins = self.game_map.adjacent(*unite.position)
                        for v in voisins:
                            if self.game_map.estConstructible(*v):
                                turn.build(unite.position, v, "C")
                                caserne_construite = True
                                break



                    # Trouve la ressource libre la plus proche
                    posLibreRessource = src.util.closestAvailableRessource(
                        unite, self.game_map
                    )
                    print("PositionLibreRessource: ", posLibreRessource)
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
                    if len(deplacementUnite)>0:
                        turn.deplacer_unite(unite.position,deplacementUnite)
                    else:
                        self.game_map.target[unite.target[0]][unite.target[1]] = False

                    # on passe au role "se deplacer vers ress"
                    unite.role = 1

                    # affecter a role 1 et trouver la ressource libre la plus proche

        # Summon le max d'ingés (autour du spawn)
        # Mise à jour de la liste d'ingés

    def PPA(self, turn, move, attack):

        for unite in self.game_map.listeUnites:
            # Check si PPA/Tank
            if unite.identifiant == "L" or unite.identifiant == "H":
                if unite.target:

                    # Se déplace vers le spawn ennemi
                    moves = src.util.nextPositions(
                        (unite.position[0], unite.position[1]),
                        self.game_map,
                        (unite.target[0], unite.target[1])
                        , unite.pointMouvement
                    )

                    turn.deplacer_unite(unite.position, moves)
                else:
                    pass

        # Summon le max d'ingés (autour du spawn)
        # Mise à jour de la liste d'ingés

    def compute_all_summonings(self,turn):
        nbInge = self.game_map.nbIngenieurs()

        print("Ressources :",self.game_map.ressources)
        #Spawn inge
        if nbInge < self.game_map.ressources*3:
            print("je suis dans le if")
            for b in self.game_map.listeBatiments:
                #Notre spawn:
                if b.identifiant=='S' and b.appartenance == 1:
                    voisins = self.game_map.adjacent(*b.position)
                    for v in voisins:
                        if nbInge < 3*self.game_map.ressources:
                            turn.summon(v,"V")
                            nbInge+=1

        #Spawn PPA
        
                        
                        
                    

    def update(self, data):
        self.game_map.update(data)

    def play_defense(self):
        # get a perimeter around spawn
        pass
