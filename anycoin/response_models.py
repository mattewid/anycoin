from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field

from ._enums import CoinSymbols, QuoteSymbols


class QuoteRow(BaseModel):
    quote: Decimal


class CoinRow(BaseModel):
    quotes: dict[QuoteSymbols, QuoteRow]


class CoinQuotes(BaseModel):
    coins: dict[CoinSymbols, CoinRow]
    api_service: Literal['coinmarketcap', 'coingecko'] = Field(
        description='API Service Name'
    )
    raw_data: dict = Field(description='Raw API response data')

    @staticmethod
    async def from_cmc_raw_data(raw_data: dict) -> 'CoinQuotes':
        from anycoin.services.coinmarketcap import (  # noqa: PLC0415
            CoinMarketCapService,
        )

        async def get_coin_quotes(coin_id) -> dict[CoinSymbols, QuoteRow]:
            quotes: dict[CoinSymbols, QuoteRow] = {}
            for quote_coin_id, quote_data in raw_data['data'][coin_id][
                'quote'
            ].items():
                quote_coin_symbol: QuoteSymbols = (
                    await CoinMarketCapService.get_quote_symbol_by_id(
                        quote_id=str(quote_coin_id)
                    )
                )
                quotes[quote_coin_symbol] = QuoteRow(
                    quote=Decimal(str(quote_data['price'])),
                )

            return quotes

        coins_data: dict[CoinSymbols, CoinRow] = {}
        for coin_id, coin_data in raw_data['data'].items():
            coin_symbol: CoinSymbols = (
                await CoinMarketCapService.get_coin_symbol_by_id(
                    coin_id=str(coin_id)
                )
            )
            quotes: dict[CoinSymbols, QuoteRow] = await get_coin_quotes(
                coin_id
            )
            coins_data[coin_symbol] = CoinRow(quotes=quotes)

        return CoinQuotes(
            coins=coins_data,
            api_service='coinmarketcap',
            raw_data=raw_data,
        )

    @staticmethod
    async def from_cgk_raw_data(raw_data: dict) -> 'CoinQuotes':
        from anycoin.services.coingecko import (  # noqa: PLC0415
            CoinGeckoService,
        )

        async def get_coin_quotes(coin_id) -> dict[CoinSymbols, QuoteRow]:
            quotes: dict[CoinSymbols, QuoteRow] = {}
            for quote_coin_id, quote_value in raw_data[coin_id].items():
                quote_coin_symbol: QuoteSymbols = (
                    await CoinGeckoService.get_quote_symbol_by_id(
                        quote_id=str(quote_coin_id)
                    )
                )
                quotes[quote_coin_symbol] = QuoteRow(
                    quote=Decimal(str(quote_value)),
                )

            return quotes

        coins_data: dict[CoinSymbols, CoinRow] = {}
        for coin_id, coin_data in raw_data.items():
            coin_symbol: CoinSymbols = (
                await CoinGeckoService.get_coin_symbol_by_id(
                    coin_id=str(coin_id)
                )
            )
            quotes: dict[CoinSymbols, QuoteRow] = await get_coin_quotes(
                coin_id
            )
            coins_data[coin_symbol] = CoinRow(quotes=quotes)

        return CoinQuotes(
            coins=coins_data,
            api_service='coingecko',
            raw_data=raw_data,
        )

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return (
            f"CoinQuotes(coins={self.coins}, api_service='{self.api_service}')"
        )
