# 🗡️ Print-Hero

> Ein rundenbasiertes Terminal-Dungeon-Crawler RPG in Python.  
> Wähle deine Klasse, kämpfe dich durch 5 Zonen, besiege Zonen-Bosse und rette das Reich.

**Aktuelle Version: v2.0** | Python 3.10+ | Keine externen Pakete

---

## 🚀 Starten

```bash
python main.py
```

---

## 📁 Projektstruktur

```
main.py                  — Spielschleife & Einstiegspunkt
config.py                — Schwierigkeitsgrade & globale Konstanten
core/
  player.py              — Spieler-Klasse, Inventar, Skills, Equipment
  combat.py              — Kampflogik, Fähigkeiten, Loot-Vergabe
  save.py                — Speichern & Laden (JSON, 3 Slots)
content/
  monsters.py            — Alle Gegner-Klassen, Rang-System, Boss-Fähigkeiten
  loot_tables.py         — Loot-Pools, Item-Definitionen, Set-Definitionen
  shop.py                — Händler-Sortiment
  classes.py             — Klassen-Definitionen & Startboni
systems/
  dungeon.py             — Dungeon-Schleife, Raumgenerierung, Raumtypen
  zones.py               — Zonen-Definitionen, Monster-Pools, Rang-Gewichtung
  world_map.py           — Weltkarte, Zonen-Bosse, Endscreen, zone_progress
  events.py              — Zufalls-Events zwischen Räumen
  skilltree.py           — Skill-Auswahl & Skill-Effekte
  achievements.py        — Achievement-System (20 Errungenschaften)
saves/
  savegame_1.json        — Spielstand Slot 1 (automatisch erstellt)
  savegame_2.json        — Spielstand Slot 2
  savegame_3.json        — Spielstand Slot 3
ui/
  pause.py               — Lagerfeuer-Menü, Inventar, Verkauf, Skills
  utils.py               — clear_screen, print_header
```

---

## 🎮 Spielsysteme

### Klassen
Beim Start wählst du eine von drei Klassen — jede hat unterschiedliche Startwerte und drei einzigartige Kampffähigkeiten:

| Klasse | Start-HP | Start-ATK | Fähigkeit 1 (immer) | Fähigkeit 2 (LVL 4) | Fähigkeit 3 (LVL 7) |
|--------|:--------:|:---------:|---------------------|---------------------|---------------------|
| ⚔️ Krieger | 40 | 8 | Schildwall — blockiert einen Angriff | Schildstoß — Schaden + Betäubung | Kriegsschrei — +5 ATK für diesen Kampf |
| 🗡️ Schurke | 28 | 12 | Aus dem Schatten — Krit + ignoriert DEF | Giftklinge — Angriff + 3 Giftstacks | Rauchbombe — garantierte Flucht |
| 🪄 Magier | 22 | 10 | Arkane Entladung — AoE-Magieschaden | Froststrahl — Schaden + Einfrieren | Mana-Schild — nächster Schaden via Energie |

---

### Zonen
Das Spiel ist in **5 Zonen** unterteilt, die sequenziell freigeschaltet werden.  
**Voraussetzung:** Mindestlevel + Zonen-Boss der vorherigen Zone besiegt.

| Zone | Emoji | Min. Level | Zonen-Boss | Dungeons bis Boss |
|------|-------|:----------:|-----------|:-----------------:|
| Wald | 🌲 | 1 | Torg, Wächter des Waldes | 3 |
| Ruinen | 🏚️ | 2 | Korroth, der Ewige Wächter | 4 |
| Wüste | 🏜️ | 4 | Razin, König der Meuchler | 5 |
| Vulkan | 🌋 | 6 | Ignar, der Ewige Drache | 6 |
| Dunkel-Reich | 💀 | 8 | Malachar, Herr der Finsternis | 7 |

**Progression:** N Dungeons abschließen → **[B] Zonen-Boss** → nächste Zone öffnet sich.  
Die **Weltkarte** ist jederzeit über **[Z]** im Lagerfeuer erreichbar.

---

### Dungeon-System
Jeder Dungeon besteht aus **3–5 Räumen**, der letzte Raum ist immer der Boss.

