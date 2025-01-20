import json
from decimal import Decimal
from enum import Enum
from http import HTTPStatus

import httpx
import pytest
import respx

from anycoin import CoinSymbols
from anycoin.exeptions import (
    ConverterCoinNotSupportedCGK as ConverterCoinNotSupportedCGKException,
)
from anycoin.exeptions import (
    CryptoCoinNotSupportedCGK as CryptoCoinNotSupportedCGKException,
)
from anycoin.exeptions import (
    GetCoinQuotes as GetCoinQuotesException,
)
from anycoin.response_models import CoinQuotes
from anycoin.services.coingecko import CoinGeckoService

pytestmark: pytest.MarkDecorator = pytest.mark.asyncio(loop_scope='session')


async def test_get_crypto_id_by_coin_symbol_coin_not_supported():
    class FakeCoinSymbols(str, Enum):
        invalid_member: str = 'invalid_member'

    coin_symbol = FakeCoinSymbols.invalid_member

    with pytest.raises(
        CryptoCoinNotSupportedCGKException,
        match=f'Crypto coin {coin_symbol} not supported',
    ):
        await CoinGeckoService.get_crypto_id_by_coin_symbol(coin_symbol)


async def test_get_crypto_coin_symbol_by_id_not_supported():
    crypto_id = 'FAKE-CRYPTO-ID|UUID:4cb1afd7-5e95-429f-89f6-cd8dbad27269'

    with pytest.raises(
        CryptoCoinNotSupportedCGKException,
        match=f'Crypto with id {crypto_id} not supported',
    ):
        await CoinGeckoService.get_crypto_coin_symbol_by_id(crypto_id)


async def test_get_converter_id_by_coin_symbol_not_supported():
    class FakeCoinSymbols(str, Enum):
        invalid_member: str = 'invalid_member'

    coin_symbol = FakeCoinSymbols.invalid_member

    with pytest.raises(
        ConverterCoinNotSupportedCGKException,
        match=f'Converter coin {coin_symbol} not supported',
    ):
        await CoinGeckoService.get_converter_id_by_coin_symbol(coin_symbol)


