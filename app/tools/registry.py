import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable


@dataclass
class ToolContext:
    user_id: str
    case: dict
    files: list[Path] = field(default_factory=list)  # files to send back to the user this turn


_TOOLS: dict[str, tuple[Callable, dict]] = {}


def tool(description: str, parameters: dict):
    """Register a function as an agent tool. The function receives (ctx, **arguments)."""

    def wrap(fn):
        _TOOLS[fn.__name__] = (fn, {
            "type": "function",
            "function": {"name": fn.__name__, "description": description, "parameters": parameters},
        })
        return fn

    return wrap


def schemas() -> list[dict]:
    return [schema for _, schema in _TOOLS.values()]


def execute(name: str, raw_args: str, ctx: ToolContext) -> dict:
    if name not in _TOOLS:
        return {"error": f"unknown tool {name}"}
    try:
        args = json.loads(raw_args or "{}")
    except json.JSONDecodeError as e:
        return {"error": f"invalid JSON arguments: {e}"}
    try:
        return _TOOLS[name][0](ctx, **args)
    except TypeError as e:
        return {"error": f"bad arguments: {e}"}
