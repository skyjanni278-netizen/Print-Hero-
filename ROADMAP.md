# 🗺️ Print-Hero — Entwicklungs-Roadmap

---

## 📍 Aktueller Stand *(wird nach jedem Schritt aktualisiert)*

**Letzte abgeschlossene Version:** v2.3 — QoL  
**In Arbeit:** v3.0 — Roguelite (Phase 1 von 4 fertig)  
**Danach:** v3.1 — Equipment-Rebalancing

### ✅ Was ist fertig
- v2.2: 8 Bugs gefixt, mage_double_arcane implementiert, Set-Beschreibung korrigiert
- Refactoring: core/abilities.py (God Class aufgebrochen), loot_tables.py aufgeteilt
- v2.3: Autosave, Upgrade-per-Item, kompakterer Kampf-Log, erweiterter Death-Screen
- ROADMAP.md angelegt mit vollständigem Plan v2.3 → v3.3
- Designentscheidungen für v3.0 geklärt (nur Roguelite, fester Segnung-Pool, kein Mythic-Limit)
- ITEMS.md (Item-/Set-Referenz) neu erstellt, README + ROADMAP auf v2.3-Stand gebracht
- **v3.0 Phase 1 (Roguelite Foundation) komplett:**
  - `core/save.py` neu: `meta_save.json` + `run_save.json`, 3-Slot-System entfernt
  - `systems/hub.py`: Zuflucht-Menü (Run starten/fortsetzen, Errungenschaften, Lifetime-Stats)
  - `main.py`: Run-Loop (Hub → Run → Tod/Sieg → Hub), Quit im Camp kehrt zur Zuflucht zurück
  - Runenessenz: 15–25/Dungeon, 50–80/Zonen-Boss, +200 Sieg-Bonus — direkt ins Meta-Save
  - NG+ komplett entfernt (Achievement „Zweite Runde" → „Bezwinger": einen Run gewinnen)
  - Achievements sind meta-persistent (überleben den Tod)
  - Basis-Balancing: Gegner +20 % HP / +15 % ATK, zentrale `scale_enemy()` in zones.py
  - Schwierigkeitsgrade bleiben, Wahl pro Run; Start-HP-Bonus/-Malus wird jetzt wirklich angewendet

### 🔧 Nächster Schritt: v3.0 — Entwicklungsphase 2 (Segnungen)
1. `systems/segnungen.py` — SEGNUNGEN_POOL (~30 Segnungen), Synergien
2. `ui/segnungen_ui.py` — Auswahlmenü (1 aus 3) nach jedem Dungeon
3. `core/player.py` — `active_segnungen`-Liste (+ to_dict/from_dict!)
4. `core/combat.py` + `core/abilities.py` — Segnung-Hooks in den Kampfphasen
5. `systems/dungeon.py` — Segnungswahl nach Dungeon-Abschluss aufrufen

Details siehe v3.0-Abschnitt unten.

### 📋 Offene Entscheidungen
*Keine — alle Designfragen für v3.0 sind geklärt.*

---

## Refactoring *(vor v2.3 — kein eigenes Release)*

Zwei Refactors die vor dem ersten Update sinnvoll sind.
Kein Release, nur Commits. Ändern keine Spiellogik.

### Refactor 1 — `core/abilities.py` (God Class aufbrechen)

**Problem:** `Character` in `core/player.py` ist eine God Class mit 700 Zeilen.
Die 12 Klassen-Fähigkeiten (Zeilen 410–530) sind Kampflogik, kein Charakterzustand.
In v3.0 müssen Segnungen in diese Abilities einhaken — das ist sauberer in einer eigenen Datei.

**Lösung:** Abilities als Standalone-Funktionen nach `core/abilities.py` auslagern.

```
core/player.py      700 → ~530 Zeilen  (Abilities entfernt)
core/abilities.py   NEU ~180 Zeilen   (alle 12 Ability-Funktionen)
```

Aufruf ändert sich von `player.brutaler_hieb(target)` zu `brutaler_hieb(player, target)`.
Einzige betroffene Aufrufstelle: `core/combat.py` (Ability-Dispatcher, ~15 Zeilen).

**Geänderte Dateien:** `core/player.py`, `core/combat.py`, `core/abilities.py` (neu)

---

### Refactor 2 — `content/loot_tables.py` splitten (Fat Module)

