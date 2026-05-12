# Print-Hero — Roadmap

> Diese Datei wird mit jedem Release aktualisiert und dient als persistente Referenz für die Planung.

## Status-Legende
- ✅ Abgeschlossen
- 🔧 In Arbeit
- ⬜ Geplant

---

## ✅ v1.8.3 — Pause-Menü Cleanup
**Typ:** Polish

- Lagerfeuer-Optionen in zwei visuelle Gruppen: ⚔️ Ausrüstung und 🧙 Charakter
- Trennlinien, saubere Formatierung als Basis für alles Kommende

---

## ✅ v1.9 — Dungeon-Fundament
**Typ:** Core Feature

- 3–5 Räume pro Dungeon, Boss immer letzter Raum
- Raumtypen: Kampf-Raum, Event-Raum, Mini-Boss-Raum, Boss-Raum
- Zwischen-Raum-Moment: Ausrüsten, Tränke benutzen, nächsten Raum einsehen
- Garantierter Schatz nach Boss-Kill (kein separater Schatz-Raum)
- Volle HP/Energie-Regeneration nach erfolgreich abgeschlossenem Dungeon
- Shop erscheint ausschließlich zwischen zwei Dungeons
- Flucht aus dem gesamten Dungeon jederzeit möglich

---

## ✅ v1.9.1 — Dungeon Raum-Vielfalt
**Typ:** Content

- **Elite-Raum** `💪`: Stärkerer Einzelgegner (Rang 2), bessere Beute als normaler Kampf
- **Schrein-Raum** `🕯️`: Wahl: +HP, +Energie, +XP-Buff oder Fluch wagen (Loot/Schaden)
- **Fallen-Raum** `⚠️`: Ausweichen (kostet Energie) oder Durchlaufen (kostet HP)
- **Leerer Raum** `🌫️`: Flavor-Text, 25% Loot-Chance, 20% Gold-Fund
- Raumreihenfolge zufällig, Boss bleibt immer letzter Raum

---

## ✅ v1.9.2 — Zonen-Vorbereitung
**Typ:** Technisch + Content

- Zonen-Themen definiert: Wald, Ruinen, Wüste, Vulkan, Dunkel-Reich
- Gegner-Pool pro Zone (nicht mehr per Spielerlevel):
  - Wald: Wölfe, Goblins, Trolle
  - Ruinen: Skelette, Zombies, Geister
  - Wüste: Sandwürmer, Banditen, Assassinen
  - Vulkan: Feuerdämonen, Golems, Drachen
  - Dunkel-Reich: Dunkelritter, Eismagierin, alle Boss-Varianten
- Loot-Pool pro Zone mit passenden Drops
- Dungeon-Schwierigkeit skaliert mit Zone statt Spielerlevel

---

## ✅ v1.9.3 — Klassen-Waffen
**Typ:** Content + Identity

- Jede Waffe hat 3 Varianten — eine pro Klasse, gleiche Stats, klassenspezifischer Name
  - Krieger → `Bastardschwert`, Schurke → `Klingenschatten`, Magier → `Magierstab`
- Drops richten sich nach aktiver Klasse
- Generische Shop-Namen bleiben als Basis erhalten

---

## 🔧 v1.9.4 — Klassen-Fähigkeiten Erweiterung
**Typ:** Feature

- 2 neue aktive Fähigkeiten pro Klasse (zusätzlich zu den bestehenden):
  - Krieger: `Schildstoß` (Schaden + Betäubung), `Kriegsschrei` (temporär +ATK)
  - Schurke: `Giftklinge` (garantierte Gift-Stacks), `Rauchbombe` (garantierte Flucht + DEF-Debuff)
  - Magier: `Froststrahl` (Angriff + Einfrieren), `Mana-Schild` (HP statt Energie für Angriff)
- Passive Klassen-Boni skalieren mit Level

---

## ✅ v1.9.5 — Klassen-Rüstungssets
**Typ:** Feature + Balance

