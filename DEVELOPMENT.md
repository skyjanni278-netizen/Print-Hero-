# DEVELOPMENT.md — Entwickler-Handbuch

Dieses Dokument richtet sich an Entwickler. Für den Überblick über Spielsysteme und
Projektstruktur siehe **README.md**, für den Entwicklungsplan **ROADMAP.md**, für die
Item-/Set-Referenz **ITEMS.md**.

---

## 1. Architektur & Spielfluss

```
main.py
  └─ load_meta() → hub_menu(meta) [systems/hub.py] → _new_run() / load_run()
  └─ _run_loop(player, meta):
       camp_menu(player, meta)     [ui/pause.py]   — [Q] kehrt zur Zuflucht zurück
         ├─ run_dungeon(player, meta)    [systems/dungeon.py]
         │    └─ combat(player, enemies)     [core/combat.py]
         │         └─ player.attack_target() [core/player.py]
         │         └─ collect_loot()         → roll_zone_loot() [content/loot.py]
         │         └─ apply_loot()           → player.inventory [core/player.py]
         │         └─ check_all()            [systems/achievements.py]
         │    └─ add_runenessenz(meta, 15–25) + save_run()  nach Abschluss
         └─ run_zone_boss(player, zone_id, meta) [systems/world_map.py]
              └─ combat() + roll_boss_loot() + add_runenessenz(meta, 50–80)
       Tod  → _handle_defeat(): Essenz bleibt, run_save gelöscht → Hub
       Sieg → victory_screen(): +200 Essenz, run_save gelöscht → Hub
```

### Kernklassen

**`Character` (core/player.py)**
- Basisklasse für Spieler UND Monster (Monster erben davon)
- Enthält: Stats, Inventar, Ausrüstung, Statuseffekte, Skill-Set, Cooldowns, Zonenfortschritt
- Serialisierung: `to_dict()` / `from_dict()` — wird direkt für JSON-Saves genutzt

**Monster (content/monsters.py)**
- Alle Monsterklassen erben von `Character`
- `_apply_rank(self, rank)` skaliert HP/ATK/Loot/XP per Rank-Config
- `boss_ability(self, player)` — eindeutige Fähigkeit, nur bei Rank 5 (~30 % Chance/Runde)

**`EQUIPMENT_DEFS` (content/items.py)**
- Zentrales Dict für alle Items: Name, Slot, ATK/DEF, Rarity, Set, Klassen-Restriktion, Passiv-Effekt

**`ZONE_DEFS` (systems/zones.py)**
- Dict mit Zone-ID → Gegnerpool, Min-Level, benötigte Dungeons für Boss-Unlock

---

## 2. Coding-Konventionen

| Konvention | Beispiel |
|-----------|---------|
| Funktionen | `snake_case` — `apply_armor_reduction()`, `roll_zone_loot()` |
| Klassen | `PascalCase` — `Character`, `StoneGolem`, `DarkKnight` |
| Konstanten / Dicts | `UPPER_CASE` — `ZONE_DEFS`, `RANK_CONFIG`, `MAX_INVENTORY_SLOTS` |
| Private Helfer | `_leading_underscore` — `_apply_rank()`, `_print_combat_screen()` |
| Kein raw `print()` | Immer `console.print()` mit Rich-Markup `[bold]`, `[red]`, `[cyan]` etc. |
| Kein `input()` in Logik-Modulen | Nur in `main.py` und `ui/` sowie `core/combat.py` — nie in `core/`-, `content/`-, `systems/`-Logik |
| Daten-getrieben | Spielinhalte stehen in Dicts/Listen, nicht als Objekte — `CLASS_DEFS`, `SEGNUNGEN_POOL` usw. |
| Kommentare | Nur Abschnitts-Divider und Constraint-Hinweise — keine Inline-Erklärungen |
| Keine Docstrings | Funktionsnamen sind selbstdokumentierend |
| Enum für Zonen | `Zone(str, Enum)` in config.py — immer `Zone.WALD` statt `"wald"` als String |

