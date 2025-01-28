import traceback
from typing import Any, Generator

from .._enums import CoinSymbols, QuoteSymbols
from ..abc import APIService
from ..exeptions import GetCoinQuotes as GetCoinQuotesException
from ..response_models import CoinQuotes


class AsyncAnyCoin:
    def __init__(
        self,
        api_services: list[APIService],
    ) -> None:
        self._api_services: list[APIService] = api_services

        if not self._api_services:
            raise RuntimeError('At least one service is required')

    async def get_coin_quotes(
        self,
        coins: list[CoinSymbols],
        quotes_in: list[QuoteSymbols],
    ) -> CoinQuotes:
        for service in self._get_services():
            try:
                return await service.get_coin_quotes(
                    coins=coins, quotes_in=quotes_in
                )
            except GetCoinQuotesException:
                traceback.print_exc()
                continue

        raise GetCoinQuotesException('Unable to get quote through services')

    def _get_services(self) -> Generator[APIService, Any, None]:
        for service in self._api_services:
            yield service
