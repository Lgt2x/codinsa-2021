class Batiment:
    def __init__(self, appartenance, position):
        #TODO: modifier une fois le format de data definie
        self.appartenance = appartenance # 0 : pas a  nous 
        self.position = position
    
class Ecole(Batiment):
    identifiant='S'
    cout=None
    pv=240
    attaque=None
    distanceAttaque=None
    pointGagnes=100
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class Amphi(Batiment):
    identifiant='C'
    cout=250
    pv=160
    attaque=None
    distanceAttaque=None
    pointGagnes=60
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
class Tourelle(Batiment):
    identifiant='T'
    cout=70
    pv=60
    attaque=35
    distanceAttaque=2
    pointGagnes=30
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class Mur(Batiment):
    identifiant='W'
    cout=30
    pv=120  
    attaque=None
    distanceAttaque=None
    pointGagnes=15
    def __init__(self, **kwargs):
        super().__init__(**kwargs)