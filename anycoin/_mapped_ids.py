import json

import aiocache
from anyio import Path, open_file


@aiocache.cached(ttl=None, cache=aiocache.Cache.MEMORY)
async def _get_json_data(file_name: str) -> dict:
    path_resolved = await Path(__file__).resolve()
    file_path = path_resolved.parent.joinpath('_data', file_name)
    async with await open_file(file_path, encoding='utf-8') as file:
        return json.loads(await file.read())


"""
Mapped coinmarketcap ids

Crypto ids: https://coinmarketcap.com/api/
    documentation/v1/#operation/getV1CryptocurrencyMap

Fiat Ids: https://coinmarketcap.com/api/documentation/
    v1/#operation/getV1FiatMap
"""


async def get_cmc_crypto_ids() -> dict[str, str]:
    return await _get_json_data('mapped_cmc_crypto_ids.json')


async def get_cmc_converters_ids() -> dict[str, str]:
    return await _get_json_data('mapped_cmc_converter_ids.json')


"""
Mapped coingecko ids

Crypto ids: https://docs.coingecko.com/
    reference/coins-list

Fiat ids: https://docs.coingecko.com/reference/
    simple-supported-currencies
"""


async def get_cgk_crypto_ids() -> dict[str, str]:
    return await _get_json_data('mapped_cgk_crypto_ids.json')


async def get_cgk_converters_ids() -> dict[str, str]:
    return await _get_json_data('mapped_cgk_converter_ids.json')
