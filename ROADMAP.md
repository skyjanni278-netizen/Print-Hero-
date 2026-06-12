# ROADMAP.md — Print-Hero

Geplante Weiterentwicklung. Erledigte Punkte wandern ins README-Changelog,
abgeschlossene Roadmap-Abschnitte werden hier entfernt (Historie bleibt im Git-Verlauf).

---

## Richtungsentscheidung (2026-06-12)

Frage: weiter Content, oder raus aus dem Terminal in eine Game-Engine / GUI?

**Befund:** Print-Hero ist inhaltlich nahezu fertig (~7.000 Zeilen, sauber getrennt in
`core / content / systems / ui`), aber die **Präsentation ist tief mit der Spiellogik
verwoben** — **857 direkte UI-Aufrufe** (`console.print` / `input()` / `clear_screen`),
davon mitten in der Logik: `events.py` 228, `combat.py` 117, `dungeon.py` 109.

**Konsequenz:** Ein Wechsel auf eine Game-Engine (Pygame/Godot) wäre für ein menü- und
textgetriebenes RPG das falsche Werkzeug *und* ein kompletter Rewrite der Steuerungs-
schicht (blockierendes `input()` vs. Frame-/Event-Loop). Pygame/Godot = schlechtestes
Aufwand/Wirkung-Verhältnis.

**Beschlossene Richtung:** Zuerst **UI von Logik entkoppeln**. Das macht den Code testbar
*und* ist die Vorbedingung für jede spätere Oberfläche. Falls je grafisch, dann
**Textual** (TUI auf dem bestehenden `rich`-Stack, kleinster Sprung) oder **Web**
(Python-Backend + HTML/CSS-Frontend) — nicht Pygame/Godot.

Teil-Entkopplung ist bereits vorhanden und bestätigt die Machbarkeit:
`core/abilities.py`, `player.attack_target()` und die Segnungs-/Spiegel-Hooks geben
bereits **Daten zurück** (`(msg, dmg)`-Tupel, Message-Listen) statt selbst zu drucken.

---

## Stufe 1 — Zentrale I/O-Schicht  *(als Nächstes)*

Jeder `console.print` / `input()` / `clear_screen` läuft künftig über ein austauschbares
Backend in `ui/io.py`:

```python
out("...")           # statt console.print(...)
ask("Deine Wahl: ")  # statt input(...)
pause()              # statt input("  ENTER...")
clear()              # statt clear_screen()
```

Backends:
- **TerminalIO** — heutiges Verhalten, 1:1 (risikoarme, rein mechanische Ersetzung)
- **CaptureIO** — sammelt Ausgaben, speist Eingaben aus einer Liste → **macht den Kampf
  automatisiert testbar** (heute unmöglich)
- **Späteres Backend** (Textual/Web) klinkt sich hier ein, ohne die Spiellogik anzufassen

### Schritte (je eigener Commit + Smoke-Test: Spiel startet, ein Run läuft)

| Version | Schritt |
|---------|---------|
| **v3.4.0** | `ui/io.py` anlegen: `IO`-Protokoll + `TerminalIO` + `CaptureIO`, globale `out/ask/pause/clear`. `ui/utils.py` darauf umstellen. **Null Verhaltensänderung.** |
| v3.4.1 | `core/combat.py` migrieren (größter Brocken, 117 Aufrufe) |
| v3.4.2 | `systems/events.py` (228 Aufrufe) |
| v3.4.3 | `systems/dungeon.py` + `systems/world_map.py` |
| v3.4.4 | `ui/pause.py`, `ui/*`, restliche `systems/` + `content/shop.py` |
| v3.5.0 | `DEVELOPMENT.md`-Regel umschreiben (kein direktes `console.print`/`input()` mehr in Logik) + erster echter **Kampf-Test mit CaptureIO** als Beweis der Entkopplung |

**Bewusste Abgrenzung:** Stufe 1 nutzt weiter *blockierendes* `ask()`. Das trägt für
Terminal, Textual und Tests. Ein echtes **Web-Frontend** bräuchte zusätzlich ein
async/Request-Modell — dieser Schritt wird erst gemacht, wenn er gebraucht wird.

---

## Stufe 2 — Reine State-Trennung  *(Fernziel, nur bei echter GUI)*

Spiellogik gibt strukturierte Events/Zustände zurück; eine eigene Render-Schicht zeichnet
sie. Sauber für eine GUI mit Event-Loop, aber großer Umbau. **Erst sinnvoll, wenn Stufe 1
steht** — und nur, wenn Print-Hero wirklich grafisch wird.

---

## Content-Ideen  *(parallel jederzeit möglich, höchster Spielwert pro Aufwand)*

- **4. Klasse** (z. B. Paladin/Druide) — multipliziert sich mit Sets, Runen, Skilltree
- **Zone 6 / Endgame-Schleife** — nach Malachar gibt es aktuell nur den Victory-Screen;
  ein „Verdammt-Modus" o. Ä. gäbe Wiederspielwert
- **Mehr Synergien & Build-Definers** — der eigentliche Suchtfaktor eines Roguelites
