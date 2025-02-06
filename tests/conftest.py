import pytest
import pytest_asyncio
from aiocache import Cache


@pytest_asyncio.fixture(
    params=[
        pytest.param({'cache_class': Cache.MEMORY}, id='memory-cache'),
        pytest.param(
            {
                'cache_class': Cache.MEMCACHED,
                'endpoint': '127.0.0.1',
                'port': 11211,
            },
            id='memcached-cache',
        ),
        pytest.param(
            {
                'cache_class': Cache.REDIS,
                'endpoint': '127.0.0.1',
                'port': 6379,
            },
            id='redis-cache',
        ),
    ]
)
async def any_aiocache(request):
    cache = Cache(**request.param)
    await cache.clear()
    yield cache
    await cache.close()
