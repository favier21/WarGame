from Armee import *
from Grille import *

#si n=4 il y a 81 possibilité
#si n=5 il y a 243 possibilité
#si n=6 il y a 729 possibilité


#fonction qui donne toute les possibilitées de n en base 3 selon la taille définis#
def possibilite(n):
    taille = n
    n = 4**n
    liste = []
    for a in range(0,n):
        r = True
        quotient = -10
        compo = []
        while r:
            if quotient != 0:
                quotient = a//3
                reste = a%3
                compo.insert(0,reste)
                a = quotient
            else:
                while len(compo) != taille:
                    compo.insert(0, 0)
                r = False
                liste.append(compo)
    return liste



    #change les nombres de la liste de liste generé par des lettres selon la valeur#

def attribuerFaction(armee,faction):
    for i,unite in enumerate(armee):
        if faction==1:
            armee[i]=unite + "1"
        else:
            armee[i]=unite + "2"

    #transforme la liste de possibilité en caractere par exemple 1-->a pour archer
def armpsb(tab):#armpsb pour armée possibilité
    for i in range(len(tab)):
        for l in range(len(tab[0])):
            if tab[i][l] == 0:
                tab[i][l] = "s"
            elif tab[i][l] == 1:
                tab[i][l] = "a"
            elif tab[i][l] == 2:
                tab[i][l] = "c"
            elif tab[i][l] == 3:
                tab[i][l] = "m"
    return tab


    #fait rencontrer chaque possibilite d'armee contre toute les autres
    #pour ainsi obtenir un classement des meilleurs configuration d'armee
def rencontre(tab, armee):
    liste_des_rencontres = []
    points=0
    for i in range(len(tab)):

        composition_evaluee=tab[i]

        for j in range(len(tab)):

            tab1=copy.copy(composition_evaluee)
            tab2=copy.copy(tab[j])
            attribuerFaction(tab1,1)
            attribuerFaction(tab2,2)

            if combatsTest(armee,tab1,tab2)==2:
                points=points+1


        liste_des_rencontres = liste_des_rencontres + [[composition_evaluee]+[points]]
        points=0

    return liste_des_rencontres

    #fais la liste des points, en prenant la liste de résultat faite avec
    # la fonction rencontre
def listepoints(tab):
    t=[]
    for i in range(len(tab)):
        t=t+[tab[i][1]]
    return t

    # maxi correspond a la liste de points
    # liste = liste de possibilité
def listemeilleurs(liste):
    return sorted(liste, key=lambda x:x[1])

def classementComposition(classement,composition):# prend une liste triée et renvoie le classement de la composition en paramettre
    for i,composition_actuelle in enumerate(classement):
        if composition_actuelle[0] == composition:
            return abs(i - len(classement))

def genereClassement(armee):
    combinaisons = possibilite(armee.SIZE)
    combinaisons_converties = armpsb(combinaisons)
    classement_non_trie = rencontre(combinaisons_converties,armee)
    classement_trie = listemeilleurs(classement_non_trie)
    return classement_trie

def genereArmees(armee, nb_de_victoire_cible = 5 * Grille.SIZE):

    composition1 = armee.genereLigneAlea(1)

    composition2 = armee.genereLigneAlea(2)
    leader = []
    compteur_victoires = 0
    while compteur_victoires <= nb_de_victoire_cible:

        composition1,composition2 = evalueArmees(armee,composition1,composition2)
        compteur_victoires += 1
        if composition1 != leader:
            leader = composition1
            compteur_victoires = 0
    return list(compositionLisible(leader))


if __name__ == "__main__":
    pass
"""
def test_ps(a):
    q=a//3
    r=a%3
    print("quotient euclidien : ", q)
    print("reste euclidien : ", r)
    return ""
"""
