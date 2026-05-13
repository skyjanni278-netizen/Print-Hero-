# Print-Hero — Roadmap

> Aktuelle Version: **v2.0**  
> Diese Datei zeigt nur noch die offene Planung. Erledigte Releases sind im Git-Log und der README dokumentiert.

## Status-Legende
- ✅ Abgeschlossen
- 🔧 In Arbeit
- ⬜ Geplant

---

## ✅ v2.0.1 — Hotfixes & Balance-Pass
**Typ:** Bugfix / Balance

- `run_dungeon` gab `"defeated"` statt `"defeat"` zurück → Niederlage hat Game-Over nicht ausgelöst (behoben)
- Zonen-Bosse: HP ×0,9, ATK ×0,9 gegenüber v2.0-Werten
- Normale Gegner: +10 % HP und ATK als Basis-Buff
- WoodTroll-Boss: Betäubungsschlag-Chance 30 % → 15 %
- Kampf-UI: HP-Balken `[####----]`, 2-Spalten-Aktionsmenü, Rundenanzeige, Auto-Target bei Einzelgegner

---

## 🔧 v2.0.2 — Events, Balance & Fixes
**Typ:** Content / Balance

- **4 neue Dungeon-Events:** Blutiger Altar, Wanderhändler im Dungeon, Flüsternder Geist, Magische Schatztruhe
- **Arkane Entladung** (Magier) gebalanced: Level-skalierender Schaden, 15 Energie-Kosten
- Zonen-Bosse nochmals gebalanced (Z2–Z5 stärker reduziert), Equipment-Progression verlangsamt
- Code-Qualität: `config.py` Konstanten, robuste Save/Load-Fehlerbehandlung, fix relativer Pfad

---

## ⬜ v2.0.3 — Content-Pass & Loot-Überarbeitung
**Typ:** Content / Progression

### Loot-System: Strukturierte Progression

Das gesamte Loot-System wird neu gestaltet. Ziel: Der Spieler weiß, **worauf er hinarbeitet**, und sammelt gezielt ein Set für seine aktuelle Zone — anstatt zufällig Legendaries zu bekommen, bevor er Zone 2 betritt.

**Grundprinzip:**
- Jede Zone hat einen **festen Equipment-Tier** — normale Gegner droppen nur Teile dieses Tiers
- **Zonen-Bosse** droppen garantiert ein oder zwei Teile des *nächsten* Tiers als Anreiz
- **Legendäre Items** gibt es ausschließlich aus dem Dunkel-Reich-Boss und dessen Dungeons
- Sets bleiben das Ziel: Man sammelt 4 Teile eines Sets und schaltet den Bonus frei

**Gear-Progression nach Zone:**

| Zone | Tier | Hauptsets |
|------|------|-----------|
| 🌲 Wald | Common / Uncommon | Leder-Set, Eisen-Set |
| 🏚️ Ruinen | Uncommon / Rare | Stahl-Set, Runen-Panzer *(neu)* |
| 🏜️ Wüste | Rare | Schatten-Set, Schattentuch *(neu)* |
| 🌋 Vulkan | Epic | Drachen-Set, Drachenschuppen *(neu)*, Klassen-Sets |
| 💀 Dunkel-Reich | Epic / Legendary | Licht-Set, Verdammten-Stahl *(neu)* |

**Boss-Drops (garantiert):**
- Zonen-Boss droppt immer **1–2 Set-Teile des nächsten Tiers** + Gold
- Dungeon-Bosse droppen **zonenspezifische** Items (kein zufälliger Rang mehr)
- Schwarzmarkt bietet **gezielt** Epic- und Legendary-Items gegen viel Gold

**Technische Umsetzung:**
- `LOOT_POOL` wird durch zonengebundene Pools ersetzt (`ZONE_LOOT_POOL["wald"]` usw.)
- `RANK_LOOT_WEIGHTS` entfällt oder wird nur noch für Konsumables/Gold genutzt
- `roll_loot()` bekommt `zone_id`-Parameter statt `rank`
- Boss-Loot via separater `roll_boss_loot(zone_id)` Funktion mit garantierten Set-Drops

---

**Neue Monster** (3 Gegnerklassen):
- **Waldgeist** (Wald): Heilt sich ~20 % HP/Runde — muss schnell besiegt werden. *Boss:* Geisterschrei (Betäubung)
- **Lich** (Ruinen): 25 % Energie-Drain. *Boss:* Nekromantie — belebt besiegten Gegner mit 30 % HP
- **Sandwurm** (Wüste): Hohes DEF, immun gegen Blutung/Gift, 20 % Angriff verschlucken. *Boss:* Sandsturm (−4 DEF)

**Neue Waffen** (mit Passiveffekten, zonengebunden):

| Waffe | Zone | ATK | Passiv |
|-------|------|:---:|--------|
| **Giftklaue** | Wald / Wüste | +5 | Jeder Angriff: +1 garantierter Giftstack |
| **Flammenklinge** | Vulkan | +8 | 25 % Chance: 2 Verbrennungsstacks (3 Runden) |
| **Eisaxt** | Ruinen / Wüste | +10 | 20 % Chance: Gegner eingefroren (1 Runde betäubt) |
| **Runen-Kriegshammer** | Ruinen / Schwarzmarkt | +12 / −2 DEF | 30 % Chance: −3 DEF-Debuff beim Gegner |

