from src.carte import position_serial_to_UD
import json
class Turn():
    """La classe Turn doit permettre d'encapsuler toutes les actions avant leur passage à la sortie pour l'api.
    On doit pouvoir interagir avec dans 'notre langage', ie notre systeme de coordonnées
    """    
    d_attack = {}
    d_mine = {}
    d_build = {}
    d_summon = {}
    d_move = {}
    def __init__(self):
        # definir des structures de données qui vont stocker toutes les actions comme vous l'aviez fait dans le main
        pass
    def conv(self, pos):
        return position_serial_to_UD(pos)
    def cdump(self,pos):
        return json.dumps(self.conv(pos))
    def f_pos(self,pos):
        return str(list(pos))
    def l_conv(self, pos):
        return list(self.conv(pos))
    def f_conv(self,pos):
        return str(list(self.conv(pos)))

    def mine(self,pos_inge, pos_ressource):
        self.d_mine[self.conv(pos_inge)] = [self.l_conv[pos_ressource]] # check double array

    def summon(self,pos_summon, type_summon):
        self.d_summon[self.conv(pos_summon)] = type_summon # OK 

    def deplacer_unite(self,position_depart, liste_pos):
        self.d_move[self.conv(position_depart)] = [self.l_conv(x) for x in liste_pos]
    
    def attaquer_position(self,position_depart, position_arrivee):
        self.d_attack[self.conv(position_depart)] = self.l_conv(position_arrivee) # check double array
    
    def build(self,pos_inge, pos_build, type_build):
        self.d_build[self.conv(pos_inge)] = [self.l_conv(pos_build), type_build]
    
    def get_json_turn(self):
        full_dict = {}
        for (d, final_key) in zip([self.d_attack, self.d_mine, self.d_build, self.d_summon, self.d_move], ["attack", "mine", "build", "summon", "move"]):
            cpd = {}
            for (key, value) in d.items():
                cpd[str(list(key))] = value
            full_dict[final_key] = cpd
        return full_dict
    # etc etc, bref notre API interne pour nous faciliter la vie