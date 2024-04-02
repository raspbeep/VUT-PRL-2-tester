## TESTY NA 2. PRL PROJEKT - GAME OF LIFE

Testy predpokladaju implementaciu na uzavrenom gride (ziadny wrap-around), teda mimo vstupneho pola je vzdy nula.

#### ❗ Requirements
* Python 3

#### Pouzitie
1. Naklonujte repozitar do zlozky s game of life binarkou alebo zmente `EXECUTABLE` v `main.py`
2. Spustite `python3 main.py`

#### Priebeh testu
1. Vygenerovanie testcase-ov podla parametrov v `main.py`
2. Spustia sa vsetky mozne prednastavene konfiguracie parametrov:
   - `np` - pocet procesov s ktorym sa spusta binarka
   - `it` - pocet iteracii od inicialneho stavu
3. Pomocou `sed` sa vymaze zaciatok riadku vystupu binarky obsahujuci `rank_id: ` a ponecha sa iba zvysok riadku
4. Porovna sa referencny vystup s upravenym z binarky

- Pri neuspesnom teste (referencny vystup `i_{idx}.txt` != `case_{test_id}_np_{n_processes}_it_{iterations}.out`) sa rozdiel suborov ulozi do `case_{idx}/difference` a python skript na to upozorni na `stdout` za behu.


- Vsetky medzivysledky (stdout/stderr z binarky) sa ukladaju do zlozky daneho test case-u pod nazvom: `case_{test_id}/case_{test_id}_np_{n_processes}_it_{iterations}.out/.err` kde:
    - `test-id`     - id test case-u
    - `n_processes` - pocet procesov pri spusteni
    - `iterations`  - pocet iteracii pri spusteni

  Takze k neuspesnym testom sa da vratit a skusit ich spusti manualne, pripadne porovnat vysledky rucne atd.

#### ⚠️ Disclaimer
* Testy su IBA orientacne.

* Testy uplne ignoruju zaciatky riadkov obsahujuce `rank_id: `, kedze toto je velmi zavisle od zvolenej implementacie.

* Neviem ako budu testy fungovat na wine, ked tak niekto poslite PR s fixom.

#### Struktura generovanych testovacich suborob
Skript generuje subory `input.txt` a nasledne stav po kazdej iteracii pre zadany pocet iteracii. Na konci kazdeho zo suborov je newline.

Vygeneruje sa struktura suborov:

* zlozka `./tests/`

  * `case_{id}/` podzlozka pre jednotlive test cases

    * `input.txt` inicialny stav pola:
        ```
        001000
        011001
        001100
        010110
        100001
        001010
        110111
        011001
        ```
    *  `i_{it}.txt` referencny stav pola po `it` pocte iteracii (napr. `i_1.txt`):
        ```
        011000
        010000
        000000
        010110
        011001
        101000
        100001
        111101
        ```
