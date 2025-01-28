from abc import ABCMeta, abstractmethod

from ._enums import CoinSymbols, QuoteSymbols


class APIService(metaclass=ABCMeta):
    """
    Interface for API Service

    API Service control data methods.
    """

    @abstractmethod
    async def get_coin_quotes(
        self,
        coins: list[CoinSymbols],
        quotes_in: list[QuoteSymbols],
    ) -> 'CoinQuotes':
        """..."""

    @staticmethod
    @abstractmethod
    async def get_coin_id_by_symbol(coin_symbol: CoinSymbols) -> str:
        """..."""

    @staticmethod
    @abstractmethod
    async def get_coin_symbol_by_id(coin_id: str) -> CoinSymbols:
        """..."""

    @staticmethod
    @abstractmethod
    async def get_quote_id_by_symbol(
        quote_symbol: QuoteSymbols,
    ) -> str:
        """..."""

    @staticmethod
    @abstractmethod
    async def get_quote_symbol_by_id(
        quote_id: str,
    ) -> QuoteSymbols:
        """..."""


from anycoin.response_models import CoinQuotes  # noqa: E402
