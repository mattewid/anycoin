import json
from decimal import Decimal
from enum import Enum
from unittest.mock import AsyncMock

import httpx
import pytest
import respx

from anycoin import CoinSymbols, QuoteSymbols
from anycoin.exeptions import (
    CoinNotSupportedCMC as CoinNotSupportedCMCException,
)
from anycoin.exeptions import (
    GetCoinQuotes as GetCoinQuotesException,
)
from anycoin.exeptions import (
    QuoteCoinNotSupportedCMC as QuoteCoinNotSupportedCMCException,
)
from anycoin.response_models import CoinQuotes
from anycoin.services.coinmarketcap import CoinMarketCapService

pytestmark: pytest.MarkDecorator = pytest.mark.asyncio(loop_scope='session')


async def test_get_coin_id_by_symbol_coin_not_supported():
    class FakeCoinSymbols(str, Enum):
        invalid_member: str = 'invalid_member'

    coin_symbol = FakeCoinSymbols.invalid_member

    with pytest.raises(
        CoinNotSupportedCMCException,
        match=f'Coin {coin_symbol} not supported',
    ):
        await CoinMarketCapService.get_coin_id_by_symbol(coin_symbol)


async def test_get_coin_symbol_by_id_not_supported():
    coin_id = 'FAKE-COIN-ID|UUID:4cb1afd7-5e95-429f-89f6-cd8dbad27269'

    with pytest.raises(
        CoinNotSupportedCMCException,
        match=f'Coin with id {coin_id} not supported',
    ):
        await CoinMarketCapService.get_coin_symbol_by_id(coin_id)


async def test_get_quote_id_by_symbol_not_supported():
    class FakeQuoteSymbols(str, Enum):
        invalid_member: str = 'invalid_member'

    quote_symbol = FakeQuoteSymbols.invalid_member

    with pytest.raises(
        QuoteCoinNotSupportedCMCException,
        match=f'Quote {quote_symbol} not supported',
    ):
        await CoinMarketCapService.get_quote_id_by_symbol(quote_symbol)


async def test_get_quote_symbol_by_id_not_supported():
    quote_id = 'FAKE-QUOTE-ID|UUID:4cb1afd7-5e95-429f-89f6-cd8dbad27269'

    with pytest.raises(
        QuoteCoinNotSupportedCMCException,
        match=f'Quote with id {quote_id} not supported',
    ):
        await CoinMarketCapService.get_quote_symbol_by_id(quote_id)


@respx.mock
async def test_send_request_path_not_startwith_bar():
    EXAMPLE_RESPONSE = {
        'data': {
            '1': {
                'id': 1,
                'name': 'Bitcoin',
                'symbol': 'BTC',
                'slug': 'bitcoin',
                'is_active': 1,
                'is_fiat': 0,
                'circulating_supply': 17199862,
                'total_supply': 17199862,
                'max_supply': 21000000,
                'date_added': '2013-04-28T00:00:00.000Z',
                'num_market_pairs': 331,
                'cmc_rank': 1,
                'last_updated': '2018-08-09T21:56:28.000Z',
                'tags': ['mineable'],
                'platform': None,
                'self_reported_circulating_supply': None,
                'self_reported_market_cap': None,
                'quote': {
                    '2781': {  # USD
                        'price': 6602.60701122,
                        'volume_24h': 4314444687.5194,
                        'volume_change_24h': -0.152774,
                        'percent_change_1h': 0.988615,
                        'percent_change_24h': 4.37185,
                        'percent_change_7d': -12.1352,
                        'percent_change_30d': -12.1352,
                        'market_cap': 852164659250.2758,
                        'market_cap_dominance': 51,
                        'fully_diluted_market_cap': 952835089431.14,
                        'last_updated': '2018-08-09T21:56:28.000Z',
                    }
                },
            }
        },
        'status': {
            'timestamp': '2025-01-19T10:00:27.010Z',
            'error_code': 0,
            'error_message': '',
            'elapsed': 10,
            'credit_count': 1,
            'notice': '',
        },
    }

    # Mock api request
    respx.get(
        'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
    ).mock(
        httpx.Response(
            status_code=200,
            json=EXAMPLE_RESPONSE,
        )
    )

    cmc_service = CoinMarketCapService(api_key='<api-key>')

    result = await cmc_service._send_request(
        path='cryptocurrency/quotes/latest',  # path not start with /
        method='get',
    )
    assert result == EXAMPLE_RESPONSE


