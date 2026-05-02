import tkinter as tk
from tkinter import messagebox
import logic
import time
import storage

class AknakeresoGUI:
    """A játék grafikus felületéért és az eseménykezelésért felelős osztály."""
    
    def __init__(self, root, sorok=10, oszlopok=10, aknak=10, kattintas_limit=None, kategoria="Normál", nev="Játékos", on_close=None):
        self.root = root
        self.root.title("Aknakereső")
        self.kategoria = kategoria
        self.jatekos_neve = nev
        self.on_close = on_close  # Ezt hívjuk meg, ha be kell zárni az ablakot
        
        # Ha a játékos az "X"-re kattint az ablak sarkában, akkor is menjen vissza a menübe!
        self.root.protocol("WM_DELETE_WINDOW", self.ablak_bezarasa)
        
        self.jatek = logic.AknakeresoLogika(sorok, oszlopok, aknak, kattintas_limit)
        self.felfedett_mezok = set()
        self.zaszlok = set()
        self.start_ido = None
        self.fut_a_jatek = False

        # UI elemek
        self.info_frame = tk.Frame(self.root)
        self.info_frame.pack(side=tk.TOP, fill=tk.X)
        
        self.ido_label = tk.Label(self.info_frame, text="Idő: 0s", font=("Arial", 10, "bold"))
        self.ido_label.pack(side=tk.LEFT, padx=10)
        
        limit_szoveg = f"Kattintások: {kattintas_limit}" if kattintas_limit else "Mód: Végtelen"
        self.limit_label = tk.Label(self.info_frame, text=limit_szoveg, font=("Arial", 10, "bold"))
        self.limit_label.pack(side=tk.RIGHT, padx=10)

        self.jatek_ter = tk.Frame(self.root)
        self.jatek_ter.pack()
        
        self.gombok = {}
        self.palyat_epit()

    def palyat_epit(self):
        """Létrehozza a gombokat a rácson."""
        for r in range(self.jatek.sorok):
            for c in range(self.jatek.oszlopok):
                btn = tk.Button(self.jatek_ter, width=2, height=1, 
                                command=lambda r=r, c=c: self.bal_kattintas(r, c))
                btn.bind("<Button-3>", lambda e, r=r, c=c: self.jobb_kattintas(r, c))
                btn.grid(row=r, column=c)
                self.gombok[(r, c)] = btn

    def ido_frissitese(self):
        """Másodpercenként frissíti az időmérőt a felületen."""
        if self.fut_a_jatek:
            eltelt_ido = int(time.time() - self.start_ido)
            self.ido_label.config(text=f"Idő: {eltelt_ido}s")
            self.root.after(1000, self.ido_frissitese)

    def bal_kattintas(self, r, c):
        """Kezeli a mező felfedését és elindítja az órát az első kattintásnál."""
        if not self.fut_a_jatek and len(self.felfedett_mezok) == 0:
            self.start_ido = time.time()
            self.fut_a_jatek = True
            self.ido_frissitese()

        if (r, c) in self.zaszlok or (r, c) in self.felfedett_mezok:
            return

        # Kattintás limit kezelése (ha nem végtelen)
        if self.jatek.kattintasok is not None:
            if self.jatek.kattintasok <= 0:
                self.jatek_vege(False, "Elfogyott a kattintásod!")
                return
            self.jatek.kattintasok -= 1
            self.limit_label.config(text=f"Kattintások: {self.jatek.kattintasok}")

        ertek = self.jatek.tabla[r][c]
        if ertek == -1:
            self.gombok[(r, c)].config(text="💣", bg="red", fg="black")
            self.jatek_vege(False, "Aknára léptél!")
        else:
            self.felfed_rekurziv(r, c)
            self.gyozelem_ellenorzese()

     def felfed_rekurziv(self, r, c):
        """Rekurzív területfelfedés, ami csak 1 kattintásnak számít."""
        if (r, c) in self.felfedett_mezok or (r, c) in self.zaszlok:
            return
        
        self.felfedett_mezok.add((r, c))
        ertek = self.jatek.tabla[r][c]
        
        # Klasszikus aknakereső színek a számokhoz
        szinek = {1: "blue", 2: "green", 3: "red", 4: "purple", 5: "maroon", 6: "turquoise", 7: "black", 8: "gray"}
        
        color = "lightgrey" if ertek == 0 else "white"
        szoveg = str(ertek) if ertek > 0 else ""
        betuszin = szinek.get(ertek, "black")
        
        self.gombok[(r, c)].config(text=szoveg, bg=color, fg=betuszin, relief=tk.SUNKEN)

        if ertek == 0:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.jatek.sorok and 0 <= nc < self.jatek.oszlopok:
                        self.felfed_rekurziv(nr, nc)

    def jobb_kattintas(self, r, c):
        """Zászló elhelyezése jobb klikkel."""
        if (r, c) in self.felfedett_mezok:
            return
        if (r, c) in self.zaszlok:
            self.zaszlok.remove((r, c))
            self.gombok[(r, c)].config(text="", bg="SystemButtonFace", fg="black")
        else:
            self.zaszlok.add((r, c))
            self.gombok[(r, c)].config(text="🚩", fg="red")
        
        if self.jatek.kattintasok == 0:
            self.gyozelem_ellenorzese()

    def gyozelem_ellenorzese(self):
        """Ellenőrzi a győzelmi feltételeket mindkét módhoz."""
        osszes_mezo = self.jatek.sorok * self.jatek.oszlopok
        biztonsagos_db = osszes_mezo - self.jatek.aknak_szama
        
        gyozelem = False
        if len(self.felfedett_mezok) == biztonsagos_db:
            gyozelem = True
        elif self.jatek.kattintasok == 0 and self.zaszlok == self.jatek.aknak_helye:
            gyozelem = True

        if gyozelem:
            self.jatek_vege(True, "Gratulálok, nyertél!")

    def ablak_bezarasa(self):
        """Bezárja a játékot és visszajelez a főmenünek."""
        self.root.destroy()
        if self.on_close:
            self.on_close()

    def jatek_vege(self, gyozelem, uzenet):
        self.fut_a_jatek = False
        vegsos_ido = int(time.time() - self.start_ido) if self.start_ido else 0
        
        if gyozelem:
            mod_nev = "Limitált" if self.jatek.kattintasok is not None else "Klasszikus"
            storage.rekord_mentese(self.jatekos_neve, vegsos_ido, self.kategoria, mod_nev)
            uzenet += f"\n\nBekerültél a dicsőséglistába ({vegsos_ido} mp)!"

        messagebox.showinfo("Játék vége", f"{uzenet}")
        self.ablak_bezarasa() # Itt hívjuk meg a visszatérést!
