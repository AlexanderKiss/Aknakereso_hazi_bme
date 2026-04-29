import tkinter as tk
from tkinter import messagebox
import gui
import storage

class BeallitoMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Aknakereső - Főmenü")
        self.root.geometry("320x500") # Kicsit magasabb ablak, hogy minden elférjen
        
        # Bemeneti változók
        self.nev_var = tk.StringVar(value="Játékos")
        self.meret_var = tk.StringVar(value="Kicsi (9x9)")
        self.nehezseg_var = tk.StringVar(value="Kezdő (12%)")
        self.limit_var = tk.BooleanVar(value=False)
        
        self.egyedi_sor = tk.IntVar(value=10)
        self.egyedi_oszlop = tk.IntVar(value=10)
        
        self.felulet_epitese()

    def felulet_epitese(self):
        # Név megadása a menüben
        tk.Label(self.root, text="Játékos neve:", font=("Arial", 11, "bold")).pack(pady=(15, 0))
        tk.Entry(self.root, textvariable=self.nev_var, justify="center", font=("Arial", 11)).pack(pady=5)

        # Méret választó
        tk.Label(self.root, text="Pálya mérete:").pack(pady=(10,0))
        meretek = ["Kicsi (9x9)", "Közepes (16x16)", "Nagy (24x24)", "Egyedi"]
        for m in meretek:
            tk.Radiobutton(self.root, text=m, variable=self.meret_var, value=m, command=self.egyedi_mezok_valtasa).pack()

        # Egyedi méret beviteli mezői (alapból rejtve)
        self.egyedi_frame = tk.Frame(self.root)
        tk.Label(self.egyedi_frame, text="Sorok:").grid(row=0, column=0)
        tk.Entry(self.egyedi_frame, textvariable=self.egyedi_sor, width=5).grid(row=0, column=1, padx=5)
        tk.Label(self.egyedi_frame, text="Oszlopok:").grid(row=0, column=2)
        tk.Entry(self.egyedi_frame, textvariable=self.egyedi_oszlop, width=5).grid(row=0, column=3)

        # Nehézség választó
        tk.Label(self.root, text="Nehézség (Akna sűrűség):").pack(pady=(10, 0))
        nehezsegek = ["Kezdő (12%)", "Haladó (16%)", "Mester (21%)"]
        for n in nehezsegek:
            tk.Radiobutton(self.root, text=n, variable=self.nehezseg_var, value=n).pack()

        # Limitált mód
        tk.Checkbutton(self.root, text="Kattintás-korlátolt mód", variable=self.limit_var).pack(pady=15)

        # Gombok egy sorban
        gomb_frame = tk.Frame(self.root)
        gomb_frame.pack(pady=10)
        
        tk.Button(gomb_frame, text="🏆 Ranglista", command=self.mutas_ranglista, bg="gold", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5)
        tk.Button(gomb_frame, text="▶ Indítás", command=self.jatek_inditasa, bg="lightgreen", font=("Arial", 10, "bold")).grid(row=0, column=1, padx=5)

    def egyedi_mezok_valtasa(self):
        if self.meret_var.get() == "Egyedi":
            self.egyedi_frame.pack(pady=5)
        else:
            self.egyedi_frame.pack_forget()

    def mutas_ranglista(self):
        """Megjeleníti a dicsőséglistát a menüből kattintva."""
        rekordok = storage.legjobb_eredmenyek_megtekintese()
        messagebox.showinfo("Dicsőséglista", rekordok)

    def jatek_inditasa(self):
        nev = self.nev_var.get().strip()
        if not nev:
            messagebox.showwarning("Hiba", "Kérlek, add meg a neved a játék kezdete előtt!")
            return

        meret_szoveg = self.meret_var.get()
        nehezseg_szoveg = self.nehezseg_var.get()

        if meret_szoveg == "Kicsi (9x9)":
            sor, oszlop = 9, 9
        elif meret_szoveg == "Közepes (16x16)":
            sor, oszlop = 16, 16
        elif meret_szoveg == "Nagy (24x24)":
            sor, oszlop = 24, 24
        else:
            sor = max(5, min(self.egyedi_sor.get(), 30))
            oszlop = max(5, min(self.egyedi_oszlop.get(), 30))
            meret_szoveg = f"Egyedi ({sor}x{oszlop})"

        osszes_mezo = sor * oszlop

        if "Kezdő" in nehezseg_szoveg:
            aknak = int(osszes_mezo * 0.12)
        elif "Haladó" in nehezseg_szoveg:
            aknak = int(osszes_mezo * 0.16)
        else:
            aknak = int(osszes_mezo * 0.21)
            
        aknak = max(1, aknak)

        limit = None
        if self.limit_var.get():
            biztonsagos_mezok = osszes_mezo - aknak
            limit = max(5, int(biztonsagos_mezok * 0.4)) 

        kategoria = f"{meret_szoveg} - {nehezseg_szoveg[:6]}"

        # Menü elrejtése a bezárás helyett
        self.root.withdraw()
        
        # Játék ablak megnyitása (Toplevel = a főablak "gyermeke")
        jatek_ablak = tk.Toplevel(self.root)
        
        # Átadjuk a deiconify-t, hogy a játék végén újra megjelenjen a menü
        app = gui.AknakeresoGUI(jatek_ablak, sor, oszlop, aknak, limit, kategoria, nev, on_close=self.root.deiconify)

def main():
    root = tk.Tk()
    app = BeallitoMenu(root)
    root.mainloop()

if __name__ == "__main__":
    main()