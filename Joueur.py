from abc import ABC,abstractmethod
from cartes import Cartes
import pandas as pd

class Joueur(ABC):
    def __init__(self,nom=None,cartesHasard=None,pioche=None,score=None):
        self.nom=nom                     # String
        self.cartesHasard=cartesHasard   # dict
        self.ListcartesHasard=[]
        self.pioche=pioche               # list
        self.score=score                 # integer
        self.objCarte = Cartes()      # objt carte
        self.pilleBotte=[]
        self.attaque_recus = ['feu_rouge']  # list, Feu-rouge, il faut un feu-vert pour rouler
        self.Borne=[]
        self.attaque = Cartes().attaque  # objet cartes attaque
        self.defense = Cartes().defense  # objet cartes defense


    @abstractmethod
    def jouerCarte(self,help=0,condition=1):
        pass

    @abstractmethod
    def TypeJoueur(self,objJoueur=None):
        pass

    #methode pour récupérer la liste des joueurs dans MilleBornes
    def getListJoueurs(self,ListJoueurs):
        self.ListJoueurs=ListJoueurs

    def piocherCarte(self):
        self.cartesHasard[6]=self.pioche[0]
        del(self.pioche[0])
        carte=Cartes()
        L=[]
        for x in self.cartesHasard.values():
            L.append(carte.TypeCarte(x))
        L.append('Defausser')
        self.ListcartesHasard=[x for x in self.cartesHasard.values()]
        L_carte=[self.cartesHasard[i] for i in range(len(self.cartesHasard))]
        L_carte.append('une  carte')
        data={'type carte':L,'Nom:'+self.nom:L_carte}
        print('cartes du joueur:\n',pd.DataFrame.from_dict(data))

    def  defausser(self,pos):
        del (self.cartesHasard[pos])  # supprimé la carte jouée
        self.ListcartesHasard = [i for i in self.cartesHasard.values()]
        self.cartesHasard = {i: j for i, j in enumerate(self.ListcartesHasard)}

    def supprimerCarte(self,pos):
        del (self.cartesHasard[pos])  # supprimé la carte jouée
        self.ListcartesHasard = [i for i in self.cartesHasard.values()]
        self.cartesHasard = {i: j for i, j in enumerate(self.ListcartesHasard)}

    def attaqueDefense(self):
        ListCarteDefense = []
        ListCarteAttaque = []
        ListCarteBotte = []
        if len(self.attaque_recus)==0: #pas d'attaque recu
            ListCarteAttaque=ListCarteDefense=ListCarteBotte= ['None','None']
            return ListCarteAttaque,ListCarteDefense,ListCarteBotte # par defaut
        elif len(self.attaque_recus)!=0:
            for x in self.attaque_recus:
                if x== 'feu_rouge':
                    ListCarteAttaque.append('feu_rouge'); ListCarteDefense.append('feu_vert'); ListCarteBotte.append('prioritaire')
                elif x== 'limitation_vitesse':
                    ListCarteAttaque.append('limitation_vitesse'); ListCarteDefense.append('fin_limitation_vitesse'); ListCarteBotte.append('prioritaire')
                elif x== 'panne_escense':
                    ListCarteAttaque.append('panne_escense'); ListCarteDefense.append('remplissage_essence'); ListCarteBotte.append('camion_citerne')
                elif x== 'roue_crevee':
                    ListCarteAttaque.append('roue_crevee'); ListCarteDefense.append('roue_reparee'); ListCarteBotte.append('roue_increvable')
                elif x== 'accident':
                    ListCarteAttaque.append('accident');ListCarteDefense.append('reparation');ListCarteBotte.append('as_du_volant')
                else: print('erreur sur les AttaqueDefense')
            return ListCarteAttaque, ListCarteDefense, ListCarteBotte


