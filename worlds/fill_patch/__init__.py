import logging
import sys
import Fill as core_fill
from worlds.AutoWorld import World
from . import Fill as local_fill

logger = logging.getLogger("FillPatch")

_PATCH_APPLIED = False


class FillPatchWorld(World):
    """Utility APWorld that patches the generation fill algorithm."""
    game = "Fill Algorithm Patch"
    hidden = True
    item_name_to_id = {}
    location_name_to_id = {}

def apply_fill_patch():
    global _PATCH_APPLIED
    if _PATCH_APPLIED:
        return

    original_fill_restrictive = getattr(core_fill, "fill_restrictive", None)
    original_remaining_fill = getattr(core_fill, "remaining_fill", None)

    core_fill.fill_restrictive = local_fill.fill_restrictive
    core_fill.remaining_fill = local_fill.remaining_fill

    # update modules which used "from Fill import fill_restrictive"
    for mod_name, mod in sys.modules.items():
        if mod and mod_name != __name__:
            if getattr(mod, "fill_restrictive", None) is original_fill_restrictive:
                setattr(mod, "fill_restrictive", local_fill.fill_restrictive)
            if getattr(mod, "remaining_fill", None) is original_remaining_fill:
                setattr(mod, "remaining_fill", local_fill.remaining_fill)

    _PATCH_APPLIED = True
    logger.info("Fill algorithm patch applied.")


apply_fill_patch()