@respx.mock
async def test_send_request():
    EXAMPLE_RESPONSE = {
        'data': {
            '1': {
                'id': 1,
                'name': 'Bitcoin',
                'symbol': 'BTC',
                'slug': 'bitcoin',
                'is_active': 1,
                'is_fiat': 0,
                'circulating_supply': 17199862,
                'total_supply': 17199862,
                'max_supply': 21000000,
                'date_added': '2013-04-28T00:00:00.000Z',
                'num_market_pairs': 331,
                'cmc_rank': 1,
                'last_updated': '2018-08-09T21:56:28.000Z',
                'tags': ['mineable'],
                'platform': None,
                'self_reported_circulating_supply': None,
                'self_reported_market_cap': None,
                'quote': {
                    '2781': {  # USD
                        'price': 6602.60701122,
                        'volume_24h': 4314444687.5194,
                        'volume_change_24h': -0.152774,
                        'percent_change_1h': 0.988615,
                        'percent_change_24h': 4.37185,
                        'percent_change_7d': -12.1352,
                        'percent_change_30d': -12.1352,
                        'market_cap': 852164659250.2758,
                        'market_cap_dominance': 51,
                        'fully_diluted_market_cap': 952835089431.14,
                        'last_updated': '2018-08-09T21:56:28.000Z',
                    }
                },
            }
        },
        'status': {
            'timestamp': '2025-01-19T10:00:27.010Z',
            'error_code': 0,
            'error_message': '',
            'elapsed': 10,
            'credit_count': 1,
            'notice': '',
        },
    }

    # Mock api request
    respx.get(
        'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
    ).mock(
        httpx.Response(
            status_code=200,
            json=EXAMPLE_RESPONSE,
        )
    )

    cmc_service = CoinMarketCapService(api_key='<api-key>')

    result = await cmc_service._send_request(
        path='/cryptocurrency/quotes/latest', method='get'
    )
    assert result == EXAMPLE_RESPONSE


@respx.mock
async def test_send_request_no_success():
    EXAMPLE_RESPONSE = {
        'data': {
            '1': {
                'id': 1,
                'name': 'Bitcoin',
                'symbol': 'BTC',
                'slug': 'bitcoin',
                'is_active': 1,
                'is_fiat': 0,
                'circulating_supply': 17199862,
                'total_supply': 17199862,
                'max_supply': 21000000,
                'date_added': '2013-04-28T00:00:00.000Z',
                'num_market_pairs': 331,
                'cmc_rank': 1,
                'last_updated': '2018-08-09T21:56:28.000Z',
                'tags': ['mineable'],
                'platform': None,
                'self_reported_circulating_supply': None,
                'self_reported_market_cap': None,
                'quote': {
                    '2781': {  # USD
                        'price': 6602.60701122,
                        'volume_24h': 4314444687.5194,
                        'volume_change_24h': -0.152774,
                        'percent_change_1h': 0.988615,
                        'percent_change_24h': 4.37185,
                        'percent_change_7d': -12.1352,
                        'percent_change_30d': -12.1352,
                        'market_cap': 852164659250.2758,
                        'market_cap_dominance': 51,
                        'fully_diluted_market_cap': 952835089431.14,
                        'last_updated': '2018-08-09T21:56:28.000Z',
                    }
                },
            }
        },
        'status': {
            'timestamp': '2025-01-19T10:00:27.010Z',
            'error_code': 1,  # No success code
            'error_message': '',
            'elapsed': 10,
            'credit_count': 1,
            'notice': '',
        },
    }

    # Mock api request
    respx.get(
        'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
    ).mock(
        httpx.Response(
            status_code=200,
            json=EXAMPLE_RESPONSE,
        )
    )

    cmc_service = CoinMarketCapService(api_key='<api-key>')

    with pytest.raises(
        GetCoinQuotesException,
        match=('Error retrieving coin quotes. API response:'),
    ):
        await cmc_service._send_request(
            path='/cryptocurrency/quotes/latest', method='get'
        )


@respx.mock
async def test_send_request_request_error():
    # Mock api request
    respx.get(
        'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
    ).mock(side_effect=httpx.RequestError)

    cmc_service = CoinMarketCapService(api_key='<api-key>')

    with pytest.raises(
        GetCoinQuotesException,
        match=('Error retrieving coin quotes'),
    ):
        await cmc_service._send_request(
            path='/cryptocurrency/quotes/latest', method='get'
        )


