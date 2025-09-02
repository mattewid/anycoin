import asyncio

from aiocache import Cache as _Cache

from ._enums import CoinSymbols, QuoteSymbols
from .response_models import CoinQuotes


class Cache(_Cache):
    """
    This class is just a wrapper around the aiocache.Cache class

    You can instantiate a cache type using the ``cache_type`` attribute like-
    this:

    >>> from anycoin.cache import Cache
    >>> Cache(Cache.REDIS)
    RedisCache (127.0.0.1:6379)

    OR
    >>> from anycoin.cache import Cache
    >>> Cache(Cache.MEMCACHED)
    MemcachedCache (127.0.0.1:6379)

    ``Cache.MEMORY`` is also available for use. See the aiocache documentation-
    to see which types are actually supported: https://aiocache.aio-libs.org/en/latest/
    """


_cached_coin_quotes_futures = {}
_locks: dict[str, asyncio.Lock] = {}


async def _get_or_set_coin_quotes_cache(
    cache: Cache, key, coro_func, ttl=None
) -> CoinQuotes:
    async def _get_value_cached() -> CoinQuotes | None:
        value = await cache.get(key)

        if value is not None:
            return CoinQuotes.model_validate_json(value)

    if value := await _get_value_cached():
        return value

    # Lock by key to avoid creating two Futures at the same time
    lock: asyncio.Lock = _locks.setdefault(key, asyncio.Lock())

    async with lock:
        # Check again inside the lock (double-checked locking)
        if value := await _get_value_cached():
            return value

        if key in _cached_coin_quotes_futures:
            return await _cached_coin_quotes_futures[key]

        loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()
        future: asyncio.Future[CoinQuotes] = loop.create_future()
        _cached_coin_quotes_futures[key] = future

        try:
            value = await coro_func()
            assert isinstance(value, CoinQuotes)

            await cache.set(key, value.model_dump_json(), ttl=ttl)
            future.set_result(value)
            return value
        except Exception as e:
            future.set_exception(e)
            raise
        finally:
            _cached_coin_quotes_futures.pop(key, None)
            _locks.pop(key, None)


def _get_cache_key_for_get_coin_quotes_method_params(
    coins: list[CoinSymbols],
    quotes_in: list[QuoteSymbols],
) -> str:
    """
    Example result:
        "coins:btc,ltc;quotes_in:usd,eur"
    """

    assert coins
    assert quotes_in

    cache_key = ''

    cache_key += 'coins:' + ','.join(coin.value for coin in coins)

    cache_key += ';quotes_in:' + ','.join(quote.value for quote in quotes_in)
    return cache_key
