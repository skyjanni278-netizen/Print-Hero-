# 🗺️ Print-Hero — Entwicklungs-Roadmap

> Ziel: Umbau zu einem vollwertigen Roguelite (Hades/Dead Cells inspiriert).
> Jeder Durchgang ist einzigartig. Der erste Run ist nicht schaffbar — Metaprogression
> macht dich stärker bis der Endboss fällt.

---

## Übersicht

| Version | Thema | Aufwand |
|---------|-------|---------|
| **v3.0** | Roguelite Foundation — Kernsystem | ████████ groß |
| **v3.1** | Segnungen — Run-Variation (Hades-Boons) | █████░░ mittel |
| **v3.2** | Der Spiegel — Metaprogression | █████░░ mittel |
| **v3.3** | Runen — Blueprints & Startkits | ████░░░ mittel |
| **v3.4** | Equipment-Rebalancing | ████████ groß |
| **v3.5** | QoL — Spielbarkeitsverbesserungen | ██░░░░░ klein |
| **v3.6** | Content-Erweiterung | ██████░ mittel |
| **v3.7** | Dunkelsiegel — Schwierigkeitsmodi | ██░░░░░ klein |

---

## v3.0 — Roguelite Foundation

### Ziel
Das Spielsystem grundlegend umbauen: weg von persistenten Speicherslots,
hin zu einem Run-basierten System mit separater Meta-Datei.

### Kern-Änderungen

**Neues Speichersystem:**
```
meta_save.json    — permanent (Runenessenz, Spiegel, freigeschaltete Runen)
run_save.json     — aktueller Run (wird bei Tod gelöscht, bei Quit behalten)
```
Die 3 alten Save-Slots entfallen. `core/save.py` wird komplett umgeschrieben.

**Run-Ablauf:**
```
Hub → Run starten → Klasse wählen → Dungeons → Tod/Sieg → Hub
```
Bei Tod: Run-Save löschen, Runenessenz aus dem Run gutschreiben, Hub zeigen.
Bei Quit: Run-Save bleibt erhalten, beim nächsten Start wird der Run fortgesetzt.

**Runenessenz — Metawährung:**
- Pro abgeschlossenem Dungeon: 15–25 Runenessenz
- Pro besiegtem Zonen-Boss: 50–80 Runenessenz
- Bei Tod: alles aus diesem Run wird ausbezahlt (kein Verlust)
- Motivation: auch ein früher Tod bringt immer etwas

**Basis-Balancing (erste Runs sollen scheitern):**
- Gegner-HP Basis: +20% gegenüber v2.2
- Gegner-ATK Basis: +15% gegenüber v2.2
- Zone 3+ ohne Metaupgrades kaum schaffbar
- Zone 5 erfordert ~8–12 Runs

**Neue/geänderte Dateien:**
```
core/save.py            — Komplett neu: meta_save + run_save Logik
systems/hub.py          — NEU: Hub-Menü zwischen Runs
systems/meta_save.py    — NEU: Metadaten laden/speichern
main.py                 — Hauptschleife angepasst (Run-Loop statt Slot-Menü)
config.py               — Neue Konstanten: RUNENESSENZ_*, BASE_DIFFICULTY_MULT
```

---

## v3.1 — Segnungen (Hades Boon-System)

### Ziel
Nach jedem abgeschlossenen Dungeon wählt man **eine von drei zufälligen Segnungen**.
Sie gelten nur für diesen Run, können aber zu starken Build-Synergien führen.

### Segnung-Pool (~30 Segnungen geplant)

**Kampf:**
| Segnung | Effekt |
|---------|--------|
| Blutdurst | Kills heilen 3 HP |
| Finstere Klinge | 10% Chance: normaler Angriff wiederholt sich kostenlos |
| Lebensraub | Gegner unter 20% HP nehmen 2× Schaden |
| Raserei | Nach 3 Kills in Folge: nächster Angriff trifft alle Gegner |
| Eisige Präsenz | Beim Betreten eines Raums: alle Gegner 1 Runde betäubt |
| Seelenernte | Kritische Treffer geben sofort 8 Energie zurück |

**Status/Effekte:**
| Segnung | Effekt |
|---------|--------|
| Giftmeister | Gift-Stacks lösen sich nicht auf — halten bis Kampfende |
| Glut-Entfesselung | Verbrennung-Stacks verursachen beim Ablaufen einmalig 3× Schaden |
| Blutfluss | Eigene Blutungsimmunität (alle Quellen) |
| Vergeltung | Beim Erleiden von Statuseffekten: Angreifer bekommt denselben Effekt (50%) |

