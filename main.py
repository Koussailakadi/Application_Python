from MilleBornes import MilleBornes

#Nom: koussaila KADI
#Nom : Nathaniel DAHON
#Groupe B   _ISI

def main():

    game = MilleBornes()
    mes='explication pour la saisi:\nNombre de joueur? entier\nNom de joueurs et type: koussaila,1 (il faut respecter cette forme)\n'
    mes+='donc ici, koussaila c\'est le nom du joueur et \'1\'  c\'est le type Humain\n'
    mes+='\nexemple partie AI :\nnombre de joueurs? 2\njoueur 1: AI_kouss,0\njoueur 2: AI_nath,0\n'
    print(mes)
    game.starNewGame()
    game.initialisation()
    game.melangerCarte()
    game.destribuerCarte()
    game.creationListJoueur()
    game.afficherJoueur()
    game.afficherCartedesJoeurs()
    #rajout de la liste des joueurs pour chaque joueur
    for joueur in game.ListJoueurs:
        joueur.ListJoueurs=game.ListJoueurs
    #---------------------------
    #début de la partie
    game.gererJeu()


if __name__ == '__main__':
    main()