**Rich-Markup in user-facing Strings:** Benutzereingaben und dynamische Namen immer escapen,
sonst Darstellungsfehler bei `[` `]`:

```python
from rich.markup import escape as _esc
console.print(f"  {_esc(player.name)} hat gewonnen")
```

**Eingaben:** `input()` gibt immer einen String zurück — immer `.strip().lower()` vor der Auswertung.

---

## 3. Save-System & Kompatibilität

Zwei Dateien in `saves/`:
- **`meta_save.json`** — permanent (Runenessenz, Spiegel-Stand, Runen, Achievements, Lifetime-Stats)
- **`run_save.json`** — aktueller Run; bei Tod/Sieg gelöscht, bei Quit behalten

### Eiserne Regeln

- **Itemnamen in `EQUIPMENT_DEFS`/`CONSUMABLE_DEFS` sind Keys in gespeicherten Saves.**
  Umbenennen bricht alle vorhandenen Spielstände. Gleiches gilt für Segnung-IDs
  (`player.active_segnungen`), Spiegel-IDs (`meta["spiegel_state"]`) und Rune-IDs
  (`meta["unlocked_runen"]`).
- **Jedes neue Attribut auf `Character`** muss in `to_dict()` UND `from_dict()`
  (core/player.py) ergänzt werden — sonst geht es beim Laden verloren.
- **Neue Meta-Felder** in `_default_meta()` in `core/save.py` eintragen —
  `load_meta()` merged Defaults automatisch in alte Saves.
- **Runenessenz** IMMER über `add_runenessenz(meta, n)` gutschreiben und über
  `spend_runenessenz(meta, n)` ausgeben (beide speichern sofort) —
  nie `meta["runenessenz"]` direkt verändern.

---

## 4. System-Constraints

### Segnungen (systems/segnungen.py)
- Gelten nur für den laufenden Run, gespeichert als ID-Liste in `player.active_segnungen`.
- Hooks: `on_combat_start`, `on_kill`, `on_player_hit`, `seg_outgoing_damage`/`seg_dmg`,
  `check_vergeltung`, `check_zweite_chance`, `check_glut_burst` — aufgerufen aus `core/combat.py`.
  Passive Effekte (ATK/Regen/XP/Tränke/Krit) leben direkt in `core/player.py`
  per `in self.active_segnungen`-Check.
- Einmal-Stat-Segnungen (Zähigkeit+, Energiequell, Eisenhaut+) mutieren den Spieler direkt
  in `apply_segnung()` — nicht zusätzlich in Gettern verrechnen.
- Klassen-Segnungen haben `"class": "warrior"/"rogue"/"mage"`; Synergien sind
  Tuple-Keys in `SYNERGIEN`.

### Der Spiegel (systems/spiegel.py)
- `apply_spiegel_effects(player, meta)` läuft beim Run-Start (`main.py` `_new_run()`):
  kopiert den Meta-Stand als **Snapshot** nach `player.spiegel` (im run_save serialisiert)
  und wendet Einmal-Boni direkt an. Alle Kampf-/Loot-Hooks lesen `player.spiegel`,
  nie das Meta.
- Preisrabatt (Händlerglück B) läuft über `spiegel_price(player, price)` —
  bei neuen Händlern/Shops aufrufen (siehe `content/shop.py`, `systems/events.py`).
- Run-Flags: `spiegel_leben_used`, `spiegel_immun_effekt`, `spiegel_first_fight` —
  in `to_dict()`/`from_dict()` serialisiert.

### Runen (systems/runen.py)
- Drops IMMER über `check_rune_drop(meta, source, zone_id=None)` —
  Quellen: `"zone_boss"` 100 %/einmalig via `meta["boss_runen_dropped"]`,
  `"dungeon_boss"` 25 %, `"elite"` 5 %, `"chest"` 15 % — speichert sofort ins Meta.
- Schatztruhen-Drop braucht `meta`: `trigger_event(player, meta)` reicht es durch
  (Spezialfall im Dispatcher für `_treasure_chest`).
