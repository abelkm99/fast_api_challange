import json
from functools import wraps

from fastapi import HTTPException

from app.persistence.cache import get_in_memory_cache


def cache_response(ttl: int = 60, namespace: str = "main"):
    """Caching decorator for FastAPI endpoints.

    ttl: Time to live for the cache in seconds.
    namespace: Namespace for cache keys in Redis.
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user = kwargs.get("user") or args[0]
            cache_key = f"{namespace}:user:{user.id}"

            cache = get_in_memory_cache()

            # Try to retrieve data from cache
            cached_value = await cache.get(cache_key)  # pyright: ignore

            if cached_value:
                return json.loads(cached_value)  # Return cached data

            # Call the actual function if cache is not hit
            response = await func(*args, **kwargs)

            try:
                # Store the response in Redis with a TTL
                await cache.set(cache_key, response, ttl=ttl)  # pyright: ignore

            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error caching data: {e}") from e

            return response

        return wrapper

    return decorator
