from datetime import datetime, timedelta

class Echipament:
    def __init__(self, id_echipament, nume, categorie):
        self.id_echipament = id_echipament
        self.nume = nume
        self.categorie = categorie
        self.disponibil = True
        self.stare = "Bună"
        self.data_ultima_mentenanta = datetime.now()
        self.numar_imprumuturi = 0
        self.defect = False

    def actualizeaza_stare(self, stare_noua):
        self.stare = stare_noua

        if stare_noua.lower() != "bună":
            self.defect = True

        print(f"[INFO] '{self.nume}' -> stare actualizată: {self.stare}")

    def efectueaza_mentenanta(self):
        self.data_ultima_mentenanta = datetime.now()
        self.stare = "Bună"
        self.defect = False

        print(f"[MENTENANȚĂ] '{self.nume}' a fost verificat.")

    def necesita_verificare(self):
        diferenta = datetime.now() - self.data_ultima_mentenanta
        return diferenta.days >= 30

    def __str__(self):
        return (
            f"ID: {self.id_echipament} | "
            f"{self.nume} | "
            f"Categorie: {self.categorie} | "
            f"Stare: {self.stare} | "
            f"Disponibil: {self.disponibil}"
        )

class Utilizator:
    def __init__(self, id_utilizator, nume, rol):
        self.id_utilizator = id_utilizator
        self.nume = nume
        self.rol = rol

    def __str__(self):
        return f"{self.nume} ({self.rol})"

class Imprumut:
    def __init__(self, echipament, utilizator, zile=7):

        if not echipament.disponibil:
            raise Exception("Echipamentul nu este disponibil!")

        self.echipament = echipament
        self.utilizator = utilizator
        self.data_imprumut = datetime.now()
        self.data_returnare = self.data_imprumut + timedelta(days=zile)
        self.returnat = False

        echipament.disponibil = False
        echipament.numar_imprumuturi += 1

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
            print(f"[ALERTĂ] Împrumut întârziat: {self.echipament.nume}")

    def __str__(self):

        status = "Returnat" if self.returnat else "Activ"

        return (
            f"{self.echipament.nume} -> "
            f"{self.utilizator.nume} | "
            f"Status: {status}"
        )

class SistemLaborator:

    def __init__(self):
        self.echipamente = []
        self.utilizatori = []
        self.imprumuturi = []

    # ADAUGARE DATE
    def adauga_echipament(self, echipament):
        self.echipamente.append(echipament)

    def adauga_utilizator(self, utilizator):
        self.utilizatori.append(utilizator)

    def creeaza_imprumut(self, echipament, utilizator, zile=7):

        imprumut = Imprumut(echipament, utilizator, zile)
        self.imprumuturi.append(imprumut)
        
    # AFISARE ECHIPAMENTE
    def afiseaza_echipamente(self):

        print("\n=== LISTĂ ECHIPAMENTE ===")

        for ech in self.echipamente:
            print(ech)

    # CĂUTARE
    def cauta_echipament(self, nume):

        print(f"\n=== CĂUTARE: {nume} ===")

        rezultate = [
            ech for ech in self.echipamente
            if nume.lower() in ech.nume.lower()
        ]

        if rezultate:
            for ech in rezultate:
                print(ech)
        else:
            print("Nu există rezultate.")

    # FILTRARE
    def filtreaza_dupa_categorie(self, categorie):

        print(f"\n=== FILTRARE CATEGORIE: {categorie} ===")

        rezultate = [
            ech for ech in self.echipamente
            if ech.categorie.lower() == categorie.lower()

        for ech in rezultate:
            print(ech)

    # SORTARE
    def sorteaza_echipamente(self):

        print("\n=== SORTARE DUPĂ NUME ===")

        lista_sortata = sorted(
            self.echipamente,
            key=lambda ech: ech.nume
        )

        for ech in lista_sortata:
            print(ech)

    # RAPORT UTILIZARE
    def raport_utilizare(self):

        print("\n=== RAPORT UTILIZARE ===")

        for ech in self.echipamente:
            print(
                f"{ech.nume} -> "
                f"Împrumuturi: {ech.numar_imprumuturi}"
            )
            
    # RAPORT DEFECTE
    def raport_defecte(self):

        print("\n=== RAPORT DEFECTE ===")

        defecte = [
            ech for ech in self.echipamente
            if ech.defect
        ]

        if defecte:
            for ech in defecte:
                print(
                    f"{ech.nume} | "
                    f"Stare: {ech.stare}"
                )
        else:
            print("Nu există echipamente defecte.")

    # VERIFICARE MENTENANȚĂ
    def verifica_mentenanta(self):

        print("\n=== VERIFICARE MENTENANȚĂ ===")

        for ech in self.echipamente:

            if ech.necesita_verificare():
                print(
                    f"[NOTIFICARE] "
                    f"{ech.nume} necesită verificare."
                )


    def verifica_imprumuturi(self):

        print("\n=== VERIFICARE ÎMPRUMUTURI ===")

        for imprumut in self.imprumuturi:
            imprumut.verifica_intarziere()

# EXEMPLU DE UTILIZARE
sistem = SistemLaborator()

# Echipamente
laptop = Echipament(1, "Laptop Dell", "IT")
microscop = Echipament(2, "Microscop Digital", "Biologie")
imprimanta = Echipament(3, "Imprimantă HP", "IT")

# Utilizatori
student = Utilizator(1, "Andrei Popescu", "Student")
profesor = Utilizator(2, "Maria Ionescu", "Profesor")

# Adăugare în sistem
sistem.adauga_echipament(laptop)
sistem.adauga_echipament(microscop)
sistem.adauga_echipament(imprimanta)

sistem.adauga_utilizator(student)
sistem.adauga_utilizator(profesor)

# Afișare
sistem.afiseaza_echipamente()

# Împrumut
sistem.creeaza_imprumut(laptop, student)
sistem.creeaza_imprumut(microscop, profesor)

# Defect
microscop.actualizeaza_stare("Defect")

# Căutare
sistem.cauta_echipament("Laptop")

# Filtrare
sistem.filtreaza_dupa_categorie("IT")

# Sortare
sistem.sorteaza_echipamente()

# Rapoarte
sistem.raport_utilizare()
sistem.raport_defecte()

# Returnare
imprumut = sistem.imprumuturi[0]
imprumut.returneaza_echipament()

# Verificări
sistem.verifica_imprumuturi()
sistem.verifica_mentenanta()
