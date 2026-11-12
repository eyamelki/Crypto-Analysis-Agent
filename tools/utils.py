import functools
import json
import time
from typing import Any, Callable

import requests

import config

RETRY_STATUS = {429, 500, 502, 503, 504}


def ttl_cache(seconds: int | None = None) -> Callable:
    def decorator(fn: Callable) -> Callable:
        store: dict[Any, tuple[float, Any]] = {}

        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            ttl = config.CACHE_TTL_SECONDS if seconds is None else seconds
            key = (args, tuple(sorted(kwargs.items())))
            now = time.monotonic()
            hit = store.get(key)
            if hit and now - hit[0] < ttl:
                return hit[1]
            value = fn(*args, **kwargs)
            store[key] = (now, value)
            return value

        wrapper.cache_clear = store.clear
        return wrapper

    return decorator


def http_get_json(url, headers=None, params=None, retries=3, backoff=1.0, timeout=30) -> Any:
    """GET -> JSON avec retries (backoff exponentiel) sur 429 / 5xx / erreurs réseau."""
    for attempt in range(retries):
        last_attempt = attempt == retries - 1
        try:
            resp = requests.get(url, headers=headers, params=params, timeout=timeout)
            if resp.status_code in RETRY_STATUS and not last_attempt:
                time.sleep(backoff * (2 ** attempt))
                continue
            resp.raise_for_status()
            return resp.json()
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            if last_attempt:
                raise
            time.sleep(backoff * (2 ** attempt))
        except ValueError as e:
            raise requests.exceptions.RequestException(f"Invalid JSON from API: {e}") from e
    raise requests.exceptions.RequestException("Unknown HTTP error")


def to_json(payload: Any) -> str:
    return json.dumps(payload, indent=2, ensure_ascii=False, default=str)


def error_json(message: str) -> str:
    return to_json({"status": False, "error": message})