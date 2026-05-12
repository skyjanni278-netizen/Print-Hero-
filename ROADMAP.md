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

## ⬜ v2.0.2 — Neue Dungeon-Events
**Typ:** Content

Vier neue Event-Raumtypen für mehr Abwechslung in Ereignis-Räumen:

- **🩸 Blutiger Altar** — HP opfern (−15 %) für einen Einmal-Buff nach Wahl: +30 % ATK, volle Energie oder XP-Bonus
- **🏪 Wanderhändler im Dungeon** — Kleiner Shop direkt im Dungeon, 2 zufällige Items, leicht erhöhte Preise
- **💀 Flüsternder Geist** — Enthüllt den Boss-Typ des Dungeon-Bosses; 50 % Chance auf +15 % XP für diesen Dungeon
- **🔮 Magische Schatztruhe** — Garantierter Item-Drop, aber 30 % Chance auf Fluch (−10 max. HP bis Dungeon-Ende)

---

## ⬜ v2.0.3 — Neue Monster
**Typ:** Content

Drei neue Gegnerklassen, verteilt auf bestehende Zonen:

- **Waldgeist** (Wald): Niedriger HP, heilt sich jede Runde um ~20 % seiner max. HP — muss schnell besiegt werden.  
  *Boss-Fähigkeit:* Geisterschrei — betäubt den Spieler für 1 Runde
- **Lich** (Ruinen): Magischer Angreifer, 25 % Chance auf Energie-Drain (−8 Energie beim Spieler).  
  *Boss-Fähigkeit:* Nekromantie — revitalisiert einen bereits besiegten Gegner mit 30 % HP
- **Sandwurm** (Wüste): Hohes DEF, immun gegen Blutung/Gift. 20 % Chance, einen Angriff zu verschlucken (Spieler überspringt 1 Runde).  
  *Boss-Fähigkeit:* Sandsturm — −4 DEF-Debuff auf den Spieler

---

## ⬜ v2.0.4 — Neue Waffen
**Typ:** Content

Vier neue Waffen mit eigenen Passiveffekten, als klassenspezifische Drops und im Schwarzmarkt:

| Waffe | ATK | Passiv |
|-------|:---:|--------|
| **Flammenklinge** | +8 | 25 % Chance: 2 Verbrennungsstacks (wirkt wie Gift, 3 Runden) |
| **Eisaxt** | +10 | 20 % Chance: Gegner eingefroren (1 Runde betäubt) |
| **Giftklaue** | +5 | Jeder Angriff: garantiert +1 Giftstack |
| **Runen-Kriegshammer** | +12 / −2 DEF | 30 % Chance: −3 DEF-Debuff beim Gegner |

- Flammenklinge droppt in Vulkan-Zone
- Eisaxt in Ruinen- und Wüsten-Zone
- Giftklaue in Wald- und Wüsten-Zone
- Runen-Kriegshammer in Ruinen-Zone und Schwarzmarkt

---

## ⬜ v2.0.5 — Neue Rüstungssets
**Typ:** Content

Vier neue **neutrale Sets** (für alle Klassen), als Zone-spezifische Drops:

| Set | Zone | 4-teiliger Bonus |
|-----|------|-----------------|
| **Drachenschuppen** | Vulkan | +12 DEF, 20 % Chance Feuer-Angriffe vollständig ignorieren |
| **Runen-Panzer** | Ruinen | +8 DEF, +25 max. HP, Blutungsschaden −1/Runde |
| **Schattentuch** | Wüste | −3 DEF, dafür 15 % Ausweich-Chance (Angriff trifft nicht) |
| **Verdammten-Stahl** | Dunkel-Reich | +6 ATK, −4 DEF — offensiver High-Risk-Style |

---

## ⬜ v2.0.6 — Rich UI: Kampf & Dungeon
**Typ:** UI-Overhaul (Teil 1)

Einführung der `rich`-Library für den Kampf- und Dungeon-Bereich:

