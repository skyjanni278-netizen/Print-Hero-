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

## 🔧 v1.9.9 — V2.0 Technische Vorbereitung
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
v1.9.5   ✅  Klassen-Rüstungssets
v1.9.6   ✅  Story & Lore
v1.9.7   ✅  Wirtschaft & Crafting
v1.9.8   ✅  Balance & Meta
v1.9.9   🔧  V2.0 Tech-Prep               ← aktuell
v1.9.9   ⬜  V2.0 Tech-Prep
─────────────────────────────────────────────
v2.0     ⬜  Weltkarte & Zones
```
