#VISTALLI SALLY 
#11612640

import random
import matplotlib.pyplot as plt

#######CITOYEN

class Citoyen:
    def __init__(self):
        self.ncontact = random.normalvariate(7,4)
        self.sante = "sain"
        self.joursMalade = 0

    def malade(self):
        self.sante = "malade"
        self.joursMalade = 1
        
    def critique(self):
        self.sante = "critique"
        self.ncontact = 0

    def immunise(self):
        self.sante = "immunise"

    def __str__(self):
        return str(self.sante) + str(self.ncontact)

    def copy(self):
        c = Citoyen()
        c.sante = self.sante
        c.ncontact = self.ncontact
        c.joursMalade = self.joursMalade
        return c


############POPULATION

class Population:
    def __init__(self,n=1000):
        self.jour = 0
        self.D = 0
        self.Pi = 0
        self.Pc = 0
        self.nContactInf = 0
        self.n = n
        self.lPop = []
        for i in range(n):
            self.lPop.append(Citoyen())

    def statSante(self):
        li = [0]*4
        for Citoyen in self.lPop:
            if Citoyen.sante== "sain":
                li[0]+=1
            elif Citoyen.sante== "malade":
                li[1]+=1
            elif Citoyen.sante== "critique":
                li[2]+=1
            else:
                li[3]+=1
        return li

    def __str__(self):
        return ("Jours:" + str(self.jour)+"\n Population de "+str(self.n)+" citoyens"+"\n Sains:"+str(self.statSante()[0])+"\n Malades:"+str(self.statSante()[1])+"\n Critiques:"+str(self.statSante()[2])+"\n Immunises:"+str(self.statSante()[3]))

    def infection(self,D,Pi,Pc):
        self.D = D
        self.Pi = Pi
        self.Pc = Pc
        self.lPop[0].malade()
        self.nContactInf = self.lPop[0].ncontact 

    def updatePop(self):
        self.jour += 1
        for Citoyen in self.lPop:
            r = random.random()
            if Citoyen.sante == "sain" and r < self.Pi*(self.nContactInf/self.n):
                Citoyen.malade()
                self.nContactInf += Citoyen.ncontact
            elif Citoyen.sante == "malade":
                if Citoyen.joursMalade == self.D:
                    Citoyen.immunise()
                    self.nContactInf -= Citoyen.ncontact
                else:
                    Citoyen.joursMalade += 1
                    if r < self.Pc:
                        self.nContactInf -= Citoyen.ncontact
                        Citoyen.critique()

    def passeJours(self,jours):
        for i in range(jours):
            self.updatePop()

    def confinementEtHygiene(self,d=2):
        self.Pi = self.Pi/2
        self.nContactInf = 0
        for Citoyen in self.lPop:
            Citoyen.ncontact=Citoyen.ncontact/d
            if Citoyen.sante == "malade":
                self.nContactInf += Citoyen.ncontact

    def copy(self):
        p = Population()
        p.jour = self.jour
        p.D = self.D
        p.Pi = self.Pi
        p.Pc = self.Pc
        p.nContactInf = self.nContactInf
        p.n = self.n
        for i in range(self.n):
            p.lPop[i]=self.lPop[i].copy()
        return p

    def simulate(self,jours,jour_confinement_start=None,valeur_confinement=None):
        li = []
        if jour_confinement_start==None:
            for i in range(jours+1):
                self.passeJours(1)
                li.append(self.statSante())
        else:
            for i in range(jours+1):
                self.passeJours(1)
                if jour_confinement_start==i:
                    self.confinementEtHygiene(valeur_confinement)
                li.append(self.statSante())
        return li

    def plot(self,jours,jour_confinement_start=None,valeur_confinement=None):
        L=self.simulate(jours,jour_confinement_start,valeur_confinement)
        N=self.n
        S=[i[0]/N for i in L]
        M=[i[1]/N for i in L]
        C=[i[2]/N for i in L]
        I=[i[3]/N for i in L]
        plt.plot(range(jours+1),S,color='black',label='Sain')
        plt.plot(range(jours+1),I,color='green',label='Immunise')
        plt.plot(range(jours+1),M,color='orange',label='Malade')
        plt.plot(range(jours+1),C,color='red',label='Critique')
        plt.legend()
        plt.show()



#######TEST CODES 1
p=Population()
p.infection(10, 0.05, 0.02) # L'infection dure 10 jours,
# la probabilite de contaminer est de 5%
# la probabilite de passer dans un etat critique est de 2%
# (proche du coronavirus)
# Avec 7 contacts en moyenne, R0 = 7 * 0.05 * 10 = 3.5
p.passeJours(2)
print(p)
p1=p.copy() # Pas de confinement au jour 2, confinement leger au jour 4
p2=p.copy() # confinement leger au jour 2
p3=p.copy() # confinement lourd au jour 2
# L'intensite du confinement peut ^etre determine avec le parametre d de la methode
# confinementEtHygiene :
# 2 reduit de moitie les interaction (mesures legeres)
# 7 abolit le plupart des interactions (puisqu'il y a en moyenne 7 interaction par citoyens)
p2.confinementEtHygiene(2)
p3.confinementEtHygiene(7)
p1.passeJours(2)
p2.passeJours(2)
p3.passeJours(2)
print("\np1 :")
print(p1)
print("\np2 :")
print(p2)
print("\np3 :")
print(p3)
p1.confinementEtHygiene()
p1.passeJours(20)
p2.passeJours(20)
p3.passeJours(20)
print("\np1 :")
print(p1)
print("\np2 :")
print(p2)
print("\np3 :")
print(p3)

#######TEST CODE 2
p=Population()
p.infection(10, 0.05, 0.02)
print(p.simulate(30,10,3)) # simuler l'evolution pendant 80 jours avec un
#confinement de valeur 3 applique au jour 10

###PLOT####
p=Population()
p.infection(10, 0.05, 0.02)
p.plot(80,20,2) # simule et trace l'evolution pendant 80 jours avec un
#confinement de valeur 2 applique au jour 20