| Symbol | Typ | Beschreibung |
|--------|-----|-------------|
| ⚔️ | Kampf | 1–3 Gegner gleichzeitig |
| 💪 | Elite-Gegner | Rang-2-Einzelkämpfer, bessere Beute |
| 💀 | Mini-Boss | Rang-3-Gegner, gute Drops |
| 🎲 | Ereignis | Zufälliger Event (Händler, Schrein, Falle…) |
| 🕯️ | Schrein | Segnung wählen: HP / Energie / XP-Buff — oder Fluch wagen |
| ⚠️ | Falle | Ausweichen (kostet Energie) oder Schaden nehmen |
| 🌫️ | Leerer Raum | Flavor-Text + Chance auf versteckten Loot |
| 🔥 | Boss | Rang-4/5-Gegner mit Bonus-Loot |

Zwischen Räumen kannst du ausrüsten, Tränke benutzen und den nächsten Raum einsehen.  
Bei vollständigem Abschluss: **volle HP/Energie-Wiederherstellung**.  
Flucht jederzeit möglich — ohne Abschluss kein Loot, keine Heilung.

---

### Kampf
Rundenbasiert. Der Kampf-Screen zeigt HP-Balken, Statuseffekte und Zone auf einen Blick.

| Taste | Aktion | Energie | Beschreibung |
|-------|--------|:-------:|-------------|
| A | Angreifen | — | Normaler Angriff auf einen Gegner |
| S | Himmelsschlag | 20 | Starker Einzelangriff (ab LVL 5) |
| R | Rundumschlag | 15 | Trifft alle lebenden Gegner (ab LVL 3) |
| C | Cleave | 10 | Angriff + 3 Blutungsstacks (ab LVL 2) |
| X | Klassen-Fähigkeit 1 | — | Einmal pro Kampf |
| 1 | Klassen-Fähigkeit 2 | variabel | Einmal pro Kampf (ab LVL 4) |
| 2 | Klassen-Fähigkeit 3 | variabel | Einmal pro Kampf (ab LVL 7) |
| M | Magieschild | — | Blockt nächsten Angriff (wenn verfügbar) |
| U | Verbrauchsgegenstände | — | Tränke & Items im Kampf |
| F | Fliehen | — | Verlässt den Kampf |

**Statuseffekte:**
- **Blutung:** Jeder Stack → 3 Schaden/Runde, reduziert sich um 1 Stack
- **Gift:** Schaden pro Runde, steigt mit der Stack-Anzahl
- **Betäubung:** Betroffene überspringen die nächste Runde
- **Säure-Debuff:** Temporäre DEF-Reduktion für den laufenden Kampf
- **Energie-Regeneration:** +3 Energie automatisch am Ende jeder Runde

Bei **Einzelgegner** entfällt die Zielauswahl — automatisches Auto-Targeting.

---

### Charakter-Progression

| Level | max. HP (je Klasse) | Basis-ATK |
|------:|:-------------------:|----------:|
| 1 | 22 – 40 | 8 – 12 |
| 5 | 38 – 56 | 12 – 16 |
| 10 | 58 – 76 | 17 – 21 |

Pro Level-Up: **+4 max. HP**, **+1 ATK**, HP wird aufgefüllt.  
Ab Level 2: **Skillpunkte** für den Skill-Tree.

---

### Skill-Tree
Skillpunkte bei Level-Up in passive Boni investieren:

- **Feuerkraft** — +ATK permanent
- **Zähigkeit** — +max. HP permanent
- **Regeneration** — mehr Energie-Regen pro Runde
- **Schnelligkeit** — höhere Fluchtchance
- Klassenspezifische Skills (Schildmeister, Schattenläufer, Arkane Kontrolle…)

---

### Klassen-Waffen
Waffen droppen als **klassenspezifische Variante** — gleiche Stats, passender Name:

| Generisch | Krieger ⚔️ | Schurke 🗡️ | Magier 🪄 |
|-----------|-----------|-----------|----------|
| Kurzschwert | Kampfschwert | Spitzdolch | Novizenstab |
| Langschwert | Bastardschwert | Klingenschatten | Magierstab |
| Kriegshammer | Streitaxt | Schattenbeil | Arkane Keule |
| Sturmklinge | Gewitterschwert | Blitzdolch | Sturmstab |
| Runenschwert | Runenklinge | Runendolch | Runenstab |
| Knochensense | Kriegssense | Seelenstehler | Totenstab |
| Drachenzahn | Drachenklaue | Drachenstich | Drachenstab |
| Göttliche Klinge | Heilige Klinge | Klingengeist | Götterstab |

