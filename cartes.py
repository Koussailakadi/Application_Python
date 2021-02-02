class Cartes:
    def __init__(self):
        self.attaque={0:'accident' ,1:'roue_crevee', 2:'panne_escense', 3:'limitation_vitesse',4:'feu_rouge'}
        self.defense = {0:'reparation', 1:'roue_reparee', 2:'remplissage_essence', 3: 'fin_limitation_vitesse', 4:'feu_vert'}
        self.distance={0:25,1:50,2:75,3:100,4:200}
        self.jokers={0:'as_du_volant',1:'camion_citerne',2:'roue_increvable',3:'prioritaire'}
        self.paquetCarte=self.__paquetCarte()


    def __paquetCarte(self):
        paquet={}
        for i in range(106):
            if i<10   :paquet[i] = self.distance[0]
            elif i<20 :paquet[i] = self.distance[1]
            elif i<30 :paquet[i] = self.distance[2]
            elif i<42 :paquet[i] = self.distance[3]
            elif i<46 :paquet[i] = self.distance[4]
            elif i<52 :paquet[i] = self.defense[0]
            elif i<58 :paquet[i] = self.defense[1]
            elif i<64 :paquet[i] = self.defense[2]
            elif i<70 :paquet[i] = self.defense[3]
            elif i<84 :paquet[i] = self.defense[4]
            elif i<87 :paquet[i] = self.attaque[0]
            elif i<90 :paquet[i] = self.attaque[1]
            elif i<93 :paquet[i] = self.attaque[2]
            elif i<97 :paquet[i] = self.attaque[3]
            elif i<102 :paquet[i] = self.attaque[4]
            elif i<103 :paquet[i] = self.jokers[0]
            elif i<104 :paquet[i] = self.jokers[1]
            elif i<105 :paquet[i] = self.jokers[2]
            elif i<106 :paquet[i] = self.jokers[3]
        return paquet

    def ChercherCarte(self,nomCarte):
        nombreCarte ={}
        for key, value in self.paquetCarte.items():
            if value == nomCarte:
                nombreCarte[key] = value
        res='\n---------------------------\n'
        res+='nombre de carte de type - {} - : {}\nCarte: {}'.format(nomCarte,len(nombreCarte),nombreCarte)
        print(res)

    def get_key(self,nomCarte):
        for key, value in self.paquetCarte.items():
            if value == nomCarte:
                return key

    def TypeCarte(self,carte=None):
        if carte in list(self.attaque.values()):
            return 'attaque'
        elif carte in list(self.defense.values()):
            return 'defense'
        elif carte in list(self.distance.values()):
            return 'distance'
        elif carte in list(self.jokers.values()) :
            return 'botte'
        else: return 'defausse'

"""carte=Cartes()
paquetCarte=carte.paquetCarte
print('nombre total de cartes:',len(paquetCarte))
print('paquet de carte:\n',paquetCarte)
carte.ChercherCarte('feu_rouge')
paquetCarteMalange=carte.paquetCarteMelange
print('paquet de carte melangé :\n',paquetCarteMalange)"""
