# CLAUDE.md — Print-Hero

## ⚠️ Arbeitsumgebung — Sicherheitshinweis

Dieses Projekt läuft auf einem **Firmenlaptop ohne Admin-/Auth-Passwort**. Eine Sicherheitssoftware des Unternehmens ist aktiv und löst bei bestimmten Shell-Befehlen automatisch Warnungen aus.

**Verboten — löst Sicherheitssoftware aus:**
- `Invoke-RestMethod` oder `Invoke-WebRequest` mit API-Tokens in PowerShell
- `subprocess.run()` / `subprocess.Popen()` aus Python heraus
- `gh`-CLI für API-Operationen (Releases, Issues via Token)
- `curl` / `wget` / externe HTTP-Requests aus dem Terminal
- API-Keys oder Tokens direkt in Shell-Befehlen einbetten

**Erlaubt:**
- `git push`, `git tag`, `git commit`, `git status` — reine git-CLI-Befehle
- Dateioperationen über Read/Edit/Write/Glob/Grep-Tools (kein Shell-Umweg)
- `python -m py_compile` für Syntax-Checks
- GitHub-Releases und Tags ausschließlich über die **GitHub-Website** erstellen

---

## 1. Projektübersicht

**Print-Hero** ist ein terminal-basiertes Roguelike-RPG, vollständig in Deutsch. Der Spieler wählt eine von 3 Klassen (Krieger, Schurke, Magier), kämpft sich durch 5 aufeinanderfolgende Zonen, besiegt Zonenbosse und kann nach dem Durchlauf eine New-Game+-Runde starten.

- **Genre:** Roguelike RPG, rundenbasierter Kampf, persistente Fortschrittsspeicherung
- **Zielplattform:** Terminal (Windows/Linux/macOS), keine GUI, kein Browser
- **Sprache:** Durchgehend Deutsch (UI, Items, Beschreibungen, Variablennamen in config/content)

---

## 2. Stack & Technologien

| Was | Details |
|-----|---------|
| Sprache | Python 3.10+ (f-Strings, `:=` Walrus, `str.Enum`) |
| Externe Deps | `rich` — Terminal-Farben, Panels, Tabellen, HP-Balken (einzige Dependency) |
| Datenpersistenz | JSON-Dateien in `saves/savegame_{1-3}.json` |
| Keine Tests | Kein pytest, kein unittest — alles manuell |
| requirements.txt | `rich` (eine Zeile) |

---

## 3. Projektstruktur

```
Print-Hero-/
├── main.py                  Einstiegspunkt: Slot-Auswahl, Hauptschleife, Game-Over
├── config.py                Globale Konstanten: Schwierigkeit, Statuswerte, XP-Kurve
├── requirements.txt         Nur: rich
├── ITEMS.md                 Referenzdokument: alle Items/Sets/Waffen als Tabelle (v2.1)
│
├── core/
│   ├── player.py            Character-Klasse: Stats, Inventar, Abilities, Statuseffekte, Serialisierung
│   ├── combat.py            Kampfschleife, Ability-Ausführung, Loot-Vergabe
│   └── save.py              3-Slot-Speichersystem, JSON load/save, Legacy-Support
│
├── content/
│   ├── classes.py           3 Klassen-Definitionen (CLASS_DEFS) + choose_class(), apply_class()
│   ├── loot_tables.py       Alle Item-Definitionen, Set-Boni, Loot-Pools nach Zone, apply_loot()
│   ├── monsters.py          14 Monsterklassen (erben alle von Character), Rank-System, Boss-Abilities
│   └── shop.py              Händler-Katalog, Shop-Stock-Refresh, Kaufmenü
│
├── systems/
│   ├── zones.py             ZONE_DEFS: 5 Zonen mit Gegnerpools, Flavor-Text, Level-Anforderungen
│   ├── dungeon.py           Dungeon-Generierung (3-5 Räume), Raumtypen, Event-Dispatching
│   ├── world_map.py         Zonenfortschritt, Zonenboss-Kämpfe, Endscreen, NG+-Logik
│   ├── events.py            Zufalls-Events im Dungeon (Schwarzmarkt, Schrein, Falle usw.)
│   ├── achievements.py      20 Achievements in 5 Kategorien, check_all() nach jedem Kampf
│   └── skilltree.py         9 passive Skills in 3 Bäumen, Tier-Unlock-Logik
│
└── ui/
    ├── utils.py             Rich-Formatierung, HP/Energie-Balken, clear_screen(), print_header()
    └── pause.py             Camp-Menü (Haupthub), Inventar, Upgrade, Crafting, Verkauf, Stats
```

---

## 4. Aktueller Stand