**Problem:** 668 Zeilen, drei logisch getrennte Datengruppen in einer Datei.
Wächst mit v3.1 (Mythic-Tier, neue Sets) auf ~900+ Zeilen.

**Lösung:** Aufteilen in drei fokussierte Module:

```
content/items.py   EQUIPMENT_DEFS, CONSUMABLE_DEFS, JUNK_DEFS,
                   CLASS_WEAPON_MAP, WEAPON_VARIANT_TO_BASE,
                   RARITY_LABEL, CRAFT_RECIPES

content/sets.py    SET_DEFS, get_active_sets(), get_set_specials()

content/loot.py    LOOT_POOL, ZONE_LOOT_POOL, BOSS_LOOT_POOL,
                   RANK_LOOT_WEIGHTS, roll_*(), apply_loot()
```

Imports in allen anderen Dateien werden angepasst (ca. 8 Dateien betroffen).
`from content.loot_tables import X` → `from content.items import X` etc.

**Geänderte Dateien:** alle Dateien die `loot_tables` importieren

---

## Versionierungs-Prinzip

```
MAJOR.MINOR.PATCH
  │      │     └─ Bugfix (v2.2.1)
  │      └─────── Neues Feature / Erweiterung (v2.3, v3.1)
  └────────────── Kompletter Umbau / Breaking Change (v3.0)
```

**Eine Versionsnummer = ein spielbares, stabiles Release.**
Die Entwicklungsschritte innerhalb einer Version sind gewöhnliche Commits,
bekommen aber keine eigene Versionsnummer. Erst wenn das Gesamtfeature
vollständig und spielbar ist, wird die Version getaggt und gepusht.

---

## Aktuelle Version: v2.2 ✅

---

## v2.3 — QoL (Quality of Life)

> Kleine Verbesserungen die sofort die Spielbarkeit erhöhen.
> Kann unabhängig vom Roguelite-Umbau umgesetzt werden.

**Autosave nach jedem Dungeon**
- Nach Dungeon-Abschluss automatisch in den aktiven Slot speichern
- Kein Fortschrittsverlust bei unerwartetem Programmabbruch
- Datei: `systems/dungeon.py`

**Upgrade per Item statt per Slot**
- Item-Dict bekommt optionales `"upgrade": N`-Feld
- Beim Ablegen bleibt der Upgrade-Stand am Item erhalten
- Beim Anlegen eines Items wird dessen eigenes Upgrade-Level verwendet
- Dateien: `core/player.py`, `ui/pause.py`

**Kompakterer Kampf-Log**
- Status-Ticks in einer Zeile zusammenfassen:
  `⚠ Blutung −3 HP  |  ☠ Gift −5 HP` statt zwei getrennte Zeilen
- ENTER-Prompts reduzieren: nur noch am Rundenende, nicht nach jeder Meldung
- Datei: `core/combat.py`

**Run-Zusammenfassung beim Tod**
- Dedizierter Death-Screen: Erreichte Zone, Gegner getötet, bestes Item, XP, Schaden
- Ersetzt den aktuellen minimalen Game-Over-Screen
- Datei: `main.py`

---

## v3.0 — Das Roguelite *(größtes Update)*

> Kompletter Umbau des Spielprinzips.
> Inspiriert von Hades (Boons, Mirror) und Dead Cells (Blueprints, Startkits).
>
> **Ziel:** Erster Run ist nicht schaffbar. Nach 8–12 Runs hat man genug
> Metaprogression um Zone 5 und den Endboss zu bezwingen.

> **🐛 Bug-Pass:** Dieser Schritt umfasst auch eine gezielte Suche nach Bugs
> und deren Behebung. Vor dem Tagging wird der neue Code auf Fehler geprüft
> und bestehende Bugs werden mitbehoben.

---

### Entwicklungsphase 1 — Roguelite Foundation

**Neues Speichersystem:**
```
meta_save.json   — permanent: Runenessenz, Spiegel-Stand, freigeschaltete Runen
run_save.json    — aktueller Run (wird bei Tod gelöscht, bei Quit behalten)
```
Die 3 alten Speicher-Slots entfallen komplett. `core/save.py` wird neu geschrieben.

**Run-Ablauf:**
```
Hub → Klasse + Startkit wählen → Run → Dungeons → Tod oder Sieg → Hub
```
- Bei Tod: `run_save.json` löschen, Runenessenz gutschreiben, Hub zeigen
- Bei Quit: `run_save.json` bleibt, beim nächsten Start wird der Run fortgesetzt
- Bei Sieg: Bonus-Runenessenz, `run_save.json` löschen, Hub zeigen

