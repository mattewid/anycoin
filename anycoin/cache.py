from aiocache import Cache as _Cache

from ._enums import CoinSymbols, QuoteSymbols


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
