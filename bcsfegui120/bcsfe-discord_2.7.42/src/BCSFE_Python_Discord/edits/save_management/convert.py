from typing import Any

from ... import helper, user_input_handler


def convert_to_jp(save_stats: dict[str, Any]) -> dict[str, Any]:
    save_stats["version"] = "jp"
    save_stats["dst"] = False

    helper.colored_text("Save data converted to jp", helper.GREEN)
    return save_stats


def convert_to_non_jp(save_stats: dict[str, Any], cc: str) -> dict[str, Any]:
    save_stats["version"] = cc
    save_stats["dst"] = True

    helper.colored_text(f"Save data converted to {cc}", helper.GREEN)
    return save_stats


def convert(save_stats: dict[str, Any], version: str) -> dict[str, Any]:
    if version == "jp":
        return convert_to_jp(save_stats)
    else:
        return convert_to_non_jp(save_stats, version)


def convert_save(save_stats: dict[str, Any], gv: str) -> dict[str, Any]:

    

    return convert(save_stats, gv)
