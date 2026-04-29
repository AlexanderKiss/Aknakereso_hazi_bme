import random

class AknakeresoLogika:
    def __init__(self, sorok, oszlopok, aknak_szama, kattintas_limit=None):
        self.sorok = sorok
        self.oszlopok = oszlopok
        self.aknak_szama = aknak_szama
        self.kattintasok = kattintas_limit
        # A tábla reprezentációja: 0-8 számok vagy -1 az akna
        self.tabla = [[0 for _ in range(oszlopok)] for _ in range(sorok)]
        self.aknak_helye = set()
        self.general_palyat()

    def general_palyat(self):
        """Véletlenszerűen elhelyezi az aknákat és kiszámolja a szomszédokat."""
        lerakott_akna = 0
        while lerakott_akna < self.aknak_szama:
            r = random.randint(0, self.sorok - 1)
            c = random.randint(0, self.oszlopok - 1)
            if (r, c) not in self.aknak_helye:
                self.aknak_helye.add((r, c))
                self.tabla[r][c] = -1
                lerakott_akna += 1
                self._szomszedok_frissitese(r, c)

    def _szomszedok_frissitese(self, r, c):
        """Megnöveli a környező mezők értékét eggyel."""
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.sorok and 0 <= nc < self.oszlopok:
                    if self.tabla[nr][nc] != -1:
                        self.tabla[nr][nc] += 1