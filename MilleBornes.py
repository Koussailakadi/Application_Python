import pandas as pd
from datetime import datetime
import random
from cartes import Cartes
from JoueurHumain import JoueurHumain
from JoueurAI import JoueurAI

#Nom: koussaila KADI
#Nom : Nathaniel DAHON

class MilleBornes:
    def __init__(self):
        self.nbJoueur=0
        self.paquetCarte=Cartes().paquetCarte  #objet carte
        self.paquetCarteMelange=None           #dict de cartes
        self.pioche=None                       #dict de cartes de la pioche
        self.cartesEnMainJoueurs=None          #dict de cartes
        self.ListNomJoueurs=[]              #list
        self.ListJoueurs=None                  #List d'objets joueur
        self.ListcartesEnMainJoueurs=None      #list
        self.stop=0 #stop game
        self.Tour=0
        self.coutTourDeTable=0
        self.objCarte=Cartes()                 #objet carte
        self.attaque=Cartes().attaque          #objet cartes attaque
        self.defense=Cartes().defense          #objet cartes defense
        self.annuler=0
        self.condition=1
        self.objJoueurH=JoueurHumain()
        self.objJoueurAI=JoueurAI()

    def starNewGame(self,nbJoueur=None):
        print('date:',datetime.now().date())
        print('----------------------------\n' + 'bienvenue Au Jeu 1000 bornes\n----------------------------')
        nbJoueur=int(input('combien de Joueurs ?'))
        self.nbJoueur = nbJoueur

    def initialisation(self):
        ListNomJoueurs = [[] for i in range(self.nbJoueur)]
        for i in range(self.nbJoueur):
            Nom_typeJoueur = input('entrer: Nom de Joueur,Type(0->AI | 1->Humain): ')
            Nom_typeJoueur=list(Nom_typeJoueur.split(","))
            ListNomJoueurs[i].append(Nom_typeJoueur[0])
            ListNomJoueurs[i].append(int(Nom_typeJoueur[1]))
        self.ListNomJoueurs=ListNomJoueurs
        print('Liste joueurs participants /initialisation (): OK\n')
        self.separateurAffichage()

    def melangerCarte(self):
        L=list(self.paquetCarte.values())
        random.shuffle(L)
        parquetCarteMelange={ i : L[i] for i in range(0,len(L) )}
        self.parquetCarteMelange=parquetCarteMelange

    def destribuerCarte(self):
        ListcartesEnMainJoueurs=[[] for i in range(self.nbJoueur)]  #creer une matrice nbJ*6
        values=self.parquetCarteMelange.values()
        listpaquetCarte = list(values)
        self.pioche={}
        cartesEnMainJoueurs = {}
        for i in range(6):
            variableAleatoire = random.randint(0, 2)
            for j in range(self.nbJoueur):
                ListcartesEnMainJoueurs[j].append(listpaquetCarte[variableAleatoire])   #distribuer une carte
                listpaquetCarte.pop(variableAleatoire)                                  #supprimer la carte distribué
        self.pioche=listpaquetCarte
        for i in range(len(ListcartesEnMainJoueurs)):
            cartesEnMainJoueurs[i] = {j: ListcartesEnMainJoueurs[i][j] for j in range(len(ListcartesEnMainJoueurs[i]))}
        self.cartesEnMainJoueurs=cartesEnMainJoueurs            #carte sous forme d'un dictionnaire
        self.ListcartesEnMainJoueurs=ListcartesEnMainJoueurs    #carte sous forme d'une liste

    def creationListJoueur(self):
        ListJoueurs = []
        for j, i in enumerate(self.ListNomJoueurs):
            if i[1] == 0:
                p = JoueurAI(i[0], self.cartesEnMainJoueurs[j], self.pioche,score=0)
                ListJoueurs.append(p)
            elif i[1] == 1:
                p = JoueurHumain(i[0], self.cartesEnMainJoueurs[j], self.pioche,score=0)
                ListJoueurs.append(p)
            self.ListJoueurs = ListJoueurs
        for joueur in self.ListJoueurs:
            joueur.ListJoueurs=ListJoueurs

    def gererTour(self):
        if self.Tour== self.nbJoueur-1:
            self.Tour = 0
            self.coutTourDeTable+=1  # compter les tours de table
        else:
            self.Tour += 1   # tour de jouer

    def gererJeu(self,):
        ListScore=[0 for i in range(self.nbJoueur)]
        while self.ListJoueurs[self.Tour].score <= 1000 and self.stop == 0:
            self.separateurAffichage()
            if self.ListJoueurs[self.Tour].score < 1000 and self.stop == 0:
                condition = 1
                ListScore[self.Tour] = self.ListJoueurs[self.Tour].score
                if self.annuler == 0:self.ListJoueurs[self.Tour].piocherCarte()  # piocher une carte
                self.annuler, choix, carteJouee = self.ListJoueurs[self.Tour].jouerCarte()  # joueur une carte
                ListScore[self.Tour]=self.ListJoueurs[self.Tour].score
                typeCarte = self.objCarte.TypeCarte(carteJouee)  # tester le type de carte jouée
                #vérifier le score du joueur
                # fin de la partie
                if self.ListJoueurs[self.Tour].score == 1000:
                    classement=[]
                    print('\n\n\n')
                    ListScore.sort(reverse=True)
                    for Joueur in self.ListJoueurs:
                        for ind, score in enumerate(ListScore):
                            if Joueur.score==score:
                                classement.append(Joueur.nom)
                    dict={'classement':classement,'score':ListScore}
                    mes='\n-----------------------------------\n'
                    mes +='         fin de la partie           '
                    mes+='\n-----------------------------------\n'
                    print(mes,pd.DataFrame.from_dict(dict))

                    print('Bravo !!!!\nle gagnat est {} score : {}'.format(self.ListJoueurs[self.Tour].nom,self.ListJoueurs[self.Tour].score))
                    self.stop = 1

                if typeCarte == 'botte' and self.annuler == 0:
                    print('vous avez jouée une botte =', carteJouee)
                    print('vous avez le droit de piocher et de jouer à nouveau !')
                    continue

                elif self.annuler == 0:
                    self.gererTour()  # le tour suivant
                    # self.stop = int(input('stop='))


# methode d'affichage---------------------------------------------------------------
    def separateurAffichage(self):
        print('\n--------------------------------------\n')

    def afficherJoueur(self):
        L=[[] for i in range(self.nbJoueur)] #Nom,Type,Score
        nom_Joueurs=[self.ListJoueurs[i].nom for i in range(self.nbJoueur)]
        type_Joueurs=[self.ListJoueurs[i].TypeJoueur(self.ListJoueurs[i]) for i in range(self.nbJoueur)]
        score_Joueurs=[self.ListJoueurs[i].score for i in range(self.nbJoueur)]
        data={'Nom':nom_Joueurs,'Type':type_Joueurs,'score':score_Joueurs}
        print('data joueurs: \n',pd.DataFrame.from_dict(data))
        self.separateurAffichage()

    def afficherCartedesJoeurs(self):
        data={str(i)+':'+str(self.ListJoueurs[i].nom):self.ListcartesEnMainJoueurs[i] for i in range(len(self.ListJoueurs))}
        print('les cartes distribuées pour chaque joueur:\n',pd.DataFrame.from_dict(data))
        self.separateurAffichage()

    def afficherPaquetCarte(self,paquetCarte=Cartes().paquetCarte):
        print(paquetCarte)