**Runenessenz — Metawährung:**
- Pro abgeschlossenem Dungeon: 15–25 Runenessenz
- Pro besiegtem Zonen-Boss: 50–80 Runenessenz
- Wird auch bei Tod ausbezahlt (kein Verlust motiviert zum Pushen)

**Basis-Balancing (erste Runs sollen scheitern):**
- Gegner-HP Basis: +20% gegenüber v2.2
- Gegner-ATK Basis: +15% gegenüber v2.2
- Zone 3+ ohne Metaupgrades kaum schaffbar
- Zone 5 setzt 8–12 Runs voraus

**Neue/geänderte Dateien:**
```
core/save.py              komplett neu: meta_save + run_save Logik
systems/hub.py            NEU: Hub-Menü zwischen Runs
systems/meta_save.py      NEU: Metadaten laden/speichern/initialisieren
main.py                   Run-Loop statt Slot-Menü
config.py                 RUNENESSENZ_*, BASE_DIFFICULTY_MULT
```

---

### Entwicklungsphase 2 — Segnungen (Hades Boon-System)

Nach jedem abgeschlossenen Dungeon wählt man **eine von drei zufälligen Segnungen**.
Sie gelten nur für den laufenden Run, können aber zu starken Builds kombiniert werden.

```
✨ Wähle eine Segnung — Zone 1, Dungeon 1 abgeschlossen:

[1] 🩸 Blutdurst         — Kills heilen 3 HP
[2] ⚡ Seelenernte        — Kritische Treffer geben sofort 8 Energie zurück
[3] 💀 Lebensraub         — Gegner unter 20% HP nehmen 2× Schaden
```

**Segnung-Pool (~30 Segnungen):**

| Segnung | Effekt |
|---------|--------|
| Blutdurst | Kills heilen 3 HP |
| Finstere Klinge | 10% Chance: Angriff wiederholt sich kostenlos |
| Lebensraub | Gegner unter 20% HP nehmen 2× Schaden |
| Raserei | Nach 3 Kills in Folge: nächster Angriff trifft alle |
| Eisige Präsenz | Raumbetreten: alle Gegner 1 Runde betäubt |
| Seelenernte | Kritischer Treffer: sofort +8 Energie |
| Giftmeister | Giftstacks lösen sich nicht auf bis Kampfende |
| Glut-Entfesselung | Verbrennung-Ablauf: einmaliger 3×-Burst |
| Schattenform | Erste Runde jedes Kampfes: 100% Ausweichen |
| Vergeltung | Erlittener Statuseffekt: Angreifer bekommt ihn auch (50%) |
| Letzter Wille | Bei ≤10% HP: +30% ATK |
| Eisenhaut+ | +5 DEF für diesen Run |
| Zähigkeit+ | +15 max HP für diesen Run |

**Klassen-spezifische Segnungen:**

| Segnung | Klasse | Effekt |
|---------|--------|--------|
| Schatten-Reflex | Schurke | Aus dem Schatten lädt bei Kill sofort neu |
| Arkane Überladung | Magier | Arkane Entladung trifft 3 Gegner extra |
| Unerschütterlich | Krieger | Schildwall blockt automatisch ersten Angriff |

**Synergien (2 passende Segnungen = Bonus-Effekt):**
```
Giftmeister + Lebensraub       → vergiftete Gegner <20% HP nehmen 3× Schaden
Blutdurst + Raserei            → Kill-Kette heilt 6 HP statt 3
Eisige Präsenz + Seelenernte   → Betäubungs-Kill: +15 Energie
```

**Neue/geänderte Dateien:**
```
systems/segnungen.py      NEU: SEGNUNGEN_POOL, choose_segnung(), synergy-Check
ui/segnungen_ui.py        NEU: Auswahlmenü (3 Optionen)
core/player.py            active_segnungen: list
systems/dungeon.py        nach Dungeon-Abschluss: segnung_choice() aufrufen
core/combat.py            Segnung-Hooks in Kampfphasen
```

---

### Entwicklungsphase 3 — Der Spiegel (Hades Mirror of Night)

Permanente Metaupgrades mit Runenessenz kaufen.
**Jedes Upgrade hat zwei Versionen (A oder B)** — man entscheidet sich für einen Spielstil.