@respx.mock
async def test_send_request_json_decode_error():
    # Mock api request
    respx.get(
        'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
    ).mock(side_effect=json.JSONDecodeError('abc', '123', 0))

    cmc_service = CoinMarketCapService(api_key='<api-key>')

    with pytest.raises(
        GetCoinQuotesException,
        match=('Error retrieving coin quotes'),
    ):
        await cmc_service._send_request(
            path='/cryptocurrency/quotes/latest', method='get'
        )


async def test_get_coin_quotes_crypto_coin_not_supported():
    class FakeCoinSymbols(str, Enum):
        invalid_member: str = 'invalid_member'

    coin_symbol = FakeCoinSymbols.invalid_member

    cmc_service = CoinMarketCapService(api_key='<api-key>')

    with pytest.raises(
        GetCoinQuotesException,
        match=f'Coin {coin_symbol} not supported',
    ):
        await cmc_service.get_coin_quotes(
            coins=[coin_symbol], quotes_in=[QuoteSymbols.usd]
        )


async def test_get_coin_quotes_quote_coin_not_supported():
    class FakeQuoteSymbols(str, Enum):
        invalid_member: str = 'invalid_member'

    quote_symbol = FakeQuoteSymbols.invalid_member

    cmc_service = CoinMarketCapService(api_key='<api-key>')

    with pytest.raises(
        GetCoinQuotesException,
        match=f'Quote {quote_symbol} not supported',
    ):
        await cmc_service.get_coin_quotes(
            coins=[CoinSymbols.btc], quotes_in=[quote_symbol]
        )


@respx.mock
async def test_get_coin_quotes():
    EXAMPLE_RESPONSE = {
        'data': {
            '1': {
                'id': 1,
                'name': 'Bitcoin',
                'symbol': 'BTC',
                'slug': 'bitcoin',
                'is_active': 1,
                'is_fiat': 0,
                'circulating_supply': 17199862,
                'total_supply': 17199862,
                'max_supply': 21000000,
                'date_added': '2013-04-28T00:00:00.000Z',
                'num_market_pairs': 331,
                'cmc_rank': 1,
                'last_updated': '2018-08-09T21:56:28.000Z',
                'tags': ['mineable'],
                'platform': None,
                'self_reported_circulating_supply': None,
                'self_reported_market_cap': None,
                'quote': {
                    '2781': {  # USD
                        'price': 6602.60701122,
                        'volume_24h': 4314444687.5194,
                        'volume_change_24h': -0.152774,
                        'percent_change_1h': 0.988615,
                        'percent_change_24h': 4.37185,
                        'percent_change_7d': -12.1352,
                        'percent_change_30d': -12.1352,
                        'market_cap': 852164659250.2758,
                        'market_cap_dominance': 51,
                        'fully_diluted_market_cap': 952835089431.14,
                        'last_updated': '2018-08-09T21:56:28.000Z',
                    }
                },
            }
        },
        'status': {
            'timestamp': '2025-01-19T10:00:27.010Z',
            'error_code': 0,
            'error_message': '',
            'elapsed': 10,
            'credit_count': 1,
            'notice': '',
        },
    }

    # Mock api request
    respx.get(
        'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
    ).mock(
        httpx.Response(
            status_code=200,
            json=EXAMPLE_RESPONSE,
        )
    )

    cmc_service = CoinMarketCapService(api_key='<api-key>')

    result: CoinQuotes = await cmc_service.get_coin_quotes(
        coins=[CoinSymbols.btc], quotes_in=[QuoteSymbols.usd]
    )
    assert isinstance(result, CoinQuotes)
    assert result.api_service == 'coinmarketcap'
    assert result.raw_data == EXAMPLE_RESPONSE

    assert result.model_dump()['coins'] == {
        CoinSymbols.btc: {
            'quotes': {QuoteSymbols.usd: {'quote': Decimal('6602.60701122')}}
        }
    }


