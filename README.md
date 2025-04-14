# RIK Programmeerija prooviülesanne (Python)

## Eesmärk
Osaühingute otsimine, info vaatamine ja loomine.

## Funktsionaalsused
* Avaleht osaühingute otsingu võimalusega
    - Otsingu võimalus osaühingu nime, registrikoodi, osanike ja nende isikukoodi või registrikoodi järgi
* Valitud osaühingu andmete vaatamine
* Uue osaühingu loomine
    - Võimalus otsida ja lisada juba andmebaasis olevaid isikuid nime järgi

## Eeltingimused
- Python 3.x

## Rakenduse käivitamine
1. Klooni repositoorium:
    ```bash
    git clone https://github.com/tikukatre/RIKAssignmentPython.git
    ```
2. Mine rakenduse peakausta:
    ```bash
    cd RIKAssignmentPython
    ```
3. Paigalda ja käivita virtuaalne keskkond (valikuline):
    ```bash
    python -m venv venv
    venv\Scripts\activate #Windows 
    source venv/bin/activate #Mac
    ```
4. Vajaliku Pythoni tarkvara laadimine
    ```bash
    pip install -r requirements.txt
    ```
5. Algandmete loomine andmebaasi
    ```bash
    python data.py
    ```
6. Rakenduse käivitamine
     ```bash
    python app.py
    ```
7. Ava http://127.0.0.1:5000



## Mõned võimalikud täiendused
* Luua olemas olevate osanike otsingu funkstionaalsus Javascriptiga. Hetkel on kasutusel puhtalt Python ja Flask selle rakendamiseks, mis ei ole eriti dünaamiline ja isikut otsides, lisades ja eemaldades laeb osaühingu asutamise vormi uuesti, tühjendas vormi väljad. Samas saaks ka sessiooni sees vormi andmeid salvestada ja selles olukorras lasta need programmil tagasi sisestada. 
* Otsingu piiramine. Hetkel saab osaühinguid üsna vabalt otsida filtrite abil kus registrikoodid, isiku andmed võivad samuti nimede moodi fragmendina olla, kuid suurte andmete puhul ei ole see alati efektiivne.
* Luua parem veateate süsteem, et iga kasutaja vea peale on korralik tagasiside, mis on valesti. Näiteks kui kogukapitali suurus ei ühti osanike osade suurustega. 


