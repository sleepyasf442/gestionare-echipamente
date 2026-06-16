from datetime import datetime, timedelta


class Echipament:

    def __init__(self, id_echipament, nume, categorie):
        self.id_echipament = id_echipament
        self.id = id_echipament  # Păstrat pentru compatibilitate cu ambele versiuni
        self.nume = nume
        self.categorie = categorie
        self.disponibil = True
        self.stare = "Disponibil"  # Inițializat cu o stare standard valabilă
        self.data_ultima_mentenanta = datetime.now()
        self.numar_imprumuturi = 0
        self.defect = False

    def actualizeaza_stare(self, stare_noua):
        self.stare = stare_noua
        if stare_noua.lower() == "defect":
            self.defect = True
            self.disponibil = False
        elif stare_noua.lower() == "disponibil":
            self.defect = False
            self.disponibil = True
        print(f"[INFO] '{self.nume}' -> stare actualizată: {self.stare}")

    def efectueaza_mentenanta(self):
        self.data_ultima_mentenanta = datetime.now()
        self.stare = "Disponibil"
        self.defect = False
        self.disponibil = True
        print(f"[MENTENANȚĂ] '{self.nume}' a fost verificat.")

    def necesita_verificare(self):
        diferenta = datetime.now() - self.data_ultima_mentenanta
        return diferenta.days >= 30

    def __str__(self):
        return (
            f"ID: {self.id_echipament} | {self.nume} | "
            f"Categorie: {self.categorie} | Stare: {self.stare} | "
            f"Disponibil: {self.disponibil}"
        )


class Utilizator:

    def __init__(self, id_utilizator, nume, rol="Student"):
        self.id_utilizator = id_utilizator
        self.id = id_utilizator
        self.nume = nume
        self.rol = rol

    def __str__(self):
        return f"{self.nume} ({self.rol})"


class Imprumut:

    def __init__(self, echipament, utilizator, zile=7):
        if not echipament.disponibil:
            raise Exception(
                f"Echipamentul '{echipament.nume}' nu este disponibil!"
            )

        self.echipament = echipament
        self.utilizator = utilizator
        self.data_imprumut = datetime.now()
        self.data_returnare = None  # Va fi setată la returnare efectivă
        self.data_scadenta = self.data_imprumut + timedelta(days=zile)
        self.returnat = False

        echipament.disponibil = False
        echipament.stare = "Imprumutat"
        echipament.numar_imprumuturi += 1

        print(
            f"[ÎMPRUMUT] {utilizator.nume} a împrumutat '{echipament.nume}'"
        )

    def returneaza_echipament(self):
        if self.returnat:
            print("[INFO] Echipamentul a fost deja returnat.")
            return

        self.returnat = True
        self.data_returnare = datetime.now()
        self.echipament.disponibil = True
        self.echipament.stare = "Disponibil"
        print(f"[RETURNARE] '{self.echipament.nume}' a fost returnat.")

    def verifica_intarziere(self):
        if not self.returnat and datetime.now() > self.data_scadenta:
            print(f"[ALERTĂ] Împrumut întârziat: {self.echipament.nume}")

    def __str__(self):
        status = "Returnat" if self.returnat else "Activ"
        return f"{self.echipament.nume} -> {self.utilizator.nume} | Status: {status}"


