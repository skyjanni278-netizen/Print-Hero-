# 🗡️ Terminal RPG — Spielhandbuch

> Ein rundenbasiertes Terminal-RPG in Python. Kämpfe dich durch Gegnerhorden, sammle Beute und steige bis Level 10 auf.

---

## 📁 Dateistruktur

```
main.py          – Spielschleife & Einstiegspunkt
player.py        – Spieler-Klasse, Inventar, Fähigkeiten
monsters.py      – Gegner-Klassen & Rang-System
combat.py        – Kampflogik & Aktionen
loot_tables.py   – Loot-Pools, Drops, Item-Definitionen
pause.py         – Lagerfeuer, Inventar, Verkauf
shop.py          – Händler
save.py          – Speichern & Laden (JSON)
utils.py         – Hilfsfunktionen (clear_screen etc.)
```

---

## ⚔️ Kampf-Aktionen

| Taste | Aktion                  | Energie | Beschreibung                              |
|-------|-------------------------|--------:|-------------------------------------------|
| A     | Angreifen               | —       | Normaler Angriff auf ein Ziel             |
| S     | Himmelsschlag           | 20      | Starker Einzelangriff (+5 Bonusschaden)   |
| R     | Rundumschlag            | 15      | Trifft alle lebenden Gegner (−2 Schaden)  |
| C     | Cleave                  | 10      | Angriff + 3 Blutungsstacks auf Ziel       |
| U     | Verbrauchsgegenstände   | —       | Öffnet Inventar für Tränke & Items        |
| F     | Fliehen                 | —       | Verlässt den Kampf                        |
| Q     | Beenden                 | —       | Spiel sofort beenden                      |

**Blutung:** Jeder Stack verursacht 3 Schaden pro Runde und reduziert sich dabei um 1.  
**Energie-Regeneration:** +3 Energie automatisch pro Runde.

---

## 📈 Level-Progression

Der Spieler startet bei Level 1 und kann bis **Level 10** aufsteigen.  
Pro Level-Up: **+4 max. HP**, **+1 ATK**, **+1 min. ATK**. HP wird vollständig aufgefüllt.

### XP-Schwellen

| Level  | XP für dieses Level | Gesamt-XP |
|--------|--------------------:|----------:|
| 1 → 2  |   80 XP |    80 XP |
| 2 → 3  |  104 XP |   184 XP |
| 3 → 4  |  135 XP |   319 XP |
| 4 → 5  |  175 XP |   494 XP |
| 5 → 6  |  227 XP |   721 XP |
| 6 → 7  |  295 XP | 1.016 XP |
| 7 → 8  |  383 XP | 1.399 XP |
| 8 → 9  |  497 XP | 1.896 XP |
| 9 → 10 |  646 XP | 2.542 XP |

> **Ø ~5 Kämpfe pro Level** bei einer Gruppe von 1–3 Gegnern.

### Spieler-Basiswerte nach Level

| Level | max. HP | Basis-ATK |
|------:|--------:|----------:|
|     1 |      30 |        10 |
|     2 |      34 |        11 |
|     3 |      38 |        12 |
|     4 |      42 |        13 |
|     5 |      46 |        14 |
|     6 |      50 |        15 |
|     7 |      54 |        16 |
|     8 |      58 |        17 |
|     9 |      62 |        18 |
|    10 |      66 |        19 |

> Zusätzlich kommen Waffen-ATK und Rüstungs-DEF aus der Ausrüstung dazu.

---

## 👹 Gegner

### Basis-Werte (Rang 1)

| Gegner       | HP | ATK | DEF | Basis-XP | Erscheint ab | Verschwindet ab |
|--------------|----|-----|-----|----------|-------------|-----------------|
| Schleim      |  8 |   3 |   0 |  10 XP   | Level 1     | Level 5         |
| Schattenwolf | 11 |   6 |   0 |  16 XP   | Level 1     | Level 7         |
| Goblin       | 10 |   5 |   1 |  15 XP   | Level 1     | Level 9         |
| Zombie       | 20 |   4 |   2 |  18 XP   | Level 1     | Level 9         |
| Bandit       | 14 |   7 |   0 |  20 XP   | Level 2     | —               |
| Waldtroll    | 35 |   6 |   4 |  30 XP   | Level 3     | —               |
| Skelett      | 12 |   8 |   1 |  24 XP   | Level 5     | —               |
| Drache       | 50 |  15 |   7 |  60 XP   | Level 7     | —               |