### Vollständig implementiert ✅
- Komplette Kampfmechanik: Angriff, Rüstungsreduktion, Statuseffekte (Blutung/Gift/Verbrennung), Ausweichen, Blocken
- 3 Klassen mit je 4 Abilities und Cooldown-System
- 5 Zonen mit Zonenbossen, sequentiellem Freischalten, NG+-Skalierung
- 14 Monstertypen mit Rank-System (1–5), Boss-Abilities
- 12 Equipment-Sets mit 2/3/4-Teilboni und Spezialeffekten
- 4 passive Waffen (Giftklaue, Flammenklinge, Eisaxt, Runen-Kriegshammer)
- Zonen-basierte Loot-Pools (`ZONE_LOOT_POOL`) und garantierte Boss-Drops (`BOSS_LOOT_POOL`)
- Speichersystem: 3 Slots, JSON, Legacy-Kompatibilität
- 9 passive Skills im Skillbaum
- 20 Achievements
- Rich-UI durchgehend (Farben, Panels, Balken)
- Crafting, Verkauf, Upgrade, Shop

### Version
**v2.1 Stable**

### Bekannte Lücken / noch offen
- Kein Testsystem — nur manuelles Playtesting
- Keine Docstrings
- Shop-Preise nicht level-skaliert (flat costs)

---

## 5. Architektur & Zusammenhänge

```
main.py
  └─ _slot_menu() → load_game() / _new_game()
  └─ Hauptschleife:
       camp_menu(player)           [ui/pause.py]
         ├─ run_dungeon(player)    [systems/dungeon.py]
         │    └─ combat(player, enemies)     [core/combat.py]
         │         └─ player.attack_target() [core/player.py]
         │         └─ collect_loot()         → roll_zone_loot() [content/loot_tables.py]
         │         └─ apply_loot()           → player.inventory [core/player.py]
         │         └─ check_all()            [systems/achievements.py]
         └─ run_zone_boss(player) [systems/world_map.py]
              └─ combat() + roll_boss_loot()
```

### Kernklassen

**`Character` (core/player.py)**
- Basisklasse für Spieler UND Monster (Monster erben davon)
- Enthält: Stats, Inventar, Ausrüstung, Statuseffekte, Skill-Set, Cooldowns, Zonenfortschritt
- Serialisierung: `to_dict()` / `from_dict()` — wird direkt für JSON-Saves genutzt

**Monster (content/monsters.py)**
- Alle 14 Monsterklassen erben von `Character`
- `_apply_rank(self, rank)` skaliert HP/ATK/Loot/XP per Rank-Config
- `boss_ability(self, player)` — eindeutige Fähigkeit, nur bei Rank 5 (~30% Chance/Runde)

**`EQUIPMENT_DEFS` (content/loot_tables.py)**
- Zentrales Dict für alle Items: Name, Slot, ATK/DEF, Rarity, Set, Klassen-Restriktion, Passiv-Effekt
- **Namensänderungen hier brechen gespeicherte Saves** — Itemnamen sind die IDs

**`ZONE_DEFS` (systems/zones.py)**
- Dict mit Zone-ID → Gegnerpool, Min-Level, benötigte abgeschlossene Dungeons für Boss-Unlock

---

## 6. Coding-Stil

| Konvention | Beispiel |
|-----------|---------|
| Funktionen | `snake_case` — `apply_armor_reduction()`, `roll_zone_loot()` |
| Klassen | `PascalCase` — `Character`, `StoneGolem`, `DarkKnight` |
| Konstanten / Dicts | `UPPER_CASE` — `ZONE_DEFS`, `RANK_CONFIG`, `MAX_INVENTORY_SLOTS` |
| Private Helfer | `_leading_underscore` — `_apply_rank()`, `_print_combat_screen()` |
| Kein raw `print()` | Immer `console.print()` mit Rich-Markup `[bold]`, `[red]`, `[cyan]` etc. |
| Kein `input()` in Modulen | Nur in `main.py`, `ui/pause.py`, `core/combat.py` — nie in `core/` Logik-Dateien |
| Daten-getrieben | Spielinhalte stehen in Dicts/Listen, nicht als Objekte — `CLASS_DEFS`, `LOOT_TABLES` usw. |
| Kommentare | Nur Abschnitts-Divider: `# ── Skill-Tree ───────────────` — keine Inline-Erklärungen |
| Keine Docstrings | Gar keine — Funktionsnamen sind selbstdokumentierend |
| Enum für Zonen | `Zone(str, Enum)` in config.py — immer `Zone.WALD` statt `"wald"` als String |

**Wichtig bei Rich-Ausgaben:** Benutzereingaben (Namen, Item-Namen) immer mit `escape()` bzw. `_esc()` wrappen bevor sie in Rich-Markup eingebettet werden — sonst Darstellungsfehler bei `[` `]`.

---

## 7. Offene Aufgaben / Nächste Schritte