**Neue Rüstungssets** (neutral, zonengebunden):

| Set | Zone | 4-teiliger Bonus |
|-----|------|-----------------|
| **Runen-Panzer** | Ruinen | +8 DEF, +25 max. HP, Blutungsschaden −1/Runde |
| **Schattentuch** | Wüste | −3 DEF, +15 % Ausweich-Chance |
| **Drachenschuppen** | Vulkan | +12 DEF, 20 % Feuer-Immunität |
| **Verdammten-Stahl** | Dunkel-Reich | +6 ATK, −4 DEF |

---

## ⬜ v2.0.4 — Fähigkeiten-Überarbeitung
**Typ:** Balance / Gameplay

Jede Klasse erhält **4 klassenspezifische Kampffähigkeiten** auf den Tasten `[S]`, `[R]`, `[C]`, `[X]`.  
Alle generischen Fähigkeiten (Himmelsschlag, Rundumschlag, Cleave) entfallen.  
Fähigkeiten sind **energie-gebunden und wiederverwendbar** — kein "einmal pro Kampf" mehr, stattdessen Cooldowns.

| Klasse | [S] | [R] | [C] | [X] |
|--------|-----|-----|-----|-----|
| ⚔️ Krieger | Brutaler Hieb (18E) | Schildwall (10E) | Schildstoß (20E, 3R CD) | Kriegsschrei (25E, 1×/Kampf) |
| 🗡️ Schurke | Aus dem Schatten (15E) | Giftklinge (12E) | Blendpulver (20E, 4R CD) | Rauchbombe (10E) |
| 🔮 Magier | Arkane Entladung (15E) | Froststrahl (18E) | Feuerball (22E, 3R CD) | Mana-Schild (0E, 4R CD) |

**Unlock-Level:** Alle [S]/[R] ab LVL 1, [C] ab LVL 3, [X] ab LVL 5.  
**Cooldown-System:** `player.ability_cooldowns` Dict ersetzt `class_ability_used`-Flags. Cooldown = 0 → unbegrenzt nutzbar, Cooldown = 99 → 1× pro Kampf.  
**Fähigkeiten-Übersicht:** Neues Menü `[?]` im Kampf und im Lagerfeuer — zeigt alle 4 Klassen-Fähigkeiten mit Name, Taste, Energiekosten, Cooldown und ausführlicher Beschreibung.  
**Code-Aufräumen:** `heavenstrike()`, `whirlwind()`, `cleave()` aus `player.py` entfernen; `class_ability_used/2/3` und `arcane_charges_remaining` aus `player.py` und `save.py` entfernen.

---

## ⬜ v2.0.5 — Rich UI
**Typ:** UI-Overhaul

Einführung der `rich`-Library (`pip install rich`, `requirements.txt`):

- **Kampf-Screen:** Farbige HP-Balken `████░░░░` (grün/gelb/rot), Live-Update ohne Flackern, Statuseffekte farbig
- **Dungeon-Screen:** Fortschrittsbalken Raum X/Y, farbige Raumtyp-Icons
- **Lagerfeuer/Menüs:** Zweispaltige Panel-Ansicht, Weltkarte als Rich-Table mit Fortschrittsbalken
- **Inventar & Shop:** Tabellen-View mit Stats, Preisen und Rarity-Farben
- **Screens:** Boss-Intros als styled Panel, Level-Up-Animation, Endscreen mit Stats-Zusammenfassung
- **Slot-Auswahl:** Übersichtliche Spielstand-Karten beim Start

---

## ⬜ v2.0.6 — UI-Finalisierung & QoL
**Typ:** UI-Polish / QoL

- Vollständige Rich-Integration — kein alter `print_header`-Code mehr, konsistente Farbpalette
- **QoL:** Zone + Dungeon-Fortschritt im Lagerfeuer-Header sichtbar
- **QoL:** Direkte Ergebnis-Summary nach Dungeon-Sieg
- **QoL:** Crafting-Menü zeigt fehlende Materialien farbig hervor
- Performance: redundante `clear_screen`-Aufrufe reduzieren
- Alle bekannten Bugs aus v2.0.x-Feedback beheben

---

## ⬜ v2.1 — Stable Release
**Typ:** Fixes / Minor Patches

- Letzter Bug-Fix- und Balance-Pass nach v2.0.6-Feedback
- README und ROADMAP auf finalen Stand bringen
- GitHub-Release mit Changelog

---

## Gesamtübersicht

```
v2.0     ✅  Weltkarte & Zones             [abgeschlossen]
──────────────────────────────────────────────────────────
v2.0.1   ✅  Hotfixes & Balance-Pass
v2.0.2   🔧  Events, Balance & Fixes
v2.0.3   ⬜  Content-Pass (Monster, Waffen, Sets)
v2.0.4   ⬜  Fähigkeiten-Überarbeitung
──────────────────────────────────────────────────────────
v2.0.5   ⬜  Rich UI (alle Screens)
v2.0.6   ⬜  UI-Finalisierung & QoL
──────────────────────────────────────────────────────────
v2.1     ⬜  Stable Release
```