### Mob-Pool nach Spieler-Level

| Spieler-Level | Mögliche Gegner                                                                        | Gruppengröße |
|---------------|----------------------------------------------------------------------------------------|:------------:|
| 1 – 2         | Schleim (45%), Schattenwolf (35%), Goblin (20%)                                        | 1–2          |
| 3 – 4         | Schleim (20%), Schattenwolf (30%), Goblin (20%), Bandit (15%), Zombie (15%)            | 1–2          |
| 5 – 6         | Schattenwolf (20%), Goblin (15%), Bandit (20%), Zombie (20%), Waldtroll (15%), Skelett (10%) | 1–3     |
| 7 – 8         | Goblin (10%), Bandit (20%), Zombie (15%), Waldtroll (20%), Skelett (25%), Drache (10%) | 1–3 / 2–4   |
| 9 – 10        | Bandit (10%), Waldtroll (25%), Skelett (35%), Drache (30%)                             | 2–4          |

---

## 🏅 Gegner-Ränge

Jeder Gegner erhält beim Spawn zufällig einen Rang, der seine Werte skaliert.  
Höhere Spieler-Level erhöhen die Wahrscheinlichkeit für starke Ränge.

| Rang | Titel         | HP-Mult | ATK-Mult | XP-Mult | Loot-Rolls |
|:----:|---------------|--------:|---------:|--------:|:----------:|
|  1   | *(kein)*      |   ×1,0  |    ×1,0  |   ×1,0  |     1      |
|  2   | ⚔️ Starker    |   ×1,4  |    ×1,3  |   ×1,4  |     2      |
|  3   | 💀 Eliter     |   ×2,0  |    ×1,6  |   ×2,0  |     3      |
|  4   | 👑 Champion   |   ×3,0  |    ×2,0  |   ×3,0  |     4      |
|  5   | 🔥 Boss       |   ×5,0  |    ×2,8  |   ×5,0  |     6      |

### Rang-Wahrscheinlichkeit nach Spieler-Level

| Spieler-Level | Rang 1 | Rang 2 | Rang 3 | Rang 4 | Rang 5 |
|---------------|-------:|-------:|-------:|-------:|-------:|
| 1 – 2         |  75 %  |  22 %  |   3 %  |   0 %  |   0 %  |
| 3 – 4         |  50 %  |  33 %  |  14 %  |   3 %  |   0 %  |
| 5 – 6         |  30 %  |  35 %  |  25 %  |   9 %  |   1 %  |
| 7 – 8         |  15 %  |  30 %  |  30 %  |  20 %  |   5 %  |
| 9 – 10        |   5 %  |  20 %  |  30 %  |  30 %  |  15 %  |

---

## 🎲 Loot-System

Nach jedem Sieg wird Loot pro Gegner gewürfelt. Die Anzahl der Würfe hängt vom **Rang** des Gegners ab.

### Drop-Wahrscheinlichkeiten nach Rang

| Loot-Seltenheit  | Rang 1 | Rang 2 | Rang 3 | Rang 4 | Rang 5 |
|------------------|-------:|-------:|-------:|-------:|-------:|
| ⬜ Gewöhnlich     |  80 %  |  62 %  |  42 %  |  22 %  |   8 %  |
| 🟩 Ungewöhnlich   |  18 %  |  28 %  |  32 %  |  30 %  |  20 %  |
| 🟦 Selten         |   2 %  |   9 %  |  20 %  |  30 %  |  32 %  |
| 🟪 Episch         |   0 %  |   1 %  |   5 %  |  15 %  |  30 %  |
| 🟨 Legendär       |   0 %  |   0 %  |   1 %  |   3 %  |  10 %  |

---

## 🗺️ Loot-Tabelle

### ⬜ Gewöhnlich
| Item           | Typ        | Menge / Wert        |
|----------------|------------|---------------------|
| Healing Potion | Consumable | 1 Stk (Heilt 10 HP) |
| Gold           | Gold       | 3 – 10 Gold         |
| Altes Seil     | Schrott    | 1 – 2 Stk           |
| Lumpen         | Schrott    | 1 – 3 Stk           |
| Knochen        | Schrott    | 1 – 2 Stk           |
| Antidot        | Consumable | 1 Stk               |
| Lederkappe     | Helm       | DEF +1              |
| Kurzschwert    | Waffe      | ATK +3              |
| Lederrüstung   | Rüstung    | DEF +2              |
| Lederstiefel   | Schuhe     | DEF +1              |
| Eisenstiefel   | Schuhe     | DEF +2              |

