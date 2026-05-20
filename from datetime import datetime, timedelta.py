from datetime import datetime, timedelta


class Echipament:
    def __init__(self, id_echipament, nume, categorie):
        self.id_echipament = id_echipament
        self.nume = nume
        self.categorie = categorie
        self.disponibil = True
        self.stare = "Bună"
        self.data_ultima_mentenanta = datetime.now()

    def actualizeaza_stare(self, stare_noua):
        self.stare = stare_noua
        print(f"[INFO] Starea echipamentului '{self.nume}' a fost actualizată la: {self.stare}")

    def efectueaza_mentenanta(self):
        self.data_ultima_mentenanta = datetime.now()
        self.stare = "Bună"
        print(f"[MENTENANȚĂ] Echipamentul '{self.nume}' a fost verificat.")

    def necesita_verificare(self):
        diferenta = datetime.now() - self.data_ultima_mentenanta
        return diferenta.days >= 30

    def __str__(self):
        return f"{self.nume} ({self.categorie}) - Stare: {self.stare} - Disponibil: {self.disponibil}"


class Utilizator:
    def __init__(self, id_utilizator, nume, rol):
        self.id_utilizator = id_utilizator
        self.nume = nume
        self.rol = rol

    def __str__(self):
        return f"{self.nume} - Rol: {self.rol}"


class Imprumut:
    def __init__(self, echipament, utilizator, zile=7):
        if not echipament.disponibil:
            raise Exception("Echipamentul nu este disponibil pentru împrumut.")

        self.echipament = echipament
        self.utilizator = utilizator
        self.data_imprumut = datetime.now()
        self.data_returnare = self.data_imprumut + timedelta(days=zile)
        self.returnat = False

        echipament.disponibil = False

        print(f"[ÎMPRUMUT] '{echipament.nume}' a fost împrumutat de {utilizator.nume}.")

    def returneaza_echipament(self):
        if self.returnat:
            print("[INFO] Echipamentul a fost deja returnat.")
            return

        self.returnat = True
        self.echipament.disponibil = True

        print(f"[RETURNARE] '{self.echipament.nume}' a fost returnat de {self.utilizator.nume}.")

    def verifica_intarziere(self):
        if datetime.now() > self.data_returnare and not self.returnat:
            print(f"[ALERTĂ] Împrumut întârziat pentru echipamentul '{self.echipament.nume}'.")

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
        imprumut = Imprumut(echipament, utilizator, zile)
        self.imprumuturi.append(imprumut)

    def afiseaza_echipamente(self):
        print("\n=== LISTĂ ECHIPAMENTE ===")
        for ech in self.echipamente:
            print(ech)

    def verifica_mentenanta(self):
        print("\n=== VERIFICARE MENTENANȚĂ ===")
        for ech in self.echipamente:
            if ech.necesita_verificare():
                print(f"[NOTIFICARE] '{ech.nume}' necesită verificare tehnică.")

    def verifica_imprumuturi(self):
        print("\n=== VERIFICARE ÎMPRUMUTURI ===")
        for imprumut in self.imprumuturi:
            imprumut.verifica_intarziere()

sistem = SistemLaborator()

# Creare echipamente
laptop = Echipament(1, "Laptop Dell", "IT")
microscop = Echipament(2, "Microscop Digital", "Biologie")

# Creare utilizatori
student = Utilizator(1, "Andrei Popescu", "Student")
profesor = Utilizator(2, "Maria Ionescu", "Profesor")

# Adăugare în sistem
sistem.adauga_echipament(laptop)
sistem.adauga_echipament(microscop)

sistem.adauga_utilizator(student)
sistem.adauga_utilizator(profesor)

# Afișare echipamente
sistem.afiseaza_echipamente()

# Împrumut echipament
sistem.creeaza_imprumut(laptop, student, zile=5)

# Verificare status
sistem.afiseaza_echipamente()

# Actualizare stare echipament
laptop.actualizeaza_stare("Necesită reparații")

# Verificare mentenanță
sistem.verifica_mentenanta()

# Returnare echipament
imprumut = sistem.imprumuturi[0]
imprumut.returneaza_echipament()

# Afișare finală
sistem.afiseaza_echipamente()

from datetime import datetime, timedelta