- Krieger-Set **"Eisenfestung"**: DEF + Block-Synergien
  - 4-teilig: +10 DEF, Schildwall blockiert zwei Angriffe statt einem
- Schurken-Set **"Schattenhülle"**: Blutung + Krit-Chance
  - 4-teilig: +15% Krit, Aus-dem-Schatten lädt sich alle 3 Runden auf
- Magier-Set **"Arkane Roben"**: Energie + Magie-Verstärkung
  - 4-teilig: +20 max. Energie, Arkane Entladung hat 2 Ladungen pro Kampf
- Klassen-Sets droppen nur für die passende Klasse
- Neutrale Sets (Runen, Drachen etc.) bleiben universell verfügbar

---

## ✅ v1.9.6 — Story & Lore
**Typ:** Content + Atmosphäre

- Boss-Intros: kurzer Einleitungstext pro benanntem Boss beim Betreten
- Zonen-Flavor: 2–3 Sätze Atmosphäre beim Betreten einer Zone (in Zone-Auswahl)
- 2 neue Event-Typen:
  - „Gefangener Soldat" — befreien (−5 HP, +Gold + Loot-Chance) oder ignorieren
  - „Alter Schmied" — einmaliges kostenloses Equipment-Upgrade
- Dungeon-Namen aus zufälligem Pool pro Zone (z.B. „Die Blutigen Ruinen", „Höhle des Ewigen Frostes")

---

## ✅ v1.9.7 — Wirtschaft & Crafting
**Typ:** Feature

- 4 Craft-Rezepte: Junk-Items → Consumables (Knochen→Antidot, Trollfell+Goblinzahn→Stärketrank, Schleimklumpen→Energie-Kristall, Wolfspelz+Lumpen→Healing Potion)
- [C] Handwerk-Menü am Lagerfeuer — zeigt Materialien und verfügbare Rezepte
- Schwarzmarkt: Wandernder Händler bietet 1× pro Zone seltene epische Items an
- Preisbalance-Pass: Frühspiel-Items 10–15% günstiger

---

## ✅ v1.9.8 — Balance & Meta-Progression
**Typ:** Balance + Polish

- 10 neue Achievements (20 gesamt): Zonen-Dungeons, Klassen-Level-10, Schlachtveteran, Dungeon-Veteran
- Achievement-Menü mit Sektionen (Kampf, Aufstieg, Dungeons & Zonen, Wirtschaft, Meta)
- Stats-Erweiterung: Dungeons abgeschlossen/geflohen, Zone-Kills-Tabelle
- NG+ Fix: Zone auf Wald zurückgesetzt, Shop und Schwarzmarkt ebenfalls zurückgesetzt
- Balance: Rang-5 Legendary-Loot 12%→8% (seltener, dafür Epic stärker gewichtet)

---

## ✅ v1.9.9 — V2.0 Technische Vorbereitung
**Typ:** Refactor

- `_create_scaled_enemy` refaktoriert: nutzt jetzt direkt den Zonen-Monster-Pool aus `ZONE_DEFS` statt `core.combat.create_enemy`
- `systems/world_map.py` als Grundgerüst angelegt: `get_zone_status()`, `show_world_map()` (Platzhalter für v2.0)
- `ZONE_DEFS` erweitert: `boss_class` (Zonen-Boss-Klasse) und `dungeon_count` (benötigte Dungeons zum Boss) pro Zone
- Savegame-Format erweitert: `zone_progress` dict (`{zone_id: {dungeons_completed, boss_defeated}}`), gespeichert, geladen und bei NG+ zurückgesetzt

---

## ✅ v2.0 — Weltkarte & Zones
**Typ:** Major Release

