from __future__ import annotations

from embervault_sdk import ModuleContext, ModuleResult

MODULE_ID = "embervault.game-tuning"


def describe() -> dict:
    return {"id": MODULE_ID, "execution": "embedded", "application_state": "staged-only", "mutates_live_game": False}


def plan_setting_change(context: ModuleContext, key: str, value, profile_id: str) -> ModuleResult:
    if context.module_id != MODULE_ID or context.profile_id != profile_id:
        return ModuleResult("blocked", "Game Tuning requires a matching profile-scoped context.")
    if context.capability_state != "plan-only":
        return ModuleResult("blocked", "Game Tuning changes must remain staged-only.")
    if not key.strip():
        return ModuleResult("blocked", "A setting key is required.")
    return ModuleResult("ready", "Game setting change prepared.", {
        "key": key.strip(), "value": value, "profile_id": profile_id,
        "application_state": "staged-only", "mutates_live_game": False,
    })


def compare_setting_plans(plans: list[dict], *, profile_id: str) -> dict:
    """Compare staged setting plans without applying or exporting them."""
    selected = [plan for plan in plans if plan.get("profile_id") == profile_id]
    changes = sorted(
        [{"key": plan.get("key", ""), "value": plan.get("value"), "state": plan.get("application_state", "unknown")}
         for plan in selected],
        key=lambda item: item["key"],
    )
    return {
        "schema_version": 1,
        "profile_id": profile_id,
        "changes": changes,
        "read_only": True,
        "application_state": "staged-only",
        "mutates_live_game": False,
        "runtime_approval": False,
        "actions": [],
    }
