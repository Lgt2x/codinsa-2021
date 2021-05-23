class Unite:
    def __init__(self,data):
        super().__init__()
        #TODO: modifier une fois le format de data definie
        self.appartenance = 0
        self.vie = 0
        self.type = 0
        self.position = 0


class Ingenieur:
    """ Roles : 0 : non affecté
                1 : déplacement vers la mine
                2 : en train de miner
                3 : se déplacer vers la caserne
    """
    def __init__(self) -> None:
        self.role=0
        self.target = None
        self.identifiant='V'
        self.cout=20
        self.pv=20
        self.attaque=10
        self.pointMouvement=2
        self.pointGagnes=10

class ULegere:

    identifiant='L'
    cout=30
    pv=60
    attaque=20
    pointMouvement=4
    pointGagnes=15

class ULourde:

    identifiant='H'
    cout=100
    pv=100
    attaque=40
    pointMouvement=2
    pointGagnes=35
