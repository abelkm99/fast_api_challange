from aiocache import caches


def set_default_cache():
    caches.set_config(
        {
            "default": {
                "cache": "aiocache.SimpleMemoryCache",
                "serializer": {"class": "aiocache.serializers.StringSerializer"},
            },
        }
    )


def get_in_memory_cache():
    return caches.get("default")  # This fails if config is missing
