"""Handler for editting uncanny legends"""
from typing import Any

from . import event_stages
from ... import user_input_handler

def edit_uncanny(save_stats: dict[str, Any], stage_id: str, star: str) -> dict[str, Any]:
    """Handler for editting uncanny legends"""
    stage_data = save_stats["uncanny"]
    lengths = stage_data["Lengths"]

    ids = []
    ids = user_input_handler.get_range(
        stage_id,
        lengths["total"],
    )
    save_stats["uncanny"] = event_stages.stage_handler(stage_data, star, ids, -1)

    return save_stats

def is_ancient_curse_clear(save_stats: dict[str, Any]) -> bool:
    """
    Check if the ancient curse is cleared

    Args:
        save_stats (dict[str, Any]): The save stats

    Returns:
        bool: If the ancient curse is cleared
    """
    return save_stats["uncanny"]["Value"]["clear_progress"][0][0] >= 1
