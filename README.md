# 🗡️ Print-Hero

> Ein rundenbasiertes Terminal-Dungeon-Crawler RPG in Python.  
> Wähle deine Klasse, kämpfe dich durch Dungeons, sammle Beute und steige bis Level 10 auf.

**Aktuelle Version: v1.9.8** | Python 3.10+ | Keine externen Pakete

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
  combat.py              — Kampflogik, Spezialattacken, Loot-Vergabe
  save.py                — Speichern & Laden (JSON)
content/
  monsters.py            — Alle Gegner-Klassen, Rang-System, Boss-Fähigkeiten
  loot_tables.py         — Loot-Pools, Item-Definitionen, Set-Definitionen
  shop.py                — Händler-Sortiment
  classes.py             — Klassen-Definitionen & Startboni
systems/
  dungeon.py             — Dungeon-Schleife, Raumgenerierung, Raumtypen
  zones.py               — Zonen-Definitionen, Monster-Pools, Rang-Gewichtung
  events.py              — Zufalls-Events zwischen Räumen
  skilltree.py           — Skill-Auswahl & Skill-Effekte
  achievements.py        — Achievement-System
saves/
  savegame.json          — Gespeicherter Spielstand (automatisch erstellt)
ui/
  pause.py               — Lagerfeuer-Menü, Inventar, Verkauf, Skills
  utils.py               — clear_screen, print_header
