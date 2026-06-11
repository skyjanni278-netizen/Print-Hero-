import random
from rich.markup import escape as _esc
from config import BURN_DAMAGE

# ── Segnung-Pool (gilt nur für den laufenden Run) ─────────────────────────────

SEGNUNGEN_POOL = {
    "blutdurst":        {"name": "Blutdurst",         "emoji": "🩸", "class": None,
                         "desc": "Kills heilen 3 HP."},
    "finstere_klinge":  {"name": "Finstere Klinge",   "emoji": "🗡️", "class": None,
                         "desc": "10% Chance: Dein Angriff wiederholt sich kostenlos."},
    "lebensraub":       {"name": "Lebensraub",        "emoji": "💀", "class": None,
                         "desc": "Gegner unter 20% HP nehmen 2× Schaden."},
    "raserei":          {"name": "Raserei",           "emoji": "🔥", "class": None,
                         "desc": "Nach 3 Kills: Dein nächster Angriff trifft alle Gegner."},
    "eisige_praesenz":  {"name": "Eisige Präsenz",    "emoji": "❄️", "class": None,
                         "desc": "Kampfbeginn: Alle Gegner sind 1 Runde betäubt."},
    "seelenernte":      {"name": "Seelenernte",       "emoji": "⚡", "class": None,
                         "desc": "Kritischer Treffer: sofort +8 Energie."},
    "giftmeister":      {"name": "Giftmeister",       "emoji": "☠️", "class": None,
                         "desc": "Giftstacks auf Gegnern lösen sich bis Kampfende nicht auf."},
    "glut_entfesselung":{"name": "Glut-Entfesselung", "emoji": "💥", "class": None,
                         "desc": "Läuft eine Verbrennung ab: einmaliger 3×-Schadens-Burst."},
    "schattenform":     {"name": "Schattenform",      "emoji": "🌑", "class": None,
                         "desc": "Erste Runde jedes Kampfes: 100% Ausweichen."},
    "vergeltung":       {"name": "Vergeltung",        "emoji": "⚖️", "class": None,
                         "desc": "Erlittener Statuseffekt: 50% Chance, dass der Angreifer ihn auch bekommt."},
    "letzter_wille":    {"name": "Letzter Wille",     "emoji": "💪", "class": None,
                         "desc": "Bei ≤10% HP: +30% ATK."},
    "eisenhaut_plus":   {"name": "Eisenhaut+",        "emoji": "🛡️", "class": None,
                         "desc": "+5 DEF für diesen Run."},
    "zaehigkeit_plus":  {"name": "Zähigkeit+",        "emoji": "❤️", "class": None,
                         "desc": "+15 max HP für diesen Run."},
    "goldgier":         {"name": "Goldgier",          "emoji": "💰", "class": None,
                         "desc": "+25% Gold aus Beute."},
    "kopfgeld":         {"name": "Kopfgeld",          "emoji": "🪙", "class": None,
                         "desc": "+3 Gold pro Kill."},
    "adlerauge":        {"name": "Adlerauge",         "emoji": "🎯", "class": None,
                         "desc": "+10% Krit-Chance."},
    "vampirseele":      {"name": "Vampirseele",       "emoji": "🦇", "class": None,
                         "desc": "Kritische Treffer heilen 4 HP."},
    "energiequell":     {"name": "Energiequell",      "emoji": "🔋", "class": None,
                         "desc": "+10 max Energie für diesen Run."},
    "fluss_der_kraft":  {"name": "Fluss der Kraft",   "emoji": "🌊", "class": None,
                         "desc": "+2 Energie-Regeneration pro Runde."},
    "dornenhaut":       {"name": "Dornenhaut",        "emoji": "🌵", "class": None,
                         "desc": "Angreifer nehmen 2 Rückstoß-Schaden."},
    "trankmeister":     {"name": "Trankmeister",      "emoji": "🧪", "class": None,
                         "desc": "Heiltränke heilen +50%."},
    "schlachtruf":      {"name": "Schlachtruf",       "emoji": "📯", "class": None,
                         "desc": "Erster normaler Angriff jedes Kampfes: +50% Schaden."},
    "giftblut":         {"name": "Giftblut",          "emoji": "🧬", "class": None,
                         "desc": "25% Chance: Angreifer erhält 1 Giftstack."},
    "eiserner_wille":   {"name": "Eiserner Wille",    "emoji": "🧠", "class": None,
                         "desc": "50% Chance, Betäubung zu widerstehen."},
    "weise_seele":      {"name": "Weise Seele",       "emoji": "📜", "class": None,
                         "desc": "+15% XP aus Kämpfen."},
    "henker":           {"name": "Henker",            "emoji": "🪓", "class": None,
                         "desc": "+3 Schaden gegen Gegner mit Statuseffekt."},
    "zweite_chance":    {"name": "Zweite Chance",     "emoji": "🕊️", "class": None,
                         "desc": "1× pro Run: Ein tödlicher Treffer lässt dich mit 1 HP überleben."},
    "schatten_reflex":  {"name": "Schatten-Reflex",   "emoji": "🗡️", "class": "rogue",
                         "desc": "Kill: Aus dem Schatten ist sofort kostenlos wieder bereit."},
    "arkane_ueberladung":{"name": "Arkane Überladung","emoji": "✨", "class": "mage",
                         "desc": "Arkane Entladung: 3 zusätzliche Treffer auf zufällige Gegner."},
    "unerschuetterlich":{"name": "Unerschütterlich",  "emoji": "🛡️", "class": "warrior",
                         "desc": "Kampfbeginn: Schildwall blockt automatisch den ersten Angriff."},
}

