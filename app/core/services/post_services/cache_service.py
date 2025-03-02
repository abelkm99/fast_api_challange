def user_posts_cache_key(f, *args, **kwargs):
    return "abel"
    """Generates a cache key based on user ID only."""
    user = kwargs.get("user")
    if user:
        return f"user_posts:{user.id}"
    # Fallback key (shouldn't occur under normal circumstances)
    return f"{f.__module__}:{f.__name__}:{args}:{kwargs}"
