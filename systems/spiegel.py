import random
from rich.markup import escape as _esc

# ── Spiegel-Upgrades (permanent, im Meta-Save) ────────────────────────────────

SPIEGEL_DEFS = {
    "zaehigkeit": {
        "name": "Zähigkeit", "emoji": "❤️", "cost": 60,
        "a": "+15 max HP beim Run-Start",
        "b": "Nach jedem gewonnenen Kampf: +5 HP",
    },
    "kriegserfahrung": {
        "name": "Kriegserfahrung", "emoji": "⚔️", "cost": 80,
        "a": "+1 ATK beim Run-Start",
        "b": "Erster Kampf jedes Dungeons: +50% Schaden",
    },
    "glueck": {
        "name": "Glück", "emoji": "🍀", "cost": 70,
        "a": "+15% Gold aus Beute",
        "b": "Boss-Beute: +1 zusätzlicher Beute-Wurf",
    },
    "zweites_leben": {
        "name": "Zweites Leben", "emoji": "🕊️", "cost": 120,
        "a": "1× pro Run: Ein tödlicher Treffer lässt dich mit 1 HP überleben",
        "b": "Bei Tod: 20% deines Goldes werden als Runenessenz gerettet",
    },
    "seelenbindung": {
        "name": "Seelenbindung", "emoji": "📿", "cost": 90,
        "a": "+8% XP aus Kämpfen",
        "b": "Level-Up: +1 Skillpunkt extra",
    },
    "haendlerglueck": {
        "name": "Händlerglück", "emoji": "🛒", "cost": 75,
        "a": "Der Wandernde Händler erscheint doppelt so oft",
        "b": "Händler-Preise −15%",
    },
    "dunkelresistenz": {
        "name": "Dunkelresistenz", "emoji": "🌓", "cost": 100,
        "a": "Erhaltene Statuseffekte: −1 Stack",
        "b": "Pro Run: Immunität gegen einen zufälligen Statuseffekt",
    },
}

SWITCH_COST_FACTOR = 0.30

_IMMUN_LABELS = {"bleed": "Blutung", "poison": "Gift", "burn": "Verbrennung"}


# ── Kauf & Wechsel ────────────────────────────────────────────────────────────

def get_variant(meta, uid: str):
    return meta.get("spiegel_state", {}).get(uid)


def switch_cost(uid: str) -> int:
    return max(1, int(SPIEGEL_DEFS[uid]["cost"] * SWITCH_COST_FACTOR))


def buy_or_switch(meta, uid: str, variant: str) -> tuple:
    from core.save import spend_runenessenz
    d       = SPIEGEL_DEFS[uid]
    state   = meta.setdefault("spiegel_state", {})
    current = state.get(uid)
    if current == variant:
        return False, f"{d['emoji']} {d['name']} [{variant}] ist bereits aktiv."
    cost = d["cost"] if current is None else switch_cost(uid)
    if meta.get("runenessenz", 0) < cost:
        return False, f"Nicht genug Runenessenz! (Benötigt: {cost}, vorhanden: {meta.get('runenessenz', 0)})"
    state[uid] = variant
    spend_runenessenz(meta, cost)
    desc = d["a"] if variant == "A" else d["b"]
    word = "freigeschaltet" if current is None else f"gewechselt ({current} → {variant})"
    return True, f"{d['emoji']} {d['name']} [{variant}] {word} — {desc}"


# ── Run-Start: Effekte anwenden ───────────────────────────────────────────────

def spiegel_active(player, uid: str, variant: str) -> bool:
    return getattr(player, "spiegel", {}).get(uid) == variant


def apply_spiegel_effects(player, meta) -> list:
    state = dict(meta.get("spiegel_state", {}))
    player.spiegel = state
    msgs = []
    if state.get("zaehigkeit") == "A":
        player.max_hp += 15
        player.hp     += 15
        msgs.append(f"❤️ Zähigkeit [[A]]: +15 max HP (HP: {player.hp}/{player.max_hp})")
    if state.get("kriegserfahrung") == "A":
        player.attack += 1
        msgs.append("⚔️ Kriegserfahrung [[A]]: +1 ATK")
    if state.get("dunkelresistenz") == "B":
        effekt = random.choice(["bleed", "poison", "burn"])
        player.spiegel_immun_effekt = effekt
        msgs.append(f"🌓 Dunkelresistenz [[B]]: Immun gegen [bold]{_IMMUN_LABELS[effekt]}[/bold] in diesem Run")
    return msgs


# ── Kampf- & Preis-Hooks ──────────────────────────────────────────────────────

def spiegel_price(player, price: int) -> int:
    if spiegel_active(player, "haendlerglueck", "B"):
        return max(1, int(price * 0.85))
    return price


def check_spiegel_leben(player) -> str:
    if player.hp > 0:
        return ""
    if spiegel_active(player, "zweites_leben", "A") and not getattr(player, "spiegel_leben_used", False):
        player.spiegel_leben_used = True
        player.hp = 1
        return "[bold green]🪞🕊️  Zweites Leben: Der Spiegel hält dich mit 1 HP am Leben![/bold green]"
    return ""


def check_dunkelresistenz(player, before: tuple) -> list:
    if before is None or not spiegel_active(player, "dunkelresistenz", "A"):
        return []
    msgs = []
    reductions = (
        ("bleed_stacks",  before[0], "Blutung"),
        ("poison_stacks", before[1], "Gift"),
        ("burn_stacks",   before[2], "Verbrennung"),
    )
    for attr, prev, label in reductions:
        now = getattr(player, attr, 0)
        if now > prev:
            setattr(player, attr, now - 1)
            msgs.append(f"[cyan]🌓 Dunkelresistenz: {label} −1 Stack ({now - 1} verbleibend)[/cyan]")
    return msgs
