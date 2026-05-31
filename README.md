# 🗡️ Print-Hero

> Ein rundenbasiertes Terminal-Dungeon-Crawler RPG in Python.  
> Wähle deine Klasse, kämpfe dich durch 5 Zonen, besiege Zonen-Bosse und rette das Reich.

**Aktuelle Version: v2.2** | Python 3.10+ | Dependency: `rich`

---

## 🚀 Starten

```bash
pip install rich
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
Beim Start wählst du eine von drei Klassen — jede hat unterschiedliche Startwerte und vier einzigartige Kampffähigkeiten auf den Tasten `[S]`, `[R]`, `[C]`, `[X]`:

| Klasse | Start-HP | Start-ATK | [S] | [R] | [C] | [X] |
|--------|:--------:|:---------:|-----|-----|-----|-----|
| ⚔️ Krieger | 40 | 12 | Brutaler Hieb (18E) | Schildwall (10E) | Schildstoß (20E, 3R CD) | Kriegsschrei (25E, 1×) |
| 🗡️ Schurke | 30 | 15 | Aus dem Schatten (15E) | Giftklinge (12E) | Blendpulver (20E, 4R CD) | Rauchbombe (10E, 1×) |
| 🔮 Magier | 25 | 8 | Arkane Entladung (15E) | Froststrahl (18E) | Feuerball (22E, 3R CD) | Mana-Schild (0E, 4R CD) |

> Im Kampf zeigt `[?]` eine ausführliche Beschreibung aller Fähigkeiten mit Energiekosten und Cooldown.

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
| S | Klassen-Fähigkeit 1 | variabel | Hauptfähigkeit der Klasse |
| R | Klassen-Fähigkeit 2 | variabel | Zweite Fähigkeit der Klasse |
| C | Klassen-Fähigkeit 3 | variabel | Dritte Fähigkeit (Cooldown) |
| X | Klassen-Fähigkeit 4 | variabel | Ultimative Fähigkeit (1× pro Kampf) |
| ? | Fähigkeiten-Übersicht | — | Zeigt alle 4 Fähigkeiten mit Details |
| U | Verbrauchsgegenstände | — | Tränke & Items im Kampf |
| F | Fliehen | — | Verlässt den Kampf |

**Statuseffekte:**
- **Blutung ⚠️:** 3 Schaden/Runde pro Stack, Stack −1 pro Runde
- **Gift ☠️:** 5 Schaden/Runde pro Stack, Stack −1 pro Runde
- **Verbrennung 🔥:** 4 Schaden/Runde pro Stack, Stack −1 pro Runde
- **Betäubung:** Betroffene überspringen die nächste Runde
- **DEF-Debuff:** Temporäre Rüstungsreduktion für den laufenden Kampf
- **Energie-Regeneration:** +3 Energie automatisch am Ende jeder Runde

Bei **Einzelgegner** entfällt die Zielauswahl — automatisches Auto-Targeting.

---

### Passive Waffen
Bestimmte Waffen lösen bei jedem Angriff einen Zusatzeffekt aus:

| Waffe | Rarity | ATK | Passiv-Effekt | Chance |
|-------|--------|:---:|---------------|:------:|
| Giftklaue | Ungewöhnlich | +5 | +1 Giftstack auf Ziel | 100 % |
| Flammenklinge | Selten | +8 | +2 Verbrennungsstacks | 25 % |
| Eisaxt | Selten | +10 | Ziel eingefroren (1 Runde betäubt) | 20 % |
| Runen-Kriegshammer | Selten | +12 | −3 DEF-Debuff auf Ziel | 30 % |

---

### Charakter-Progression

| Level | max. HP (je Klasse) | Basis-ATK |
|------:|:-------------------:|----------:|
| 1 | 25 – 40 | 8 – 15 |
| 5 | 41 – 56 | 12 – 19 |
| 10 | 61 – 76 | 17 – 24 |

Pro Level-Up: **+4 max. HP**, **+1 ATK**, HP wird aufgefüllt, **+1 Skillpunkt**.

---

### Skill-Tree
9 passive Skills in 3 Bäumen — Skillpunkte bei Level-Up investieren:

- **Kampf:** Scharfe Klingen (+2 ATK), Kritischer Treffer (+15% Krit), Blutgier (20% Lifesteal)
- **Überleben:** Eisenhaut (+3 DEF), Zähigkeit (+10 HP), Regeneration (+1 HP/Runde)
- **Energie:** Energiefluss (+2 Regen/Runde), Fokus (−5 Energiekosten), Magieschild (1× Blockieren)

---

### Klassen-Waffen
Waffen droppen, werden im **Shop angezeigt** und am **Schwarzmarkt verkauft** als klassenspezifische Variante — gleiche Stats, passender Name:

| Generisch | Krieger ⚔️ | Schurke 🗡️ | Magier 🔮 |
|-----------|-----------|-----------|----------|
| Kurzschwert | Kampfschwert | Spitzdolch | Novizenstab |
| Langschwert | Bastardschwert | Klingenschatten | Magierstab |
| Kriegshammer | Streitaxt | Schattenbeil | Arkane Keule |
| Sturmklinge | Gewitterschwert | Blitzdolch | Sturmstab |
| Runenschwert | Runenklinge | Runendolch | Runenstab |
| Knochensense | Kriegssense | Seelenstehler | Totenstab |
| Drachenzahn | Drachenklaue | Drachenstich | Drachenstab |
| Göttliche Klinge | Heilige Klinge | Klingengeist | Götterstab |

---

### Equipment & Sets
Vier Ausrüstungsslots: **Waffe, Rüstung, Helm, Schuhe**.  
Equipment kann mit Gold **aufgewertet** werden (+1 ATK bzw. DEF pro Upgrade).

**Neutrale Sets** (für alle Klassen, zonengebunden):

| Set | Zone | 4-teiliger Bonus | Spezial |
|-----|------|-----------------|---------|
| Leder-Set | Wald | +4 DEF, +3 ATK | 10 % Ausweichen |
| Eisen-Set | Wald | +6 DEF, +4 ATK | +3 Energie/Runde |
| Stahl-Set | Ruinen | +8 DEF, +6 ATK | Blutungsimmunität |
| Runen-Panzer | Ruinen | +8 DEF, +5 ATK | Blutungsschaden −1/Stack |
| Schatten-Set | Ruinen/Wüste | +8 DEF, +8 ATK | +15 % Krit-Chance |
| Runen-Set | Ruinen/Wüste | +12 DEF, +8 ATK | +20 % XP |
| Schattentuch | Wüste | −3 DEF, +2 ATK | 15 % Ausweichen |
| Drachen-Set | Vulkan | +15 DEF, +12 ATK | 15 % Angriff vollst. blocken |
| Drachenschuppen | Vulkan | +12 DEF, +8 ATK | 20 % Angriff vollst. blocken |
| Verdammten-Stahl | Dunkel-Reich | +6 ATK, −4 DEF | — |
| Licht-Set | Dunkel-Reich | +20 DEF, +18 ATK | +3 HP/Runde |

**Klassen-Sets** (nur für die jeweilige Klasse):

| Set | Klasse | 4-teiliger Bonus | Spezial |
|-----|--------|-----------------|---------|
| Eisenfestung | ⚔️ Krieger | +10 DEF, +5 ATK | Schildwall blockt 2 Angriffe |
| Schattenhülle | 🗡️ Schurke | +8 DEF, +5 ATK, +15 % Krit | +15 % Krit-Chance bei "Aus dem Schatten" |
| Arkane Roben | 🔮 Magier | +8 DEF, +4 ATK, +20 Energie | Arkane Entladung trifft 2× (doppelter Schaden) |

---

### Gegner & Ränge
**17 Gegnertypen** — Gegner werden mit einem zufälligen **Rang** gespawnt, höhere Zonen bevorzugen höhere Ränge.

| Rang | Titel | HP-Mult | ATK-Mult | Loot-Rolls |
|:----:|-------|:-------:|:--------:|:----------:|
| 1 | *(normal)* | ×1,0 | ×1,0 | 1 |
| 2 | ⚔️ Stark | ×1,4 | ×1,3 | 2 |
| 3 | 💀 Elite | ×2,0 | ×1,6 | 3 |
| 4 | 👑 Champion | ×3,0 | ×2,0 | 4 |
| 5 | 🔥 Boss | ×5,0 | ×2,8 | 6 |

**Gegner im Spiel:** Schleim, Schattenwolf, Goblin, Zombie, Bandit, Waldtroll, Skelett, Waldgeist, Lich, Sandwurm, Assassin, Dunkelritter, Eismagierin, Steingolem, Giftige Spinne, Flammendämon, Drache

---

### Schwierigkeitsgrade

| Modus | Gegner-HP | Gegner-ATK | Start-HP |
|-------|:---------:|:----------:|:--------:|
| Einfach 🟢 | ×0,80 | ×0,85 | +5 |
| Normal 🟡 | ×1,00 | ×1,00 | — |
| Schwer 🔴 | ×1,25 | ×1,20 | −5 |

---

### New Game+
Nach dem Besiegen **aller 5 Zonen-Bosse** erscheint der Endscreen mit NG+-Angebot:
- Gegner skalieren mit **×1,3 HP und ATK** pro NG+-Runde (kumulativ, max. ×3,0)
- Du behältst **Gold** und alle **legendären Items**
- Level, Skills und normale Ausrüstung werden zurückgesetzt
- Alle Zonen starten wieder gesperrt
- Dungeon- und Zonen-Statistiken werden für den neuen Durchlauf zurückgesetzt

---

### Achievements
**20 freischaltbare Errungenschaften** in 5 Sektionen:  
Kampf · Aufstieg · Dungeons & Zonen · Wirtschaft · Meta

---

### Crafting & Schwarzmarkt
Am Lagerfeuer über **[C] Handwerk** erreichbar:
- Junk-Items zu Consumables verarbeiten (4 Rezepte)
- **Wandernder Händler:** Zufalls-Event im Dungeon — bis zu 3 Consumables mit 20 % Rabatt, mehrere Käufe möglich
- **Schwarzmarkt:** Selteneres Event beim Wandernden Händler — epische/legendäre Items zu Festpreisen, einmalig pro Run verfügbar

---

## 💾 Speichern & Laden

Bis zu **3 Spielstände** in `saves/savegame_1.json` bis `_3.json`.  
Beim Start: Auswahl mit Klasse, Level, Schwierigkeit und NG+-Runde pro Slot.

---

## 📋 Changelog

### v2.2
- Bugfix: Gegner nahmen keinen Giftschaden (check_poison fehlte im Status-Tick)
- Bugfix: KeyError bei vollem Inventar während Equipment-Drop behoben
- Bugfix: Schurke passive_crit_bonus wird bei NG+ korrekt zurückgesetzt
- Bugfix: Level-Up-Meldung zeigte falsche Krit-Basis (15% statt 10%) für Schurken
- Bugfix: Energie-Tränke respektieren jetzt den Set-Bonus-Cap (Arkane Roben)
- Bugfix: Dungeon-Händler zeigt jetzt klassenspezifische Waffennamen
- Bugfix: Verlassener Schrein überschreibt keinen höheren XP-Buff mehr
- Feature: Arkane Roben 4-Set-Effekt (mage_double_arcane) implementiert — Arkane Entladung trifft 2× 
- Fix: Schattenhülle Set-Beschreibung korrigiert (tatsächlicher Effekt: +15% Krit)

### v2.1
- Shop und Schwarzmarkt zeigen klassenspezifische Waffennamen (Rogue sieht Spitzdolch, Magier sieht Novizenstab)
- Shop zeigt Set-Zugehörigkeit pro Item
- Wandernder Händler: mehrere Käufe möglich, Stack-Stand sichtbar
- Lagerfeuer- & Inventar-Menü: Ausrüstungsanzeige mit Rarity, Set und Upgrade-Level pro Zeile
- NG+: Stats werden beim Reset korrekt zurückgesetzt
- NG+: Skalierung auf max. ×3,0 begrenzt