**Überlebensfähigkeit:**
| Segnung | Effekt |
|---------|--------|
| Schattenform | Erste Runde jedes Kampfes: 100% Ausweich-Chance |
| Eisenhaut+ | +5 DEF für diesen Run |
| Zähigkeit+ | +15 max HP für diesen Run |
| Letzter Wille | Bei ≤10% HP: +30% ATK |

**Klassen-spezifisch (erscheinen nur mit passender Klasse):**
| Segnung | Klasse | Effekt |
|---------|--------|--------|
| Schatten-Reflex | Schurke | Aus dem Schatten lädt sich bei Kill sofort neu |
| Arkane Überladung | Magier | Arkane Entladung trifft 3 Gegner zufällig extra |
| Unerschütterlich | Krieger | Schildwall blockt automatisch den ersten Angriff jedes Kampfes |

**Synergien (2 passende Segnungen = Bonus):**
```
Giftmeister + Lebensraub     → Vergiftete Gegner unter 20% HP nehmen 3× Schaden
Blutdurst + Raserei          → Kill-Kette heilt 6 HP statt 3
Eisige Präsenz + Seelenernte → Betäubungs-Kill: +15 Energie
```

### Implementierung

```
systems/segnungen.py     — NEU: SEGNUNGEN_POOL, choose_segnung(), apply_segnung()
core/player.py           — active_segnungen: list, check_segnungen_synergies()
systems/dungeon.py       — Nach Dungeon-Abschluss: segnung_choice(player) aufrufen
core/combat.py           — Segnung-Effekte in Kampfphasen prüfen
ui/segnungen_ui.py       — NEU: Auswahlmenü (3 Optionen anzeigen)
```

---

## v3.2 — Der Spiegel (Hades Mirror of Night)

### Ziel
Permanente Metaupgrades mit Runenessenz kaufen.
**Jedes Upgrade hat zwei Versionen (A oder B)** — du entscheidest dich für einen Spielstil.

### Spiegel-Upgrades

| Upgrade | Version A | Version B |
|---------|-----------|-----------|
| **Zähigkeit** | +15 max HP | Starte jeden Run mit vollen HP |
| **Kriegserfahrung** | +1 ATK permanent | Erster Kampf jedes Dungeons: +50% Schaden |
| **Glück** | +15% Gold-Drop | Einmal pro Run: Item-Qualität +1 Stufe |
| **Zweites Leben** | 1× pro Run: nicht sterben (Death Defiance) | Bei Tod im Dungeon: behalte alle Items dieses Dungeons |
| **Seelenbindung** | +8% XP-Gain | Level-Ups geben +1 Skillpunkt extra |
| **Händlerglück** | Wandernder Händler erscheint 1× öfter pro Run | Händler-Preise permanent −15% |
| **Dunkelresistenz** | Statuseffekte dauern 1 Runde kürzer | Immunität gegen einen zufälligen Statuseffekt pro Run |

Kosten: 60–150 Runenessenz pro Upgrade, skalierend.
A↔B-Wechsel kostet 30% des ursprünglichen Preises.

### Implementierung

```
ui/spiegel.py            — NEU: Spiegel-Menü, A/B Auswahl, Fortschritt anzeigen
systems/meta_save.py     — spiegel_state speichern: {slot: "A"/"B"/None}
core/player.py           — apply_spiegel_effects(meta) beim Run-Start aufrufen
systems/hub.py           — [S] Spiegel-Option im Hub
```

---

## v3.3 — Runen (Dead Cells Blueprint-System)

### Ziel
Seltene Drops aus Gegnern und Bossen schalten dauerhaft neue Dinge frei.
Jede Rune erscheint nur einmal — danach ist sie dauerhaft freigeschaltet.

### Rune-Kategorien

**Startkits** (wählbar vor Run-Start):
```
Rune: Kriegers Vermächtnis   → Startkit: Kettenhemd + Streitaxt + 60 Gold
Rune: Schurken-Einsteiger    → Startkit: Giftklaue + 2× Antidot + 30 Gold
Rune: Magier-Erbe            → Startkit: Novizenstab + volle Energie + 1 Stärketrank
Rune: Überlebender           → Startkit: 3× Healing Potion + 1× Phönixfeder + 80 Gold
```

