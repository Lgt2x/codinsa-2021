import math
from queue import PriorityQueue


def dijkstra(depart, map, arrivee):
    x, y = map.x, map.y

    visited = [[False for _ in range(x)] for _ in range(y)]
    pQ = PriorityQueue()
    pQ.put((0, depart))

    dist = [[-1 for _ in range(x)] for _ in range(y)]
    pred = [["" for _ in range(x)] for _ in range(y)]

    dist[depart[1]][depart[0]] = 0

    while not pQ.empty():

        current = pQ.get()

        print("Current= ", current)

        if visited[current[1][1]][current[1][0]]:
            continue
        if current[1] == arrivee:
            break

        visited[current[1][1]][current[1][0]] = True



        for adj in map.adjacent(current[1][0], current[1][1]):
            terrain = map.terrain[adj[1]][adj[0]]
            cout = 0
            if terrain == 'R':
                continue
            if terrain == 'F':
                cout = 1
            elif terrain == 'M':
                cout = 2
            elif terrain == 'A':
                cout = math.inf

            if dist[adj[1]][adj[0]] == -1:
                dist[adj[1]][adj[0]] = dist[current[1][1]][current[1][0]] + cout
                pred[adj[1]][adj[0]] = current[1]
                pQ.put((dist[adj[1]][adj[0]], adj))
            else:
                if dist[adj[1]][adj[0]] > dist[current[1][1]][current[1][0]] + cout:
                    dist[adj[1]][adj[0]] = dist[current[1][1]][current[1][0]] + cout
                    pred[adj[1]][adj[0]] = current[1]
                    pQ.put((dist[adj[1]][adj[0]], adj))

    rep =arrivee
    print("dist: ",dist)
    print("Pred: ",pred)
    print(rep)
    print("Autre: ",pred[rep[1]][rep[0]])
    while list(pred[rep[1]][rep[0]]) != list(depart):
        rep = pred[rep[1]][rep[0]]

    return rep