### 🟩 Ungewöhnlich
| Item                   | Typ        | Menge / Wert         |
|------------------------|------------|----------------------|
| Großes Heiltrank       | Consumable | 1 Stk (Heilt 25 HP)  |
| Gold                   | Gold       | 10 – 25 Gold         |
| Energie-Kristall       | Consumable | 1 Stk (+15 Energie)  |
| Stärketrank            | Consumable | 1 Stk (+3 ATK)       |
| Schleimklumpen         | Schrott    | 1 – 2 Stk            |
| Goblinzahn             | Schrott    | 1 – 2 Stk            |
| Eisenhelm              | Helm       | DEF +2               |
| Langschwert            | Waffe      | ATK +6               |
| Kriegshammer           | Waffe      | ATK +9               |
| Kettenhemd             | Rüstung    | DEF +4               |
| Plattenpanzer          | Rüstung    | DEF +7               |
| Schnellläuferstiefel   | Schuhe     | DEF +4               |

### 🟦 Selten
| Item         | Typ        | Menge / Wert        |
|--------------|------------|---------------------|
| Gold         | Gold       | 25 – 60 Gold        |
| Elixier      | Consumable | 1 Stk (Heilt 40 HP) |
| Energie-Kristall | Consumable | 1 – 2 Stk       |
| Stahlhelm    | Helm       | DEF +4              |
| Runenschwert | Waffe      | ATK +13             |
| Runenrüstung | Rüstung    | DEF +10             |
| Runenhelm    | Helm       | DEF +6              |
| Runenstiefel | Schuhe     | DEF +6              |

### 🟪 Episch
| Item            | Typ        | Menge / Wert            |
|-----------------|------------|-------------------------|
| Gold            | Gold       | 60 – 120 Gold           |
| Phönixfeder     | Consumable | 1 Stk (15 HP + Cleanse) |
| Stärketrank     | Consumable | 1 – 2 Stk               |
| Drachenzahn     | Waffe      | ATK +17                 |
| Drachenschuppen | Rüstung    | DEF +14                 |
| Drachenkrone    | Helm       | DEF +9                  |
| Drachenklauen   | Schuhe     | DEF +9                  |

### 🟨 Legendär
| Item                  | Typ     | Wert           |
|-----------------------|---------|----------------|
| Gold                  | Gold    | 150 – 300 Gold |
| Göttliche Klinge      | Waffe   | ATK +25        |
| Rüstung des Lichts    | Rüstung | DEF +20        |
| Krone des Ewigen      | Helm    | DEF +13        |
| Stiefel der Ewigkeit  | Schuhe  | DEF +12        |

---

## 🛡️ Equipment-Progression

Es gibt **vier Ausrüstungsslots**: Waffe, Rüstung, Helm, Schuhe.  
Epic & Legendär sind nur durch Loot erhältlich — nicht im Shop.

### Waffen

| Stufe      | Name              | ATK  | Quelle      | Verkauf  |
|------------|-------------------|-----:|-------------|--------:|
| ⬜ Common   | Kurzschwert       |  +3  | Shop / Loot |  20 Gold |
| 🟩 Uncommon | Langschwert       |  +6  | Shop / Loot |  40 Gold |
| 🟩 Uncommon | Kriegshammer      |  +9  | Shop / Loot |  60 Gold |
| 🟦 Rare     | Runenschwert      | +13  | Shop / Loot | 100 Gold |
| 🟪 Epic     | Drachenzahn       | +17  | Nur Loot    | 160 Gold |
| 🟨 Legendär | Göttliche Klinge  | +25  | Nur Loot    | 350 Gold |

### Rüstungen

| Stufe      | Name                | DEF  | Quelle      | Verkauf  |
|------------|---------------------|-----:|-------------|--------:|
| ⬜ Common   | Lederrüstung        |  +2  | Shop / Loot |  17 Gold |
| 🟩 Uncommon | Kettenhemd          |  +4  | Shop / Loot |  35 Gold |
| 🟩 Uncommon | Plattenpanzer       |  +7  | Shop / Loot |  60 Gold |
| 🟦 Rare     | Runenrüstung        | +10  | Shop / Loot | 100 Gold |
| 🟪 Epic     | Drachenschuppen     | +14  | Nur Loot    | 160 Gold |
| 🟨 Legendär | Rüstung des Lichts  | +20  | Nur Loot    | 350 Gold |

