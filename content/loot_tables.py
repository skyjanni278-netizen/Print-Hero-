# Kompatiblitäts-Shim — importiert alles aus den aufgeteilten Modulen.
# Bestehende Imports (from content.loot_tables import X) funktionieren weiterhin.
# Neue Importe sollten direkt aus content.items / content.sets / content.loot kommen.

from content.items import (  # noqa: F401
    CONSUMABLE_DEFS,
    JUNK_DEFS,
    EQUIPMENT_DEFS,
    CLASS_WEAPON_MAP,
    WEAPON_VARIANT_TO_BASE,
    RARITY_LABEL,
    CRAFT_RECIPES,
)

from content.sets import (  # noqa: F401
    SET_DEFS,
    get_active_sets,
    get_set_specials,
)

from content.loot import (  # noqa: F401
    LOOT_POOL,
    RANK_LOOT_WEIGHTS,
    ZONE_LOOT_POOL,
    BOSS_LOOT_POOL,
    roll_zone_loot,
    roll_boss_loot,
    roll_loot,
    apply_loot,
)