@respx.mock
async def test_get_coin_quotes_multi_coins():
    EXAMPLE_RESPONSE = {
        'data': {
            '1': {
                'id': 1,
                'name': 'Bitcoin',
                'symbol': 'BTC',
                'slug': 'bitcoin',
                'is_active': 1,
                'is_fiat': 0,
                'circulating_supply': 17199862,
                'total_supply': 17199862,
                'max_supply': 21000000,
                'date_added': '2013-04-28T00:00:00.000Z',
                'num_market_pairs': 331,
                'cmc_rank': 1,
                'last_updated': '2018-08-09T21:56:28.000Z',
                'tags': ['mineable'],
                'platform': None,
                'self_reported_circulating_supply': None,
                'self_reported_market_cap': None,
                'quote': {
                    '2781': {  # USD
                        'price': 6602.60701122,
                        'volume_24h': 4314444687.5194,
                        'volume_change_24h': -0.152774,
                        'percent_change_1h': 0.988615,
                        'percent_change_24h': 4.37185,
                        'percent_change_7d': -12.1352,
                        'percent_change_30d': -12.1352,
                        'market_cap': 852164659250.2758,
                        'market_cap_dominance': 51,
                        'fully_diluted_market_cap': 952835089431.14,
                        'last_updated': '2018-08-09T21:56:28.000Z',
                    }
                },
            },
            '1027': {
                'id': 1027,
                'name': 'Ethereum',
                'symbol': 'ETH',
                'slug': 'ethereum',
                'is_active': 1,
                'is_fiat': 0,
                'circulating_supply': 17199862,
                'total_supply': 17199862,
                'max_supply': 21000000,
                'date_added': '2013-04-28T00:00:00.000Z',
                'num_market_pairs': 331,
                'cmc_rank': 1,
                'last_updated': '2018-08-09T21:56:28.000Z',
                'tags': ['mineable'],
                'platform': None,
                'self_reported_circulating_supply': None,
                'self_reported_market_cap': None,
                'quote': {
                    '2781': {  # USD
                        'price': 1,  # Any value
                        'volume_24h': 4314444687.5194,
                        'volume_change_24h': -0.152774,
                        'percent_change_1h': 0.988615,
                        'percent_change_24h': 4.37185,
                        'percent_change_7d': -12.1352,
                        'percent_change_30d': -12.1352,
                        'market_cap': 852164659250.2758,
                        'market_cap_dominance': 51,
                        'fully_diluted_market_cap': 952835089431.14,
                        'last_updated': '2018-08-09T21:56:28.000Z',
                    }
                },
            },
        },
        'status': {
            'timestamp': '2025-01-19T10:00:27.010Z',
            'error_code': 0,
            'error_message': '',
            'elapsed': 10,
            'credit_count': 1,
            'notice': '',
        },
    }

    # Mock api request
    respx.get(
        'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
    ).mock(
        httpx.Response(
            status_code=200,
            json=EXAMPLE_RESPONSE,
        )
    )

    cmc_service = CoinMarketCapService(api_key='<api-key>')

    result: CoinQuotes = await cmc_service.get_coin_quotes(
        coins=[CoinSymbols.btc, CoinSymbols.eth], quotes_in=[QuoteSymbols.usd]
    )
    assert isinstance(result, CoinQuotes)
    assert result.api_service == 'coinmarketcap'
    assert result.raw_data == EXAMPLE_RESPONSE

    assert result.model_dump()['coins'] == {
        CoinSymbols.btc: {
            'quotes': {QuoteSymbols.usd: {'quote': Decimal('6602.60701122')}}
        },
        CoinSymbols.eth: {
            'quotes': {QuoteSymbols.usd: {'quote': Decimal('1')}}
        },
    }


