import random

class Armee(object):
    """docstring for Armee."""
    SIZE = 4
    def __init__(self,points):
        self.points=points


    def genereLigneAlea(self,faction):
        armee=[]
        if faction==1:
            for i in range(self.SIZE):
                choix=random.randint(1,4)
                if choix==1:
                    armee.append("s1")
                elif choix==2:
                    armee.append("a1")
                elif choix==3:
                    armee.append("c2")
                else:
                    armee.append("m1")
        else:
            for i in range(self.SIZE):
                choix=random.randint(1,4)
                if choix==1:
                    armee.append("s2")
                elif choix==2:
                    armee.append("a2")
                elif choix==3:
                    armee.append("c2")
                else:
                    armee.append("m2")
        return armee


    def placerArmees(self,armee1,armee2): # placerAmees doit prendre comme paramettre armee1 armee2 et renvoyer le plan qui servira à créer la grille
        plan=[[" " for j in range(self.SIZE)] for i in range(self.SIZE)]
        plan[0]=armee1
        plan[-1]=armee2
        return plan

    def attribuerFaction(self,armee,faction):
        for i,unit in enumerate(armee):
            if faction==1:
                armee[i]=unit + "1"
            else:
                armee[i]=unit + "2"


    def changerFaction(self,armee):
        for i,unite in enumerate(armee):
            if unite =="s1":
                armee[i]="s2"
            elif unite =="a1":
                armee[i]="a2"
            elif unite =="c1":
                armee[i]="c2"
            elif unite =="m1":
                armee[i]="m2"

            elif unite =="s2":
                armee[i]="s1"
            elif unite =="a2":
                armee[i]="a1"
            elif unite =="c2":
                armee[i]="c1"
            elif unite =="m2":
                armee[i]="m1"

    def compterLesPoints(self,armee):
        cout=0
        for unit in armee:
            if list(unit)[0]=='s':
                cout+=20
            elif list(unit)[0]=='a':
                cout+=50
            elif list(unit)[0]=='c':
                cout+=30
            elif list(unit)[0]=='m':
                cout+=40

        return self.points-cout >= 0

    def penaliseArmee(self,grille,faction):
        for unit in grille.selectFaction(faction):
            unit.penalite()

    def mutationArmee(self,armee):
        choix=random.randint(0,self.SIZE-1)

        if list(armee[choix])[1]=="1":
            faction=1
        else:
            faction=2
        if list(armee[choix])[0]=="s":
            while list(armee[choix])[0]=="s":
                armee[choix]=self.mutationPerso(faction)

            return armee

        elif list(armee[choix])[0]=="a":
            while list(armee[choix])[0]=="a":
                armee[choix]=self.mutationPerso(faction)
            return armee

        elif list(armee[choix])[0]=="c":
            while list(armee[choix])[0]=="c":
                armee[choix]=self.mutationPerso(faction)
            return armee

        elif list(armee[choix])[0]=="m":
            while list(armee[choix])[0]=="m":
                armee[choix]=self.mutationPerso(faction)
            return armee


    def mutationPerso(self,faction):
        choix=random.randint(1,4)
        if choix == 1:
            return "s"+str(faction)
        elif choix == 2:
            return "a"+str(faction)
        elif choix == 3:
            return "c"+str(faction)
        else:
            return "m"+str(faction)

def construitPersonnage(caractere, pos):
    if caractere == 'a1':
        return Archer(pos,1)
    elif caractere == 's1' :
        return Soldat(pos,1)

    elif caractere == 'c1':
        return Cavalier(pos,1)
    elif caractere == 'm1':
        return Mage(pos,1)

    elif caractere == 'a2':
        return Archer(pos,2)
    elif caractere == 's2' :
        return Soldat(pos,2)

    elif caractere == 'c2':
        return Cavalier(pos,2)
    elif caractere == 'm2':
        return Mage(pos,1)

    elif caractere == " ":
        return Vide(pos,0)

def construitVide():
    return construitPersonnage(" ", [-1, -1])

