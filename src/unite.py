class Unite:
    def __init__(self, appartenance, position):
        self.appartenance = appartenance
        self.position = position


class Ingenieur(Unite):
    """ Roles : 0 : non affecté
                1 : déplacement vers la mine
                2 : en train de miner
                3 : se déplacer vers la caserne
    """
    role=0
    target = None
    identifiant='V'
    cout=20
    pv=20
    attaque=10
    pointMouvement=2
    pointGagnes=10
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)

class ULegere(Unite):
    target = None
    identifiant='L'
    cout=30
    pv=60
    attaque=20
    pointMouvement=4
    pointGagnes=15
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ULourde(Unite):
    target = None
    identifiant='H'
    cout=100
    pv=100
    attaque=40
    pointMouvement=2
    pointGagnes=35
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
