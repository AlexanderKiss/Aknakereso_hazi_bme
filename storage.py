import os

def rekord_mentese(nev, ido, kategoria, mod):
    """Elmenti a játékos eredményét kategóriánként tagolva."""
    # Formátum: Kategória;Mód;Név;Idő
    sor = f"{kategoria};{mod};{nev};{ido}\n"
    
    try:
        with open("rekordok.txt", "a", encoding="utf-8") as f:
            f.write(sor)
    except IOError as e:
        print(f"Hiba a mentés során: {e}")

def legjobb_eredmenyek_megtekintese():
    """Beolvassa, csoportosítja és sorba rendezi a rekordokat."""
    if not os.path.exists("rekordok.txt"):
        return "Még nincsenek mentett rekordok."
    
    eredmenyek = {} # Szótár a kategóriák tárolására
    try:
        with open("rekordok.txt", "r", encoding="utf-8") as f:
            for sor in f:
                adatok = sor.strip().split(';')
                if len(adatok) == 4:
                    kat, mod, nev, ido = adatok
                    kulcs = f"{kat} | {mod} mód"
                    
                    if kulcs not in eredmenyek:
                        eredmenyek[kulcs] = []
                    eredmenyek[kulcs].append((nev, int(ido)))
    except Exception as e:
        return f"Hiba a fájl olvasásakor: {e}"

    if not eredmenyek:
        return "Üres vagy hibás a rekordok fájl."

    # Szöveges kimenet generálása (Top 3 kategóriánként)
    szoveg = ""
    for kulcs, lista in eredmenyek.items():
        szoveg += f"🏆 {kulcs} 🏆\n"
        lista.sort(key=lambda x: x[1]) # Rendezzük idő szerint növekvőbe
        for i, (nev, ido) in enumerate(lista[:3], 1):
            szoveg += f"  {i}. {nev}: {ido} mp\n"
        szoveg += "\n"
        
    return szoveg