@respx.mock
async def test_get_coin_quotes_multi_quotes():
    EXAMPLE_RESPONSE = {
        'data': {
            '1': {
                'id': 1,
                'name': 'Bitcoin',
                'symbol': 'BTC',
                'slug': 'bitcoin',
                'is_active': 1,
                'is_fiat': 0,
                'circulating_supply': 17199862,
                'total_supply': 17199862,
                'max_supply': 21000000,
                'date_added': '2013-04-28T00:00:00.000Z',
                'num_market_pairs': 331,
                'cmc_rank': 1,
                'last_updated': '2018-08-09T21:56:28.000Z',
                'tags': ['mineable'],
                'platform': None,
                'self_reported_circulating_supply': None,
                'self_reported_market_cap': None,
                'quote': {
                    '2781': {  # USD
                        'price': 6602.60701122,
                        'volume_24h': 4314444687.5194,
                        'volume_change_24h': -0.152774,
                        'percent_change_1h': 0.988615,
                        'percent_change_24h': 4.37185,
                        'percent_change_7d': -12.1352,
                        'percent_change_30d': -12.1352,
                        'market_cap': 852164659250.2758,
                        'market_cap_dominance': 51,
                        'fully_diluted_market_cap': 952835089431.14,
                        'last_updated': '2018-08-09T21:56:28.000Z',
                    },
                    '2790': {  # EUR
                        'price': 2,  # Any value
                        'volume_24h': 4314444687.5194,
                        'volume_change_24h': -0.152774,
                        'percent_change_1h': 0.988615,
                        'percent_change_24h': 4.37185,
                        'percent_change_7d': -12.1352,
                        'percent_change_30d': -12.1352,
                        'market_cap': 852164659250.2758,
                        'market_cap_dominance': 51,
                        'fully_diluted_market_cap': 952835089431.14,
                        'last_updated': '2018-08-09T21:56:28.000Z',
                    },
                },
            },
        },
        'status': {
            'timestamp': '2025-01-19T10:00:27.010Z',
            'error_code': 0,
            'error_message': '',
            'elapsed': 10,
            'credit_count': 1,
            'notice': '',
        },
    }

    # Mock api request
    respx.get(
        'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
    ).mock(
        httpx.Response(
            status_code=200,
            json=EXAMPLE_RESPONSE,
        )
    )

    cmc_service = CoinMarketCapService(api_key='<api-key>')

    result: CoinQuotes = await cmc_service.get_coin_quotes(
        coins=[CoinSymbols.btc], quotes_in=[QuoteSymbols.usd, QuoteSymbols.eur]
    )
    assert isinstance(result, CoinQuotes)
    assert result.api_service == 'coinmarketcap'
    assert result.raw_data == EXAMPLE_RESPONSE

    assert result.model_dump()['coins'] == {
        CoinSymbols.btc: {
            'quotes': {
                QuoteSymbols.usd: {'quote': Decimal('6602.60701122')},
                QuoteSymbols.eur: {'quote': Decimal('2')},
            }
        },
    }