Generische Waffennamen bleiben im **Shop** erhalten.

---

### Equipment & Sets
Vier Ausrüstungsslots: **Waffe, Rüstung, Helm, Schuhe**.  
Equipment kann mit Gold **aufgewertet** werden (+1 ATK bzw. DEF pro Upgrade).

**Neutrale Sets** (für alle Klassen):

| Set | 4-teiliger Bonus |
|-----|-----------------|
| Leder-Set | +4 DEF, +3 ATK |
| Eisen-Set | +6 DEF, +4 ATK |
| Stahl-Set | +8 DEF, +6 ATK |
| Schatten-Set | +8 DEF, +8 ATK |
| Runen-Set | +12 DEF, +8 ATK |
| Drachen-Set | +15 DEF, +12 ATK |
| Licht-Set *(nur Loot)* | +20 DEF, +18 ATK |

**Klassen-Sets** (nur für die jeweilige Klasse):

| Set | Klasse | 4-teiliger Bonus |
|-----|--------|-----------------|
| Eisenfestung | Krieger | +10 DEF, Schildwall blockt 2 Angriffe |
| Schattenhülle | Schurke | +15% Krit, Aus-dem-Schatten lädt alle 3 Runden auf |
| Arkane Roben | Magier | +20 max. Energie, Arkane Entladung hat 2 Ladungen |

---

### Gegner & Ränge
Gegner werden mit einem zufälligen **Rang** gespawnt — höhere Zonen bevorzugen höhere Ränge.

| Rang | Titel | HP-Mult | ATK-Mult | Loot-Rolls |
|:----:|-------|:-------:|:--------:|:----------:|
| 1 | *(normal)* | ×1,0 | ×1,0 | 1 |
| 2 | ⚔️ Stark | ×1,4 | ×1,3 | 2 |
| 3 | 💀 Elite | ×2,0 | ×1,6 | 3 |
| 4 | 👑 Champion | ×3,0 | ×2,0 | 4 |
| 5 | 🔥 Boss | ×5,0 | ×2,8 | 6 |

**Aktuell im Spiel:** Schleim, Schattenwolf, Goblin, Zombie, Bandit, Waldtroll, Skelett, Drache, Assassin, Dunkelritter, Eismagierin, Steingolem, Giftige Spinne, Flammendämon

---

### Schwierigkeitsgrade

| Modus | Gegner-HP | Gegner-ATK | Start-HP |
|-------|:---------:|:----------:|:--------:|
| Einfach | ×0,8 | ×0,8 | +5 |
| Normal | ×1,0 | ×1,0 | — |
| Schwer | ×1,3 | ×1,2 | −5 |

---

### New Game+
Nach dem Besiegen **aller 5 Zonen-Bosse** erscheint der Endscreen mit NG+-Angebot:
- Gegner skalieren mit **×1,3 HP und ATK** pro NG+-Runde (kumulativ)
- Du behältst **Gold** und alle **legendären Items**
- Level, Skills und normale Ausrüstung werden zurückgesetzt
- Alle Zonen starten wieder gesperrt

---

### Achievements
**20 freischaltbare Errungenschaften** in 5 Sektionen:
Kampf · Aufstieg · Dungeons & Zonen · Wirtschaft · Meta

---

### Crafting & Schwarzmarkt
Am Lagerfeuer über **[C] Handwerk** erreichbar:
- Junk-Items zu Consumables verarbeiten (4 Rezepte)
- **Schwarzmarkt:** Wandernder Händler mit seltenen epischen Items — einmal pro Zone verfügbar

---

## 💾 Speichern & Laden

Bis zu **3 Spielstände** in `saves/savegame_1.json` bis `_3.json`.  
Beim Start: Auswahl mit Klasse, Level, Schwierigkeit und NG+-Runde pro Slot.

---

## 📋 Roadmap

Siehe [ROADMAP.md](ROADMAP.md) für die Planung bis v2.1.