# =========================
# CLASA ECHIPAMENT
# =========================
class Echipament:
    def __init__(self, id_echipament, nume, categorie):
        self.id = id_echipament
        self.nume = nume
        self.categorie = categorie
        self.stare = "Bună"
        self.disponibil = True
        self.data_verificare = datetime.now() + timedelta(days=30)

    def afiseaza_info(self):
        print(f"""
ID: {self.id}
Nume: {self.nume}
Categorie: {self.categorie}
Stare: {self.stare}
Disponibil: {self.disponibil}
Următoarea verificare: {self.data_verificare.strftime('%d-%m-%Y')}
""")

    def actualizeaza_stare(self, stare_noua):
        self.stare = stare_noua
        print(f"[INFO] Starea echipamentului '{self.nume}' a fost actualizată la: {self.stare}")


# =========================
# CLASA UTILIZATOR
# =========================
class Utilizator:
    def __init__(self, id_utilizator, nume, rol):
        self.id = id_utilizator
        self.nume = nume
        self.rol = rol

    def afiseaza_utilizator(self):
        print(f"{self.nume} ({self.rol})")


# =========================
# CLASA IMPRUMUT
# =========================
class Imprumut:
    def __init__(self, utilizator, echipament, zile=7):
        self.utilizator = utilizator
        self.echipament = echipament
        self.data_imprumut = datetime.now()
        self.data_returnare = self.data_imprumut + timedelta(days=zile)

        if echipament.disponibil:
            echipament.disponibil = False
            print(f"[IMPRUMUT] {utilizator.nume} a împrumutat '{echipament.nume}'")
        else:
            print(f"[EROARE] Echipamentul '{echipament.nume}' nu este disponibil!")

    def returneaza_echipament(self):
        self.echipament.disponibil = True
        print(f"[RETURNARE] '{self.echipament.nume}' a fost returnat.")

    def verifica_intarziere(self):
        if datetime.now() > self.data_returnare:
            print(f"[ATENTIE] Împrumutul pentru '{self.echipament.nume}' este întârziat!")
        else:
            print(f"[INFO] Împrumutul este în termen.")
            
class SistemLaborator:
    def __init__(self):
        self.echipamente = []
        self.utilizatori = []
        self.imprumuturi = []

    # Adăugare echipament
    def adauga_echipament(self, echipament):
        self.echipamente.append(echipament)

    # Adăugare utilizator
    def adauga_utilizator(self, utilizator):
        self.utilizatori.append(utilizator)

    # Afișare echipamente
    def afiseaza_echipamente(self):
        print("\n=== LISTA ECHIPAMENTE ===")

        for echipament in self.echipamente:
            print(
                f"{echipament.nume} ({echipament.categorie}) "
                f"- Stare: {echipament.stare} "
                f"- Disponibil: {echipament.disponibil}"
            )

    # Creare împrumut
    def imprumuta_echipament(self, utilizator, echipament):
        imprumut = Imprumut(utilizator, echipament)
        self.imprumuturi.append(imprumut)

    # Verificare mentenanță
    def verifica_mentenanta(self):
        print("\n=== VERIFICARE MENTENANȚĂ ===")

        for echipament in self.echipamente:
            if datetime.now() >= echipament.data_verificare:
                print(f"[MENTENANȚĂ] '{echipament.nume}' necesită verificare!")
            else:
                print(f"[OK] '{echipament.nume}' este în regula

sistem = SistemLaborator()

# Creare echipamente
laptop = Echipament(1, "Laptop Dell", "IT")
microscop = Echipament(2, "Microscop Digital", "Biologie")

# Creare utilizatori
student = Utilizator(1, "Andrei Popescu", "Student")
profesor = Utilizator(2, "Maria Ionescu", "Profesor")

# Adăugare în sistem
sistem.adauga_echipament(laptop)
sistem.adauga_echipament(microscop)

sistem.adauga_utilizator(student)
sistem.adauga_utilizator(profesor)

# Afișare echipamente
sistem.afiseaza_echipamente()

# Împrumut echipament
sistem.imprumuta_echipament(student, laptop)

# Actualizare stare
laptop.actualizeaza_stare("Necesită reparații")

# Verificare mentenanță
sistem.verifica_mentenanta()

# Returnare echipament
imprumut = sistem.imprumuturi[0]
imprumut.returneaza_echipament()

# Afișare finală
sistem.afiseaza_echipamente()
