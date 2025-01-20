# ruff: noqa: PLC2701

import pytest

from anycoin import CoinSymbols
from anycoin._mapped_ids import (
    get_cgk_converters_ids,
    get_cgk_crypto_ids,
    get_cmc_converters_ids,
    get_cmc_crypto_ids,
)

pytestmark: pytest.MarkDecorator = pytest.mark.asyncio(loop_scope='session')


async def test_mapped_cmc_crypto_ids_keys_is_valid():
    data: dict = await get_cmc_crypto_ids()

    for coin_symbol in data.keys():
        # The CryptoSymbols enumeration will-
        # raise an error if the key is not a valid member
        CoinSymbols(coin_symbol)


async def test_mapped_cmc_converters_ids_keys_is_valid():
    data: dict = await get_cmc_converters_ids()

    for coin_symbol in data.keys():
        # The CryptoSymbols enumeration will-
        # raise an error if the key is not a valid member
        CoinSymbols(coin_symbol)


async def test_mapped_cgk_crypto_ids_keys_is_valid():
    data: dict = await get_cgk_crypto_ids()

    for coin_symbol in data.keys():
        # The CryptoSymbols enumeration will-
        # raise an error if the key is not a valid member
        CoinSymbols(coin_symbol)


async def test_mapped_cgk_converters_ids_keys_is_valid():
    data: dict = await get_cgk_converters_ids()

    for coin_symbol in data.keys():
        # The CryptoSymbols enumeration will-
        # raise an error if the key is not a valid member
        CoinSymbols(coin_symbol)