async def test_get_converter_coin_symbol_by_id_not_supported():
    converter_id = (
        'FAKE-CONVERTER-ID|UUID:4cb1afd7-5e95-429f-89f6-cd8dbad27269'
    )

    with pytest.raises(
        ConverterCoinNotSupportedCGKException,
        match=f'Converter coin with id {converter_id} not supported',
    ):
        await CoinGeckoService.get_converter_coin_symbol_by_id(converter_id)


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

    cmc_service = CoinGeckoService(api_key='<api-key>')

    result = await cmc_service._send_request(
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

    cmc_service = CoinGeckoService(api_key='<api-key>')

    result = await cmc_service._send_request(
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

    cmc_service = CoinGeckoService(api_key='<api-key>')

    with pytest.raises(
        GetCoinQuotesException,
        match=('Error retrieving coin quotes. API response:'),
    ):
        await cmc_service._send_request(path='/simple/price', method='get')


@respx.mock
async def test_send_request_request_error():
    # Mock api request
    respx.get('https://pro-api.coingecko.com/api/v3/simple/price').mock(
        side_effect=httpx.RequestError
    )

    cmc_service = CoinGeckoService(api_key='<api-key>')

    with pytest.raises(
        GetCoinQuotesException,
        match=('Error retrieving coin quotes'),
    ):
        await cmc_service._send_request(path='/simple/price', method='get')


@respx.mock
async def test_send_request_json_decode_error():
    # Mock api request
    respx.get('https://pro-api.coingecko.com/api/v3/simple/price').mock(
        side_effect=json.JSONDecodeError('abc', '123', 0)
    )

    cmc_service = CoinGeckoService(api_key='<api-key>')

    with pytest.raises(
        GetCoinQuotesException,
        match=('Error retrieving coin quotes'),
    ):
        await cmc_service._send_request(path='/simple/price', method='get')


async def test_get_coin_quotes_crypto_coin_not_supported():
    class FakeCoinSymbols(str, Enum):
        invalid_member: str = 'invalid_member'

    coin_symbol = FakeCoinSymbols.invalid_member

    cmc_service = CoinGeckoService(api_key='<api-key>')

    with pytest.raises(
        GetCoinQuotesException,
        match=f'Crypto coin {coin_symbol} not supported',
    ):
        await cmc_service.get_coin_quotes(
            coins=[coin_symbol], quotes_in=[CoinSymbols.usd]
        )


async def test_get_coin_quotes_converter_coin_not_supported():
    class FakeCoinSymbols(str, Enum):
        invalid_member: str = 'invalid_member'

    converter_symbol = FakeCoinSymbols.invalid_member

    cmc_service = CoinGeckoService(api_key='<api-key>')

    with pytest.raises(
        GetCoinQuotesException,
        match=f'Converter coin {converter_symbol} not supported',
    ):
        await cmc_service.get_coin_quotes(
            coins=[CoinSymbols.btc], quotes_in=[converter_symbol]
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

    cmc_service = CoinGeckoService(api_key='<api-key>')

    result: CoinQuotes = await cmc_service.get_coin_quotes(
        coins=[CoinSymbols.btc], quotes_in=[CoinSymbols.usd]
    )
    assert isinstance(result, CoinQuotes)
    assert result.api_service is cmc_service
    assert result.raw_data == EXAMPLE_RESPONSE

    assert result.model_dump()['coins'] == {
        CoinSymbols.btc: {
            'quotes': {CoinSymbols.usd: {'quote': Decimal('100811')}}
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

    cmc_service = CoinGeckoService(api_key='<api-key>')

    result: CoinQuotes = await cmc_service.get_coin_quotes(
        coins=[CoinSymbols.btc, CoinSymbols.eth], quotes_in=[CoinSymbols.usd]
    )
    assert isinstance(result, CoinQuotes)
    assert result.api_service is cmc_service
    assert result.raw_data == EXAMPLE_RESPONSE

    assert result.model_dump()['coins'] == {
        CoinSymbols.btc: {
            'quotes': {CoinSymbols.usd: {'quote': Decimal('100811')}}
        },
        CoinSymbols.eth: {
            'quotes': {CoinSymbols.usd: {'quote': Decimal('3000')}}
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

    cmc_service = CoinGeckoService(api_key='<api-key>')

    result: CoinQuotes = await cmc_service.get_coin_quotes(
        coins=[CoinSymbols.btc], quotes_in=[CoinSymbols.usd, CoinSymbols.eur]
    )
    assert isinstance(result, CoinQuotes)
    assert result.api_service is cmc_service
    assert result.raw_data == EXAMPLE_RESPONSE

    assert result.model_dump()['coins'] == {
        CoinSymbols.btc: {
            'quotes': {
                CoinSymbols.usd: {'quote': Decimal('100811')},
                CoinSymbols.eur: {'quote': Decimal('101811')},
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

    cmc_service = CoinGeckoService(api_key='<api-key>')

    result: CoinQuotes = await cmc_service.get_coin_quotes(
        coins=[CoinSymbols.btc, CoinSymbols.eth],
        quotes_in=[CoinSymbols.usd, CoinSymbols.eur],
    )
    assert isinstance(result, CoinQuotes)
    assert result.api_service is cmc_service
    assert result.raw_data == EXAMPLE_RESPONSE

    assert result.model_dump()['coins'] == {
        CoinSymbols.btc: {
            'quotes': {
                CoinSymbols.usd: {'quote': Decimal('100811')},
                CoinSymbols.eur: {'quote': Decimal('101812')},
            }
        },
        CoinSymbols.eth: {
            'quotes': {
                CoinSymbols.usd: {'quote': Decimal('3000')},
                CoinSymbols.eur: {'quote': Decimal('3001')},
            }
        },
    }


def test_repr():
    service = CoinGeckoService(api_key='<api-key>')
    assert repr(service) == ("CoinGeckoService(api_key='***')")
