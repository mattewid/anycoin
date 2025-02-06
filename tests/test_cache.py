from anycoin import CoinSymbols, QuoteSymbols
from anycoin.cache import (
    _get_cache_key_for_get_coin_quotes_method_params,  # noqa: PLC2701
)


def test_get_cache_key_for_get_coin_quotes_method_params_one_coin_and_one_quote():  # noqa: E501
    result = _get_cache_key_for_get_coin_quotes_method_params(
        coins=[CoinSymbols.btc],
        quotes_in=[
            QuoteSymbols.usd,
        ],
    )
    assert result == 'coins:btc;quotes_in:usd'


def test_get_cache_key_for_get_coin_quotes_method_params_multi_coin_and_one_quote():  # noqa: E501
    result = _get_cache_key_for_get_coin_quotes_method_params(
        coins=[CoinSymbols.btc, CoinSymbols.ltc],
        quotes_in=[
            QuoteSymbols.usd,
        ],
    )
    assert result == 'coins:btc,ltc;quotes_in:usd'


def test_get_cache_key_for_get_coin_quotes_method_params_multi_coin_and_multi_quote():  # noqa: E501
    result = _get_cache_key_for_get_coin_quotes_method_params(
        coins=[CoinSymbols.btc, CoinSymbols.ltc],
        quotes_in=[QuoteSymbols.usd, QuoteSymbols.eur],
    )
    assert result == 'coins:btc,ltc;quotes_in:usd,eur'


def test_get_cache_key_for_get_coin_quotes_method_params_one_coin_and_multi_quote():  # noqa: E501
    result = _get_cache_key_for_get_coin_quotes_method_params(
        coins=[CoinSymbols.btc],
        quotes_in=[QuoteSymbols.usd, QuoteSymbols.eur],
    )
    assert result == 'coins:btc;quotes_in:usd,eur'
