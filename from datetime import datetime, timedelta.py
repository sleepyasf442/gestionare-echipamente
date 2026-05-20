from datetime import datetime, timedelta

# CLASA ECHIPAMENT
class Echipament:
    def __init__(self, id_echipament, nume, categorie):
        self.id = id_echipament
        self.nume = nume
        self.categorie = categorie
        self.stare = "Bună"
        self.disponibil = True
        self.data_verificare = datetime.now() + timedelta(days=30)

    def actualizeaza_stare(self, stare_noua):
        self.stare = stare_noua
        print(f"[INFO] Starea echipamentului '{self.nume}' a fost actualizată la: {self.stare}")

    def necesita_verificare(self):
        return datetime.now() >= self.data_verificare

    def __str__(self):
        return f"{self.nume} ({self.categorie}) - Stare: {self.stare} - Disponibil: {self.disponibil}"

# CLASA UTILIZATOR
class Utilizator:
    def __init__(self, id_utilizator, nume, rol):
        self.id = id_utilizator
        self.nume = nume
        self.rol = rol

    def __str__(self):
        return f"{self.nume} ({self.rol})"

# CLASA IMPRUMUT
class Imprumut:
    def __init__(self, utilizator, echipament, zile=7):
        if not echipament.disponibil:
            raise Exception(f"[EROARE] '{echipament.nume}' nu este disponibil!")

        self.utilizator = utilizator
        self.echipament = echipament
        self.data_imprumut = datetime.now()
        self.data_returnare = self.data_imprumut + timedelta(days=zile)
        self.returnat = False

        echipament.disponibil = False
        print(f"[ÎMPRUMUT] {utilizator.nume} a împrumutat '{echipament.nume}'")

    def returneaza_echipament(self):
        if self.returnat:
            print("[INFO] Echipamentul a fost deja returnat.")
            return

        self.returnat = True
        self.echipament.disponibil = True
        print(f"[RETURNARE] '{self.echipament.nume}' a fost returnat.")

    def verifica_intarziere(self):
        if datetime.now() > self.data_returnare and not self.returnat:
            print(f"[ATENȚIE] Împrumutul pentru '{self.echipament.nume}' este întârziat!")

    def __str__(self):
        status = "Returnat" if self.returnat else "Activ"
        return f"{self.echipament.nume} -> {self.utilizator.nume} | Status: {status}"

# CLASA SISTEM LABORATOR
class SistemLaborator:
    def __init__(self):
        self.echipamente = []
        self.utilizatori = []
        self.imprumuturi = []

    def adauga_echipament(self, echipament):
        self.echipamente.append(echipament)

    def adauga_utilizator(self, utilizator):
        self.utilizatori.append(utilizator)

    def afiseaza_echipamente(self):
        print("\n=== LISTA ECHIPAMENTE ===")
        for ech in self.echipamente:
            print(ech)

    def imprumuta_echipament(self, utilizator, echipament, zile=7):
        imprumut = Imprumut(utilizator, echipament, zile)
        self.imprumuturi.append(imprumut)

    def verifica_mentenanta(self):
        print("\n=== VERIFICARE MENTENANȚĂ ===")
        for ech in self.echipamente:
            if ech.necesita_verificare():
                print(f"[MENTENANȚĂ] '{ech.nume}' necesită verificare!")
            else:
                print(f"[OK] '{ech.nume}' este în regulă.")

    def verifica_imprumuturi(self):
        print("\n=== VERIFICARE ÎMPRUMUTURI ===")
        for imprumut in self.imprumuturi:
            imprumut.verifica_intarziere()


# TESTARE SISTEM
sistem = SistemLaborator()

laptop = Echipament(1, "Laptop Dell", "IT")
microscop = Echipament(2, "Microscop Digital", "Biologie")

student = Utilizator(1, "Andrei Popescu", "Student")
profesor = Utilizator(2, "Maria Ionescu", "Profesor")

sistem.adauga_echipament(laptop)
sistem.adauga_echipament(microscop)

sistem.adauga_utilizator(student)
sistem.adauga_utilizator(profesor)

sistem.afiseaza_echipamente()

sistem.imprumuta_echipament(student, laptop, zile=5)

laptop.actualizeaza_stare("Necesită reparații")

sistem.verifica_mentenanta()

imprumut = sistem.imprumuturi[0]
imprumut.returneaza_echipament()

sistem.afiseaza_echipamente()
