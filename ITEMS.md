# 📦 Print-Hero — Item-Referenz

> Vollständige Übersicht aller Items, Sets und Waffen.
> Quelle: `content/items.py`, `content/sets.py`, `content/loot.py` — **Stand: v3.1**

⚠️ **Itemnamen sind Save-Keys.** Eine Umbenennung in `EQUIPMENT_DEFS` bricht alle gespeicherten Spielstände.

---

## 🧪 Verbrauchsgegenstände (`CONSUMABLE_DEFS`)

| Item | Effekt | Wert | Max. Stack | Verkauf |
|------|--------|:----:|:----------:|:-------:|
| 🧪 Healing Potion | Heilung | 10 HP | 5 | 7 |
| 🍶 Großes Heiltrank | Heilung | 25 HP | 5 | 17 |
| ✨ Elixier | Heilung | 40 HP | 3 | 30 |
| 🪶 Phönixfeder | Heilung + Cleanse | 15 HP | 3 | 40 |
| 💎 Energie-Kristall | Energie | +15 | 5 | 12 |
| 💪 Stärketrank | ATK (1 Kampf) | +3 | 3 | 20 |
| 🌿 Antidot | Cleanse (Blutung & Gift) | — | 5 | 5 |

---

## 🗑️ Schrott (`JUNK_DEFS`)

| Item | Verkauf | Crafting-Material für |
|------|:-------:|----------------------|
| 🪢 Altes Seil | 3 | — |
| 🧣 Lumpen | 2 | Healing Potion |
| 🦴 Knochen | 4 | Antidot |
| 🟢 Schleimklumpen | 5 | Energie-Kristall |
| 🦷 Goblinzahn | 6 | Stärketrank |
| 🐾 Trollfell | 8 | Stärketrank |
| 🐺 Wolfspelz | 7 | Healing Potion |
| 🏴 Banditen-Abzeichen | 9 | — |

### Rezepte (`CRAFT_RECIPES`)

| Output | Materialien |
|--------|-------------|
| 1× Antidot | 3× Knochen |
| 1× Stärketrank | 2× Trollfell + 1× Goblinzahn |
| 1× Energie-Kristall | 3× Schleimklumpen |
| 1× Healing Potion | 2× Wolfspelz + 1× Lumpen |

---

## ⚔️ Waffen (generisch)

| Waffe | ATK | Rarity | Verkauf |
|-------|:---:|--------|:-------:|
| 🗡️ Kurzschwert | 3 | Gewöhnlich | 20 |
| ⚔️ Langschwert | 6 | Ungewöhnlich | 40 |
| 🔨 Kriegshammer | 9 | Ungewöhnlich | 60 |
| ⚡ Sturmklinge | 11 | Selten | 90 |
| 🌀 Runenschwert | 13 | Selten | 100 |
| 💀 Knochensense | 15 | Episch | 145 |
| 🐉 Drachenzahn | 17 | Episch | 160 |
| ✨ Göttliche Klinge | 25 | Legendär | 350 |

### Mythic-Items (v3.1 — Zone 5, sehr seltene Einzeldrops)

| Item | Slot | Stat | Effekt | Verkauf |
|------|------|:----:|--------|:-------:|
| 🔱 Götterspeer | Waffe | ATK 28 | Gegner unter 30 % HP: immer kritisch | 600 |
| 🪬 Seelenpanzer | Rüstung | DEF 22 | Absorbiert den ersten Angriff jedes Kampfes | 580 |
| 👑 Krone der Götter | Helm | DEF 16 | +15 % XP solange getragen | 550 |

### Passive Waffen

| Waffe | ATK | Rarity | Passiv | Chance |
|-------|:---:|--------|--------|:------:|
| ☠️ Giftklaue | 5 | Ungewöhnlich | +1 Giftstack | 100 % |
| 🔥 Flammenklinge | 8 | Selten | +2 Verbrennungsstacks | 25 % |
| ❄️ Eisaxt | 10 | Selten | Ziel eingefroren (1 Runde) | 20 % |
| 🔨 Runen-Kriegshammer | 12 | Selten | −3 DEF-Debuff | 30 % |

> Passiveffekte werden in `core/combat.py` (`_apply_weapon_passive`) ausgelöst — nach Normalangriffen
> und physischen Abilities (Krieger S/C, Schurke R), nicht bei Magier-Zaubern.

### Klassenspezifische Waffennamen (`CLASS_WEAPON_MAP`)

Gleiche Stats, klassenspezifischer Name. Auflösung zur Laufzeit (Shop, Schwarzmarkt, Loot).

