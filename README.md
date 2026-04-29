# Aknakereső - Python Projekt

Ez a projekt a klasszikus Aknakereső játék egy Pythonban és Tkinterben megírt, kibővített változata. A program platformfüggetlen, objektumorientált és moduláris felépítéssel készült, megfelelve a Python 3.12-es szabványoknak.

## Jellemzők és Funkciók
A játék az alábbi főbb funkciókkal rendelkezik:
* **Központi Főmenü:** Kényelmes felület a név, a pálya és a játékmódok beállítására. A játék végén a program visszatér ide.
* **Dinamikus Méret és Nehézség:** Választható előre definiált méretek (Kicsi, Közepes, Nagy), vagy teljesen egyedi NxM-es pálya. A nehézség (Kezdő, Haladó, Mester) az aknák sűrűségét szabályozza.
* **Két Játékmód:** * *Klasszikus:* Végtelen kattintás, a cél a legjobb idő elérése.
  * *Kattintás-korlátolt (Extra):* A játékosnak limitált lépésszámból kell kitalálnia az aknák helyét.
* **Intelligens Dicsőséglista (Fájlkezelés):** A program a `rekordok.txt` fájlba menti a győzelmeket kategóriák (méret + nehézség + mód) szerint szétválogatva, és top 3-as listát készít.
* **Automatikus területfelfedés:** Üres (0-ás) mezőre kattintva a program rekurzívan felfedi a szomszédos biztonságos területeket (ami limitált módban is csak 1 kattintásnak számít!).

## Telepítés és Futtatás
A program futtatásához **Python 3.12** (vagy újabb) verzió ajánlott. Külső, harmadik féltől származó könyvtárakat nem igényel, kizárólag beépített modulokat (`tkinter`, `os`, `time`, `random`) használ, így a telepítés és futtatás teljesen platformfüggetlen.

1. Töltsd le vagy csomagold ki a projekt mappáját.
2. Győződj meg róla, hogy a mappában szerepel a `requirements.txt` fájl (a követelményeknek megfelelően, jelen esetben üresen).
3. Indítsd el a programot a fő modul futtatásával a terminálból vagy a fejlesztőkörnyezetből (pl. VS Code):
   ```bash
   python main.py
