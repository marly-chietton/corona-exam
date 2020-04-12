# VISTALLI SALLY
# 11612640

import random
from copy import deepcopy

import matplotlib.pyplot as plt

#######CITOYEN


class Citoyen:
    def __init__(self):
        self.ncontact = random.normalvariate(7, 4)
        self.sante = "sain"
        self.joursMalade = 0

    def malade(self):
        """
        Rend le citoyen malade.
        """
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
        return deepcopy(self)


############POPULATION


class Population:
    def __init__(self, n=1000):
        self.jour = 0
        self.D = 0  # probabilité qu'un malade soit
        self.Pi = 0
        self.Pc = 0
        self.nContactInf = 0
        self.n = n
        self.lPop = [Citoyen() for i in range(n)]
        self.updateStatSante()
        self.progression = []  # chaque élement du tableau correspond à un jour simulé

    def updateStatSante(self):
        self.statSante = {
            "sain": 0,
            "malade": 0,
            "critique": 0,
            "immunise": 0,
        }
        for citoyen in self.lPop:
            self.statSante[citoyen.sante] += 1

    def __str__(self):
        return (
            "Jours:"
            + str(self.jour)
            + "\n\tPopulation de "
            + str(self.n)
            + " citoyens"
            + "\n\tSains:"
            + str(self.statSante["sain"])
            + "\n\tMalades:"
            + str(self.statSante["malade"])
            + "\n\tCritiques:"
            + str(self.statSante["critique"])
            + "\n\tImmunises:"
            + str(self.statSante["immunise"])
        )

    def infection(self, D, Pi, Pc):
        self.D = D
        self.Pi = Pi
        self.Pc = Pc
        first_citizen = self.lPop[0]
        # make him sick
        first_citizen.malade()
        # at start of infection set number of infected people
        self.nContactInf = first_citizen.ncontact

    def updatePop(self):
        self.jour += 1
        for citoyen in self.lPop:
            r = random.random()
            # probility that the citizen is infected
            is_infected = r < self.Pi * (self.nContactInf / self.n)
            # update citizen if citizen has been infected
            if citoyen.sante == "sain" and is_infected:
                citoyen.malade()
                self.nContactInf += citoyen.ncontact
            elif citoyen.sante == "malade":
                if citoyen.joursMalade == self.D:
                    citoyen.immunise()
                    self.nContactInf -= citoyen.ncontact
                else:
                    citoyen.joursMalade += 1
                    if r < self.Pc:
                        self.nContactInf -= citoyen.ncontact
                        citoyen.critique()

    def passeJours(self, jours):
        for i in range(jours):
            self.updatePop()

    def confinementEtHygiene(self, d=2):
        self.Pi = self.Pi / 2
        self.nContactInf = 0
        for citoyen in self.lPop:
            citoyen.ncontact = citoyen.ncontact / d
            if citoyen.sante == "malade":
                self.nContactInf += citoyen.ncontact

    def copy(self):
        return deepcopy(self)

    def simulate(self, jours, jour_confinement_start=None, valeur_confinement=None):
        if jour_confinement_start == None:
            for i in range(jours + 1):
                self.passeJours(1)
                self.updateStatSante()
                self.progression.append(self.statSante)
        else:
            for i in range(jours + 1):
                self.passeJours(1)
                if jour_confinement_start == i:
                    self.confinementEtHygiene(valeur_confinement)
                self.updateStatSante()
                self.progression.append(self.statSante)

    def plot(self, jours, jour_confinement_start=None, valeur_confinement=None):
        self.simulate(jours, jour_confinement_start, valeur_confinement)
        N = self.n  # pas utile en soi
        # y'aurait une petite opti à faire ici (on itère 4 fois), mais pas sur que ce soit utile
        # le nombre de jour n'est jamais vraiment très grand
        S = [i["sain"] / N for i in self.progression]
        M = [i["malade"] / N for i in self.progression]
        C = [i["critique"] / N for i in self.progression]
        I = [i["immunise"] / N for i in self.progression]
        c = (
            ["blue"] * (jours + 1)
            + ["grey"] * (jours + 1)
            + ["orange"] * (jours + 1)
            + ["red"] * (jours + 1)
        )
        fig, ax = plt.subplots()
        scatter = ax.scatter([range(jours + 1)] * 4, [S, M, C, I], c=c)
        print(scatter.legend_elements())
        #        legend1 = ax.legend([',
        #                    loc="upper right", title="Classes")
        #        ax.add_artist(legend1)
        plt.legend()
        plt.show()


#######TEST CODES 1
p = Population()
p.infection(10, 0.05, 0.02)  # L'infection dure 10 jours,
# la probabilite de contaminer est de 5%
# la probabilite de passer dans un etat critique est de 2%
# (proche du coronavirus)
# Avec 7 contacts en moyenne, R0 = 7 * 0.05 * 10 = 3.5
p.passeJours(2)
print(p)
p1 = p.copy()  # Pas de confinement au jour 2, confinement leger au jour 4
p2 = p.copy()  # confinement leger au jour 2
p3 = p.copy()  # confinement lourd au jour 2
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
p = Population()
p.infection(10, 0.05, 0.02)
print(p.simulate(30, 10, 3))  # simuler l'evolution pendant 80 jours avec un
# confinement de valeur 3 applique au jour 10

###PLOT####
p = Population()
p.infection(10, 0.05, 0.02)
p.plot(80, 20, 2)  # simule et trace l'evolution pendant 80 jours avec un
# confinement de valeur 2 applique au jour 20
