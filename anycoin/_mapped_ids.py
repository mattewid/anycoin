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

Coin ids: https://coinmarketcap.com/api/
    documentation/v1/#operation/getV1CryptocurrencyMap

Quote Ids: https://coinmarketcap.com/api/documentation/
    v1/#operation/getV1FiatMap
"""


async def get_cmc_coins_ids() -> dict[str, str]:
    return await _get_json_data('mapped_cmc_coin_ids.json')


async def get_cmc_quotes_ids() -> dict[str, str]:
    return await _get_json_data('mapped_cmc_quote_ids.json')


"""
Mapped coingecko ids

Coin ids: https://docs.coingecko.com/
    reference/coins-list

Quote ids: https://docs.coingecko.com/reference/
    simple-supported-currencies
"""


async def get_cgk_coin_ids() -> dict[str, str]:
    return await _get_json_data('mapped_cgk_coin_ids.json')


async def get_cgk_quotes_ids() -> dict[str, str]:
    return await _get_json_data('mapped_cgk_quote_ids.json')