@respx.mock
async def test_get_coin_quotes_multi_coins_and_quotes():
    EXAMPLE_RESPONSE = {
        'data': {
            '1': {
                'id': 1,
                'name': 'Bitcoin',
                'symbol': 'BTC',
                'slug': 'bitcoin',
                'is_active': 1,
                'is_fiat': 0,
                'circulating_supply': 17199862,
                'total_supply': 17199862,
                'max_supply': 21000000,
                'date_added': '2013-04-28T00:00:00.000Z',
                'num_market_pairs': 331,
                'cmc_rank': 1,
                'last_updated': '2018-08-09T21:56:28.000Z',
                'tags': ['mineable'],
                'platform': None,
                'self_reported_circulating_supply': None,
                'self_reported_market_cap': None,
                'quote': {
                    '2781': {  # USD
                        'price': 6602.60701122,
                        'volume_24h': 4314444687.5194,
                        'volume_change_24h': -0.152774,
                        'percent_change_1h': 0.988615,
                        'percent_change_24h': 4.37185,
                        'percent_change_7d': -12.1352,
                        'percent_change_30d': -12.1352,
                        'market_cap': 852164659250.2758,
                        'market_cap_dominance': 51,
                        'fully_diluted_market_cap': 952835089431.14,
                        'last_updated': '2018-08-09T21:56:28.000Z',
                    },
                    '2790': {  # EUR
                        'price': 2,  # Any value
                        'volume_24h': 4314444687.5194,
                        'volume_change_24h': -0.152774,
                        'percent_change_1h': 0.988615,
                        'percent_change_24h': 4.37185,
                        'percent_change_7d': -12.1352,
                        'percent_change_30d': -12.1352,
                        'market_cap': 852164659250.2758,
                        'market_cap_dominance': 51,
                        'fully_diluted_market_cap': 952835089431.14,
                        'last_updated': '2018-08-09T21:56:28.000Z',
                    },
                },
            },
            '1027': {
                'id': 1027,
                'name': 'Ethereum',
                'symbol': 'ETH',
                'slug': 'ethereum',
                'is_active': 1,
                'is_fiat': 0,
                'circulating_supply': 17199862,
                'total_supply': 17199862,
                'max_supply': 21000000,
                'date_added': '2013-04-28T00:00:00.000Z',
                'num_market_pairs': 331,
                'cmc_rank': 1,
                'last_updated': '2018-08-09T21:56:28.000Z',
                'tags': ['mineable'],
                'platform': None,
                'self_reported_circulating_supply': None,
                'self_reported_market_cap': None,
                'quote': {
                    '2781': {  # USD
                        'price': 1,  # Any value
                        'volume_24h': 4314444687.5194,
                        'volume_change_24h': -0.152774,
                        'percent_change_1h': 0.988615,
                        'percent_change_24h': 4.37185,
                        'percent_change_7d': -12.1352,
                        'percent_change_30d': -12.1352,
                        'market_cap': 852164659250.2758,
                        'market_cap_dominance': 51,
                        'fully_diluted_market_cap': 952835089431.14,
                        'last_updated': '2018-08-09T21:56:28.000Z',
                    },
                    '2790': {  # EUR
                        'price': 3,  # Any value
                        'volume_24h': 4314444687.5194,
                        'volume_change_24h': -0.152774,
                        'percent_change_1h': 0.988615,
                        'percent_change_24h': 4.37185,
                        'percent_change_7d': -12.1352,
                        'percent_change_30d': -12.1352,
                        'market_cap': 852164659250.2758,
                        'market_cap_dominance': 51,
                        'fully_diluted_market_cap': 952835089431.14,
                        'last_updated': '2018-08-09T21:56:28.000Z',
                    },
                },
            },
        },
        'status': {
            'timestamp': '2025-01-19T10:00:27.010Z',
            'error_code': 0,
            'error_message': '',
            'elapsed': 10,
            'credit_count': 1,
            'notice': '',
        },
    }

    # Mock api request
    respx.get(
        'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
    ).mock(
        httpx.Response(
            status_code=200,
            json=EXAMPLE_RESPONSE,
        )
    )

    cmc_service = CoinMarketCapService(api_key='<api-key>')

    result: CoinQuotes = await cmc_service.get_coin_quotes(
        coins=[CoinSymbols.btc, CoinSymbols.eth],
        quotes_in=[QuoteSymbols.usd, QuoteSymbols.eur],
    )
    assert isinstance(result, CoinQuotes)
    assert result.api_service == 'coinmarketcap'
    assert result.raw_data == EXAMPLE_RESPONSE

    assert result.model_dump()['coins'] == {
        CoinSymbols.btc: {
            'quotes': {
                QuoteSymbols.usd: {'quote': Decimal('6602.60701122')},
                QuoteSymbols.eur: {'quote': Decimal('2')},
            }
        },
        CoinSymbols.eth: {
            'quotes': {
                QuoteSymbols.usd: {'quote': Decimal('1')},
                QuoteSymbols.eur: {'quote': Decimal('3')},
            }
        },
    }


async def test_get_coin_quotes_with_cache_and_value_in_cache(any_aiocache):
    EXAMPLE_RESPONSE = {
        'data': {
            '1': {
                'id': 1,
                'name': 'Bitcoin',
                'symbol': 'BTC',
                'slug': 'bitcoin',
                'is_active': 1,
                'is_fiat': 0,
                'circulating_supply': 17199862,
                'total_supply': 17199862,
                'max_supply': 21000000,
                'date_added': '2013-04-28T00:00:00.000Z',
                'num_market_pairs': 331,
                'cmc_rank': 1,
                'last_updated': '2018-08-09T21:56:28.000Z',
                'tags': ['mineable'],
                'platform': None,
                'self_reported_circulating_supply': None,
                'self_reported_market_cap': None,
                'quote': {
                    '2781': {  # USD
                        'price': 6602.60701122,
                        'volume_24h': 4314444687.5194,
                        'volume_change_24h': -0.152774,
                        'percent_change_1h': 0.988615,
                        'percent_change_24h': 4.37185,
                        'percent_change_7d': -12.1352,
                        'percent_change_30d': -12.1352,
                        'market_cap': 852164659250.2758,
                        'market_cap_dominance': 51,
                        'fully_diluted_market_cap': 952835089431.14,
                        'last_updated': '2018-08-09T21:56:28.000Z',
                    }
                },
            }
        },
        'status': {
            'timestamp': '2025-01-19T10:00:27.010Z',
            'error_code': 0,
            'error_message': '',
            'elapsed': 10,
            'credit_count': 1,
            'notice': '',
        },
    }

    any_aiocache.get = AsyncMock(
        return_value=(
            '{'
            """"coins": {"btc": {"quotes": {"usd": {"quote": "6602.60701122"}}}},"""  # noqa: E501
            """"api_service": "coinmarketcap","""
            f""""raw_data": {json.dumps(EXAMPLE_RESPONSE)}"""
            '}'
        )
    )

    cmc_service = CoinMarketCapService(
        api_key='<api-key>',
        cache=any_aiocache,
    )

    result: CoinQuotes = await cmc_service.get_coin_quotes(
        coins=[CoinSymbols.btc], quotes_in=[QuoteSymbols.usd]
    )

    any_aiocache.get.assert_called_once_with('coins:btc;quotes_in:usd')

    assert isinstance(result, CoinQuotes)
    assert result.api_service == 'coinmarketcap'
    assert result.raw_data == EXAMPLE_RESPONSE

    assert result.model_dump()['coins'] == {
        CoinSymbols.btc: {
            'quotes': {QuoteSymbols.usd: {'quote': Decimal('6602.60701122')}}
        }
    }


