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
                    print("POS RESSOURCE: ", posRessource)
                    print("POS UNITE: ", unite.position)
                    if len(posRessource) > 0:
                        print("F")
                        turn.mine(unite.position, posRessource)
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
                if unite.role == 1:
                    # continuer déplacement
                    moves = src.util.nextPositions(
                        (unite.position[0], unite.position[1]),
                        self.game_map,
                        (unite.target[0], unite.target[1])
                        , unite.pointMouvement
                    )

                    if len(moves) > 0:
                        turn.deplacer_unite(unite.position, moves)
                    else:
                        unite.role = 0
                        self.game_map.target[unite.target[0]][unite.target[1]] = False

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
                    print("Position: ", unite.position)

                    # Si on a assez de gold, on crée une caserne pour former des PPA
                    if self.game_map.balance > 350 and self.game_map.nombreCasernes() == 0 and not caserne_construite:
                        # Ordre de construction de la caserne a cote du larbin
                        voisins = self.game_map.adjacent(*unite.position)

                        # ne garder que les voisins qui peuvent rellement être construits
                        def compute_min_distance_others(case, batiments):
                            mini = float('inf')
                            for b in batiments:
                                mini = min(mini, self.game_map.distance(case[0], b.position[0], case[1], b.position[1]))
                            return mini

                        my_batiments = [x for x in self.game_map.listeBatiments if x.appartenance]
                        minis = [compute_min_distance_others(x, my_batiments) for x in voisins]
                        voisins_ok = []
                        for it_voisin in range(len(voisins)):
                            if minis[it_voisin] >= 2 and minis[it_voisin] <= 4:
                                voisins_ok.append(voisins[it_voisin])
                        for v in voisins:
                            # list constructibles around
                            v_v = self.game_map.adjacent(*v)
                            cpt_ok = sum([self.game_map.estConstructible(*x) for x in v_v])
                            if self.game_map.estConstructible(*v) and cpt_ok >= 2:
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
                    if len(deplacementUnite) > 0:
                        turn.deplacer_unite(unite.position, deplacementUnite)
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
                attaque = src.util.attaquerAdj(unite, self.game_map)
                if attaque:
                    turn.attaquer_position(unite.position, attaque)
                else:
                    # Se déplace vers le spawn ennemi
                    ennemy = src.util.ennemyFinder(unite.position, self.game_map)
                    if ennemy:
                        moves = src.util.nextPositions(
                            (unite.position[0], unite.position[1]),
                            self.game_map,
                            ennemy
                            , unite.pointMouvement
                        )
                    if len(moves) > 0:
                        turn.deplacer_unite(unite.position, moves)

        # Summon le max d'ingés (autour du spawn)
        # Mise à jour de la liste d'ingés

    def compute_all_summonings(self,turn):
        nbInge = self.game_map.nbIngenieurs()
        #Spawn inge
        if nbInge < self.game_map.ressources*3:
            for b in self.game_map.listeBatiments:
                #Notre spawn:
                if b.identifiant=='S' and b.appartenance == 1:
                    voisins = self.game_map.adjacent(*b.position)
                    for v in voisins:
                        if nbInge < 3*self.game_map.ressources:
                            turn.summon(v,"V")
                            nbInge+=1


        #Spawn PPA
        for b in self.game_map.listeBatiments:
            if b.identifiant == 'C' and b.appartenance == 1:
                voisins = self.game_map.adjacent(*b.position)
                for v in voisins:
                    turn.summon(v,"L")


    def update(self, data):
        self.game_map.update(data)


