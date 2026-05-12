import random

class AknakeresoLogika:
    def __init__(self, sorok, oszlopok, aknak_szama, kattintas_limit=None):
        self.sorok = sorok
        self.oszlopok = oszlopok
        self.aknak_szama = aknak_szama
        self.kattintasok = kattintas_limit
        
        # Kezdetben teljesen üres táblát hozunk létre (0-k)
        self.tabla = [[0 for _ in range(oszlopok)] for _ in range(sorok)]
        self.aknak_helye = set()
        self.elso_kattintas_megvolt = False

    def general_palyat(self, elso_r, elso_c):
        """Véletlenszerűen elhelyezi az aknákat, kihagyva az első kattintást és szomszédait."""
        biztonsagos_mezok = set()
        
        # A kattintott mező és 8 szomszédja védett lesz
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                biztonsagos_mezok.add((elso_r + dr, elso_c + dc))

        elerheto_helyek = []
        for r in range(self.sorok):
            for c in range(self.oszlopok):
                if (r, c) not in biztonsagos_mezok:
                    elerheto_helyek.append((r, c))
                    
        # Extrém eset (pl. túl sok akna egy pici pályán), ahol a szomszédok védelme nem férne el
        if len(elerheto_helyek) < self.aknak_szama:
            biztonsagos_mezok = {(elso_r, elso_c)} # Ekkor csak magát a kattintott mezőt védjük
            elerheto_helyek = [(r, c) for r in range(self.sorok) for c in range(self.oszlopok) if (r, c) not in biztonsagos_mezok]

        # Aknák kisorsolása
        aknak = random.sample(elerheto_helyek, self.aknak_szama)
        for r, c in aknak:
            self.aknak_helye.add((r, c))
            self.tabla[r][c] = -1
            self._szomszedok_frissitese(r, c)
            
        self.elso_kattintas_megvolt = True

    def _szomszedok_frissitese(self, r, c):
        """Megnöveli a környező mezők értékét eggyel az aknák körül."""
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.sorok and 0 <= nc < self.oszlopok:
                    if self.tabla[nr][nc] != -1:
                        self.tabla[nr][nc] += 1