```
╔══════════════ Der Spiegel ══════════════╗
║ Runenessenz: 240                        ║
╠═════════════════════════════════════════╣
║ Zähigkeit      [A] +15 max HP           ║
║                [B] Starte mit vollen HP ║
║                ── Kosten: 60  [0/1] ──  ║
║ Kriegserfahrung [A] +1 ATK permanent    ║
║                 [B] 1. Kampf/Dungeon +50%DMG ║
║                ── Kosten: 80  [0/1] ──  ║
║ ...                                     ║
╚═════════════════════════════════════════╝
```

**Spiegel-Upgrades (A / B):**

| Upgrade | A | B | Kosten |
|---------|---|---|--------|
| Zähigkeit | +15 max HP | Starte mit vollen HP | 60 |
| Kriegserfahrung | +1 ATK permanent | 1. Kampf/Dungeon: +50% Schaden | 80 |
| Glück | +15% Gold-Drop | 1× pro Run: Item-Qualität +1 Stufe | 70 |
| Zweites Leben | 1× pro Run nicht sterben | Bei Tod im Dungeon: Items behalten | 120 |
| Seelenbindung | +8% XP-Gain | Level-Ups: +1 Skillpunkt extra | 90 |
| Händlerglück | Wandernder Händler 1× öfter | Händler-Preise −15% | 75 |
| Dunkelresistenz | Statuseffekte −1 Runde | Immunität gg. 1 zufälligen Effekt/Run | 100 |

A↔B-Wechsel kostet 30% des Originalpreises.

**Neue/geänderte Dateien:**
```
ui/spiegel.py             NEU: Spiegel-Menü, A/B Auswahl, Fortschritt
systems/meta_save.py      spiegel_state: {slot_id: "A"/"B"/None}
core/player.py            apply_spiegel_effects(meta) beim Run-Start
systems/hub.py            [S] Spiegel-Option
```

---

### Entwicklungsphase 4 — Runen (Dead Cells Blueprint-System)

Seltene Drops aus Gegnern und Bossen schalten dauerhaft neue Dinge frei.
Jede Rune erscheint genau einmal — danach permanent freigeschaltet.

**Rune-Kategorien:**

*Startkits* — vor dem Run wählbar, sobald Rune freigeschaltet:
```
Kriegers Vermächtnis    Kettenhemd + Streitaxt + 60 Gold
Schurken-Einsteiger     Giftklaue + 2× Antidot + 30 Gold
Magier-Erbe             Novizenstab + volle Energie + 1 Stärketrank
Überlebender            3× Healing Potion + 1× Phönixfeder + 80 Gold
```

*Klassen-Varianten* — neue Startoptionen nach mehreren Runs:
```
Berserker-Erbe     Krieger-Variante: −10 HP, +6 ATK, kein Schildwall
Meuchler-Erbe      Schurken-Variante: 15 HP, 18 ATK, Flucht immer erfolgreich
```

*Hub-NPCs* — erscheinen dauerhaft im Hub nachdem die Rune gefunden wurde:
```
Schmiedegeheimnis       Schmied im Hub: 1 kostenloses Upgrade vor jedem Run
Händlernetzwerk         Händlerin: kaufe Verbrauchsgüter für Runenessenz
Orakelwissen            Orakel: zeigt Zone-Boss-Stats des nächsten Bosses vorab
```

**Drop-Chancen:**
- Zonen-Boss: 100% (pro Boss nur einmal in der gesamten Meta)
- Dungeon-Boss (Rang 5): 25%
- Elite-Gegner: 5%
- Truhen-Event: 15%

**Neue/geänderte Dateien:**
```
systems/runen.py          NEU: RUNE_DEFS, check_rune_drop(), apply_rune_unlock()
systems/meta_save.py      unlocked_runen: list
ui/hub.py                 [R] Runen-Übersicht + Startkit-Auswahl
systems/world_map.py      Boss-Rune-Drop nach Sieg
core/combat.py            Enemy-Rune-Drop-Check nach Kill
```

---

### v3.0 Release-Kriterien

Alle vier Entwicklungsphasen vollständig umgesetzt und stabil:
- [ ] Run-basiertes Speichersystem funktioniert
- [ ] Segnungen erscheinen nach jedem Dungeon, Synergien funktionieren
- [ ] Spiegel kaufbar, Effekte greifen im Run
- [ ] Runen droppen, Hub-NPCs erscheinen
- [ ] Basis-Balancing: erster Run erreicht nicht Zone 5
- [ ] Bug-Pass durchgeführt: neuer Code geprüft, gefundene Bugs behoben

