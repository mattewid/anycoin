import json
from decimal import Decimal
from enum import Enum
from http import HTTPStatus
from unittest.mock import AsyncMock

import httpx
import pytest
import respx

from anycoin import CoinSymbols, QuoteSymbols
from anycoin.exeptions import (
    CoinNotSupportedCGK as CoinNotSupportedCGKException,
)
from anycoin.exeptions import (
    GetCoinQuotes as GetCoinQuotesException,
)
from anycoin.exeptions import (
    QuoteCoinNotSupportedCGK as QuoteCoinNotSupportedCGKException,
)
from anycoin.response_models import CoinQuotes
from anycoin.services.coingecko import CoinGeckoService

pytestmark: pytest.MarkDecorator = pytest.mark.asyncio(loop_scope='session')


async def test_get_coin_id_by_symbol_coin_not_supported():
    class FakeCoinSymbols(str, Enum):
        invalid_member: str = 'invalid_member'

    coin_symbol = FakeCoinSymbols.invalid_member

    with pytest.raises(
        CoinNotSupportedCGKException,
        match=f'Coin {coin_symbol} not supported',
    ):
        await CoinGeckoService.get_coin_id_by_symbol(coin_symbol)


async def test_get_coin_symbol_by_id_not_supported():
    coin_id = 'FAKE-COIN-ID|UUID:4cb1afd7-5e95-429f-89f6-cd8dbad27269'

    with pytest.raises(
        CoinNotSupportedCGKException,
        match=f'Coin with id {coin_id} not supported',
    ):
        await CoinGeckoService.get_coin_symbol_by_id(coin_id)


async def test_get_quote_id_by_symbol_not_supported():
    class FakeCoinSymbols(str, Enum):
        invalid_member: str = 'invalid_member'

    coin_symbol = FakeCoinSymbols.invalid_member

    with pytest.raises(
        QuoteCoinNotSupportedCGKException,
        match=f'Quote {coin_symbol} not supported',
    ):
        await CoinGeckoService.get_quote_id_by_symbol(coin_symbol)


async def test_get_quote_symbol_by_id_not_supported():
    quote_id = 'FAKE-QUOTE-ID|UUID:4cb1afd7-5e95-429f-89f6-cd8dbad27269'

    with pytest.raises(
        QuoteCoinNotSupportedCGKException,
        match=f'Quote with id {quote_id} not supported',
    ):
        await CoinGeckoService.get_quote_symbol_by_id(quote_id)


@respx.mock
async def test_send_request_path_not_startwith_bar():
    EXAMPLE_RESPONSE = {'bitcoin': {'usd': 100811}}

    # Mock api request
    respx.get('https://pro-api.coingecko.com/api/v3/simple/price').mock(
        httpx.Response(
            status_code=200,
            json=EXAMPLE_RESPONSE,
        )
    )

    cgk_service = CoinGeckoService(api_key='<api-key>')

    result = await cgk_service._send_request(
        path='simple/price',  # path not start with /
        method='get',
    )
    assert result == EXAMPLE_RESPONSE


@respx.mock
async def test_send_request():
    EXAMPLE_RESPONSE = {'bitcoin': {'usd': 100811}}

    # Mock api request
    respx.get('https://pro-api.coingecko.com/api/v3/simple/price').mock(
        httpx.Response(
            status_code=200,
            json=EXAMPLE_RESPONSE,
        )
    )

    cgk_service = CoinGeckoService(api_key='<api-key>')

    result = await cgk_service._send_request(
        path='/simple/price', method='get'
    )
    assert result == EXAMPLE_RESPONSE


@respx.mock
async def test_send_request_no_success():
    EXAMPLE_RESPONSE = {'error': 'error'}

    # Mock api request
    respx.get('https://pro-api.coingecko.com/api/v3/simple/price').mock(
        httpx.Response(
            status_code=HTTPStatus.NOT_IMPLEMENTED,
            json=EXAMPLE_RESPONSE,
        )
    )

    cgk_service = CoinGeckoService(api_key='<api-key>')

    with pytest.raises(
        GetCoinQuotesException,
        match=('Error retrieving coin quotes. API response:'),
    ):
        await cgk_service._send_request(path='/simple/price', method='get')


