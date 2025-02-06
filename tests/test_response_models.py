from decimal import Decimal

from anycoin import CoinSymbols, QuoteSymbols
from anycoin.response_models import CoinQuotes, CoinRow, QuoteRow


def test_coin_quotes_repr():
    model = CoinQuotes(
        coins={
            CoinSymbols.btc: CoinRow(
                quotes={QuoteSymbols.usd: QuoteRow(quote=Decimal('100000'))}
            )
        },
        api_service='coingecko',
        raw_data={'bitcoin': {'usd': 100000}},
    )
    assert repr(model) == (
        f"CoinQuotes(coins={model.coins}, api_service='coingecko')"
    )


def test_coin_quotes_str():
    model = CoinQuotes(
        coins={
            CoinSymbols.btc: CoinRow(
                quotes={QuoteSymbols.usd: QuoteRow(quote=Decimal('100000'))}
            )
        },
        api_service='coingecko',
        raw_data={'bitcoin': {'usd': 100000}},
    )
    assert str(model) == (
        f"CoinQuotes(coins={model.coins}, api_service='coingecko')"
    )


def test_coin_quotes_dump_json():
    model = CoinQuotes(
        coins={
            CoinSymbols.btc: CoinRow(
                quotes={QuoteSymbols.usd: QuoteRow(quote=Decimal('100000'))}
            )
        },
        api_service='coingecko',
        raw_data={'bitcoin': {'usd': 100000}},
    )
    assert model.model_dump(mode='json') == {
        'coins': {'btc': {'quotes': {'usd': {'quote': '100000'}}}},
        'api_service': 'coingecko',
        'raw_data': {'bitcoin': {'usd': 100000}},
    }


def test_coin_quotes_model_validate_json():
    model = CoinQuotes(
        coins={
            CoinSymbols.btc: CoinRow(
                quotes={QuoteSymbols.usd: QuoteRow(quote=Decimal('100000'))}
            )
        },
        api_service='coingecko',
        raw_data={'bitcoin': {'usd': 100000}},
    )
    model_json: str = model.model_dump_json()

    assert CoinQuotes.model_validate_json(model_json) == model