"""
    def play_defense(self, turn):
        def dToSpawn(position):
            return self.game_map.distance(position[0], self.game_map.spawn[0], position[1], self.game_map.spawn[1])
        # get opponent units in perimeter:
        PERIMETER_DANGER = 5
        optimum_amphi = 2
        opponents_perimeter = [x for x in self.game_map.listeUnites if x.appartenance==0 and dToSpawn(x.position) <= PERIMETER_DANGER]
        unites_perimeter = [x for x in self.game_map.listeUnites if x.appartenance==1 and dToSpawn(x.position) <= PERIMETER_DANGER]
        positions_futur_taken = []

        batiments_perimeter = [x for x in self.game_map.listeBatiments if x.appartenance==1 and dToSpawn(x.position) <= PERIMETER_DANGER]
        if(len(opponents_perimeter)) == 0: # no enemy nearby
            camps = [x for x in batiments_perimeter if x.identifiant == "C"]
            tours = [x for x in batiments_perimeter if x.identifiant == "T"]
            if len(camps) < optimum_amphi:
                for unite in unites_perimeter:
                    if unite.identifiant == "V":
                        unite.role = 0
                        if unite.target != None:
                            self.game_map.target[unite.target[0]][unite.target[1]] = False
                            unite.target = None
                self.ingenieurs()
            else:
                
                # build tower
                pass
        else:
            # si rapport de force déséquilibré, former des unités
            MAX_FORMATION = 4
            if 3*sum([x.pv for x in opponents_perimeter])>= sum([x.pv for x in unites_perimeter]):
                # lister les positions de formations
                all_pos_formations = []
                for camp in camps:
                    positions_formations = self.game_map.adjacent(*camp.position)
                    all_pos_formations.extend(positions_formations)
                
                # Lister les positions constructibles, construire unité sur la plus proche du danger la plus proche
                distances_positions_unites = [[x.position, dToSpawn(x.position)] for x in opponents_perimeter]
                all_pos_formations = list(set([x for x in all_pos_formations if self.game_map.estConstructible(*x)]))
                distances_positions_unites = sorted(distances_positions_unites, key = lambda x: x[1])
                cpt_forme = 0
                while(cpt_forme < MAX_FORMATION and all_pos_formations):
                    close_enemy = distances_positions_unites[0][0]
                    # former sur la position la plus proche d un ennemi
                    all_pos_formations = sorted(all_pos_formations, key = lambda x: self.game_map.distance(x[0], close_enemy[0], x[1], close_enemy[1]))
                    # tout en restant aussi proche que possible du spawn
                    all_pos_formations = sorted(all_pos_formations, key = lambda x: dToSpawn(x))

                    turn.spawn(all_pos_formations[0], "L")
                    positions_futur_taken.append(all_pos_formations[0])
                    cpt_forme +=1
                    all_pos_formations = all_pos_formations[1:]
                    distances_positions_unites[0][1] += 1 # faire comme si il s eloignait pour voir les autres menaces

            # target unit, starting by the closest one to spawn
            # for each of my units, if I can already target someone, do it
            for my_unit in unites_perimeter:
                for opp_unit in opponents_perimeter:
                    if self.game_map.distance(my_unit.position[0], opp_unit.position[0], my_unit.position[1], opp_unit.position[1]) == 1:
                        turn.attaquer_position(my_unit.position, opp_unit.position)
                        opp_unit.targeted = True
                        my_unit.moved = True
                # in case of equality : d'abord si on peut achever quelqu'un, ensuite au plus proche
            for my_unit in unites_perimeter:
                opp_targets = [x for x in opponents_perimeter if x.targeted]
                opp_targets = sorted(opp_targets, key = lambda x: self.game_map.distance(x.position[0], my_unit.position[0], x.position[1], my_unit.position[1]))
                target_case = closestPath(my_unit, self.game_map, opp_targets[0].position[0], opp_targets.position[1])
                moves = nextPositions(my_unit.position, self.game_map, target_case, my_unit.pointMouvement)
                
                if len(moves) != 0 and tuple(moves[-1]) not in [tuple(x) for x in positions_futur_taken]:
                    turn.move(my_unit.position, moves)
                    positions_futur_taken.append(moves[-1])
                    my_unit.moved = True
            """