---

## v3.1 — Equipment-Rebalancing

> Progression verlangsamen. Zone 5 soll noch echte Überraschungen bieten.

> **🐛 Bug-Pass:** Dieser Schritt umfasst auch eine gezielte Suche nach Bugs
> und deren Behebung. Vor dem Tagging wird der neue Code auf Fehler geprüft
> und bestehende Bugs werden mitbehoben.

**Problem:** Zu wenige Items pro Zone, Progression zu schnell.
Epic-Items erscheinen bereits ab Zone 3, Zone 5 bietet kaum Neues.

### Fünf-Zonen-Equipment-Kurve

| Zone | Rarity-Schwerpunkt | Max erlaubte Rarity |
|------|-------------------|---------------------|
| 1 Wald | Common | Uncommon (selten) |
| 2 Ruinen | Uncommon | Rare (sehr selten) |
| 3 Wüste | Rare | Epic (sehr selten, nur Einzelteile) |
| 4 Vulkan | Epic | Legendary (selten) |
| 5 Dunkel-Reich | Legendary | Mythic (sehr selten) |

### Klassen-Sets strecken (Zone 3–5 statt alle Zone 4)

```
Aktuell: Alle Klassen-Set-Teile ab Zone 4
Neu:
  2 Teile eines Klassen-Sets → Zone 3 (Wüste)
  2 Teile                    → Zone 4 (Vulkan)
  → Vollständiges Set erst in Zone 4–5 möglich
```

### Neue Sets

**Totenritter-Set** *(Epic, Zone 4–5 — überbrückt Verdammten-Stahl → Licht)*
```
Totenklinge      weapon  ATK +16  epic
Totenrüstung     chest   DEF +14  epic
Totenschädel     head    DEF +9   epic
Totenstiefel     feet    DEF +7   epic
4-Set: Bei ≤25% HP → +50% ATK und +20% Ausweichen
Special: totenritter_berserker
```

**Abyssal-Set** *(Legendary, Zone 5 exklusiv)*
```
Abyssalklinge    weapon  ATK +22  legendary
Abyssalrobe      chest   DEF +18  legendary
Abyssalhelm      head    DEF +12  legendary
Abyssalsohlen    feet    DEF +10  legendary
4-Set: Erleidest du Schaden → alle Gegner nehmen 30% davon als Rückstoß
Special: abyssal_thorns
```

**Mythic-Tier** *(neue höchste Rarity, Zone 5, Einzeldrops, sehr selten)*
```
Götterspeer      weapon  ATK +28  mythic  — trifft immer kritisch wenn Gegner <30% HP
Seelenpanzer     chest   DEF +22  mythic  — absorbiert ersten Angriff jedes Kampfes
Krone der Götter head    DEF +16  mythic  — +3 Skillpunkte zu Run-Beginn
```

**Geänderte Dateien:**
```
content/loot_tables.py    EQUIPMENT_DEFS, SET_DEFS, ZONE_LOOT_POOL, BOSS_LOOT_POOL
README.md                 Equipment-Tabellen aktualisieren
```

---

## v3.2 — Content-Erweiterung

> **🐛 Bug-Pass:** Dieser Schritt umfasst auch eine gezielte Suche nach Bugs
> und deren Behebung. Vor dem Tagging wird der neue Code auf Fehler geprüft
> und bestehende Bugs werden mitbehoben.

### 3 neue Monster

**Knochengoliat** *(Zone 2–3, hohe HP, selbstheilend)*
```python
class BoneColossus(Character):
    BASE_HP, BASE_ATTACK, BASE_XP = 60, 9, 42
    # boss_ability: heilt 20% max HP + setzt Blutungsstacks
```

**Wüstenschakal** *(Zone 3, schnell, Rudeltier)*
```python
class DesertJackal(Character):
    BASE_HP, BASE_ATTACK, BASE_XP = 10, 12, 26
    # Erscheint zu 2–3, hohe Ausweich-Chance per attack_target-Override
```

**Dunkelmagierin** *(Zone 5, Energie-Drain, Flüche)*
```python
class DarkSorceress(Character):
    BASE_HP, BASE_ATTACK, BASE_XP = 35, 14, 58
    # boss_ability: zufälliger Debuff + Energie-Drain
```

