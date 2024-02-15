import copy
from Armee import *
from baseArmee import *
from time import sleep
class Grille:

    SIZE = Armee.SIZE
    """classe pour créer la grille et lui donner une dimension"""

    def __init__(self,grille):
        self.grille = grille

        for i,ligne in enumerate(self.grille): #
            for j,pion in enumerate(ligne) :
                self.grille[i][j]=construitPersonnage(pion,[i,j])

    def efface(self, i, j): #construitVide une case vide à la position donnée en ecrasant toute unitée sur place
        self.grille[i][j] = construitVide()

    def positionne(self, i, j, personnage):# place un personnage sur la grille à une position donnée en paramettre
        self.grille[i][j] = personnage

    def cheminLibre(self, i, j): # teste si la case à la position donnée est vide
        return self.grille[i][j].getType() == "vide"

    def selectFaction(self, fac):# cette fonction liste les unitées d'une faction donnée en paramettre
        liste_unite=[]
        for ligne in self.grille:
            for case in ligne:
                if case.faction == fac:
                    liste_unite.append(case)
        if liste_unite == []:
            return -1
        else:
            return liste_unite

    def info(self):#donne les informations de base (position,pv, type d'unitée) de chaque unitée sur le terrain
        return [[pion.info() for pion in ligne] for ligne in self.grille]

    def afficherGrille(self):# cette fonction sert à la démonstration du déroulement des simulation de bataille
        for ligne in self.grille:
            for case in ligne:
                print(case.toString(), end = " ")
            print()# cette fonction sert à la démonstration du déroulement des simulation de bataille,elle affiche la grille de manière lisible

    def tour(self,visuel=0):# cette fonction simule un tour, chaque unité dans le terrain se déplace vers son ennemie le plus proche et le combat si il est à portée, renvoie le numéro de la faction vaincue


        if self.selectFaction(2) == -1:
            return 2
        if self.selectFaction(1) == -1:
            return 1

        for unit in self.selectFaction(1):
            unit.allerEnemie(unit.trouverEnemie(self),self)
            if visuel==1:
                self.afficherGrille()
                print()
                sleep(0.7)

            if self.selectFaction(2) == -1:
                return 2

        for unit in self.selectFaction(2):
            unit.allerEnemie(unit.trouverEnemie(self),self)
            if visuel==1:
                self.afficherGrille()
                print()
                sleep(0.7)

            if self.selectFaction(1) == -1:
                return 1

    def combat(self,visuel=0):
        #si l'armée coute plus cher que le nb de points allouées à l'armée, alors les composant ne peuvent plus etre nouris faut d'une restriction bugetaire importante,ils seront donc pénalisé

        v=0
        while v != 1 and v != 2:
            v=self.tour(visuel)
        if v==1:
            if visuel==1:
                print("la faction 2 gagne")
            return -1
        else:
            if visuel==1:
                print("la faction 1 gagne")
            return 1

def combatsTest(armee,composition1,composition2,visuel=0):

    compo1 = copy.copy(composition1)
    compo2 = copy.copy(composition2)
    nb_victoire=0

    plan = armee.placerArmees(compo1,compo2)
    grille_de_test=Grille(plan)

    if not(armee.compterLesPoints(composition1)):
        armee.penaliseArmee(grille_de_test,int(list(composition1[0])[1]))
    if not(armee.compterLesPoints(composition2)):
        armee.penaliseArmee(grille_de_test,int(list(composition2[0])[1]))


    nb_victoire+=grille_de_test.combat()

    armee.changerFaction(composition1)
    armee.changerFaction(composition2)

    compo1 = copy.copy(composition1)
    compo2 = copy.copy(composition2)

    plan = armee.placerArmees(compo2,compo1)
    grille_de_test=Grille(plan)

    if not(armee.compterLesPoints(composition1)):
        armee.penaliseArmee(grille_de_test,int(list(composition1[0])[1]))
    if not(armee.compterLesPoints(composition2)):
        armee.penaliseArmee(grille_de_test,int(list(composition2[0])[1]))

    nb_victoire+=grille_de_test.combat(visuel)

    return nb_victoire #fait deux combats entre les composition 1 et 2 renvoie le nombre de nb_victoire de la compo1 2 = 2victoires de la 1 -2 = 2 victoire de la 3

def evalueArmees(armee,composition1,composition2):#utilise la fonction combatsTest pour évaluer deux composition d'armée, renvoie la composition gagnante et une version modifié de la composition perdante

    nb_victoire=combatsTest(armee,composition1,composition2)
    if nb_victoire == 2:
        return composition1,armee.mutationArmee(composition2)
    elif nb_victoire ==-2:
        return composition2,armee.mutationArmee(composition1)
    else:
        choix=random.randint(1,2)
        if choix == 1:
            return composition1,armee.mutationArmee(composition2)
        else:
            return composition2,armee.mutationArmee(composition1)


def compositionLisible(compo):#prend une composition sous forme de liste d'unitée et l'affiche
    composition_lisible=""
    for lettre in compo:
        composition_lisible=composition_lisible+str(list(lettre)[0])

    return composition_lisible

if __name__ == "__main__":

        A=Armee(130)
        print(genereArmees(A))






#    def afficherT(self):
#        for celx in self.cells:
#            for cell in celx:
#                print("-", end = " ")
#            print()

"""
for i in range(1,n+1):
    for j in range(1,n+1):
        if j<=n:
            print("-",end="")

        [[self.cells.add(construitPersonnage(self.grille[celx][cell])) for cell in celx] for celx in self.cells]

    print("")
"""
