"""Evaluate expressions."""

from collections.abc import Sequence
from types import SimpleNamespace

from .util import McColeExc

ENV_VARS = ("site", "page")


def create_env(config):
    """Create evaluation environment from configuration data."""
    return {key: _json_to_ns(config.get(key, {})) for key in ENV_VARS}


def evaluate(config, expr):
    """Evaluate an expression in a context."""
    env = create_env(config)
    try:
        return str(eval(expr, {"__builtins__": {}}, env))
    except NameError as exc:
        raise McColeExc(str(exc))
    except AttributeError as exc:
        raise McColeExc(str(exc))


def _json_to_ns(obj, root=False):
    """Recursively convert JSON-compatible structure to namespace."""
    if isinstance(obj, str):
        return obj
    elif isinstance(obj, Sequence):
        return list(obj)
    elif isinstance(obj, dict):
        return SimpleNamespace(**{k: _json_to_ns(v) for (k, v) in obj.items()})
    else:
        return obj
