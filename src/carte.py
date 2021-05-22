from enum import Enum
class Terrain(Enum):
    F = 0
    M = 1
    A = 2
    R = 3

import json
from queue import PriorityQueue
class Carte:

    def __init__(self,data):
        #TODO : Adapter selon format du json*

        self.terrain = [b.split(" ") for b in data['map'].split("\n")]
        spawn = data['spawn']
        self.x = len(self.terrain[0])
        self.y = len(self.terrain)

        print(spawn.split(" "))
            
        self.batiments = [[None]* len(self.terrain) for i in range(len(self.terrain[0]))]
        self.unites = [[None]* len(self.terrain) for i in range(len(self.terrain[0]))]

    def adjacent(self,x,y):
        adj1=None
        adj2=None
        adj3=None
        if x%2: #down
            if x+1<self.x:
                adj1 = [x+1,y]
            else:
                adj1 = None
            if x-1>=0:
                if y-1>=0: 
                    adj2 = [x-1,y-1]
                else:
                    adj2 = None
                adj3 = [x-1,y]
            else:
                adj2 = None
                adj3 = None
        else: #up
            if x-1>=0:
                adj1 = [x-1,y]
            else:
                ajd1 = None
            if x+1<self.x:
                adj3 = [x+1,y]    
                if y+1<self.y:
                    adj2 = [x+1,y+1]
                else:
                    ajd2 = None
            else:
                adj3 = None    
                
        #return [adj1,adj2,adj3]

    def distance(self,x1,y1,x2,y2):
        return abs(x2//2 - x1//2)+abs(y2 - y1)+abs(x2//2-x1//2+y1-y2+x2%2-x1%2)

    def convToDown(self,x,y):
        return x//2,y,x%2
    
    def updateTerrain(self,x,y,down,val):
        self.terrain[x][y][down] = val

    def updateBatiments(self,x,y,down,val):
        self.batiments[x][y][down] = val
    
    def updateUnites(self,x,y,down,val):
        self.unites[x][y][down] = val
    
    def dijkstra(self, depart, map, arrivee):
        x, y = map.x, map.y

        visited = [[False for _ in range(x)] for _ in range(y)]
        pQ = PriorityQueue()
        pQ.put((0, depart))

        dist = [[-1 for _ in range(x)] for _ in range(y)]
        pred = [["" for _ in range(x)] for _ in range(y)]

        dist[depart[1]][depart[0]] = 0

        while not pQ.empty():

            current = pQ.get()

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

        rep = (-1, -1)
        p = pred[arrivee[1]][arrivee[0]]

        while pred[p[1]][p[0]] != '':
            p=pred[p[1]][p[0]]
        
        return p
