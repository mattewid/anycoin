from http import HTTPStatus

import httpx
import pytest
import respx

from anycoin import AsyncAnyCoin, CoinSymbols
from anycoin.exeptions import GetCoinQuotes as GetCoinQuotesException
from anycoin.response_models import CoinQuotes
from anycoin.services.coingecko import CoinGeckoService

pytestmark: pytest.MarkDecorator = pytest.mark.asyncio(loop_scope='session')


def test_asyncanycoin_api_services_empty():
    with pytest.raises(RuntimeError, match='At least one service is required'):
        AsyncAnyCoin(api_services=[])


@respx.mock
async def test_get_coin_quotes():
    EXAMPLE_RESPONSE = {'bitcoin': {'usd': 100811}}

    # Mock api request
    respx.get('https://pro-api.coingecko.com/api/v3/simple/price').mock(
        httpx.Response(
            status_code=200,
            json=EXAMPLE_RESPONSE,
        )
    )

    cgk_service = CoinGeckoService(
        api_key='<api-key>',
    )

    anyc = AsyncAnyCoin(api_services=[cgk_service])

    result: CoinQuotes = await anyc.get_coin_quotes(
        coins=[
            CoinSymbols.btc,
        ],
        quotes_in=[CoinSymbols.usd],
    )
    assert result.coins[CoinSymbols.btc]
    assert result.api_service is cgk_service
    assert result.raw_data


@respx.mock
async def test_get_coin_quotes_exception():
    EXAMPLE_RESPONSE = {'error': 'fake error'}

    # Mock api request
    respx.get('https://pro-api.coingecko.com/api/v3/simple/price').mock(
        httpx.Response(
            status_code=HTTPStatus.CONFLICT,
            json=EXAMPLE_RESPONSE,
        )
    )

    cgk_service = CoinGeckoService(
        api_key='<api-key>',
    )

    anyc = AsyncAnyCoin(api_services=[cgk_service])

    with pytest.raises(
        GetCoinQuotesException, match='Unable to get quote through services'
    ):
        await anyc.get_coin_quotes(
            coins=[
                CoinSymbols.btc,
            ],
            quotes_in=[CoinSymbols.usd],
        )
