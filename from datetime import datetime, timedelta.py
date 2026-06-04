from datetime import datetime


class Echipament:
    def __init__(self, id_echipament, nume, categorie):
        self.id = id_echipament
        self.nume = nume
        self.categorie = categorie
        self.stare = "Disponibil"

    def __str__(self):
        return str(self.id) + " | " + self.nume + " | " + self.categorie + " | " + self.stare


class Utilizator:
    def __init__(self, id_utilizator, nume):
        self.id = id_utilizator
        self.nume = nume

    def __str__(self):
        return str(self.id) + " | " + self.nume


class Imprumut:
    def __init__(self, echipament, utilizator):
        self.echipament = echipament
        self.utilizator = utilizator
        self.data_imprumut = datetime.now()
        self.data_returnare = None

    def returneaza(self):
        self.data_returnare = datetime.now()


class SistemLaborator:
    def __init__(self):
        self.echipamente = []
        self.utilizatori = []
        self.imprumuturi = []

    def adauga_echipament(self, echipament):
        self.echipamente.append(echipament)

    def adauga_utilizator(self, utilizator):
        self.utilizatori.append(utilizator)

    def cauta_echipament(self, nume):
        rezultate = []

        for e in self.echipamente:
            if nume.lower() in e.nume.lower():
                rezultate.append(e)

        return rezultate

    def filtreaza_stare(self, stare):
        rezultate = []

        for e in self.echipamente:
            if e.stare == stare:
                rezultate.append(e)

        return rezultate

    def sorteaza_echipamente(self):
        return sorted(self.echipamente, key=lambda x: x.nume)

    def imprumuta(self, id_echipament, id_utilizator):
        echipament = None
        utilizator = None

        for e in self.echipamente:
            if e.id == id_echipament:
                echipament = e

        for u in self.utilizatori:
            if u.id == id_utilizator:
                utilizator = u

        if echipament and utilizator:
            if echipament.stare == "Disponibil":
                imprumut = Imprumut(echipament, utilizator)
                self.imprumuturi.append(imprumut)
                echipament.stare = "Imprumutat"
                print("Imprumut realizat")
            else:
                print("Echipamentul nu este disponibil")

    def returneaza(self, id_echipament):
        for imprumut in self.imprumuturi:
            if imprumut.echipament.id == id_echipament and imprumut.data_returnare is None:
                imprumut.returneaza()
                imprumut.echipament.stare = "Disponibil"
                print("Echipament returnat")

    def marcheaza_defect(self, id_echipament):
        for e in self.echipamente:
            if e.id == id_echipament:
                e.stare = "Defect"

    def raport_utilizare(self):
        print("\nRAPORT UTILIZARE")

        for i in self.imprumuturi:
            print(
                i.echipament.nume,
                "-",
                i.utilizator.nume,
                "-",
                i.data_imprumut.strftime("%d/%m/%Y")
            )

    def raport_defecte(self):
        print("\nRAPORT DEFECTE")

        defecte = self.filtreaza_stare("Defect")

        if len(defecte) == 0:
            print("Nu exista defecte")
        else:
            for e in defecte:
                print(e)

    def afiseaza_echipamente(self):
        print("\nECHIPAMENTE")

        for e in self.echipamente:
            print(e)


sistem = SistemLaborator()

sistem.adauga_echipament(Echipament(1, "Osciloscop", "Electronica"))
sistem.adauga_echipament(Echipament(2, "Laptop Dell", "IT"))
sistem.adauga_echipament(Echipament(3, "Multimetru", "Electronica"))

sistem.adauga_utilizator(Utilizator(1, "Andrei"))
sistem.adauga_utilizator(Utilizator(2, "Maria"))

sistem.afiseaza_echipamente()

sistem.imprumuta(1, 1)

sistem.marcheaza_defect(3)

print("\nCAUTARE")
for e in sistem.cauta_echipament("Laptop"):
    print(e)

print("\nFILTRARE")
for e in sistem.filtreaza_stare("Defect"):
    print(e)

print("\nSORTARE")
for e in sistem.sorteaza_echipamente():
    print(e)

sistem.raport_utilizare()

sistem.raport_defecte()

sistem.returneaza(1)

print("\nSTARE FINALA")
sistem.afiseaza_echipamente()
