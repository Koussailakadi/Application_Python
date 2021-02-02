from Joueur import Joueur

class JoueurHumain(Joueur):
    def __init__(self, nom=None, cartesHasard=None, pioche=None, score=None,ListJoueurs=None):
        super().__init__(nom, cartesHasard, pioche, score)
        self.annuler=0
        self.ListJoueurs=ListJoueurs

    def TypeJoueur(self,objJoueur=None):
        if isinstance(objJoueur,JoueurHumain):
            return 'Humain'
        else:
            print('vous avez oublié l\'objet joueur en argument')

    def getChoix(self, condition=1):
        while condition == 1:
            print('entrer un choix entre 0 et 7:')
            try:
                choix = int(input('choix :'))
                if choix >= 0 and choix <= 7:
                    condition = 0  # condition de fin de boucle
                    return choix
                else:
                    print('votre choix doit etre 0 et 7')
                    continue
            except:
                print('erreur!')
                continue

    def help(self,help=1):
        print('help activated !')
        if help == 1:  # afficher les helps : chercher un feu vert ou une carte correspondante
            for i, x in enumerate(self.cartesHasard.values()):
                if x == 'feu_vert':
                    print('help: feu_vert :' + str(i))
                elif x == 'prioritaire':
                    print('help: prioritaire :' + str(i))
                elif x in self.objCarte.attaque.values():
                    print('help: attauqer !', x, 'positon', i)
                else:
                    if i==len(self.cartesHasard): print('help: defausser une carte en choisissant 7')


    def RegleJeu(self,condition=1,carteAttaque=None,carteDefense=None,carteBotte=None):
        annuler=0  #varaible utiliser dans MillesBorne
        while condition == 1:
            choix = self.getChoix()  # une valeur de 0-7
            if choix >= 0 and choix < 7:
                carteChoisi = self.cartesHasard[choix]
            # se defendre
            if len(self.attaque_recus) != 0 and choix != 7:
                for i in range(len(self.attaque_recus)):
                    # carteAttaque='feu_rouge' , carteDefense='feu_vert', carteBotte='prioritaire',carteChoisi=carteChoisi,choix=choix
                    if carteChoisi == carteDefense[i]:
                        self.attaque_recus.pop(i)  # annuler l'effet de feu rouge
                        self.supprimerCarte(choix)  # supprimer la carte jouer
                        condition = 0
                        annuler=0
                        return annuler,choix, carteChoisi
                    elif carteChoisi == carteBotte[i]:
                        self.attaque_recus.pop(i)  # annuler effet feu rouge
                        self.pilleBotte.append(carteChoisi)  # ajouter la botte
                        self.supprimerCarte(choix)  # supprimer la carte jouer
                        annuler=0
                        condition = 0
                        return annuler,choix, carteChoisi
                    elif carteChoisi in list(self.objCarte.distance.values()):
                        if carteAttaque[i] == 'limitation_vitesse':
                            print('vous ne pouvez rouler à une vitesse > 50 KM !')
                            if carteChoisi > 50:
                                print('help: vitesse limitée, roulez à <50KM')
                                continue
                            elif carteChoisi <= 50:
                                self.Borne.append(carteChoisi)
                                self.score += carteChoisi  # update score
                                self.supprimerCarte(choix)  # supprimer la carte jouer
                                annuler=0
                                condition = 0
                                return annuler,choix, carteChoisi
                        else:
                            print('vous ne pouvez rouler, à cause de : ' + str(carteAttaque))
                            self.help()
                            continue
                    else:
                        if carteChoisi in list(self.objCarte.defense.values()):
                            print('help: vous ne pouvez pas jouer que la carte defense: ' + str(carteDefense))
                            continue
                        elif carteChoisi in list(self.objCarte.jokers.values()):
                            self.pilleBotte.append(carteChoisi)  # rajouer à la pille
                            self.supprimerCarte(choix)  # supprimer la carte jouer
                            annuler = 0
                            condition = 0
                            return annuler,choix, carteChoisi  # la carte soit botte
                        elif carteChoisi in list(self.objCarte.attaque.values()):
                            self.gererAttaqueHumain(carteJouee=carteChoisi,choix=choix)
                            condition = 0
                            annuler=self.annuler
                            return annuler,choix, carteChoisi  # la carte attaque


            elif len(self.attaque_recus) == 0 and choix != 7:
                if carteChoisi in list(self.objCarte.defense.values()):
                    print('help: carte defense se joue en cas d\'attaque recu')
                    continue
                elif carteChoisi in list(self.objCarte.distance.values()):
                    self.score += carteChoisi
                    self.Borne.append(carteChoisi)
                    self.supprimerCarte(choix)  # supprimer la carte choisi
                    annuler=0
                    condition = 0
                    return annuler,choix,carteChoisi
                elif carteChoisi in list(self.objCarte.jokers.values()):
                    self.pilleBotte.append(carteChoisi)  # rajouer à la pille
                    self.supprimerCarte(choix)  # supprimer la carte jouer
                    annuler = 0
                    condition = 0
                    return annuler,choix,carteChoisi
                elif carteChoisi in list(self.objCarte.attaque.values()):
                    self.gererAttaqueHumain(carteJouee=carteChoisi, choix=choix)
                    condition = 0
                    annuler = self.annuler
                    return annuler,choix,carteChoisi  # carte attaque

            elif choix == 7:
                print('defausser une carte:')
                ind = self.getChoix()
                if ind < 7:
                    print('carte {} : {} est défaussée avec succès!'.format(self.objCarte.TypeCarte(self.cartesHasard[ind]),self.cartesHasard[ind]))
                    carteDefaussee=self.cartesHasard[ind]
                    self.supprimerCarte(ind)  # supprimer la carte jouer
                    condition = 0
                    annuler=0
                    return annuler,choix,str(carteDefaussee)+' defaussée !'
                else:
                    print('erreur ! maivais choix, carte non defausser')
                    continue

    def gererAttaqueHumain(self,carteJouee, choix, condition=1):
        self.annuler = 0
        condition = 1
        while condition == 1 and self.annuler == 0:
            self.annuler = int(input('entrer (1/annuler) -(0/valier) l\'attaque:'))
            if self.annuler == 1:
                print('help: l\'attaque est annulée!')
                condition = 0
                break
            else:
                adversaire = input('Nom de l\'adversaire: ')
                for joueur in self.ListJoueurs:
                    if adversaire == joueur.nom:
                        Botte = joueur.pilleBotte
                        attaques_recus = joueur.attaque_recus
                        if len(attaques_recus) == 2:
                            print('help: vous ne pouvez pas attaquer: {} car il a subit 2 attaques {}'.format(
                                joueur.nom, attaques_recus))
                            print('help: choisi un autre adversaire sinon annuler l\'attaque')
                            continue
                        elif len(Botte) == 0:  # pas de botte
                            if len(attaques_recus) == 0:  # pas d'attaque reçu
                                joueur.attaque_recus.append(carteJouee)  # attaquer
                                self.supprimerCarte(choix)  # supprimer la carte attaque jouée
                                self.annuler = 0
                                condition = 0
                            elif len(attaques_recus) == 1:  # une attaque deja reçue
                                if attaques_recus[
                                    0] == 'limitation_vitesse' and carteJouee != 'limitation_vitesse':
                                    joueur.attaque_recus.append(carteJouee)  # eviter 2 fois limitation vitesse
                                    self.supprimerCarte(choix)  # supprimer la carte attaque jouée
                                    self.annuler = 0
                                    condition = 0
                                elif attaques_recus[0] != 'limitation_vitesse' and carteJouee == 'limitation_vitesse':
                                    joueur.attaque_recus.append(carteJouee)
                                    self.supprimerCarte(choix)  # supprimer la carte attaque jouée
                                    self.annuler = 0
                                    condition = 0
                                elif attaques_recus[0] != 'limitation_vitesse' and carteJouee != 'limitation_vitesse':
                                    print('help: vous ne pouvez pas attaquer {} car il a déjà subi {}'.format(
                                        joueur.nom, attaques_recus))
                                    print('help: choisi un autre adversaire sinon annuler l\'attaque')
                                    print(self.annuler)
                                    continue
                                else:
                                    print('erreur!')
                                    continue

                        elif len(Botte) != 0:
                            if 'as_du_volant' in Botte:
                                if carteJouee == 'accident':
                                    print('help: impossible d\'attaquer: {} car il a une botte: {}'.format(
                                        joueur.nom, 'as_du_volant'))
                                    print('help: choisi un autre adversaire sinon annuler l\'attaque')
                                    continue
                                else:
                                    joueur.attaque_recus.append(carteJouee)
                                    self.supprimerCarte(choix)  # supprimer la carte attaque jouée
                                    print('attaque aacèptée !')
                                    self.annuler = 0
                                    condition = 0
                            elif 'camion_citerne' in Botte:
                                if carteJouee == 'panne_escense':
                                    print('help: impossible d\'attaquer: {} car il a une botte: {}'.format(
                                        joueur.nom, 'camion_citerne'))
                                    print('help: choisi un autre adversaire sinon annuler l\'attaque')
                                    continue
                                else:
                                    joueur.attaque_recus.append(carteJouee)
                                    self.supprimerCarte(choix)  # supprimer la carte attaque jouée
                                    print('attaque aaceptée !')
                                    self.annuler = 0
                                    condition = 0
                            elif 'roue_increvable' in Botte:
                                if carteJouee == 'roue_crevee':
                                    print('help: impossible d\'attaquer: {} car il a une botte: {}'.format(
                                        joueur.nom, 'roue_increvable'))
                                    print('help: choisi un autre adversaire sinon annuler l\'attaque')
                                    continue
                                else:
                                    joueur.attaque_recus.append(carteJouee)
                                    self.supprimerCarte(choix)  # supprimer la carte attaque jouée
                                    print('attaque acceptée !')
                                    self.annuler = 0
                                    condition = 0
                            elif 'prioritaire' in Botte:
                                if carteJouee == 'feu_rouge' or carteJouee == 'limitation_vitesse':
                                    print('help: impossible d\'attaquer: {} car il a une botte: {}'.format(
                                        joueur.nom, 'prioritaire'))
                                    print('help: choisi un autre adversaire sinon annuler l\'attaque')
                                    continue
                                else:
                                    joueur.attaque_recus.append(carteJouee)
                                    self.supprimerCarte(choix)  # supprimer la carte attaque jouée
                                    print('attaque acceptée !')
                                    self.annuler = 0
                                    condition = 0
                            else:
                                print('erreur sur les bottes! ')
                                continue
                        else:
                            print('erreur sur la partie ou len(botte)!=0')
                            continue
                    else : pass



    def jouerCarte(self,help=0,condition=1):
        res1 = ' '
        if len(self.attaque_recus) != 0:
            for x in self.attaque_recus:
                res1 += str(x) + ','
        res2 = ' '
        if len(self.pilleBotte) != 0:
            for y in self.pilleBotte:
                res2 += str(y) + ','
        print("tour de jeu : {} (score:{},{}{})".format(self.nom, self.score, res1, res2))
        carteAttaque, carteDefense, carteBotte = self.attaqueDefense()
        annuler, choix, carteJouee = self.RegleJeu(carteAttaque=carteAttaque, carteDefense=carteDefense,carteBotte=carteBotte)
        return annuler, choix, carteJouee
