class Unite:
    def __init__(self, appartenance, position):
        super().__init__()
        #TODO: modifier une fois le format de data definie
        self.appartenance = appartenance
        self.position = position
    


class Ingenieur(Unite):
    identifiant='V'
    cout=20
    pv=20
    attaque=10
    pointMouvement=2
    pointGagnes=10
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
class ULegere(Unite):
    identifiant='L'
    cout=30
    pv=60
    attaque=20
    pointMouvement=4
    pointGagnes=15
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class ULourde(Unite):
    identifiant='H'
    cout=100
    pv=100
    attaque=40
    pointMouvement=2
    pointGagnes=35
    def __init__(self, **kwargs):
        super().__init__(**kwargs)