**Klassen-Varianten** (nach 5 Runs mit einer Klasse):
```
Rune: Berserker-Erbe         → Neue Klasse: Berserker (−10 HP, +6 ATK, kein Schildwall)
Rune: Meuchler-Erbe          → Neue Klasse: Meuchler (15 HP, 18 ATK, Flucht immer erfolgreich)
```

**Hub-NPCs** (erscheinen dauerhaft im Hub):
```
Rune: Schmiedegeheimnis      → Schmied im Hub: kostenloser Upgrade vor jedem Run
Rune: Händlernetzwerk        → Händlerin im Hub: kaufe Items für Runenessenz
Rune: Orakelwissen           → Orakel im Hub: zeigt nächste Zone-Boss-Stats vorab
```

**Drop-Chancen:**
- Zonen-Boss: 100% (eine garantierte Rune, pro Boss nur einmal)
- Dungeon-Boss (Rang 5): 25%
- Elite-Gegner (Rang 3+): 5%
- Truhen-Events: 15%

### Implementierung

```
systems/runen.py         — NEU: RUNE_DEFS, check_rune_drop(), apply_rune_unlock()
systems/meta_save.py     — unlocked_runen: list speichern
ui/hub.py                — [R] Runen-Übersicht, freigeschaltete Startkits anzeigen
systems/world_map.py     — Boss-Rune-Drop nach Sieg
core/combat.py           — Enemy-Rune-Drop nach Kill
```

---

## v3.4 — Equipment-Rebalancing

### Problem
Progression zu schnell: bereits in Zone 3-4 ist man vollständig ausgerüstet.
Zone 5 bietet keine echten Equipment-Entdeckungen mehr.

### Lösung: Fünf-Zonen-Equipmentkurve

Jede Zone soll **eigene, exklusive Items** haben. Epische und legendäre Items
dürfen nur in den letzten Zonen auftauchen. Klassen-Sets werden über Zonen 3–5 gestreckt.

**Neue Rarity-Verteilung:**

| Zone | Rarity-Schwerpunkt | Max verfügbare Rarity |
|------|-------------------|----------------------|
| 1 Wald | Common | Uncommon (selten) |
| 2 Ruinen | Uncommon | Rare (sehr selten) |
| 3 Wüste | Rare | Epic (sehr selten, nur Einzelteile) |
| 4 Vulkan | Epic | Legendary (selten) |
| 5 Dunkel-Reich | Legendary | Mythic (sehr selten) |

**Klassen-Sets über Zonen strecken:**
```
Aktuell: Alle Klassen-Set-Teile ab Zone 4 (Vulkan)
Neu:
  - 1-2 Teile eines Klassen-Sets: Zone 3 (Wüste)
  - Restliche 2-3 Teile: Zone 4 (Vulkan)
  → Vollständiges Set erst in Zone 4-5 machbar
```

**Neue Items:**

*Totenritter-Set* (Epic, Zone 4-5 — überbrückt Verdammten-Stahl → Licht):
```
Totenklinge       weapon  ATK +16  epic
Totenrüstung      chest   DEF +14  epic
Totenschädel      head    DEF +9   epic
Totenstiefel      feet    DEF +7   epic
4-Set-Bonus: Bei ≤25% HP → +50% ATK, +20% Ausweichen
Special: totenritter_berserker
```

*Abyssal-Set* (Legendary, Zone 5 exklusiv):
```
Abyssalklinge     weapon  ATK +22  legendary
Abyssalrobe       chest   DEF +18  legendary
Abyssalhelm       head    DEF +12  legendary
Abyssalsohlen     feet    DEF +10  legendary
4-Set-Bonus: Erleidest du Schaden → alle Gegner nehmen 30% davon als Rückstoß
Special: abyssal_thorns
```

*Mythic-Tier* (neue höchste Rarity, Zone 5, sehr seltene Einzeldrops):
```
Götterspeer       weapon  ATK +28  mythic  — trifft immer kritisch wenn Gegner unter 30% HP
Seelenpanzer      chest   DEF +22  mythic  — absorbiert ersten Angriff jedes Kampfes
Krone der Götter  head    DEF +16  mythic  — +3 Skillpunkte zu Beginn des Runs
```

**ZONE_LOOT_POOL Anpassungen:**
- Rare Items aus Zone 1-2 entfernen
- Epic Items aus Zone 1-3 entfernen
- Zone 5: Legendary-Pool erweitern (Abyssal-Set hinzufügen)
- Mythic-Pool: eigene sehr seltene Gewichtung in Zone 5