### Helme

| Stufe      | Name             | DEF  | Quelle      | Verkauf  |
|------------|------------------|-----:|-------------|--------:|
| ⬜ Common   | Lederkappe       |  +1  | Shop / Loot |  12 Gold |
| ⬜ Common   | Eisenhelm        |  +2  | Shop / Loot |  22 Gold |
| 🟩 Uncommon | Stahlhelm        |  +4  | Shop / Loot |  45 Gold |
| 🟦 Rare     | Runenhelm        |  +6  | Shop / Loot |  90 Gold |
| 🟪 Epic     | Drachenkrone     |  +9  | Nur Loot    | 140 Gold |
| 🟨 Legendär | Krone des Ewigen | +13  | Nur Loot    | 300 Gold |

### Schuhe

| Stufe      | Name                   | DEF  | Quelle      | Verkauf  |
|------------|------------------------|-----:|-------------|--------:|
| ⬜ Common   | Lederstiefel           |  +1  | Shop / Loot |  10 Gold |
| ⬜ Common   | Eisenstiefel           |  +2  | Shop / Loot |  20 Gold |
| 🟩 Uncommon | Schnellläuferstiefel   |  +4  | Shop / Loot |  42 Gold |
| 🟦 Rare     | Runenstiefel           |  +6  | Shop / Loot |  85 Gold |
| 🟪 Epic     | Drachenklauen          |  +9  | Nur Loot    | 130 Gold |
| 🟨 Legendär | Stiefel der Ewigkeit   | +12  | Nur Loot    | 280 Gold |

---

## 🧪 Consumables

| Item               | Effekt                         | Max-Stapel | Quelle      | Verkauf |
|--------------------|--------------------------------|:----------:|-------------|--------:|
| 🧪 Healing Potion   | Heilt 10 HP                    |     5      | Shop / Loot |  7 Gold |
| 🍶 Großes Heiltrank | Heilt 25 HP                    |     5      | Shop / Loot | 17 Gold |
| ✨ Elixier          | Heilt 40 HP                    |     3      | Nur Loot    | 30 Gold |
| 🪶 Phönixfeder      | Heilt 15 HP + entfernt Blutung |     3      | Nur Loot    | 40 Gold |
| 💎 Energie-Kristall | +15 Energie                    |     5      | Shop / Loot | 12 Gold |
| 💪 Stärketrank      | +3 ATK (für diesen Kampf)      |     3      | Shop / Loot | 20 Gold |
| 🌿 Antidot          | Entfernt alle Blutungsstacks   |     5      | Shop / Loot |  5 Gold |

---

## 🗑️ Schrott-Items

Schrott hat keinen Effekt — ausschließlich zum Verkaufen.

| Item                | Emoji | Verkauf |
|---------------------|-------|--------:|
| Altes Seil          | 🪢    |  3 Gold |
| Lumpen              | 🧣    |  2 Gold |
| Knochen             | 🦴    |  4 Gold |
| Schleimklumpen      | 🟢    |  5 Gold |
| Goblinzahn          | 🦷    |  6 Gold |
| Wolfspelz           | 🐺    |  7 Gold |
| Trollfell           | 🐾    |  8 Gold |
| Banditen-Abzeichen  | 🏴    |  9 Gold |

---

## 🎒 Inventar-System

- **20 Slots** insgesamt
- Jeder einzigartige Consumable-/Schrott-Stapel = **1 Slot**
- Jedes Equipment-Stück = **1 Slot** (nicht stapelbar)
- Consumables haben ein **Stack-Limit** (siehe Tabelle oben)
- Bei vollem Inventar oder vollem Stapel geht der Drop verloren

---

## 💾 Speichern & Laden

Das Spiel speichert in `savegame.json` im Spielverzeichnis.  
Alte Saves werden automatisch migriert — fehlende Slots (Helm, Schuhe) werden mit Starter-Items ergänzt.

---

## 🚀 Starten

```bash
python main.py
```

Benötigt Python 3.10+, keine externen Pakete.