- Weltkarte mit 5 Zonen, die sequenziell freigeschaltet werden (Zonen-Boss besiegt → nächste Zone öffnet sich)
- 5 einzigartige Zonen-Bosse mit eigenem Namen, Intro-Text und verstärkten Stats (×2.5–3.5 HP)
  - Wald: **Torg, Wächter des Waldes** (WoodTroll)
  - Ruinen: **Korroth, der Ewige Wächter** (StoneGolem)
  - Wüste: **Razin, König der Meuchler** (Assassin)
  - Vulkan: **Ignar, der Ewige Drache** (Dragon)
  - Dunkel-Reich: **Malachar, Herr der Finsternis** (DarkKnight)
- Zone-Progress-System: N Dungeons pro Zone → Boss-Kampf freigeschaltet ([B] im Lagerfeuer)
- Interaktive Weltkarte ([Z] im Lagerfeuer) mit Zonen-Status: 🔒 / 🟢 / 🔵 / 🔥 / ✅
- Endscreen nach allen 5 Zonen: vollständige Stats-Zusammenfassung + NG+-Angebot
- NG+ weiterhin möglich (Trigger durch Endscreen, nicht mehr durch Level 10)
- Legacy-Save-Kompatibilität: alte Spielstände werden automatisch korrekt freigeschaltet
- Refactoring: `zone_menu` → `world_map.show_world_map`, `create_enemy` Wrapper entfernt, `camp_menu` gibt Aktion zurück

---

---

## ⬜ v2.1.1 — Bugfixes & Stabilität
**Typ:** Polish / QoL

- Bekannte Fehler nach v2.0 beheben (Encoding, Edge-Cases, Savegame-Checks)
- Code-Cleanup: Redundante Logik konsolidieren, Magic Numbers als Konstanten
- Save/Load-Fehlerbehandlung robuster machen (korrupte Saves abfangen)
- QoL: Aktuelle Zone sichtbar im Lagerfeuer-Header
- QoL: Nach einem Dungeon-Sieg direkt Ergebnis-Summary vor dem Lagerfeuer
- Balance-Feinschliff falls nach mehr Spielzeit nötig

---

## ⬜ v2.1.2 — Neue Monster & Dungeon-Events
**Typ:** Content

### Neue Monster (3 gesamt, verteilt auf Zonen)
- **Waldgeist** (Wald): Niedriger HP, heilt sich jede Runde um 20% — muss schnell besiegt werden
- **Lich** (Ruinen): Magischer Angreifer, 25% Chance auf Energie-Drain (−8 Energie beim Spieler)
- **Sandwurm** (Wüste): Hohes DEF, kein Blut/Gift — dafür kann er ein Gruppenmitglied kurz "verschlucken" (1 Runde handlungsunfähig)

### Neue Dungeon-Events (4 neue Event-Raum-Typen)
- **🩸 Blutiger Altar**: HP opfern (−15%) für einen starken Einmal-Buff (Wahl: +30% ATK, volle Energie, oder XP-Boost)
- **🏪 Wanderhändler**: Kleiner Shop direkt im Dungeon — 2 zufällige Items, Preise etwas höher als normal
- **💀 Flüsternder Geist**: Enthüllt den Boss-Typ des Dungeon-Bosses; 50% Chance auf +15% XP für diesen Dungeon
- **🔮 Magische Schatztruhe**: Garantierter Item-Drop, aber 30% Chance auf Fluch (−10 Max-HP bis Dungeon-Ende)

---

## ⬜ v2.1.3 — Equipment-Erweiterung
**Typ:** Content

### Neue Rüstungssets (4 neutrale Sets — nicht klassengebunden)
- **Drachenschuppen-Set** (4-teilig, Vulkan-Drops): +12 DEF, 20% Chance Feuer-Angriffe ignorieren
- **Runen-Panzer** (4-teilig, Ruinen-Drops): +8 DEF, +25 Max-HP, passiver Blut-Widerstand (−1 Blutungsschaden/Runde)
- **Schattentuch-Set** (4-teilig, Wüste-Drops): −3 DEF, aber 15% Ausweich-Chance (Angriff trifft nicht)
- **Verdammten-Stahl** (4-teilig, Dunkelreich-Drops): +6 ATK, −4 DEF — offensiver High-Risk-Style

