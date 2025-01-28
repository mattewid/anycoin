# ruff: noqa: PLC2701

import pytest

from anycoin import CoinSymbols, QuoteSymbols
from anycoin._mapped_ids import (
    get_cgk_coin_ids,
    get_cgk_quotes_ids,
    get_cmc_coins_ids,
    get_cmc_quotes_ids,
)

pytestmark: pytest.MarkDecorator = pytest.mark.asyncio(loop_scope='session')


async def test_mapped_cmc_coin_ids_keys_is_valid():
    data: dict = await get_cmc_coins_ids()

    for coin_symbol in data.keys():
        # The CoinSymbols enumeration will-
        # raise an error if the key is not a valid member
        CoinSymbols(coin_symbol)


async def test_mapped_cmc_quote_ids_keys_is_valid():
    data: dict = await get_cmc_quotes_ids()

    for coin_symbol in data.keys():
        # The QuoteSymbols enumeration will-
        # raise an error if the key is not a valid member
        QuoteSymbols(coin_symbol)


async def test_mapped_cgk_coin_ids_keys_is_valid():
    data: dict = await get_cgk_coin_ids()

    for coin_symbol in data.keys():
        # The CoinSymbols enumeration will-
        # raise an error if the key is not a valid member
        CoinSymbols(coin_symbol)


async def test_mapped_cgk_quote_ids_keys_is_valid():
    data: dict = await get_cgk_quotes_ids()

    for coin_symbol in data.keys():
        # The QuoteSymbols enumeration will-
        # raise an error if the key is not a valid member
        QuoteSymbols(coin_symbol)
