from .._enums import CoinSymbols, QuoteSymbols
from ..abc import APIService
from ..response_models import CoinQuotes


class BaseAPIService(APIService):
    """Base class for api services."""

    async def get_coin_quotes(
        self,
        coins: list[CoinSymbols],
        quotes_in: list[CoinSymbols],
    ) -> CoinQuotes:
        """..."""

    @staticmethod
    async def get_coin_id_by_symbol(coin_symbol: CoinSymbols) -> str:
        """..."""

    @staticmethod
    async def get_coin_symbol_by_id(coin_id: str) -> CoinSymbols:
        """..."""

    @staticmethod
    async def get_quote_id_by_symbol(
        quote_symbol: QuoteSymbols,
    ) -> str:
        """..."""

    @staticmethod
    async def get_quote_symbol_by_id(
        quote_id: str,
    ) -> QuoteSymbols:
        """..."""

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return f'{self.__class__.__name__}(***)'
