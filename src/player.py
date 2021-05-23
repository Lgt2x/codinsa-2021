import json
class Player:
    def __init__(self, game_map):
        self.game_map = game_map
    
    def play(self):
        print("asked for play.")
        move = {}
        attack = {}
        mine = {}
        build = {}
        summon = {}
        self.compute_all_summonings(summon)
        final_summon = {}
        for location, unit in summon.items():
            key = str(list(self.game_map.convToDown(*location))).lower()
            final_summon[json.dumps(self.game_map.convToDown(*location))] = unit
        return {"move":move,"attack":attack,"mine":mine,"build":build,"summon":final_summon}

    def ingenieurs(self,move,attack,mine,build):
        pass

    def PPA(self,move,attack):
        pass

    def compute_all_summonings(self,dict_summons):
        for i in self.game_map.listeBatiments:
            if(i.appartenance):
                if(i.identifiant=='S'):
                    voisins = self.game_map.adjacent(i.position[0],i.position[1])
                    for v in voisins:
                        if(v!=None):
                            if(self.game_map.unites[v[0]][v[1]] == None and (self.game_map.terrain[v[0]][v[1]] == "F" or self.game_map.terrain[v[0]][v[1]] == "M")): #Case vide
                                dict_summons[tuple(v)] = "V"
                                break
                if(i.identifiant=='C'):
                    voisins = self.game_map.adjacent(i.position[0],i.position[1])       
                    for v in voisins:
                        if(v!=None):
                            if(self.game_map.unites[v[0]][v[1]] == None and (self.game_map.terrain[v[0]][v[1]] == 0 or self.game_map.terrain[v[0]][v[1]] == 1)): #Case vide
                                dict_summons[tuple(v)] = "L"
                                break
            
        
    


        """
        for i in range(len(self.game_map.batiments)):
            for j in range(len(self.game_map.batiments[0])):
                if self.game_map.batiments[i][j] == None:
                    continue
                if self.game_map.batiments[i][j].identifiant == 'S' and self.game_map.batiments[i][j].appartenance == 1:
                    voisins = self.game_map.adjacent(i,j)
                    # print(voisins)   
                    for v in voisins:
                        if(v!=None):
                            if(self.game_map.unites[v[0]][v[1]] == None and (self.game_map.terrain[v[0]][v[1]] == "F" or self.game_map.terrain[v[0]][v[1]] == "M")): #Case vide
                                dict_summons[tuple(v)] = "V"
                                break
                    
                if self.game_map.batiments[i][j].identifiant == 'C' and self.game_map.batiments[i][j].appartenance == 1:
                    voisins = self.game_map.adjacent(i,j)       
                    for v in voisins:
                        if(v!=None):
                            if(self.game_map.unites[v[0]][v[1]] == None and (self.game_map.terrain[v[0]][v[1]] == 0 or self.game_map.terrain[v[0]][v[1]] == 1)): #Case vide
                                dict_summons[tuple(v)] = "L"
                                break
            """
    
    def update(self, data):
        self.game_map.update(data)
