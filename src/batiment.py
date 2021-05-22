class Batiment:
    def __init__(self,data):
        #TODO: modifier une fois le format de data definie
        self.appartenance = 0 # 0 : pas a  nous 
        self.vie = 0
        self.type = 0
        self.position = 0
    
class Ecole:

    identifiant='S'
    cout=None
    pv=240
    attaque=None
    distanceAttaque=None
    pointGagnes=100

class Amphi:

    identifiant='C'
    cout=250
    pv=160
    attaque=None
    distanceAttaque=None
    pointGagnes=60

class Tourelle:

    identifiant='T'
    cout=70
    pv=60
    attaque=35
    distanceAttaque=2
    pointGagnes=30

class Mur:

    identifiant='W'
    cout=30
    pv=120  
    attaque=None
    distanceAttaque=None
    pointGagnes=15
