import os

import redis.asyncio as redis


def _get_redis_client() -> redis.Redis:
    return redis.from_url(
        os.getenv("REDIS_URL", "redis://localhost:6379"),
        decode_responses=True,
    )


_TTL_SECONDS = 60 * 60 * 24  # 24 horas


async def was_processed(message_id: str | None) -> bool:
    if not message_id:
        return False

    async with _get_redis_client() as client:
        return await client.exists(f"msg:{message_id}") == 1


async def mark_as_processed(message_id: str | None) -> None:
    if not message_id:
        return

    async with _get_redis_client() as client:
        await client.set(f"msg:{message_id}", "1", ex=_TTL_SECONDS)
