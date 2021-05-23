from enum import Enum
import src.batiment as batiment
import src.unite as unite
import math


class Terrain(Enum):
    F = 0
    M = 1
    A = 2
    R = 3


dict_classes_batiment = {
    "S": batiment.Ecole,
    "C": batiment.Amphi,
    "T": batiment.Tourelle,
    "W": batiment.Mur
}
dict_classes_unites = {
    "V": unite.Ingenieur,
    "L": unite.ULegere,
    "H": unite.ULourde,
}


def position_UD_to_serial(position):
    return (position[0] * 2 + int(position[2]), position[1])


def position_serial_to_UD(position):
    return (position[0] // 2, position[1], position[0] % 2)


class Carte:

    def decode_raw_terrain(self, raw_terrain, spawn):

        for j in range(len(raw_terrain)):
            for i in range(len(raw_terrain[0])):
                split_tile = raw_terrain[j][i].split(";")
                self.terrain[i][j] = split_tile[0]
                if split_tile[0] == "A":
                    self.discovered[i][j] = True  # une abysse est techniquement découverte

                if len(split_tile) != 1:  # terrain
                    if split_tile[1] in "SCTW":
                        class_instantiate = dict_classes_batiment[split_tile[1]]
                        is_ours = False
                        if split_tile[1] == "S":
                            # print("x:",i,",y:",j, ",spawn",spawn, ",convtodownspawn:",self.convToDown(spawn[0], spawn[1]))
                            # TODO appel orga
                            if i == spawn[0] and j == spawn[1]:
                                is_ours = True
                            # print(is_ours," - x:",i,",y:",j, ",spawn",spawn, ",convtodownspawn:",self.convToDown(spawn[0], spawn[1]))

                            # print(i,j, spawn, is_ours)
                        self.batiments[i][j] = class_instantiate(appartenance=is_ours, position=[i, j])
                    elif split_tile[1] in "VLH":
                        class_instantiate = dict_classes_unites[split_tile[1]]
                        self.unites[i][j] = class_instantiate(appartenance=0, position=[i, j])

    def __init__(self, data):
        raw_terrain = [b.split(" ") for b in data['map'].split("\n")][:-1]
        # print("raw spawn",data["spawn"])
        self.spawn = position_UD_to_serial(data['spawn'])
        self.x = len(raw_terrain[0])
        self.y = len(raw_terrain)

        self.terrain = [["" for _ in range(self.y)] for _ in range(self.x)]
        self.batiments = [[None for _ in range(self.y)] for _ in range(self.x)]
        self.unites = [[None for _ in range(self.y)] for _ in range(self.x)]
        self.discovered = [[False for _ in range(self.y)] for _ in range(self.x)]

        self.decode_raw_terrain(raw_terrain=raw_terrain, spawn=self.spawn)

    def adjacent(self, x, y):
        adj1 = None
        adj2 = None
        adj3 = None
        if x % 2:  # down
            if x + 1 < self.x:
                adj1 = [x + 1, y]
            else:
                adj1 = None
            if x - 1 >= 0:
                if y - 1 >= 0:
                    adj2 = [x - 1, y - 1]
                else:
                    adj2 = None
                adj3 = [x - 1, y]
            else:
                adj2 = None
                adj3 = None
        else:  # up
            if x - 1 >= 0:
                adj1 = [x - 1, y]
            else:
                ajd1 = None
            if x + 1 < self.x:
                adj3 = [x + 1, y]
                if y + 1 < self.y:
                    adj2 = [x + 1, y + 1]
                else:
                    ajd2 = None
            else:
                adj3 = None

        rep = []
        for i in [adj1, adj2, adj3]:
            if i != None:
                rep.append(i)
        return rep

    def distance(self, x1, y1, x2, y2):
        return abs(x2 // 2 - x1 // 2) + abs(y2 - y1) + abs(x2 // 2 - x1 // 2 + y1 - y2 + x2 % 2 - x1 % 2)

    def convToDown(self, x, y):
        return x // 2, y, bool(x % 2)

    def update(self, data):
        # update summoned
        for summon in data["summoned"]:
            if not summon[-1]:
                continue  # skip, there was a fail
            converted_position = position_UD_to_serial(summon[0])
            self.unites[converted_position[0]][converted_position[1]] = dict_classes_unites[summon[1]](appartenance=1,
                                                                                                       position=converted_position)

        for (position, info) in data["visible"].items():
            # print(position, info)
            pass
            # position = self.position_UD_to_serial(position)
            # TODO actually update
            pass

    def convToDown(self, x, y):
        return x // 2, y, x % 2

    def updateTerrain(self, x, y, down, val):
        self.terrain[x][y][down] = val

    def updateBatiments(self, x, y, down, val):
        self.batiments[x][y][down] = val

    def updateUnites(self, x, y, down, val):
        self.unites[x][y][down] = val