### 4 neue Events

**Verfallene Bibliothek**
```
[W] Waffenkunde   → +2 ATK für diesen Run
[R] Runen-Lore    → +15% XP für diesen Run
[M] Magiebuch     → sofort eine zufällige Segnung erhalten
[?] Unlesbares Buch → unbekannter Effekt (gut oder schlecht)
```

**Gefallener Held**
```
[N] Ausrüstung nehmen → zufälliges Epic-Item, aber −10 max HP (dieser Run)
[R] Ruhe lassen       → nichts passiert
[B] Bestatten         → +20% XP nächster Kampf + 15% Rune-Drop-Chance
```

**Händler-Auktion**
```
3 Gegner bieten auf ein seltenes Item.
Überbiete alle → Item gehört dir.
Verlierst → dieser Gegner erscheint verstärkt im nächsten Raum.
```

**Zeitkapsel**
```
Enthält ein zufälliges Item aus dem letzten Run
(gelesen aus dem gelöschten run_save.json-Snapshot).
```

### 10 neue Achievements *(Roguelite-spezifisch)*
```
Erster Schritt        5 Runs abgeschlossen
Spiegel-Meister       Alle Spiegel-Upgrades freigeschaltet
Rune-Sammler          10 verschiedene Runen gefunden
Synergist             2 Segnung-Synergien gleichzeitig aktiv
Unberührt             Dungeon ohne Schaden zu nehmen abgeschlossen
Todesverächter        Zweites Leben genutzt und Run dennoch gewonnen
Gilden-Gründer        Alle Hub-NPCs freigeschaltet
Mythisch              Mythic-Item gefunden
Ewige Legende         Spiel mit allen Klassen durchgespielt
Verdammter Held       Run mit allen 3 Dunkelsiegeln abgeschlossen
```

---

## v3.3 — Dunkelsiegel

> Optionale Schwierigkeitsmodifikatoren für Spieler, die das Spiel beherrschen.

> **🐛 Bug-Pass:** Dieser Schritt umfasst auch eine gezielte Suche nach Bugs
> und deren Behebung. Vor dem Tagging wird der neue Code auf Fehler geprüft
> und bestehende Bugs werden mitbehoben.

| Siegel | Malus | Runenessenz-Bonus |
|--------|-------|-------------------|
| 💀 Siegel I — Fluch des Blutes | Gegner +20% HP | +40% |
| 💀 Siegel II — Stille | Kein Shop, kein Wandernder Händler | +60% |
| 💀 Siegel III — Verhängnis | Zweites Leben deaktiviert | +80% |

Siegel sind stackbar. Alle 3 aktiv = +180% Runenessenz, aber extrem schwer.
Sonderbedingung: Alle 3 Siegel + Sieg = Cosmetic-Unlock im Hub.

**Neue/geänderte Dateien:**
```
systems/dunkelsiegel.py   NEU: SIEGEL_DEFS, siegel_menu(), apply_siegel()
systems/hub.py            [D] Dunkelsiegel-Option vor Run-Start
systems/meta_save.py      aktive Siegel für laufenden Run speichern
```

---

## Designentscheidungen *(geklärt)*

1. **Nur Roguelite** — kein Klassisch-Modus. Altes 3-Slot-System fliegt komplett raus.

2. **Fester Segnungen-Pool** — alle ~30 Segnungen von Beginn an verfügbar.
   Zufälligkeit und Synergien sorgen für Abwechslung, kein Freischalt-Aufwand nötig.

3. **Mythic-Items ohne Limit** — Drop-Chance ist so gering dass kein Hard-Cap nötig ist.
   Weniger Sonderfalllogik im Code.

---

## Gesamtübersicht

| Version | Inhalt | Status |
|---------|--------|--------|
| v2.2 | Bugfixes (8 Bugs behoben) | ✅ released |
| **v2.3** | QoL: Autosave, Upgrade/Item, Kampf-Log, Death-Screen | ✅ released |
| **v3.0** | Roguelite: Foundation + Segnungen + Spiegel + Runen | 🔲 geplant |
| **v3.1** | Equipment-Rebalancing + Mythic-Tier | 🔲 geplant |
| **v3.2** | Content: 3 Monster, 4 Events, 10 Achievements | 🔲 geplant |
| **v3.3** | Dunkelsiegel + Cosmetics | 🔲 geplant |
