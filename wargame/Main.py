from baseArmee import *
from sys import *


if len(argv) == 4:
    Armee.SIZE = int(argv[1])
    Grille.SIZE = int(argv[1])
    version_graphique = int(argv[2])
    nb_clible=int(argv[4])

elif len(argv) == 3:
    Armee.SIZE = int(argv[1])
    Grille.SIZE = int(argv[1])
    version_graphique = int(argv[2])
    nb_clible=0
elif len(argv) == 2:
    Armee.SIZE = int(argv[1])
    Grille.SIZE = int(argv[1])
    version_graphique = 0
    nb_clible= 0
else:
    version_graphique = 0
    nb_clible=0
print("La grille est de taille ",Armee.SIZE," sur ",Armee.SIZE)

print("La version graphique du moteur est ","activée" if version_graphique==1 else "désactivée")

print("L'algorithme génétique ne gardera que les armées qui on ",nb_clible if nb_clible!=0 else 5*Grille.SIZE,"victoires de suite")
sleep(1)
armee = Armee(200)
print()
print("démonstration du moteur avec le générateur aléatoire")


armee_exemple_1 = armee.genereLigneAlea(1)
armee_exemple_2 = armee.genereLigneAlea(2)

plan = armee.placerArmees(armee_exemple_1,armee_exemple_2)

grille = Grille(plan)

print(grille.combat(version_graphique))
if version_graphique==0:
    print("démonstration de l'algorithme de recherche systèmatique")

    classement = genereClassement(armee)

    print("voici le classement \n",classement,"\nL'arméee ",classement[-1][0]," est la meilleurs possible")

    print("démonstration de l'algorithme génétique")
    if nb_clible==0:
        armee_genetique = genereArmees(armee)
    else:
        armee_genetique = genereArmees(armee,nb_clible)

    print("l'armée qui à été selectionné est ",armee_genetique,"\nElle est n°",classementComposition(classement,armee_genetique)," du classement")

    print("classement moyen sur 10 armées sélectionnées génétiquement:")
    m=0
    for i in range(10):
        if nb_clible==0:
            m+=classementComposition(classement,genereArmees(armee))
        else:
            m+=classementComposition(classement,genereArmees(armee,nb_clible))
    m=m/10
    print(m)


#print(sorted(pb))
#print(pourcentage,"% des compositions sont dans le top 15")
#print(sum / generation)
