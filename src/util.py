import math
from queue import PriorityQueue


def nextPositions(depart, carte, arrivee, nbDeplacement):
    x, y = carte.x, carte.y

    if depart == arrivee:
        return []

    visited = [[False for _ in range(y)] for _ in range(x)]
    pQ = PriorityQueue()
    pQ.put((0, depart))

    dist = [[-1 for _ in range(y)] for _ in range(x)]
    pred = [["" for _ in range(y)] for _ in range(x)]

    dist[depart[0]][depart[1]] = 0

    while not pQ.empty():

        current = pQ.get()

        # print("Current= ", current)

        if visited[current[1][0]][current[1][1]]:
            continue
        if current[1] == arrivee:
            break

        visited[current[1][0]][current[1][1]] = True

        for adj in carte.adjacent(current[1][0], current[1][1]):

            terrain = carte.terrain[adj[0]][adj[1]]
            cout = 0
            if terrain == 'R':
                continue
            if terrain == 'F':
                cout = 1
            elif terrain == 'M':
                cout = 2
            elif terrain == 'A':
                continue
            if carte.batiments[adj[0]][adj[1]] is not None and not carte.batiments[adj[0]][adj[1]].appartenance:
                continue
            elif carte.unites[adj[0]][adj[1]] is not None:
                continue

            if dist[adj[0]][adj[1]] == -1:
                dist[adj[0]][adj[1]] = dist[current[1][0]][current[1][1]] + cout
                pred[adj[0]][adj[1]] = current[1]
                pQ.put((dist[adj[0]][adj[1]], adj))
            else:
                if dist[adj[0]][adj[1]] > dist[current[1][0]][current[1][1]] + cout:
                    dist[adj[0]][adj[1]] = dist[current[1][0]][current[1][1]] + cout
                    pred[adj[0]][adj[1]] = current[1]
                    pQ.put((dist[adj[0]][adj[1]], adj))
    rep = []
    if dist[arrivee[0]][arrivee[1]] == -1:
        return rep
    rep.append(arrivee)
    # print("dist: ", dist)
    # print("Pred: ", pred)
    # print(rep)
    # print("Autre: ", pred[rep[-1][0]][rep[-1][1]])
    while list(pred[rep[-1][0]][rep[-1][1]]) != list(depart):
        rep.append(pred[rep[-1][0]][rep[-1][1]])
    # print(rep)
    return [rep.pop(-1) for _ in range(min(len(rep), nbDeplacement))]


def closestAvailableRessource(unite, carte):
    posActuel = unite.position

    dest = posActuel
    minDist = math.inf

    for x in range(carte.x):
        for y in range(carte.y):
            if carte.terrain[x][y] == 'R':
                # print("Ressource trouve: ", x, y)

                for adj in carte.adjacent(x, y):
                    # print("adj: ", adj)
                    if carte.terrain[adj[0]][adj[1]] == 'F' or carte.terrain[adj[0]][adj[1]] == 'M':
                        if carte.batiments[adj[0]][adj[1]] is None and carte.unites[adj[0]][adj[1]] is None and not \
                        carte.target[adj[0]][adj[1]]:
                            dist = carte.distance(adj[0], adj[1], posActuel[0], posActuel[1])
                            if dist < minDist:
                                minDist = dist
                                dest = adj
    return dest


def closestPath(unite, carte, x, y, compteurRec=0):
    posActuel = unite.position
    if compteurRec > 10:
        return unite.position
    dest = posActuel
    minDist = math.inf

    for adj in carte.adjacent(x, y):
        # print("adj: ", adj)
        if carte.terrain[adj[0]][adj[1]] == 'F' or carte.terrain[adj[0]][adj[1]] == 'M':
            dist = carte.distance(adj[0], adj[1], posActuel[0], posActuel[1])
            if dist < minDist:
                minDist = dist
                dest = adj

    if carte.batiments[dest[0]][dest[1]] is not None or carte.unites[dest[0]][dest[1]] is not None or \
            carte.target[dest[0]][dest[1]]:
        print("Appel recursif")
        dest = closestPath(unite, carte, dest[0], dest[1], compteurRec + 1)
    return dest


def miner(unite, game_map):
    if unite.identifiant == 'V':
        # on check si les cases adjacentes a l'inge sont des ressources
        voisins = game_map.adjacent(unite.position[0], unite.position[1])
        for v in voisins:
            if game_map.terrain[v[0]][v[1]] == 3:
                # On retourne la pos de la ressource
                return v
    # si pas de ressources ou mauvaise unite
    return []


def attaquerAdj(unite, game_map, target=None):
    if target is None:
        voisins = game_map.adjacent(unite.position[0], unite.position[1])
        posTarget = None
        vieTarget = 999
        for v in voisins:
            if game_map.unites[v[0]][v[1]] is not None and game_map.unites[v[0]][v[1]].appartenance == 0:
                if vieTarget > game_map.unites[v[0]][v[1]].pv:
                    vieTarget = game_map.unites[v[0]][v[1]].pv
                    posTarget = v
        if posTarget is not None:
            return posTarget
        for v in voisins:
            if game_map.batiments[v[0]][v[1]] is not None and game_map.batiments[v[0]][v[1]].appartenance == 0:
                if vieTarget > game_map.batiments[v[0]][v[1]].pv:
                    vieTarget = game_map.batiments[v[0]][v[1]].pv
                    posTarget = v
        if posTarget is not None:
            return posTarget

    else:
        if (game_map.unites[target[0]][target[1]] is not None and game_map.unites[target[0]][
            target[1]].appartenance == 0) or \
                (game_map.batiments[target[0]][target[1]] is not None and game_map.batiments[target[0]][
                    target[1]].appartenance != 1):
            return target
    return []
