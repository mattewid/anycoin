from anycoin import CoinSymbols, QuoteSymbols


def test_coin_symbols_enum():
    coin_symbol = CoinSymbols.btc

    # Test value
    assert coin_symbol.value == 'btc'
    # Test coin name
    assert coin_symbol.name == 'Bitcoin'
    # Test is
    assert coin_symbol is CoinSymbols.btc
    # Test ==
    assert coin_symbol == CoinSymbols.btc


def test_quote_symbols_enum():
    quote_symbol = QuoteSymbols.usd

    # Test value
    assert quote_symbol.value == 'usd'
    # Test quote coin name
    assert quote_symbol.name == 'United States Dollar'
    # Test is
    assert quote_symbol is QuoteSymbols.usd
    # Test ==
    assert quote_symbol == QuoteSymbols.usd