SYNERGIEN = {
    ("giftmeister", "lebensraub"):       {"name": "Toxischer Ruin",
                                          "desc": "Vergiftete Gegner unter 20% HP nehmen 3× Schaden."},
    ("blutdurst", "raserei"):            {"name": "Blutrausch",
                                          "desc": "Kills heilen 6 HP statt 3."},
    ("eisige_praesenz", "seelenernte"):  {"name": "Frosternte",
                                          "desc": "Kill an einem betäubten Gegner: +15 Energie."},
}


# ── Auswahl & Verwaltung ──────────────────────────────────────────────────────

def seg_active(player, sid: str) -> bool:
    return sid in getattr(player, "active_segnungen", [])


def synergy_active(player, a: str, b: str) -> bool:
    segs = getattr(player, "active_segnungen", [])
    return a in segs and b in segs


def get_active_synergien(player) -> list:
    return [(pair, sdef) for pair, sdef in SYNERGIEN.items()
            if synergy_active(player, pair[0], pair[1])]


def roll_segnung_choices(player, n: int = 3) -> list:
    owned = set(getattr(player, "active_segnungen", []))
    pool  = [sid for sid, d in SEGNUNGEN_POOL.items()
             if sid not in owned and (d["class"] is None or d["class"] == player.player_class)]
    if getattr(player, "class_variant", None) == "berserker":
        pool = [sid for sid in pool if sid != "unerschuetterlich"]
    random.shuffle(pool)
    return pool[:n]


def apply_segnung(player, sid: str) -> list:
    d = SEGNUNGEN_POOL[sid]
    player.active_segnungen.append(sid)
    msgs = [f"{d['emoji']} [bold]{_esc(d['name'])}[/bold] erhalten — [dim]{_esc(d['desc'])}[/dim]"]

    if sid == "zaehigkeit_plus":
        player.max_hp += 15
        player.hp     += 15
        msgs.append(f"[green]❤️  +15 max HP! (HP: {player.hp}/{player.max_hp})[/green]")
    elif sid == "energiequell":
        player.max_energy += 10
        msgs.append(f"[blue]🔋 +10 max Energie! (Max: {player.get_effective_max_energy()})[/blue]")
    elif sid == "eisenhaut_plus":
        player.armor += 5
        msgs.append(f"[yellow]🛡️  +5 DEF! (DEF: {player.get_total_armor()})[/yellow]")

    for pair, sdef in SYNERGIEN.items():
        if sid in pair:
            other = pair[0] if pair[1] == sid else pair[1]
            if other in player.active_segnungen and other != sid:
                msgs.append(f"[bold cyan]🔗 Synergie freigeschaltet: {_esc(sdef['name'])} — {_esc(sdef['desc'])}[/bold cyan]")
    return msgs


# ── Kampf-Hooks ───────────────────────────────────────────────────────────────

def on_combat_start(player, enemy_list) -> list:
    msgs = []
    segs = player.active_segnungen
    if "eisige_praesenz" in segs:
        for e in enemy_list:
            e.stunned = True
        msgs.append("❄️  Eisige Präsenz: Alle Gegner sind 1 Runde betäubt!")
    if "unerschuetterlich" in segs:
        player.block_next    = True
        player.block_charges = max(player.block_charges, 1)
        msgs.append("🛡️  Unerschütterlich: Der erste Angriff wird automatisch geblockt!")
    if "schlachtruf" in segs:
        player.seg_first_strike = True
        msgs.append("📯 Schlachtruf: Dein erster Angriff macht +50% Schaden!")
    if "schattenform" in segs:
        msgs.append("🌑 Schattenform: Erste Runde 100% Ausweichen!")
    return msgs


def seg_outgoing_damage(player, target, dmg: int) -> tuple:
    tags = []
    segs = player.active_segnungen
    if "henker" in segs and (
        getattr(target, "bleed_stacks", 0) > 0
        or getattr(target, "poison_stacks", 0) > 0
        or getattr(target, "burn_stacks", 0) > 0
        or getattr(target, "stunned", False)
    ):
        dmg += 3
        tags.append("🪓 Henker +3")
    if "lebensraub" in segs and target.hp <= int(target.max_hp * 0.20):
        mult = 3 if (synergy_active(player, "giftmeister", "lebensraub")
                     and getattr(target, "poison_stacks", 0) > 0) else 2
        dmg *= mult
        tags.append(f"💀 Lebensraub ×{mult}")
    return dmg, (" " + " ".join(tags) if tags else "")