**Geänderte Dateien:**
```
content/loot_tables.py   — EQUIPMENT_DEFS, SET_DEFS, ZONE_LOOT_POOL, BOSS_LOOT_POOL
README.md                — Equipment-Tabellen aktualisieren
CLAUDE.md                — Item-Referenz aktualisieren
```

---

## v3.5 — QoL (Quality of Life)

### Autosave
- Nach jedem Dungeon-Abschluss automatisch speichern (run_save.json)
- Kein Fortschrittsverlust bei unerwartetem Programmabbruch
- Änderung in: `systems/dungeon.py`

### Upgrade per Item (nicht per Slot)
- Equipment-Dict bekommt optionales `"upgrade": N`-Feld
- Beim Anlegen wird das Item-eigene Upgrade-Level behalten
- Beim Ablegen bleibt das Upgrade am Item erhalten
- Änderung in: `core/player.py`, `ui/pause.py`

### Kompakterer Kampf-Log
- Status-Ticks werden in einer Zeile zusammengefasst:
  `⚠ Blutung -3 HP | ☠ Gift -5 HP` statt zwei separate Zeilen
- ENTER nur noch am Rundenende, nicht nach jeder Aktion
- Änderung in: `core/combat.py`

### Run-Zusammenfassung beim Tod
- Beim Tod: dedizierter Screen mit Run-Statistiken
  (Erreichte Zone, Gegner getötet, bestes Item, Schaden, Runenessenz verdient)
- Änderung in: `main.py`, neue Funktion `_run_summary(player, runenessenz)`

### Flucht-Feedback
- Beim Flüchten aus Dungeon: kurze Anzeige was man verpasst hat
  (erwarteter Loot dieser Zone, verpasste XP)
- Änderung in: `systems/dungeon.py`

---

## v3.6 — Content-Erweiterung

### 3 neue Monster

**Knochengoliat** (Zone 2-3, hohe HP, selbstheilend):
```python
class BoneColossus(Character):
    BASE_HP, BASE_ATTACK, BASE_XP = 60, 9, 42
    # boss_ability: heilt 20% max HP, setzt Blutungsstacks auf Spieler
```

**Wüstenschakal** (Zone 3, schnell, niedrige HP, Rudeltier):
```python
class DesertJackal(Character):
    BASE_HP, BASE_ATTACK, BASE_XP = 10, 12, 26
    # Erscheint immer zu 2-3, hohe Ausweich-Chance
```

**Dunkelmagierin** (Zone 5, Energie-Drain, Flüche):
```python
class DarkSorceress(Character):
    BASE_HP, BASE_ATTACK, BASE_XP = 35, 14, 58
    # boss_ability: legt random Debuff + entzieht Energie
```

### 4 neue Events

**Verfallene Bibliothek:**
```
Wähle ein altes Buch:
[W] Waffenkunde   → +2 ATK für diesen Run
[R] Runen-Lore    → +15% XP für diesen Run
[M] Magiebuch     → Zufällige Segnung sofort erhalten
[?] Unlesbares Buch → unbekannter Effekt
```

**Gefallener Held:**
```
Du findest die Leiche eines mächtigen Kriegers.
[N] Ausrüstung nehmen → zufälliges Epic-Item, aber -10 max HP permanent (dieser Run)
[R] Ruhe lassen       → nichts passiert
[B] Bestatten         → +20% XP nächster Kampf + kleine Chance auf Rune
```

**Händler-Auktion:**
```
3 Gegner bieten auf ein seltenes Item — du kannst mitbieten.
Überbiete jeden Gegner: zahle meistbietend, Item gehört dir.
Zu wenig Gold: Gegner nimmt es. Nächster Raum: dieser Gegner ist verstärkt.
```

**Zeitkapsel:**
```
Du findest einen versiegelten Behälter.
Enthält: zufälliges Item aus deinem letzten Run (aus dem Run-Save der vorherigen Session)
```

### 10 neue Achievements (Roguelite-spezifisch)

