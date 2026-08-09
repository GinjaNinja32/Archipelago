import logging
import sys
import Fill
from worlds.AutoWorld import World
from .Fill import fill_restrictive, remaining_fill

logger = logging.getLogger("FillPatch")

_PATCH_APPLIED = False


class FillPatchWorld(World):
    """Utility APWorld that patches the generation fill algorithm."""
    game = "Fill Algorithm Patch"
    hidden = True


def apply_fill_patch():
    global _PATCH_APPLIED
    if _PATCH_APPLIED:
        return

    Fill.fill_restrictive = fill_restrictive
    Fill.remaining_fill = remaining_fill

    # update modules which used "from Fill import fill_restrictive"
    for mod_name, mod in sys.modules.items():
        if mod and mod_name != __name__:
            if hasattr(mod, "fill_restrictive"):
                setattr(mod, "fill_restrictive", fill_restrictive)
            if hasattr(mod, "remaining_fill"):
                setattr(mod, "remaining_fill", remaining_fill)

    _PATCH_APPLIED = True
    logger.info("Fill algorithm patch applied.")


apply_fill_patch()