| Generisch | ⚔️ Krieger | 🗡️ Schurke | 🔮 Magier |
|-----------|-----------|------------|-----------|
| Kurzschwert | Kampfschwert | Spitzdolch | Novizenstab |
| Langschwert | Bastardschwert | Klingenschatten | Magierstab |
| Kriegshammer | Streitaxt | Schattenbeil | Arkane Keule |
| Sturmklinge | Gewitterschwert | Blitzdolch | Sturmstab |
| Runenschwert | Runenklinge | Runendolch | Runenstab |
| Knochensense | Kriegssense | Seelenstehler | Totenstab |
| Drachenzahn | Drachenklaue | Drachenstich | Drachenstab |
| Göttliche Klinge | Heilige Klinge | Klingengeist | Götterstab |

---

## 🛡️ Rüstungen, Helme, Schuhe

| Rüstung (chest) | DEF | Rarity | | Helm (head) | DEF | Rarity | | Schuhe (feet) | DEF | Rarity |
|------|:---:|--------|-|------|:---:|--------|-|------|:---:|--------|
| Lederrüstung | 2 | Gewöhnlich | | Lederkappe | 1 | Gewöhnlich | | Lederstiefel | 1 | Gewöhnlich |
| Kettenhemd | 4 | Ungewöhnlich | | Eisenhelm | 2 | Gewöhnlich | | Eisenstiefel | 2 | Gewöhnlich |
| Plattenpanzer | 7 | Ungewöhnlich | | Stahlhelm | 4 | Ungewöhnlich | | Kriegsstiefel | 3 | Ungewöhnlich |
| Runenrüstung | 10 | Selten | | Runenhelm | 6 | Selten | | Schnellläuferstiefel | 4 | Ungewöhnlich |
| Drachenschuppen | 14 | Episch | | Drachenkrone | 9 | Episch | | Runenstiefel | 6 | Selten |
| Rüstung des Lichts | 20 | Legendär | | Krone des Ewigen | 13 | Legendär | | Drachenklauen | 9 | Episch |
| | | | | | | | | Stiefel der Ewigkeit | 12 | Legendär |

---

## 🎽 Sets (`SET_DEFS`) — 16 Sets

Boni gelten ab 2 angelegten Teilen. Klassenvarianten von Waffen zählen über `WEAPON_VARIANT_TO_BASE` als Basiswaffe.

### Neutrale Sets

| Set | Teile (Waffe / Rüstung / Helm / Schuhe) | 4er-Bonus | Special |
|-----|------------------------------------------|-----------|---------|
| 🥋 Leder-Set | Kurzschwert / Lederrüstung / Lederkappe / Lederstiefel | +4 DEF +3 ATK | `leder_dodge` — 10 % Ausweichen |
| ⛓️ Eisen-Set | Langschwert / Kettenhemd / Eisenhelm / Eisenstiefel | +6 DEF +4 ATK | `eisen_energy_regen` — +3 Energie/Runde |
| 🔩 Stahl-Set | Kriegshammer / Plattenpanzer / Stahlhelm / Schnellläuferstiefel | +8 DEF +6 ATK | `stahl_bleed_immune` — Blutungsimmunität |
| 🌑 Schatten-Set | Schattendolch / Schattenrüstung / Schattenhelm / Schattenstiefel | +8 DEF +8 ATK | `schatten_crit` — +15 % Krit |
| 🌀 Runen-Set | Runenschwert / Runenrüstung / Runenhelm / Runenstiefel | +12 DEF +8 ATK | `runen_xp_bonus` — +20 % XP |
| 🐉 Drachen-Set | Drachenzahn / Drachenschuppen / Drachenkrone / Drachenklauen | +15 DEF +12 ATK | `drachen_block` — 15 % Block |
| ✨ Licht-Set | Göttliche Klinge / Rüstung des Lichts / Krone des Ewigen / Stiefel der Ewigkeit | +20 DEF +18 ATK | `licht_hp_regen` — +3 HP/Runde |
| 🛡️ Runen-Panzer | Panzerklinge / Runen-Platte / Runen-Visier / Runen-Schritte | +8 DEF +5 ATK | `panzer_bleed_reduce` — Blutung −1/Stack |
| 🌙 Schattentuch | Mondklinge / Schattengewand / Schattenkapuze / Schattensandale | −3 DEF +2 ATK | `schattentuch_dodge` — 15 % Ausweichen |
| 🐉 Drachenschuppen | Schuppenklinge / Schuppenpanzer / Schuppenhelm / Schuppenstiefel | +12 DEF +8 ATK | `schuppen_block` — 20 % Block |
| 💀 Verdammten-Stahl | Verdammte Klinge / Verdammte Rüstung / Verdammter Helm / Verdammte Stiefel | +6 ATK −4 DEF | — |
| ⚰️ Totenritter | Totenklinge / Totenrüstung / Totenschädel / Totenstiefel | +10 DEF +8 ATK | `totenritter_berserker` — bei ≤25 % HP: +50 % ATK, +20 % Ausweichen |
| 🕳️ Abyssal-Set | Abyssalklinge / Abyssalrobe / Abyssalhelm / Abyssalsohlen | +16 DEF +12 ATK | `abyssal_thorns` — 30 % des erlittenen Schadens als Rückstoß an alle Gegner |

### Klassen-Sets (`class_only`)

