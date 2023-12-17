import logging
from typing import Never, NoReturn

logger = logging.getLogger(__name__)


def assert_never(_: Never) -> NoReturn:
    raise AssertionError("Expected to be unreachable")


def get_default(obj, keys: list, default):
    try:
        current_value = obj
        for key in keys:
            current_value = current_value[key]
        if current_value is None:
            return default
        return current_value
    except Exception:
        return default