```

---

## 🎮 Spielsysteme

### Klassen
Beim Start wählst du eine von drei Klassen — jede hat unterschiedliche Startwerte und eine einzigartige Kampffähigkeit:

| Klasse  | Start-HP | Start-ATK | Klassen-Fähigkeit |
|---------|:--------:|:---------:|-------------------|
| Krieger | 40       | 8         | Schildwall — blockiert einen Angriff |
| Schurke | 28       | 12        | Aus dem Schatten — garantierter Kritischer Treffer |
| Magier  | 22       | 10        | Arkane Entladung — Magie-Angriff + DEF-Debuff |

---

### Zonen
Das Spiel ist in **5 Zonen** unterteilt, die mit dem Level freigeschaltet werden. Jede Zone hat ihren eigenen Gegner-Pool und eine andere Schwierigkeitsverteilung.

| Zone | Emoji | Freischaltung | Gegner |
|------|-------|:-------------:|--------|
| Wald | 🌲 | Lv. 1 | Schleim, Schattenwolf, Goblin, Waldtroll |
| Ruinen | 🏚️ | Lv. 2 | Zombie, Skelett, Bandit, Waldtroll |
| Wüste | 🏜️ | Lv. 4 | Bandit, Meuchler, Giftige Spinne, Goblin |
| Vulkan | 🌋 | Lv. 6 | Flammendämon, Steingolem, Drache, Dunkelritter |
| Dunkel-Reich | 💀 | Lv. 8 | Dunkelritter, Eismagierin, Drache, Flammendämon |

Die Zone wird im Lagerfeuer-Menü unter **[Z] Zone wählen** gewechselt und im Spielstand gespeichert.

---

### Dungeon-System
Das Herzstück des Spiels. Jeder Dungeon besteht aus **3–5 Räumen**, der letzte Raum ist immer der Boss.

**Raumtypen:**

| Symbol | Typ | Beschreibung |
|--------|-----|-------------|
| ⚔️ | Kampf | 1–3 Gegner gleichzeitig |
| 💪 | Elite-Gegner | Stärkerer Einzelkämpfer, bessere Beute |
| 💀 | Mini-Boss | Rang-3-Gegner, gute Drops |
| 🎲 | Ereignis | Zufälliger Event (Händler, Schrein, Falle…) |
| 🕯️ | Schrein | Garantierte Segnung: HP, Energie, XP-Buff oder Fluch wagen |
| ⚠️ | Falle | Ausweichen (kostet Energie) oder Schaden nehmen |
| 🌫️ | Leerer Raum | Flavor + Chance auf versteckten Loot |
| 🔥 | Boss | Rang-4/5-Gegner mit Bonus-Loot nach dem Kill |

**Zwischen den Räumen** kannst du Ausrüstung anlegen, Tränke benutzen und den nächsten Raum einsehen.  
Du kannst den Dungeon jederzeit verlassen — ohne Abschluss gibt es kein Loot und keine HP-Heilung.  
Nach einem **vollständig abgeschlossenen Dungeon** werden HP und Energie vollständig wiederhergestellt.

---

### Kampf
Rundenbasiert. Du und deine Gegner handeln abwechselnd.

| Taste | Aktion | Energie | Beschreibung |
|-------|--------|:-------:|-------------|
| A | Angreifen | — | Normaler Angriff |
| S | Himmelsschlag | 20 | Starker Einzelangriff |
| R | Rundumschlag | 15 | Trifft alle Gegner (−2 Schaden) |
| C | Cleave | 10 | Angriff + 3 Blutungsstacks |
| K | Klassen-Fähigkeit | — | Einmal pro Kampf nutzbar |
| U | Verbrauchsgegenstände | — | Tränke & Items im Kampf |
| F | Fliehen | — | Verlässt den Kampf |

**Statuseffekte:**
- **Blutung:** Jeder Stack → 3 Schaden/Runde, reduziert sich um 1
- **Gift:** Steigender Schaden pro Runde (+1 pro Stack)
- **Energie-Regeneration:** +3 Energie automatisch pro Runde

---

### Charakter-Progression

| Level | max. HP (je nach Klasse) | Basis-ATK |
|------:|:------------------------:|----------:|
|     1 | 22 – 40                  |      8–12 |
|     5 | 38 – 56                  |     12–16 |
|    10 | 58 – 76                  |     17–21 |

Pro Level-Up: **+4 max. HP**, **+1 ATK**, HP wird aufgefüllt.  
Ab Level 2: Du erhältst **Skillpunkte** für den Skill-Tree.

---

### Skill-Tree
Skillpunkte bei Level-Up investieren in passive Boni:

- Feuerkraft — +ATK permanent
- Zähigkeit — +max. HP permanent
- Regeneration — mehr Energie-Regen pro Runde
- Schnelligkeit — höhere Fluchtchance
- Schildmeister — verbesserter Schildwall (Krieger)
- … und weitere klassenspezifische Skills

---

### Klassen-Waffen
Jede Waffe droppt als **klassenspezifische Variante** — gleiche Stats, aber passender Name und Emoji:

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

**Set-Boni** bei 2/3/4 angelegten Teilen eines Sets:

| Set | 4-teiliger Bonus |
|-----|-----------------|
| Leder-Set | +4 DEF, +3 ATK |
| Eisen-Set | +6 DEF, +4 ATK |
| Stahl-Set | +8 DEF, +6 ATK |
| Schatten-Set | +8 DEF, +8 ATK |
| Runen-Set | +12 DEF, +8 ATK |
| Drachen-Set | +15 DEF, +12 ATK |
| Licht-Set *(nur Loot)* | +20 DEF, +18 ATK |

---

### Gegner & Ränge
Gegner werden mit einem zufälligen **Rang** gespawnt:

| Rang | Titel | HP-Mult | ATK-Mult | Loot-Rolls |
|:----:|-------|:-------:|:--------:|:----------:|
| 1 | *(normal)* | ×1,0 | ×1,0 | 1 |
| 2 | ⚔️ Stark | ×1,4 | ×1,3 | 2 |
| 3 | 💀 Elite | ×2,0 | ×1,6 | 3 |
| 4 | 👑 Champion | ×3,0 | ×2,0 | 4 |
| 5 | 🔥 Boss | ×5,0 | ×2,8 | 6 |

Aktuell im Spiel: Schleim, Schattenwolf, Goblin, Zombie, Bandit, Waldtroll, Skelett, Drache, Assassine, Dunkelritter, Eismagierin, Golem, Werwolf.

---

### Schwierigkeitsgrade

| Modus | Gegner-HP | Gegner-ATK | Start-HP |
|-------|:---------:|:----------:|:--------:|
| Einfach | ×0,8 | ×0,8 | +5 |
| Normal | ×1,0 | ×1,0 | — |
| Schwer | ×1,3 | ×1,2 | −5 |

---

### New Game+
Nach Erreichen von **Level 10** kannst du New Game+ starten:
- Gegner skalieren mit **×1.3 HP und ATK** pro NG+-Runde
- Du behältst dein **Gold** und alle **legendären Items**
- Level, Skills und normale Ausrüstung werden zurückgesetzt

---

### Achievements
10 freischaltbare Errungenschaften — z.B. für erste Kills, Gold-Meilensteine, Dungeons ohne Tode und mehr.

---

### Inventar
- **30 Slots** insgesamt
- Consumables stapeln bis zu einem festgelegten Limit
- Equipment belegt je 1 Slot (nicht stapelbar)

---

## 💾 Speichern & Laden

Spielstand wird in `savegame.json` gespeichert.  
Beim nächsten Start: vorhandenen Spielstand laden oder neu beginnen.

---

## 📋 Roadmap

Siehe [ROADMAP.md](ROADMAP.md) für die vollständige Planung bis v2.0.