```
Erster Schritt        — 5 Runs abgeschlossen
Spiegel-Meister       — Alle Spiegel-Upgrades gekauft
Rune-Sammler          — 10 verschiedene Runen freigeschaltet
Synergist             — 2 Segnung-Synergien gleichzeitig aktiv
Unberührt             — Dungeon ohne Schaden abgeschlossen
Todesverächter        — Zweites Leben genutzt und Run trotzdem gewonnen
Gilden-Gründer        — Alle Hub-NPCs freigeschaltet
Mythisch              — Mythic-Item gefunden
Siegel-Träger         — Run mit allen 3 Dunkelsiegeln abgeschlossen
Ewige Legende         — Spiel mit allen 3 Klassen durchgespielt
```

---

## v3.7 — Dunkelsiegel (Difficulty Modifiers)

### Ziel
Optionale Schwierigkeitsmodifikatoren vor dem Run-Start.
Hohes Risiko, hohe Belohnung. Für Spieler die das Spiel beherrschen.

### Siegel

| Siegel | Malus | Runenessenz-Bonus |
|--------|-------|-------------------|
| 💀 Siegel I — Fluch des Blutes | Gegner +20% HP | +40% |
| 💀 Siegel II — Stille | Kein Shop, kein Wandernder Händler | +60% |
| 💀 Siegel III — Verhängnis | Zweites Leben deaktiviert | +80% |

Siegel sind stackbar. Alle 3 aktiv = +180% Runenessenz, aber extrem schwerer Run.

**Sonderbedingung:** Wer einen Run mit allen 3 Siegeln abschließt schaltet ein
einzigartiges Cosmetic frei (z.B. Titelzeile im Lagerfeuer: "☠ Verdammter Held").

### Implementierung

```
systems/dunkelsiegel.py  — NEU: SIEGEL_DEFS, siegel_menu(), apply_siegel_effects()
systems/hub.py           — [D] Dunkelsiegel-Option vor Run-Start
systems/meta_save.py     — aktive Siegel für laufenden Run speichern
```

---

## Implementierungs-Reihenfolge

```
v3.0  → v3.4  → v3.5  → v3.1  → v3.2  → v3.3  → v3.6  → v3.7
```

**Begründung:**
1. **v3.0 zuerst** — ohne das Fundament funktioniert nichts anderes
2. **v3.4 direkt danach** — Equipment-Balancing muss vor dem Testen der neuen
   Systeme stimmen, sonst balanciert man zweimal
3. **v3.5 (QoL) früh** — macht alle weiteren Tests angenehmer
4. Dann aufeinander aufbauend: Segnungen → Spiegel → Runen
5. Content und Schwierigkeit zuletzt — wenn das Fundament steht

---

## Datei-Übersicht: Was sich ändert

| Datei | Änderung |
|-------|----------|
| `main.py` | Run-Loop statt Slot-Menü |
| `core/save.py` | Komplett neu: meta_save + run_save |
| `core/player.py` | active_segnungen, spiegel_effects, upgrade-per-item |
| `core/combat.py` | Segnung-Hooks, kompakterer Log |
| `content/loot_tables.py` | Neue Sets, Mythic-Tier, Zone-Pool-Anpassung |
| `systems/dungeon.py` | Segnung-Auswahl nach Dungeon, Autosave |
| `systems/world_map.py` | Rune-Drops, Hub-Transition |
| `config.py` | Neue Konstanten (Runenessenz, Balancing-Multiplier) |
| **NEU** `systems/hub.py` | Hub-Menü zwischen Runs |
| **NEU** `systems/meta_save.py` | Persistente Metadaten |
| **NEU** `systems/segnungen.py` | Segnung-Pool und Logik |
| **NEU** `systems/runen.py` | Rune-Definitionen und Drops |
| **NEU** `systems/dunkelsiegel.py` | Siegel-System |
| **NEU** `ui/spiegel.py` | Spiegel-Menü |
| **NEU** `ui/hub.py` | Hub-UI |
| **NEU** `ui/segnungen_ui.py` | Segnung-Auswahlmenü |

---

## Offene Designfragen (vor Umsetzung klären)

1. **Alter Save-Modus behalten?** — Gibt es einen "Klassisch"-Modus mit Speicherslots
   neben dem Roguelite-Modus, oder ist der Roguelite-Modus das einzige?

2. **Runenessenz verlieren bei Siegel-Aktivierung?** — Oder nur Bonus für erfolgreiche Runs?

3. **Segnungen wählbar oder zufällig?** — Aktuell: 3 zufällige zur Auswahl.
   Alternative: Pool wird größer je mehr Runen man hat (Hades-Style).

4. **Mythic-Items: zu stark?** — Müssen getestet werden, eventuell nur 1 pro Run möglich.