@respx.mock
async def test_get_coin_quotes_with_cache_and_value_not_in_cache(any_aiocache):
    EXAMPLE_RESPONSE = {
        'data': {
            '1': {
                'id': 1,
                'name': 'Bitcoin',
                'symbol': 'BTC',
                'slug': 'bitcoin',
                'is_active': 1,
                'is_fiat': 0,
                'circulating_supply': 17199862,
                'total_supply': 17199862,
                'max_supply': 21000000,
                'date_added': '2013-04-28T00:00:00.000Z',
                'num_market_pairs': 331,
                'cmc_rank': 1,
                'last_updated': '2018-08-09T21:56:28.000Z',
                'tags': ['mineable'],
                'platform': None,
                'self_reported_circulating_supply': None,
                'self_reported_market_cap': None,
                'quote': {
                    '2781': {  # USD
                        'price': 6602.60701122,
                        'volume_24h': 4314444687.5194,
                        'volume_change_24h': -0.152774,
                        'percent_change_1h': 0.988615,
                        'percent_change_24h': 4.37185,
                        'percent_change_7d': -12.1352,
                        'percent_change_30d': -12.1352,
                        'market_cap': 852164659250.2758,
                        'market_cap_dominance': 51,
                        'fully_diluted_market_cap': 952835089431.14,
                        'last_updated': '2018-08-09T21:56:28.000Z',
                    }
                },
            }
        },
        'status': {
            'timestamp': '2025-01-19T10:00:27.010Z',
            'error_code': 0,
            'error_message': '',
            'elapsed': 10,
            'credit_count': 1,
            'notice': '',
        },
    }

    # Mock api request
    respx.get(
        'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
    ).mock(
        httpx.Response(
            status_code=200,
            json=EXAMPLE_RESPONSE,
        )
    )

    cmc_service = CoinMarketCapService(
        api_key='<api-key>',
        cache=any_aiocache,
    )

    result: CoinQuotes = await cmc_service.get_coin_quotes(
        coins=[CoinSymbols.btc], quotes_in=[QuoteSymbols.usd]
    )

    # --------- Checks if the return was cached correctly ---------
    EXPECTED_VALUE_IN_CACHE = (
        '{'
        """"coins": {"btc": {"quotes": {"usd": {"quote": "6602.60701122"}}}},"""  # noqa: E501
        """"api_service": "coinmarketcap","""
        f""""raw_data": {json.dumps(EXAMPLE_RESPONSE)}"""
        '}'
    )
    await any_aiocache.get(
        'coins:btc;quotes_in:usd'
    ) == EXPECTED_VALUE_IN_CACHE
    # End

    assert isinstance(result, CoinQuotes)
    assert result.api_service == 'coinmarketcap'
    assert result.raw_data == EXAMPLE_RESPONSE

    assert result.model_dump()['coins'] == {
        CoinSymbols.btc: {
            'quotes': {QuoteSymbols.usd: {'quote': Decimal('6602.60701122')}}
        }
    }


def test_repr():
    service = CoinMarketCapService(api_key='<api-key>')
    assert repr(service) == ("CoinMarketCapService(api_key='***')")
