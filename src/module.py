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