### v2.1 — abgeschlossen ✅
- [x] Klassenspezifische Waffennamen in Shop, Shop-Unlock-Vorschau und Schwarzmarkt
- [x] Shop zeigt Set-Zugehörigkeit pro Item
- [x] Wandernder Händler: mehrere Käufe möglich, Stack-Stand sichtbar
- [x] Lagerfeuer- & Inventar-Menü: Ausrüstungsanzeige mit Rarity/Set/Upgrade pro Zeile
- [x] NG+: `zones_cleared` + `dungeons_completed` werden beim Reset korrekt zurückgesetzt
- [x] NG+-Skalierung auf max. ×3,0 begrenzt (war unbegrenzt ×1,3^n)
- [x] Schwarzmarkt: `CLASS_WEAPON_MAP` wird bei Kauf und Anzeige angewendet
- [x] Architektur-Refactoring: `to_dict()`/`from_dict()`, `check_level_up()` returns list, `Zone`-Enum, `XP_MULTIPLIERS` in config

### v2.2 — Potentielle Erweiterungen (nicht geplant, aber architektonisch vorbereitet)
- Weitere Passive Waffen (Slot bereits in `EQUIPMENT_DEFS` vorhanden)
- Neue Monster via Subklasse von `Character` + Eintrag in `ZONE_DEFS`
- Neue Achievements: Eintrag in `ACHIEVEMENT_DEFS` + Trigger-Logik in `check_all()`
- Weiteres Set: Eintrag in `SET_DEFS` + Items in `EQUIPMENT_DEFS`
- Shop-Preise level-abhängig skalieren

---

## 8. Wichtige Hinweise — Was du beachten musst

### Save-Kompatibilität
- **Itemnamen in `EQUIPMENT_DEFS` sind Keys in gespeicherten JSON-Saves.** Umbenennen bricht alle vorhandenen Saves.
- `Character.to_dict()` / `from_dict()` in `core/player.py` muss bei jedem neuen Attribut auf der `Character`-Klasse erweitert werden — sonst gehen neue Felder beim Laden verloren.
- Das Legacy-Save-Format (alter Einzeldatei-Pfad) wird in `save.py` noch unterstützt.

### Monster-Erstellung
- Alle neuen Monster erben von `Character` und rufen `super().__init__(name, hp, attack)` und dann `self._apply_rank(rank)` auf.
- `create_zone_enemy(zone_id, rank)` in `systems/zones.py` ist die einzige Fabrik — neue Monster müssen dort in den Gegnerpool eingetragen werden.

### Klassenspezifische Waffen (shop.py / events.py)
- **`CLASS_WEAPON_MAP`** in `content/loot_tables.py` übersetzt generische Katalognamen (z.B. `"Kurzschwert"`) in klassenspezifische Varianten (`"Spitzdolch"` für Schurke, `"Novizenstab"` für Magier).
- Auflösung erfolgt in `shop.py` via `_resolve_weapon(item_key, player_class)` — sowohl für Anzeige als auch Kauf.
- Dasselbe muss in `events.py` (`_schwarzmarkt`) manuell nachgezogen werden, da der Schwarzmarkt keinen `shop_menu`-Flow nutzt.
- Neue Waffenkataloge (Shop, Schwarzmarkt) müssen keine klassenspezifischen Namen enthalten — die Auflösung passiert zur Laufzeit.

### Passive Waffen (combat.py)
- Passive Waffeneffekte sind **nur in `core/combat.py`** implementiert, nicht in `player.attack_target()`.
- Der Passiv-Check läuft nach dem Normalangriff, bevor Gegner angreift. Neue Passiveffekte müssen in `combat.py` in `_apply_weapon_passives()` (oder äquivalentem Block) eingetragen werden.

### Energie-System
- Energie regeneriert automatisch `ENERGY_REGEN = 3` pro Runde (in `config.py`).
- Fähigkeiten-Energie-Kosten werden in `CLASS_DEFS` (content/classes.py) definiert — der Ability-Dispatcher in `combat.py` liest diese Werte.
- Der Fokus-Skill (`-5 Energiekosten`) wird in `combat.py` beim Ability-Verbrauch berücksichtigt.

### Zonenfortschritt
- Der Fortschritt steckt in `player.zone_progress[zone_id]` als Dict `{"dungeons_completed": N, "boss_defeated": bool}`.
- Zonenboss-Unlock: `dungeons_completed >= ZONE_DEFS[zone_id]["dungeons_required"]` UND vorherige Zone boss besiegt.
- Nach dem 5. Zonenboss: `check_all_zones_cleared()` → Endscreen → NG+ oder freies Erkunden.

### Rich-Markup in user-facing Strings
```python
from rich.markup import escape as _esc
console.print(f"  {_esc(player.name)} hat gewonnen")  # IMMER escapen!
```

### Eingaben
- `input()` gibt immer einen String zurück — immer `.strip().lower()` bevor du ihn auswertest.
- Kein `input()` in Logik-Modulen (`core/`, `content/`, `systems/`) — nur in `main.py` und `ui/`.