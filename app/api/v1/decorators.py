from functools import wraps

from app.core.domain.commons.exceptions import BaseExceptionError
from app.persistence.cache import get_in_memory_cache


def cache_response(ttl: int = 60, namespace: str = "main"):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user_id = kwargs.get("user_id") or args[0]
            cache_key = f"{namespace}:user:{user_id}"

            cache = get_in_memory_cache()

            # Try to retrieve data from cache
            already_cached = await cache.exists(cache_key)  # pyright: ignore

            if already_cached:
                return await cache.get(cache_key)  # pyright: ignore

            response = await func(*args, **kwargs)

            try:
                # Store the cache
                await cache.set(cache_key, response, ttl=ttl)  # pyright: ignore

            except Exception as e:
                raise BaseExceptionError(status_code=500, message=f"Error caching data: {e}") from e

            return response

        return wrapper

    return decorator