- `pip install rich` → `requirements.txt`
- `ui/rich_utils.py` als zentrales Modul für alle Shared-Helpers
- **Kampf-Screen:** Farbige Panels, echte Unicode-HP-Balken `████░░░░`, Live-Update mit `rich.live` (kein Flackern)
  - HP-Farbe: grün (>60 %), gelb (>30 %), rot (≤30 %)
  - Statuseffekte farbig hervorgehoben (rot = Blutung, lila = Gift, grau = Betäubung)
  - Animierter Schadens-Text beim Treffer
- **Dungeon-Screen:** Fortschrittsanzeige Raum X/Y mit Rich-Balken, farbige Raumtyp-Icons

---

## ⬜ v2.0.7 — Rich UI: Menüs & Weltkarte
**Typ:** UI-Overhaul (Teil 2)

- **Lagerfeuer / Camp-Menü:** Zweispaltige Panel-Ansicht (links Spielerinfo, rechts Aktionen)
- **Weltkarte:** Rich-Table mit Zone-Status-Spalten, Fortschrittsbalken pro Zone
- **Inventar:** Tabellen-View mit Spalten (Name · Stats · Menge · Effekt)
- **Shop:** Übersichtliche Tabelle mit Preisspalte, aktuelles Gold sichtbar
- **Schwarzmarkt:** Eigener styled Panel mit seltenem Flair

---

## ⬜ v2.0.8 — Rich UI: Screens & Boss-Intros
**Typ:** UI-Overhaul (Teil 3)

- **Achievement-Screen:** Fortschrittsbalken pro Gruppe, farbige Unlock-Anzeige
- **Endscreen:** Animierter Text, farbige Stats-Zusammenfassung
- **Boss-Intros:** Styled Panel mit Intro-Text, Boss-Stats und dramatischem Farbakzent
- **Slot-Auswahl:** Übersichtlichere Spielstand-Karten beim Start
- **Level-Up:** Animierter Panel mit neuen Werten

---

## ⬜ v2.0.9 — UI-Finalisierung & QoL
**Typ:** UI-Polish / QoL

- Vollständige Integration aller Rich-Screens — kein alter `print_header`-Code mehr
- Konsistente Farbpalette und Rahmenstile überall
- **QoL:** Aktuelle Zone + Dungeon-Fortschritt sichtbar im Lagerfeuer-Header
- **QoL:** Nach Dungeon-Sieg direkte Ergebnis-Summary vor Rückkehr ins Lagerfeuer
- **QoL:** Crafting-Menü zeigt fehlende Materialien farbig hervor
- Save/Load-Fehlerbehandlung robuster (korrupte Saves abfangen, Backup anlegen)
- Performance: Imports optimieren, redundante `clear_screen`-Aufrufe reduzieren
- Alle bekannten Bugs aus v2.0.x-Feedback beheben

---

## ⬜ v2.1 — Stable Release
**Typ:** Fixes / Minor Patches

- Letzter Bug-Fix-Pass nach v2.0.9-Feedback
- Balance-Feinschliff falls nach mehr Spielzeit nötig
- README und ROADMAP auf finalen Stand bringen
- GitHub-Release mit Changelog erstellen

---

## Gesamtübersicht

```
v2.0     ✅  Weltkarte & Zones          [abgeschlossen]
─────────────────────────────────────────────────────────
v2.0.1   ✅  Hotfixes & Balance-Pass
v2.0.2   ⬜  Neue Dungeon-Events
v2.0.3   ⬜  Neue Monster
v2.0.4   ⬜  Neue Waffen
v2.0.5   ⬜  Neue Rüstungssets
─────────────────────────────────────────────────────────
v2.0.6   ⬜  Rich UI: Kampf & Dungeon
v2.0.7   ⬜  Rich UI: Menüs & Weltkarte
v2.0.8   ⬜  Rich UI: Screens & Boss-Intros
v2.0.9   ⬜  UI-Finalisierung & QoL
─────────────────────────────────────────────────────────
v2.1     ⬜  Stable Release
```