@respx.mock
async def test_send_request_request_error():
    # Mock api request
    respx.get('https://pro-api.coingecko.com/api/v3/simple/price').mock(
        side_effect=httpx.RequestError
    )

    cgk_service = CoinGeckoService(api_key='<api-key>')

    with pytest.raises(
        GetCoinQuotesException,
        match=('Error retrieving coin quotes'),
    ):
        await cgk_service._send_request(path='/simple/price', method='get')


@respx.mock
async def test_send_request_json_decode_error():
    # Mock api request
    respx.get('https://pro-api.coingecko.com/api/v3/simple/price').mock(
        side_effect=json.JSONDecodeError('abc', '123', 0)
    )

    cgk_service = CoinGeckoService(api_key='<api-key>')

    with pytest.raises(
        GetCoinQuotesException,
        match=('Error retrieving coin quotes'),
    ):
        await cgk_service._send_request(path='/simple/price', method='get')


async def test_get_coin_quotes_coin_not_supported():
    class FakeCoinSymbols(str, Enum):
        invalid_member: str = 'invalid_member'

    coin_symbol = FakeCoinSymbols.invalid_member

    cgk_service = CoinGeckoService(api_key='<api-key>')

    with pytest.raises(
        GetCoinQuotesException,
        match=f'Coin {coin_symbol} not supported',
    ):
        await cgk_service.get_coin_quotes(
            coins=[coin_symbol], quotes_in=[QuoteSymbols.usd]
        )


async def test_get_coin_quotes_quote_coin_not_supported():
    class FakeQuoteSymbols(str, Enum):
        invalid_member: str = 'invalid_member'

    quote_symbol = FakeQuoteSymbols.invalid_member

    cgk_service = CoinGeckoService(api_key='<api-key>')

    with pytest.raises(
        GetCoinQuotesException,
        match=f'Quote {quote_symbol} not supported',
    ):
        await cgk_service.get_coin_quotes(
            coins=[CoinSymbols.btc], quotes_in=[quote_symbol]
        )


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

    cgk_service = CoinGeckoService(api_key='<api-key>')

    result: CoinQuotes = await cgk_service.get_coin_quotes(
        coins=[CoinSymbols.btc], quotes_in=[QuoteSymbols.usd]
    )
    assert isinstance(result, CoinQuotes)
    assert result.api_service == 'coingecko'
    assert result.raw_data == EXAMPLE_RESPONSE

    assert result.model_dump()['coins'] == {
        CoinSymbols.btc: {
            'quotes': {QuoteSymbols.usd: {'quote': Decimal('100811')}}
        }
    }


@respx.mock
async def test_get_coin_quotes_multi_coins():
    EXAMPLE_RESPONSE = {'bitcoin': {'usd': 100811}, 'ethereum': {'usd': 3000}}

    # Mock api request
    respx.get('https://pro-api.coingecko.com/api/v3/simple/price').mock(
        httpx.Response(
            status_code=200,
            json=EXAMPLE_RESPONSE,
        )
    )

    cgk_service = CoinGeckoService(api_key='<api-key>')

    result: CoinQuotes = await cgk_service.get_coin_quotes(
        coins=[CoinSymbols.btc, CoinSymbols.eth], quotes_in=[QuoteSymbols.usd]
    )
    assert isinstance(result, CoinQuotes)
    assert result.api_service == 'coingecko'
    assert result.raw_data == EXAMPLE_RESPONSE

    assert result.model_dump()['coins'] == {
        CoinSymbols.btc: {
            'quotes': {QuoteSymbols.usd: {'quote': Decimal('100811')}}
        },
        CoinSymbols.eth: {
            'quotes': {QuoteSymbols.usd: {'quote': Decimal('3000')}}
        },
    }


@respx.mock
async def test_get_coin_quotes_multi_quotes():
    EXAMPLE_RESPONSE = {'bitcoin': {'usd': 100811, 'eur': 101811}}

    # Mock api request
    respx.get('https://pro-api.coingecko.com/api/v3/simple/price').mock(
        httpx.Response(
            status_code=200,
            json=EXAMPLE_RESPONSE,
        )
    )

    cgk_service = CoinGeckoService(api_key='<api-key>')

    result: CoinQuotes = await cgk_service.get_coin_quotes(
        coins=[CoinSymbols.btc], quotes_in=[QuoteSymbols.usd, QuoteSymbols.eur]
    )
    assert isinstance(result, CoinQuotes)
    assert result.api_service == 'coingecko'
    assert result.raw_data == EXAMPLE_RESPONSE

    assert result.model_dump()['coins'] == {
        CoinSymbols.btc: {
            'quotes': {
                QuoteSymbols.usd: {'quote': Decimal('100811')},
                QuoteSymbols.eur: {'quote': Decimal('101811')},
            }
        },
    }


