from decimal import Decimal
from http import HTTPStatus

import httpx
import pytest
import respx

from anycoin import AnyCoin, CoinSymbols, QuoteSymbols
from anycoin.exeptions import ConvertCoin as ConvertCoinException
from anycoin.exeptions import GetCoinQuotes as GetCoinQuotesException
from anycoin.response_models import CoinQuotes
from anycoin.services.coingecko import CoinGeckoService


def test_anycoin_api_services_empty():
    with pytest.raises(RuntimeError, match='At least one service is required'):
        AnyCoin(api_services=[])


@respx.mock
def test_get_coin_quotes():
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

    anyc = AnyCoin(api_services=[cgk_service])

    result: CoinQuotes = anyc.get_coin_quotes(
        coins=[
            CoinSymbols.btc,
        ],
        quotes_in=[QuoteSymbols.usd],
    )
    assert result.coins[CoinSymbols.btc]
    assert result.api_service == 'coingecko'
    assert result.raw_data


@respx.mock
def test_get_coin_quotes_exception():
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

    anyc = AnyCoin(api_services=[cgk_service])

    with pytest.raises(
        GetCoinQuotesException, match='Unable to get quote through services'
    ):
        anyc.get_coin_quotes(
            coins=[
                CoinSymbols.btc,
            ],
            quotes_in=[QuoteSymbols.usd],
        )


@respx.mock
def test_convert_coin_with_from_coin_is_CoinSymbols_and_to_coin_is_QuoteSymbols():  # noqa: E501
    EXAMPLE_RESPONSE = {'litecoin': {'usd': 127.41098851451477}}

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

    anyc = AnyCoin(api_services=[cgk_service])

    result: Decimal = anyc.convert_coin(
        amount=Decimal('1.2'),
        from_coin=CoinSymbols.ltc,
        to_coin=QuoteSymbols.usd,
    )
    assert result == Decimal('152.893186217417724')


@respx.mock
def test_convert_coin_with_from_coin_is_CoinSymbols_and_to_coin_is_CoinSymbols():  # noqa: E501
    EXAMPLE_RESPONSE = {
        'binancecoin': {'usd': 675.2103782980719},
        'litecoin': {'usd': 127.41098851451477},
    }

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

    anyc = AnyCoin(api_services=[cgk_service])

    result: Decimal = anyc.convert_coin(
        amount=Decimal('2.55'),
        from_coin=CoinSymbols.bnb,
        to_coin=CoinSymbols.ltc,
    )
    assert result == Decimal('13.51364183524826778891989760')


@respx.mock
def test_convert_coin_with_from_coin_is_QuoteSymbols_and_to_coin_is_CoinSymbols():  # noqa: E501
    EXAMPLE_RESPONSE = {'dogecoin': {'usd': 0.32769167949926686}}

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

    anyc = AnyCoin(api_services=[cgk_service])

    result: Decimal = anyc.convert_coin(
        amount=Decimal('3.23'),
        from_coin=QuoteSymbols.usd,
        to_coin=CoinSymbols.doge,
    )
    assert result == Decimal('9.856826407480469560449673338')


@respx.mock
def test_convert_coin_with_from_coin_is_QuoteSymbols_and_to_coin_is_QuoteSymbols():  # noqa: E501
    EXAMPLE_RESPONSE = {
        'tether': {'usd': 0.999743929278962, 'brl': 5.835382003285947}
    }

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

    anyc = AnyCoin(api_services=[cgk_service])

    result: Decimal = anyc.convert_coin(
        amount=Decimal('100'),
        from_coin=QuoteSymbols.usd,
        to_coin=QuoteSymbols.brl,
    )
    assert result == Decimal('583.6876656499986822275017460')


def test_convert_coin_conversion_error():
    cgk_service = CoinGeckoService(
        api_key='<api-key>',
    )
    anyc = AnyCoin(api_services=[cgk_service])

    with pytest.raises(ConvertCoinException, match='Invalid conversion from'):
        anyc.convert_coin(
            amount=Decimal('100'),
            from_coin='invalid-type',
            to_coin=QuoteSymbols.brl,
        )
