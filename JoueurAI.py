from Joueur import Joueur
from random import shuffle,randint

class JoueurAI(Joueur):
    def __init__(self,nom=None,cartesHasard=None,pioche=None,score=None,NiveauDuJeu=1,ListJoueurs=None):
        super().__init__(nom,cartesHasard,pioche,score)
        self.NiveauDuJeu=NiveauDuJeu
        self.ListJoueurs=ListJoueurs


    def TypeJoueur(self,objJoueur=None):

        if isinstance(objJoueur,JoueurAI):
            return 'Robot'
        else:
            return 'Defausse'

    def jouerCarte(self,help=0,condition=1):
        print("jouer carte AI")
        res1 = ' '
        if len(self.attaque_recus) != 0:
            for x in self.attaque_recus:
                res1 += str(x) + ','
        res2 = ' '
        if len(self.pilleBotte) != 0:
            for y in self.pilleBotte:
                res2 += str(y) + ','
        print("tour de jeu : {} (score:{},{}{})".format(self.nom, self.score, res1, res2))
        if self.NiveauDuJeu==1:
            annuler, choix, carteJouee=self.AI_niveau1()
            if self.objCarte.TypeCarte(carteJouee)!='defausse':
                print('carte jouée : {} ,type: {}, updated score: {}'.format(carteJouee, self.objCarte.TypeCarte(carteJouee),self.score))
            return annuler, choix, carteJouee


    def updateScore(self,ListCarteDistance,iter=0):
        for iter,carteJouee in enumerate(ListCarteDistance):
            if self.score > 800 and self.score < 900:
                if carteJouee == 200: # ne pas jouer la carte
                    continue
                else:
                    ind = ListCarteDistance.index(carteJouee)
                    self.supprimerCarte(ind)
                    annuler = 0
                    choix = 0
                    return annuler, choix, carteJouee

            elif self.score == 900 :
                if  carteJouee == 200:
                    continue
                else:
                    ind = ListCarteDistance.index(carteJouee)
                    self.supprimerCarte(ind)
                    annuler = 0
                    choix = 0
                    return annuler, choix, carteJouee

            elif self.score == 925:
                if  carteJouee == 100 or carteJouee == 200:
                    continue
                else:
                    ind = ListCarteDistance.index(carteJouee)
                    self.supprimerCarte(ind)
                    annuler = 0
                    choix = 0
                    return annuler, choix, carteJouee

            elif self.score == 950:
                if carteJouee == 75 or carteJouee == 100 or carteJouee == 200:
                    continue
                else:
                    ind = ListCarteDistance.index(carteJouee)
                    self.supprimerCarte(ind)
                    annuler = 0
                    choix = 0
                    return annuler, choix, carteJouee

            elif self.score == 975:
                if carteJouee == 50 or carteJouee == 75 or carteJouee == 100 or carteJouee == 200:
                    continue
                else:
                    ind = ListCarteDistance.index(carteJouee)
                    self.supprimerCarte(ind)
                    annuler = 0
                    choix = 0
                    return annuler, choix, carteJouee

        choix = randint(0, len(self.cartesHasard) - 1)
        carteJouee = self.cartesHasard[choix]
        self.supprimerCarte(choix)
        print('carte défaussée avec succès :{}'.format(carteJouee))
        annuler = 0
        choix = 0
        return annuler, choix, 'defausse'

    def AI_niveau1(self):
        indicecarteDistance=[]
        ListCarteDistance =[]
        ListCarteAttaque, ListCarteDefense, ListCarteBotte=self.attaqueDefense()
        # se defendre:
        if len(self.attaque_recus) != 0:
            for j, attaque in enumerate(ListCarteAttaque):
                for i, x in enumerate(list(self.cartesHasard.values())):
                    if x in ListCarteDefense:  # jouer la carte défense
                        carteJouee = self.cartesHasard[i]
                        self.supprimerCarte(i)
                        self.attaque_recus.pop(j)  # annuler l'effet d'attaque
                        annuler = 0
                        choix = 0
                        return annuler, choix, carteJouee
                    elif x in ListCarteBotte:
                        carteJouee = self.cartesHasard[i]
                        self.supprimerCarte(i)
                        self.attaque_recus.pop(j)  # annuler l'effet d'attaque
                        annuler = 0
                        choix = 0
                        return annuler, choix, carteJouee
                    elif i == len(self.cartesHasard)-1:
                        choix=randint(0,len(self.cartesHasard)-1)
                        carteJouee = self.cartesHasard[choix]
                        self.supprimerCarte(choix)
                        print('carte défaussée avec succès :{}'.format(carteJouee))
                        annuler = 0
                        choix = 0
                        return annuler, choix, 'defausse'

        elif len(self.attaque_recus) == 0:
            for i,x in enumerate(list(self.cartesHasard.values())):
                if x in list(self.objCarte.distance.values()):  #
                    indicecarteDistance.append(i)
                    ListCarteDistance.append(self.cartesHasard[i])

        # soit rouler
            if  len(indicecarteDistance) !=0 and self.score<=800:  # choix carte distance d'une maniere aléatoire
                shuffle(indicecarteDistance)
                ind = indicecarteDistance[0]
                carteJouee = self.cartesHasard[ind]
                print('la carte choisie: ', carteJouee)
                print('indice cartes distance', indicecarteDistance)
                self.score += carteJouee
                self.supprimerCarte(ind)
                annuler = 0
                choix = 0
                return annuler, choix, carteJouee
            elif len(indicecarteDistance) !=0 and self.score>800:
                    annuler, choix, carteJouee=self.updateScore(ListCarteDistance)
                    if carteJouee != 'defausse':
                        self.score += carteJouee
                    annuler = 0
                    choix = 0
                    return annuler, choix, carteJouee

        # defausser
            elif len(indicecarteDistance) ==0 :
                choix = randint(0, len(self.cartesHasard) - 1)
                carteJouee = self.cartesHasard[choix]
                self.supprimerCarte(choix)
                print('carte défaussée avec succès :{}'.format(carteJouee))
                annuler = 0
                choix = 0
                return annuler, choix, 'defausse'