### Neue Waffen (4, mit eigenen Passiveffekten)
- **Flammenklinge** (Vulkan): +8 ATK, 25% Chance auf 2 Verbrennungsstacks (wirkt wie Gift, 3 Runden)
- **Eisaxt** (Wüste/Ruinen): +10 ATK, 20% Chance Gegner eine Runde einfrieren (betäubt)
- **Giftklaue** (Wald/Wüste): +5 ATK, jeder Angriff: +1 Giftstack garantiert
- **Runen-Kriegshammer** (Ruinen): +12 ATK, −2 DEF — langsam aber schwer; 30% Chance auf Erschütterung (−3 DEF Debuff beim Gegner)

---

## ⬜ v2.1 — Rich Terminal UI
**Typ:** Major Release / UI-Overhaul

**Ziel:** Kompletterneuerung aller Screens mit der Python `rich`-Library. Gleiches Spiel,
dramatisch bessere Optik. Kein Architektur-Umbau nötig — nur UI-Schicht.

### Was `rich` ermöglicht
- Echte Unicode-HP-Balken `████░░░░` mit Farben (rot bei <30%, gelb <60%, grün)
- Farbige Panels mit Rahmen für alle Screens (Kampf, Lagerfeuer, Weltkarte)
- Tabellen für Inventar, Shop, Achievements
- **Live-Update im Kampf** (`rich.live`) — HP-Balken aktualisieren sich in Echtzeit ohne Flackern
- Farbige Status-Effekte (rotes Blutung-Icon, lila Gift, etc.)
- Spinner/Animationen für Ladesequenzen und Boss-Intros

### Geplante Screen-Überarbeitungen
- **Kampf-Screen**: Live-Panel mit Echtzeit-HP, farbige Statuseffekte, animierter Schadens-Text
- **Lagerfeuer / Camp-Menü**: Zweispaltige Panel-Ansicht (Links: Spielerinfo, Rechts: Aktionen)
- **Weltkarte**: Rich-Table mit Zone-Status-Spalten, Fortschrittsbalken pro Zone
- **Inventar / Shop**: Tabellen-View mit Spalten (Name, Stats, Preis, Effekt)
- **Dungeon**: Fortschrittsanzeige Raum X/Y, farbige Raumtyp-Icons
- **Achievement-Screen**: Fortschrittsbalken pro Achievement-Gruppe
- **Endscreen / Boss-Sieg**: Animierter Text, farbige Stats-Zusammenfassung

### Technischer Plan
1. `pip install rich` → in `requirements.txt` eintragen
2. `ui/rich_utils.py` als zentrales Modul für alle `rich`-Helpers
3. Schrittweise Ablösung: Datei für Datei, beginnend mit `core/combat.py`
4. Fallback auf ASCII wenn `rich` nicht installiert (optional)

---

## Gesamtübersicht

```
v1.8.3   ✅  Pause-Menü Cleanup
v1.9     ✅  Dungeon-Fundament
─────────────────────────────────────────────
v1.9.1   ✅  Dungeon Raum-Vielfalt
v1.9.2   ✅  Zonen-Vorbereitung
v1.9.3   ✅  Klassen-Waffen
v1.9.4   ✅  Klassen-Fähigkeiten
v1.9.5   ✅  Klassen-Rüstungssets
v1.9.6   ✅  Story & Lore
v1.9.7   ✅  Wirtschaft & Crafting
v1.9.8   ✅  Balance & Meta
v1.9.9   ✅  V2.0 Tech-Prep
─────────────────────────────────────────────
v2.0     ✅  Weltkarte & Zones
─────────────────────────────────────────────
v2.1.1   ⬜  Bugfixes & Stabilität
v2.1.2   ⬜  Neue Monster & Dungeon-Events
v2.1.3   ⬜  Equipment-Erweiterung
v2.1     ⬜  Rich Terminal UI
```