| Set | Klasse | Teile | 4er-Bonus | Special |
|-----|--------|-------|-----------|---------|
| 🏰 Eisenfestung | Krieger | Festungsklinge / Festungsplatte / Festungshelm / Festungsstiefel | +10 DEF +5 ATK | `warrior_2block` — Schildwall blockt 2× |
| 🌙 Schattenhülle | Schurke | Hüllendolch / Hüllenpanzer / Hüllenmaske / Hüllenstiefel | +8 DEF +5 ATK | `rogue_shadow_regen` — Aus dem Schatten: +15 % Krit |
| 🔮 Arkane Roben | Magier | Arkaner Stab / Arkane Robe / Arkane Kapuze / Arkane Schuhe | +8 DEF +4 ATK +20 Energie | `mage_double_arcane` — Arkane Entladung trifft 2× |

### Set-Teil-Stats

| Set | Waffe (ATK) | Rüstung (DEF) | Helm (DEF) | Schuhe (DEF) | Rarity |
|-----|:-----------:|:-------------:|:----------:|:------------:|--------|
| Schatten-Set | 7 | 8 | 5 | 3 | Ungew./Selten |
| Runen-Panzer | 9 | 8 | 4 | 3 | Selten |
| Schattentuch | 7 | 5 | 2 | 1 | Selten |
| Drachenschuppen | 14 | 12 | 7 | 5 | Episch |
| Verdammten-Stahl | 18 | 12 | 7 | 5 | Episch |
| Eisenfestung | 15 | 12 | 8 | 7 | Episch |
| Schattenhülle | 14 | 11 | 7 | 6 | Episch |
| Arkane Roben | 13 | 10 | 6 | 5 | Episch |
| Totenritter | 16 | 14 | 9 | 7 | Episch |
| Abyssal-Set | 22 | 18 | 12 | 10 | Legendär |

---

## 🗺️ Drop-Quellen

### Zonen-Loot (`ZONE_LOOT_POOL`) — Schwerpunkte

Seit v3.1 folgt der Loot der **Fünf-Zonen-Rarity-Kurve**: Wald = Common, Ruinen = Uncommon,
Wüste = Rare (+ einzelne Klassen-Set-Teile), Vulkan = Epic (+ Legendary selten),
Dunkel-Reich = Legendary (+ Mythic sehr selten).

| Zone | Equipment-Schwerpunkt | Passive Waffe |
|------|----------------------|---------------|
| 🌲 Wald | Leder-/Eisen-Teile, Kurzschwert | Giftklaue |
| 🏚️ Ruinen | Stahl-Teile, Schattendolch, Runen-Panzer-Set (selten) | Eisaxt, Runen-Kriegshammer |
| 🏜️ Wüste | Runen-Set, Schatten-Teile, Schattentuch-Set, Klassen-Sets: Waffe + Schuhe (sehr selten) | Flammenklinge |
| 🌋 Vulkan | Drachen-Set, Drachenschuppen-Set, Totenritter-Set, Klassen-Sets: Rüstung + Helm, Licht-Teile (selten) | — |
| 💀 Dunkel-Reich | Licht-Set, Abyssal-Set, Verdammten-Stahl, Totenritter, Mythic-Items (sehr selten) | — |

### Zonen-Boss-Drops (`BOSS_LOOT_POOL`) — 2 garantierte Teile + Gold

| Zonen-Boss | Pool |
|------------|------|
| Wald | Stahl-Set-Teile + Runen-Panzer-Teile |
| Ruinen | Runen-Set-Teile + Schattentuch-Teile |
| Wüste | Drachen-Set-Teile + Drachenschuppen-Teile |
| Vulkan | Verdammten-Stahl-Teile + Totenritter-Teile |
| Dunkel-Reich | Licht-Set-Teile + Abyssal-Teile |

### Rang-Loot (`RANK_LOOT_WEIGHTS`) — für Events/Truhen (`roll_loot`)

| Rang | Common | Uncommon | Rare | Epic | Legendary |
|:----:|:------:|:--------:|:----:|:----:|:---------:|
| 1 | 80 | 18 | 2 | 0 | 0 |
| 2 | 65 | 28 | 7 | 0 | 0 |
| 3 | 48 | 35 | 15 | 2 | 0 |
| 4 | 25 | 33 | 33 | 9 | 0 |
| 5 | 8 | 17 | 33 | 33 | 9 |

---

## ⬆️ Upgrades

- Max. Stufe 3 pro Item, Kosten: 50 / 120 / 250 Gold (`ui/pause.py`)
- Waffe: +2 ATK pro Stufe, Rüstungsteile: +1 DEF pro Stufe
- Seit v2.3 wird das Upgrade-Level am Item gespeichert (`"upgrade": N` im Item-Dict) und bleibt beim Ablegen erhalten
- Starter-Items (Fäuste, Lumpen, Kein Helm, Keine Schuhe) sind nicht aufwertbar und nicht verkaufbar
