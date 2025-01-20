from decimal import Decimal

from anycoin import CoinSymbols
from anycoin.response_models import CoinQuotes, CoinRow, QuoteRow
from anycoin.services.coingecko import CoinGeckoService


def test_coin_quotes_repr():
    model = CoinQuotes(
        coins={
            CoinSymbols.btc: CoinRow(
                quotes={CoinSymbols.usd: QuoteRow(quote=Decimal('100000'))}
            )
        },
        api_service=CoinGeckoService(api_key='<api-key>'),
        raw_data={'bitcoin': {'usd': 100000}},
    )
    assert repr(model) == (
        f'CoinQuotes(coins={model.coins}, api_service={model.api_service})'
    )


def test_coin_quotes_str():
    model = CoinQuotes(
        coins={
            CoinSymbols.btc: CoinRow(
                quotes={CoinSymbols.usd: QuoteRow(quote=Decimal('100000'))}
            )
        },
        api_service=CoinGeckoService(api_key='<api-key>'),
        raw_data={'bitcoin': {'usd': 100000}},
    )
    assert str(model) == (
        f'CoinQuotes(coins={model.coins}, api_service={model.api_service})'
    )


def test_coin_quotes_dump_json():
    model = CoinQuotes(
        coins={
            CoinSymbols.btc: CoinRow(
                quotes={CoinSymbols.usd: QuoteRow(quote=Decimal('100000'))}
            )
        },
        api_service=CoinGeckoService(api_key='<api-key>'),
        raw_data={'bitcoin': {'usd': 100000}},
    )
    assert model.model_dump(mode='json') == {
        'coins': {'btc': {'quotes': {'usd': {'quote': '100000'}}}},
        'api_service': "CoinGeckoService(api_key='***')",
        'raw_data': {'bitcoin': {'usd': 100000}},
    }
