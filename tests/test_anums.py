from anycoin import CoinSymbols


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