@respx.mock
async def test_get_coin_quotes_multi_coins_and_quotes():
    EXAMPLE_RESPONSE = {
        'bitcoin': {'usd': 100811, 'eur': 101812},
        'ethereum': {'usd': 3000, 'eur': 3001},
    }

    # Mock api request
    respx.get('https://pro-api.coingecko.com/api/v3/simple/price').mock(
        httpx.Response(
            status_code=200,
            json=EXAMPLE_RESPONSE,
        )
    )

    cgk_service = CoinGeckoService(api_key='<api-key>')

    result: CoinQuotes = await cgk_service.get_coin_quotes(
        coins=[CoinSymbols.btc, CoinSymbols.eth],
        quotes_in=[QuoteSymbols.usd, QuoteSymbols.eur],
    )
    assert isinstance(result, CoinQuotes)
    assert result.api_service == 'coingecko'
    assert result.raw_data == EXAMPLE_RESPONSE

    assert result.model_dump()['coins'] == {
        CoinSymbols.btc: {
            'quotes': {
                QuoteSymbols.usd: {'quote': Decimal('100811')},
                QuoteSymbols.eur: {'quote': Decimal('101812')},
            }
        },
        CoinSymbols.eth: {
            'quotes': {
                QuoteSymbols.usd: {'quote': Decimal('3000')},
                QuoteSymbols.eur: {'quote': Decimal('3001')},
            }
        },
    }


async def test_get_coin_quotes_with_cache_and_value_in_cache(any_aiocache):
    EXAMPLE_RESPONSE = {'bitcoin': {'usd': 100811}}

    any_aiocache.get = AsyncMock(
        return_value=(
            '{'
            """"coins": {"btc": {"quotes": {"usd": {"quote": "100811"}}}},"""
            """"api_service": "coingecko","""
            f""""raw_data": {json.dumps(EXAMPLE_RESPONSE)}"""
            '}'
        )
    )

    cgk_service = CoinGeckoService(
        api_key='<api-key>',
        cache=any_aiocache,
    )

    result: CoinQuotes = await cgk_service.get_coin_quotes(
        coins=[CoinSymbols.btc], quotes_in=[QuoteSymbols.usd]
    )

    any_aiocache.get.assert_called_once_with('coins:btc;quotes_in:usd')

    assert isinstance(result, CoinQuotes)
    assert result.api_service == 'coingecko'
    assert result.raw_data == EXAMPLE_RESPONSE

    assert result.model_dump()['coins'] == {
        CoinSymbols.btc: {
            'quotes': {QuoteSymbols.usd: {'quote': Decimal('100811')}}
        }
    }


@respx.mock
async def test_get_coin_quotes_with_cache_and_value_not_in_cache(any_aiocache):
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
        cache=any_aiocache,
    )

    result: CoinQuotes = await cgk_service.get_coin_quotes(
        coins=[CoinSymbols.btc], quotes_in=[QuoteSymbols.usd]
    )

    # --------- Checks if the return was cached correctly ---------
    EXPECTED_VALUE_IN_CACHE = (
        '{'
        """"coins": {"btc": {"quotes": {"usd": {"quote": "100811"}}}},"""
        """"api_service": "coingecko","""
        f""""raw_data": {json.dumps(EXAMPLE_RESPONSE)}"""
        '}'
    )
    await any_aiocache.get(
        'coins:btc;quotes_in:usd'
    ) == EXPECTED_VALUE_IN_CACHE
    # End

    assert isinstance(result, CoinQuotes)
    assert result.api_service == 'coingecko'
    assert result.raw_data == EXAMPLE_RESPONSE

    assert result.model_dump()['coins'] == {
        CoinSymbols.btc: {
            'quotes': {QuoteSymbols.usd: {'quote': Decimal('100811')}}
        }
    }


def test_repr():
    service = CoinGeckoService(api_key='<api-key>')
    assert repr(service) == ("CoinGeckoService(api_key='***')")
