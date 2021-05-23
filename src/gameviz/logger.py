import sys
sys.path.append("..")
from src.carte import Carte
from src.player import Player
import json
class TileState():
    def __init__(self, map_shard, batiment_shard, units_shard):
        self.is_unit = (units_shard != None)
        self.is_batiment = (batiment_shard != None)
        self.ours = False
        self.identifiant = map_shard
        self.type = map_shard
        if self.is_batiment:
            self.ours = batiment_shard.appartenance
            self.type = batiment_shard.identifiant
        elif self.is_unit:
            self.ours = units_shard.appartenance
            self.type = units_shard.identifiant
        
    def to_dict(self):
        return {
            "terrain" : self.identifiant,
            "type" : self.type,
            "ours" : self.ours
        }
    
class GameLogger():
    def __init__(self, target_file_location):
        self.all_states = []
        self.target_file_location = target_file_location
    def log_gamestate(self, player : Player): 
        carte = player.game_map
        len_x = len(carte.terrain)
        len_y = len(carte.terrain[0])
        map_representation = [[{} for _ in range(len_x)] for _ in range(len_y)]       
        for x in range(len_x):
            for y in range(len_y):
                map_representation[y][x] = TileState(carte.terrain[x][y], carte.batiments[x][y], carte.unites[x][y]).to_dict()
        self.all_states.append({"map_representation" : map_representation, 
        "balance" : player.game_map.balance, 
        "points" : player.game_map.points
        })
    
    def save_logs(self):
        with open(self.target_file_location, 'w') as outfile : 
            json.dump(self.all_states, outfile)