def seg_dmg(player, target, dmg: int) -> int:
    if not getattr(player, "active_segnungen", None):
        return dmg
    new_dmg, _ = seg_outgoing_damage(player, target, dmg)
    return new_dmg


def on_kill(player, enemy) -> list:
    msgs = []
    segs = player.active_segnungen
    if "blutdurst" in segs:
        amount = 6 if synergy_active(player, "blutdurst", "raserei") else 3
        healed = min(amount, player.max_hp - player.hp)
        player.hp += healed
        msgs.append(f"[red]🩸 Blutdurst: +{healed} HP[/red]")
    if "kopfgeld" in segs:
        player.inventory["Gold"] = player.inventory.get("Gold", 0) + 3
        player.stats["gold_earned"] = player.stats.get("gold_earned", 0) + 3
        msgs.append("[yellow]🪙 Kopfgeld: +3 Gold[/yellow]")
    if synergy_active(player, "eisige_praesenz", "seelenernte") and getattr(enemy, "stunned", False):
        gain = min(15, player.get_effective_max_energy() - player.energy)
        player.energy += gain
        msgs.append(f"[cyan]❄️⚡ Frosternte: +{gain} Energie[/cyan]")
    if "schatten_reflex" in segs and not player.shadow_strike_ready:
        player.shadow_strike_ready = True
        msgs.append("[magenta]🗡️  Schatten-Reflex: Aus dem Schatten ist sofort wieder bereit![/magenta]")
    if "raserei" in segs and not player.seg_raserei_ready:
        player.seg_kill_streak += 1
        if player.seg_kill_streak >= 3:
            player.seg_raserei_ready = True
            player.seg_kill_streak   = 0
            msgs.append("[bold red]🔥 RASEREI: Dein nächster Angriff trifft ALLE Gegner![/bold red]")
    return msgs


def on_player_hit(player, attacker, dmg: int) -> list:
    msgs = []
    if dmg <= 0:
        return msgs
    segs = player.active_segnungen
    if "dornenhaut" in segs and attacker.is_alive():
        attacker.hp = max(0, attacker.hp - 2)
        msgs.append(f"[green]🌵 Dornenhaut: {_esc(attacker.name)} nimmt 2 Rückstoß-Schaden![/green]")
    if ("giftblut" in segs and attacker.is_alive()
            and not getattr(attacker, "immune_to_bleed_poison", False)
            and random.random() < 0.25):
        attacker.poison_stacks = getattr(attacker, "poison_stacks", 0) + 1
        msgs.append(f"[magenta]🧬 Giftblut: {_esc(attacker.name)} erhält 1 Giftstack![/magenta]")
    return msgs


def status_snapshot(target) -> tuple:
    return (
        getattr(target, "bleed_stacks", 0),
        getattr(target, "poison_stacks", 0),
        getattr(target, "burn_stacks", 0),
        getattr(target, "stunned", False),
    )


def check_vergeltung(player, attacker, before: tuple) -> list:
    if "vergeltung" not in player.active_segnungen or before is None:
        return []
    msgs  = []
    after = status_snapshot(player)
    immune = getattr(attacker, "immune_to_bleed_poison", False)
    transfers = (
        ("bleed_stacks",  after[0] - before[0], "Blutung",     immune),
        ("poison_stacks", after[1] - before[1], "Gift",        immune),
        ("burn_stacks",   after[2] - before[2], "Verbrennung", immune),
    )
    for attr, diff, label, blocked in transfers:
        if diff > 0 and not blocked and random.random() < 0.50:
            setattr(attacker, attr, getattr(attacker, attr, 0) + diff)
            msgs.append(f"[cyan]⚖️  Vergeltung: {_esc(attacker.name)} erhält {diff}× {label} zurück![/cyan]")
    if not before[3] and after[3] and random.random() < 0.50:
        attacker.stunned = True
        msgs.append(f"[cyan]⚖️  Vergeltung: {_esc(attacker.name)} ist ebenfalls betäubt![/cyan]")
    return msgs


def check_zweite_chance(player) -> str:
    if player.hp > 0:
        return ""
    if "zweite_chance" in player.active_segnungen and not player.seg_zweite_chance_used:
        player.seg_zweite_chance_used = True
        player.hp = 1
        return "[bold green]🕊️  Zweite Chance: Du überlebst mit 1 HP![/bold green]"
    return ""


def check_glut_burst(player, target, burn_before: int) -> str:
    if "glut_entfesselung" not in player.active_segnungen:
        return ""
    if burn_before > 0 and getattr(target, "burn_stacks", 0) == 0 \
            and target.is_alive() and not getattr(target, "_glut_burst_done", False):
        target._glut_burst_done = True
        burst = BURN_DAMAGE * 3
        target.hp = max(0, target.hp - burst)
        return f"[orange1]💥 Glut-Entfesselung: {_esc(target.name)} nimmt {burst} Burst-Schaden![/orange1]"
    return ""
