import traceback
from decimal import Decimal
from typing import Any, Generator

from .._enums import CoinSymbols, QuoteSymbols
from ..abc import APIService
from ..exeptions import ConvertCoin as ConvertCoinException
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

    async def convert_coin(
        self,
        amount: int | float | Decimal,
        from_coin: CoinSymbols | QuoteSymbols,
        to_coin: CoinSymbols | QuoteSymbols,
    ) -> Decimal:
        if isinstance(from_coin, CoinSymbols) and isinstance(
            to_coin, QuoteSymbols
        ):
            result: CoinQuotes = await self.get_coin_quotes(
                coins=[from_coin],
                quotes_in=[to_coin],
            )
            coin_quote: Decimal = result.coins[from_coin].quotes[to_coin].quote
            return Decimal(str(amount)) * coin_quote

        elif isinstance(from_coin, CoinSymbols) and isinstance(
            to_coin, CoinSymbols
        ):
            quote_in = QuoteSymbols.usd

            result: CoinQuotes = await self.get_coin_quotes(
                coins=[from_coin, to_coin],
                quotes_in=[quote_in],
            )
            from_rate: Decimal = result.coins[from_coin].quotes[quote_in].quote
            to_rate: Decimal = result.coins[to_coin].quotes[quote_in].quote
            return (Decimal(str(amount)) * from_rate) / to_rate

        elif isinstance(from_coin, QuoteSymbols) and isinstance(
            to_coin, CoinSymbols
        ):
            result: CoinQuotes = await self.get_coin_quotes(
                coins=[to_coin],
                quotes_in=[from_coin],
            )
            to_rate: Decimal = result.coins[to_coin].quotes[from_coin].quote
            return Decimal(str(amount)) / to_rate

        elif isinstance(from_coin, QuoteSymbols) and isinstance(
            to_coin, QuoteSymbols
        ):
            coin_symbol_reference = CoinSymbols.usdt

            result: CoinQuotes = await self.get_coin_quotes(
                coins=[coin_symbol_reference],
                quotes_in=[from_coin, to_coin],
            )
            rates = result.coins[coin_symbol_reference]

            from_rate: Decimal = rates.quotes[from_coin].quote
            to_rate: Decimal = rates.quotes[to_coin].quote
            return (Decimal(str(amount)) / from_rate) * to_rate

        raise ConvertCoinException(
            f'Invalid conversion from {from_coin} to {to_coin}'
        )

    def _get_services(self) -> Generator[APIService, Any, None]:
        for service in self._api_services:
            yield service