class Personnage(object):
    SIZE = 4
    def __init__(self, position, att, pv, portee, faction):
        self.position = position
        self.att = att
        self.pv = pv
        self.portee = portee
        self.faction = faction

    def info(self):
        return self.position,self.pv,self.getType()

    def bas(self, grille): #la fonction
        if self.position[0] < self.SIZE:
            if grille.cheminLibre(self.position[0]+1,self.position[1]):
                grille.efface(self.position[0], self.position[1])
                self.position[0] += 1
                grille.positionne(self.position[0], self.position[1], self)

    def haut(self, grille):
        if self.position[0] > 0:
            if grille.cheminLibre(self.position[0]-1,self.position[1]):
                grille.efface(self.position[0], self.position[1])
                self.position[0] -= 1
                grille.positionne(self.position[0], self.position[1], self)

    def droite(self, grille):
        if self.position[1] < self.SIZE:
            if grille.cheminLibre(self.position[0],self.position[1]+1):
                grille.efface(self.position[0], self.position[1])
                self.position[1] += 1
                grille.positionne(self.position[0], self.position[1], self)

    def gauche(self, grille):
        if self.position[1] > 0:
            if grille.cheminLibre(self.position[0],self.position[1]-1):
                grille.efface(self.position[0], self.position[1])
                self.position[1] -= 1
                grille.positionne(self.position[0], self.position[1], self)

    def combatContre(self, opposant, grille):
        if opposant.pv > 0:
            opposant.pv -= self.att
            if opposant.pv <= 0:
                #print("Un",opposant.getType(),"est mort")
                #IDEE; système d'épuisement:un soldat qui gagne un combat devient moins fort à chaques ennemies tuées
                opposant.meurs(grille)

    def allerEnemie(self, enemie, grille):
        if self.aCote(enemie):
            self.combatContre(enemie, grille)
        else:
            if self.memeColone(enemie):
                if self.position[0] < enemie.position[0]:
                    self.bas(grille)
                else:
                    self.haut(grille)
            elif self.memeLigne(enemie):
                if self.position[1] < enemie.position[1]:
                    self.droite(grille)
                else:
                    self.gauche(grille)
            else:
                    if self.position[0] < enemie.position[0]:
                        self.bas(grille)
                    else:
                        self.haut(grille)

    def meurs(self, grille):
        grille.efface(self.position[0], self.position[1])

    def aCote(self, personnage): # renvoie 1 si self est à une case de distance du personnage
        return self.distance(personnage) <= self.portee

    def memeColone(self, enemie):
        return self.position[1] == enemie.position[1]

    def memeLigne(self, enemie):
        return self.position[0] == enemie.position[0]

    def distance(self, personnage): # calcule et renvoie la distance etre self et le personnage donnée (nb de case totale (distance x + distance y))
        distance_x = abs(personnage.position[0] - self.position[0]) #x du personnage - le x de self
        distance_y = abs(personnage.position[1] - self.position[1]) #y du personnage - le y de self
        return distance_x + distance_y

    def trouverEnemie(self, grille):
        if self.faction == 1: #définit la faction des enemies
            faction_enemie = 2
        else:
            faction_enemie = 1
        # demande à la grille une liste des personnage dans la faction enemie
        enemies = grille.selectFaction(faction_enemie)

        #cherche l'enemie le plus proche en comparant les distances entre lui et les enemies de la liste
        if enemies != -1:
            plusproche = enemies[0]
            for unit in enemies[0:]:
                if self.distance(unit) <= self.distance(plusproche):
                    plusproche = unit

            return plusproche
        else:
            return -1

    def penalite(self):
        self.att = 1
        self.pv = 1


class Soldat(Personnage):
    def __init__(self, pos, faction):
        super().__init__(pos, 200, 1500, 1, faction)

    def getType(self):
        return "soldat"

    def toString(self):
        return "s"

class Archer(Personnage):
    def __init__(self, pos, faction):
        super().__init__(pos,140,700,3,faction)

    def getType(self):
        return "archer"

    def toString(self):
        return "a"

class Cavalier(Personnage):
    def __init__(self, pos, faction):
        super().__init__(pos,600,600,2,faction)

    def getType(self):
        return "cavalier"

    def toString(self):
        return "c"

class Mage(Personnage):
    def __init__(self, pos, faction):
        super().__init__(pos,450,600,4,faction)

    def getType(self):
        return "mage"

    def toString(self):
        return "m"

class Vide(Personnage):
    def __init__(self, pos, faction):
        super().__init__(pos,0,0,0,faction)

    def getType(self):
        return "vide"

    def toString(self):
        return "-"

if __name__ == "__main__":

    david=construitPersonnage('s1',(0,0))
    print(david.att)
    david.penalite()
    print(david.att)
    print(david.info())