- Klassen-Varianten setzen `player.class_variant` (`"berserker"`/`"meuchler"`):
  Berserker blockt Schildwall in `core/combat.py` und filtert „Unerschütterlich" in
  `roll_segnung_choices()`; Meuchler überschreibt `try_flee()`.
- Startkit-/NPC-Flows laufen beim Run-Start in `main.py` `_new_run()`
  (Reihenfolge: Variante → Spiegel → Startkit → Essenz-Shop → Schmied-Flag).

### Kampf & Energie
- Passive Waffeneffekte sind **nur in `core/combat.py`** implementiert
  (`_apply_weapon_passive()`), nicht in `player.attack_target()`.
- Energie regeneriert `ENERGY_REGEN = 3` pro Runde (config.py). Fähigkeiten-Kosten
  stehen in `CLASS_ABILITY_DEFS` (content/classes.py); der Fokus-Skill (−5 Energie)
  wird beim Verbrauch in `combat.py` berücksichtigt.
- Maximale Energie immer über `get_effective_max_energy()` lesen —
  `max_energy` allein ignoriert Set-Boni.

### Klassenspezifische Waffen
- `CLASS_WEAPON_MAP` (content/items.py) übersetzt generische Katalognamen in
  klassenspezifische Varianten. Auflösung zur Laufzeit in `shop.py`
  (`_resolve_weapon`) — in `events.py` (Schwarzmarkt, Dungeon-Händler) manuell nachgezogen.
- Neue Kataloge brauchen keine klassenspezifischen Namen — nur die Auflösung beim
  Anzeigen und Kaufen.

### Zonenfortschritt
- Steckt in `player.zone_progress[zone_id]` als `{"dungeons_completed": N, "boss_defeated": bool}`.
- Zonenboss-Unlock: `dungeons_completed >= ZONE_DEFS[zone_id]["dungeon_count"]`
  UND vorherige Zone besiegt.
- Nach dem 5. Zonenboss: `check_all_zones_cleared()` → `victory_screen()` → Hub.

---

## 5. Erweiterungs-Rezepte

**Neues Monster**
1. Subklasse von `Character` in `content/monsters.py`; `super().__init__(name, hp, attack)`
   und danach `self._apply_rank(rank)` aufrufen.
2. In den Gegnerpool der Zone in `ZONE_DEFS` (systems/zones.py) eintragen —
   `create_zone_enemy()` ist die einzige Fabrik.
3. Optional `boss_ability(self, player)` für Rank-5-Verhalten.

**Neues Item / Set**
1. Eintrag in `EQUIPMENT_DEFS` (content/items.py) — Name = Save-ID, gut wählen.
2. Für Sets: Eintrag in `SET_DEFS` (content/sets.py) + Items dem Set zuordnen.
3. In Loot-Pools aufnehmen (`content/loot.py`) und ITEMS.md ergänzen.

**Neue Segnung**
1. Eintrag in `SEGNUNGEN_POOL` (systems/segnungen.py).
2. Effekt-Hook in einem bestehenden Hook ergänzen oder passiv in `core/player.py` prüfen.

**Neue Rune**
1. Eintrag in `RUNEN_DEFS` (systems/runen.py).
2. Effekt: Startkits in `apply_startkit()`, Varianten in `apply_klassen_variante()`,
   NPCs in `systems/hub.py` bzw. `main.py` `_new_run()`.

**Neues Spiegel-Upgrade**
1. Eintrag in `SPIEGEL_DEFS` (systems/spiegel.py) mit Varianten `"a"`/`"b"`.
2. Einmal-Boni in `apply_spiegel_effects()`, Kampf-/Preis-Hooks über `spiegel_active()`.

**Neues Achievement**
1. Eintrag in `ACHIEVEMENTS` (systems/achievements.py).
2. Trigger-Logik in `check_all()` ergänzen.

**Neues Event**
1. Funktion in `systems/events.py` + Eintrag in `_EVENTS` mit Gewicht.
2. Bei Händler-Events `spiegel_price()` anwenden; braucht das Event `meta`,
   im Dispatcher `trigger_event()` durchreichen (siehe `_treasure_chest`).
