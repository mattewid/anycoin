import json
from http import HTTPStatus

import httpx

from .._enums import CoinSymbols, QuoteSymbols
from .._mapped_ids import get_cgk_coin_ids as _get_cgk_coin_ids
from .._mapped_ids import get_cgk_quotes_ids as _get_cgk_quotes_ids
from ..cache import (
    Cache,
    _get_cache_key_for_get_coin_quotes_method_params,
    _get_or_set_coin_quotes_cache,
)
from ..exeptions import (
    CoinNotSupportedCGK as CoinNotSupportedCGKException,
)
from ..exeptions import GetCoinQuotes as GetCoinQuotesException
from ..exeptions import (
    QuoteCoinNotSupportedCGK as QuoteCoinNotSupportedCGKException,
)
from ..response_models import CoinQuotes
from .base import BaseAPIService


class CoinGeckoService(BaseAPIService):
    def __init__(
        self,
        api_key: str,
        cache: Cache | None = None,
        cache_ttl: int = 300,
    ) -> None:
        self._api_key = api_key
        self._cache = cache
        self._cache_ttl = cache_ttl

    async def get_coin_quotes(
        self,
        coins: list[CoinSymbols],
        quotes_in: list[QuoteSymbols],
    ) -> CoinQuotes:
        if self._cache is None:
            coin_quotes: CoinQuotes = await self._get_coin_quotes(
                coins=coins, quotes_in=quotes_in
            )
        else:
            cache_key: str = _get_cache_key_for_get_coin_quotes_method_params(
                coins=coins, quotes_in=quotes_in
            )
            coin_quotes: CoinQuotes = await _get_or_set_coin_quotes_cache(
                cache=self._cache,
                key=cache_key,
                coro_func=lambda: self._get_coin_quotes(
                    coins=coins, quotes_in=quotes_in
                ),
                ttl=self._cache_ttl,
            )

        return coin_quotes

    @staticmethod
    async def get_coin_id_by_symbol(coin_symbol: CoinSymbols) -> str:
        coin_ids = await _get_cgk_coin_ids()
        try:
            return coin_ids[coin_symbol.value]
        except KeyError:
            raise CoinNotSupportedCGKException(
                f'Coin {coin_symbol} not supported'
            ) from None

    @staticmethod
    async def get_coin_symbol_by_id(coin_id: str) -> CoinSymbols:
        coin_ids = await _get_cgk_coin_ids()
        coins = list(filter(lambda item: item[1] == coin_id, coin_ids.items()))
        if not coins:
            raise CoinNotSupportedCGKException(
                f'Coin with id {coin_id} not supported'
            )

        coin_symbol_str = coins[0][0]
        return CoinSymbols(coin_symbol_str)

    @staticmethod
    async def get_quote_id_by_symbol(
        quote_symbol: QuoteSymbols,
    ) -> str:
        quote_ids = await _get_cgk_quotes_ids()
        try:
            return quote_ids[quote_symbol.value]
        except KeyError:
            raise QuoteCoinNotSupportedCGKException(
                f'Quote {quote_symbol} not supported'
            ) from None

    @staticmethod
    async def get_quote_symbol_by_id(
        quote_id: str,
    ) -> QuoteSymbols:
        quote_ids = await _get_cgk_quotes_ids()
        coins = list(
            filter(
                lambda item: item[1] == quote_id,
                quote_ids.items(),
            )
        )
        if not coins:
            raise QuoteCoinNotSupportedCGKException(
                f'Quote with id {quote_id} not supported'
            )

        coin_symbol_str = coins[0][0]
        return QuoteSymbols(coin_symbol_str)

    async def _get_coin_quotes(
        self,
        coins: list[CoinSymbols],
        quotes_in: list[QuoteSymbols],
    ) -> CoinQuotes:
        try:
            coin_ids: list[str] = [
                await self.get_coin_id_by_symbol(coin) for coin in coins
            ]
            convert_ids: list[str] = [
                await self.get_quote_id_by_symbol(quote) for quote in quotes_in
            ]
        except CoinNotSupportedCGKException as expt:
            raise GetCoinQuotesException(str(expt)) from expt

        except QuoteCoinNotSupportedCGKException as expt:
            raise GetCoinQuotesException(str(expt)) from expt

        params = {
            'ids': ','.join(coin_ids),
            'vs_currencies': ','.join(convert_ids),
            'precision': 'full',
        }

        raw_data = await self._send_request(
            path='/simple/price', method='get', params=params
        )
        return await CoinQuotes.from_cgk_raw_data(raw_data=raw_data)

    async def _send_request(
        self,
        path: str,
        method: str,
        params: dict | None = None,
    ) -> dict:
        if not path.startswith('/'):
            path = '/' + path  # Add leading slash to path

        headers = {
            'accept': 'application/json',
            'x-cg-pro-api-key': self._api_key,
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.request(
                    method=method,
                    url=(f'https://pro-api.coingecko.com/api/v3{path}'),
                    params=params,
                    headers=headers,
                )
                json_data = response.json()

                if response.status_code == HTTPStatus.OK:  # Success
                    return json_data

                raise GetCoinQuotesException(
                    f'Error retrieving coin quotes. API response: {json_data}'
                )
            except httpx.RequestError as expt:
                raise GetCoinQuotesException(
                    'Error retrieving coin quotes'
                ) from expt
            except json.JSONDecodeError as expt:
                raise GetCoinQuotesException(
                    'Error retrieving coin quotes'
                ) from expt

    def __repr__(self):
        return f"{self.__class__.__name__}(api_key='***')"
