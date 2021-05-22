class Unite:
    def __init__(self,data):
        super().__init__()
        #TODO: modifier une fois le format de data definie
        self.appartenance = 0
        self.vie = 0
        self.type = 0
        self.position = 0
    


class Ingenieur:

    identifiant='V'
    cout=20
    pv=20
    attaque=10
    pointMouvement=2
    pointGagnes=10

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
