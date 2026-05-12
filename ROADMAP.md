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

## 🔧 v1.9.5 — Klassen-Rüstungssets
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

## ⬜ v1.9.6 — Story & Lore
**Typ:** Content + Atmosphäre

- Boss-Intros: kurzer Einleitungstext pro benanntem Boss beim Betreten
- Zonen-Flavor: 2–3 Sätze Atmosphäre beim Betreten einer Zone
- 3–4 neue Event-Typen mit mehr Dialog-Optionen:
  - z.B. „Gefangener Soldat" — befreien (spätere Belohnung) oder ignorieren
  - z.B. „Alter Schmied" — zahle Gold für einmaliges Gratis-Upgrade
- Dungeon-Namen aus zufälligem Pool (z.B. „Die Blutigen Ruinen", „Höhle des Ewigen Frostes")

---

## ⬜ v1.9.7 — Wirtschaft & Crafting
**Typ:** Feature

- Junk-Items kombinieren zu Consumables:
  - 3× Knochen → 1× Antidot
  - 2× Trollfell + 1× Goblinzahn → 1× Stärketrank
- Rezept-System: Rezepte beim Schmied oder in Truhen finden
- Preisbalance-Pass aller Shop- und Verkaufspreise
- Wandernder Händler bekommt 1× pro Zone einen „Schwarzmarkt"-Event

---

## ⬜ v1.9.8 — Balance & Meta-Progression
**Typ:** Balance + Polish

- Vollständiger Balance-Pass: Monster-Stats, Loot-Chancen, XP-Kurven, Preise
- Achievement-Erweiterung: Zonen- und Klassen-spezifische Achievements
- NG+ nutzt Dungeon/Zonen-System korrekt
- Statistiken-Erweiterung: Zonen-Kills, Dungeons abgeschlossen, schnellster Run

---

## ⬜ v1.9.9 — V2.0 Technische Vorbereitung
**Typ:** Refactor

- Dungeon-System für Zonen-Kontext refaktorieren
- `world_map.py` als leeres Grundgerüst anlegen
- Zone-Klasse definieren (Name, Monster-Pool, Dungeons, Boss, Unlock-Bedingung)
- Savegame-Format für Weltkarte erweitern (Zonen-Fortschritt, abgeschlossene Dungeons)

---

## ⬜ v2.0 — Weltkarte & Zones
**Typ:** Major Release

- Weltkarte mit 5 Zonen, die nacheinander freigeschaltet werden
- Je Zone: 3–5 Dungeons + 1 einzigartiger Zonen-Boss mit eigenem Namen und Fähigkeiten
- Unlock-System: Zonen-Boss besiegt → nächste Zone öffnet sich
- Dungeons bleiben nach Abschluss gesperrt (kein endloses Farmen in derselben Zone)
- NG+ = zweiter Weltkarten-Durchlauf mit 1.3× Skalierung pro Runde
- Endscreen nach Abschluss aller 5 Zonen: Stats-Zusammenfassung + NG+-Angebot

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
v1.9.5   🔧  Klassen-Rüstungssets        ← aktuell
v1.9.6   ⬜  Story & Lore
v1.9.7   ⬜  Wirtschaft & Crafting
v1.9.8   ⬜  Balance & Meta
v1.9.9   ⬜  V2.0 Tech-Prep
─────────────────────────────────────────────
v2.0     ⬜  Weltkarte & Zones
```
