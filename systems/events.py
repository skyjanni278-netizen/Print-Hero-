import random
from ui.utils import clear_screen, print_header


def _wandering_merchant(player):
    clear_screen()
    print_header("Wandernder Haendler")
    print("Ein Haendler tritt aus dem Gebusch — sein Sortiment wirkt verlockend.")
    print("Er bietet dir 3 zuefaellige Items zu einem Sonderpreis an!\n")

    # 3 zufaellige Consumables aus dem Shop-Sortiment mit 20% Rabatt
    from content.shop import SHOP_CATALOGUE
    available = [item for item in SHOP_CATALOGUE if item.get("type") == "consumable"
                 and item.get("min_level", 1) <= player.level]
    if not available:
        print("Er hat leider nichts fuer dich.")
        input("(ENTER)")
        return

    picks = random.sample(available, min(3, len(available)))
    print(f"Gold: {player.inventory['Gold']} Muenzen\n")
    for i, item in enumerate(picks):
        discounted = max(1, int(item["price"] * 0.8))
        print(f"  [{i+1}] {item.get('emoji','🧪')} {item['name']:<22} {discounted} Gold  (statt {item['price']})")
    print("\n  [0] Weiterziehen")

    while True:
        choice = input("\nWas kaufen? ").strip()
        if choice == "0" or not choice.isdigit():
            break
        idx = int(choice) - 1
        if not (0 <= idx < len(picks)):
            print("Ungueltige Auswahl.")
            continue
        item = picks[idx]
        discounted = max(1, int(item["price"] * 0.8))
        if player.inventory["Gold"] < discounted:
            print("Zu wenig Gold!")
            input("(ENTER)")
            break
        added = player.add_consumable(item["name"], 1)
        if added:
            player.inventory["Gold"] -= discounted
            print(f"Gekauft! Gold verbleibend: {player.inventory['Gold']}")
        else:
            print("Inventar voll oder Stapel bereits voll!")
        input("(ENTER)")
        break


def _abandoned_shrine(player):
    clear_screen()
    print_header("Verlassener Schrein")
    print("Du entdeckst einen alten Schrein am Wegesrand.")
    print("Eine schwache Energie liegt in der Luft...\n")
    print("  [B] Blutopfer — zahle 10 HP fuer +25% XP im naechsten Kampf")
    print("  [G] Gratis beten — ungewisser Ausgang")
    print("  [W] Weitergehen")

    choice = input("\nDeine Wahl: ").lower()
    if choice == "b":
        if player.hp <= 10:
            print("Du hast zu wenig HP fuer ein Opfer!")
        else:
            player.hp -= 10
            player.next_fight_xp_mult = 1.25
            print(f"Du opferst 10 HP. Der Schrein leuchtet auf! (HP: {player.hp}/{player.max_hp})")
            print("Naechster Kampf: +25% XP")
    elif choice == "g":
        roll = random.random()
        if roll < 0.5:
            from content.loot_tables import CONSUMABLE_DEFS
            key = random.choice(["Healing Potion", "Energie-Kristall"])
            added = player.add_consumable(key, 1)
            if added:
                print(f"Der Schrein beschenkt dich mit: {key}!")
            else:
                print("Der Schrein reagiert... aber dein Inventar ist voll.")
        else:
            print("Stille. Der Schrein gibt dir nichts.")
    input("\n(ENTER)")


def _poison_trap(player):
    clear_screen()
    print_header("Giftige Falle")
    avoid_roll = random.random()
    if avoid_roll < 0.40:
        print("Du bemerkst eine Falle im Boden und weichst geschickt aus!")
    else:
        dmg = random.randint(5, 12)
        player.hp = max(1, player.hp - dmg)
        print(f"Du trittst in eine vergiftete Falle! -{dmg} HP (HP: {player.hp}/{player.max_hp})")
    input("\n(ENTER)")


def _treasure_chest(player):
    from content.loot_tables import roll_loot, apply_loot
    clear_screen()
    print_header("Schatz-Truhe")
    print("Du entdeckst eine verstaubte Truhe im Dickicht!\n")
    loot_items = roll_loot(rank=2, rolls=2)
    msgs = apply_loot(player, loot_items)
    if msgs:
        for m in msgs:
            print(m)
    else:
        print("Die Truhe ist leider leer.")
    input("\n(ENTER)")


def _mysterious_stranger(player):
    clear_screen()
    print_header("Mysterioeoser Fremder")
    print("Ein vermummter Fremder tritt aus den Schatten.")
    print("Er sieht dich schweigend an und bietet dir etwas an...\n")
    heal_amt = max(1, player.max_hp // 5)
    print(f"  [H] Heilung annehmen   — +{heal_amt} HP")
    print(f"  [G] Gold erhalten      — +20 Gold")
    print(f"  [A] Ablehnen")

    choice = input("\nDeine Wahl: ").lower()
    if choice == "h":
        healed = min(heal_amt, player.max_hp - player.hp)
        player.hp = min(player.max_hp, player.hp + heal_amt)
        print(f"Der Fremde legt seine Hand auf deine Schulter. +{healed} HP (HP: {player.hp}/{player.max_hp})")
    elif choice == "g":
        player.inventory["Gold"] += 20
        player.stats["gold_earned"] += 20
        print(f"Der Fremde drueckt dir einen Beutel Gold in die Hand. +20 Gold (Gold: {player.inventory['Gold']})")
    else:
        print("Du lehnst ab. Der Fremde nickt und verschwindet.")
    input("\n(ENTER)")


# Gewichtete Event-Tabelle: (Funktion, Gewicht)
_EVENTS = [
    (_wandering_merchant,  12),
    (_abandoned_shrine,     9),
    (_poison_trap,          9),
    (_treasure_chest,       9),
    (_mysterious_stranger,  9),
    (None,                 52),  # Kein Event
]


def trigger_event(player):
    funcs, weights = zip(*_EVENTS)
    chosen = random.choices(funcs, weights=weights, k=1)[0]
    if chosen is not None:
        chosen(player)