class SistemLaborator:

    def __init__(self):
        self.echipamente = []
        self.utilizatori = []
        self.imprumuturi = []

    def adauga_echipament(self, echipament):
        self.echipamente.append(echipament)

    def adauga_utilizator(self, utilizator):
        self.utilizatori.append(utilizator)

    def creeaza_imprumut(self, echipament, utilizator, zile=7):
        try:
            imprumut = Imprumut(echipament, utilizator, zile)
            self.imprumuturi.append(imprumut)
        except Exception as e:
            print(f"[EROARE] {e}")

    def afiseaza_echipamente(self):
        print("\n=== LISTĂ ECHIPAMENTE ===")
        for ech in self.echipamente:
            print(ech)

    def cauta_echipament(self, nume):
        print(f"\n=== CĂUTARE: {nume} ===")
        rezultate = [
            ech
            for ech in self.echipamente
            if nume.lower() in ech.nume.lower()
        ]
        if rezultate:
            for ech in rezultate:
                print(ech)
        else:
            print("Nu există rezultate.")
        return rezultate

    def filtreaza_dupa_categorie(self, categorie):
        print(f"\n=== FILTRARE CATEGORIE: {categorie} ===")
        rezultate = [
            ech
            for ech in self.echipamente
            if ech.categorie.lower() == categorie.lower()
        ]
        for ech in rezultate:
            print(ech)
        return rezultate

    def filtreaza_stare(self, stare):
        rezultate = [
            ech for ech in self.echipamente if ech.stare.lower() == stare.lower()
        ]
        return rezultate

    def sorteaza_echipamente(self):
        return sorted(self.echipamente, key=lambda x: x.nume)

    def imprumuta(self, id_echipament, id_utilizator):
        echipament = next((e for e in self.echipamente if e.id == id_echipament), None)
        utilizator = next((u for u in self.utilizatori if u.id == id_utilizator), None)

        if echipament and utilizator:
            self.creeaza_imprumut(echipament, utilizator)
        else:
            print("[EROARE] Echipamentul sau utilizatorul nu a fost găsit.")

    def returneaza(self, id_echipament):
        for imprumut in self.imprumuturi:
            if imprumut.echipament.id == id_echipament and not imprumut.returnat:
                imprumut.returneaza_echipament()
                return
        print(f"[INFO] Nu s-a găsit niciun împrumut activ pentru ID {id_echipament}")

    def marcheaza_defect(self, id_echipament):
        for e in self.echipamente:
            if e.id == id_echipament:
                e.actualizeaza_stare("Defect")

    def raport_utilizare(self):
        print("\n=== RAPORT UTILIZARE ===")
        for i in self.imprumuturi:
            data_str = i.data_imprumut.strftime("%d/%m/%Y")
            print(f"{i.echipament.nume} - {i.utilizator.nume} - {data_str}")

    def raport_defecte(self):
        print("\n=== RAPORT DEFECTE ===")
        defecte = self.filtreaza_stare("Defect")
        if defecte:
            for ech in defecte:
                print(f"{ech.nume} | Stare: {ech.stare}")
        else:
            print("Nu există echipamente defecte.")

    def verifica_mentenanta(self):
        print("\n=== VERIFICARE MENTENANȚĂ ===")
        necesita = False
        for ech in self.echipamente:
            if ech.necesita_verificare():
                print(f"[NOTIFICARE] {ech.nume} necesită verificare.")
                necesita = True
        if not necesita:
            print("Toate echipamentele sunt la zi cu mentenanța.")

    def verifica_imprumuturi(self):
        print("\n=== VERIFICARE ÎMPRUMUTURI ===")
        for imprumut in self.imprumuturi:
            imprumut.verifica_intarziere()

# EXEMPLU DE UTILIZARE (RULARE ȘI TESTARE)
if __name__ == "__main__":
    sistem = SistemLaborator()

    # Adăugare Echipamente unice 
    sistem.adauga_echipament(Echipament(1, "Osciloscop", "Electronica"))
    sistem.adauga_echipament(Echipament(2, "Laptop Dell", "IT"))
    sistem.adauga_echipament(Echipament(3, "Multimetru", "Electronica"))
    sistem.adauga_echipament(Echipament(4, "Microscop Digital", "Biologie"))
    sistem.adauga_echipament(Echipament(5, "Imprimantă HP", "IT"))

    # Adăugare Utilizatori unici
    student = Utilizator(1, "Andrei Popescu", "Student")
    profesor = Utilizator(2, "Maria Ionescu", "Profesor")
    sistem.adauga_utilizator(student)
    sistem.adauga_utilizator(profesor)

    # Afișare inițială
    sistem.afiseaza_echipamente()

    # Împrumuturi
    print("\n--- TESTARE ÎMPRUMUTURI ---")
    sistem.imprumuta(2, 1)  # Andrei împrumută Laptop Dell (ID 2)
    sistem.imprumuta(4, 2)  # Maria împrumută Microscop (ID 4)

    # Defecte
    print("\n--- TESTARE DEFECTE ---")
    sistem.marcheaza_defect(3)  # Marcăm Multimetrul ca Defect

    # Căutare
    sistem.cauta_echipament("Laptop")

    # Filtrare
    sistem.filtreaza_dupa_categorie("IT")

    # Sortare
    print("\n=== SORTARE DUPĂ NUME ===")
    for e in sistem.sorteaza_echipamente():
        print(e)

    # Rapoarte
    sistem.raport_utilizare()
    sistem.raport_defecte()

    # Returnare
    print("\n--- TESTARE RETURNARE ---")
    sistem.returneaza(2)  # Returnează Laptop Dell

    # Verificări finale
    sistem.verifica_imprumuturi()
    sistem.verifica_mentenanta()

while True:
    print("\n===== MENIU =====")
    print("1. Afiseaza toate echipamentele")
    print("2. Afiseaza echipamente IT")
    print("3. Afiseaza echipamente defecte")
    print("4. Sortare dupa nume")
    print("0. Iesire")

    optiune = input("Alege o optiune: ")

    if optiune == "1":
        sistem.afiseaza_echipamente()

    elif optiune == "2":
        sistem.filtreaza_dupa_categorie("IT")

    elif optiune == "3":
        defecte = sistem.filtreaza_stare("Defect")

        if defecte:
            for e in defecte:
                print(e)
        else:
            print("Nu exista echipamente defecte.")

    elif optiune == "4":
        print("\n=== SORTARE DUPA NUME ===")
        for e in sistem.sorteaza_echipamente():
            print(e)

    elif optiune == "0":
        print("Program inchis.")
        break

    else:
        print("Optiune invalida!")
