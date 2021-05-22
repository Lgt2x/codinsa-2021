class Player:
    def __init__(self, map):
        self.map = map
    
    def play(self):
        move = {}
        attack = {}
        mine = {}
        build = {}
        summon = {}

        for i in range(len(self.map.batiments)):
            for j in range(len(self.map.batiments[0])):
                if self.map.batiments[i][j].identifiant == 'S' & self.map.batiments[i][j].appartenance == 1:
                    voisins = self.map.adjacent(i,j)       
                    for v in voisins:
                        if(v!=None):
                            if(self.map.unites[v[0]][v[1]] == None & (self.map.terrain[v[0]][v[1]] == 0 | self.map.terrain[v[0]][v[1]] == 1)): #Case vide
                                x,y,d = self.map.convToDown(v[0],v[1])
                                summon['['+x+','+y+','+('true','false')[d]+']'] = "V"


        return {"move":move,"attack":attack,"mine":mine,"build":build,"summon":summon}

    def update(self, data):
        pass