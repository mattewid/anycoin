from abc import ABCMeta, abstractmethod

from ._enums import CoinSymbols


class APIService(metaclass=ABCMeta):
    """
    Interface for API Service

    API Service control data methods.
    """

    @abstractmethod
    async def get_coin_quotes(
        self,
        coins: list[CoinSymbols],
        quotes_in: list[CoinSymbols],
    ) -> 'CoinQuotes':
        """..."""

    @staticmethod
    @abstractmethod
    async def get_crypto_id_by_coin_symbol(coin_symbol: CoinSymbols) -> str:
        """..."""

    @staticmethod
    @abstractmethod
    async def get_crypto_coin_symbol_by_id(crypto_id: str) -> CoinSymbols:
        """..."""

    @staticmethod
    @abstractmethod
    async def get_converter_id_by_coin_symbol(coin_symbol: CoinSymbols) -> str:
        """..."""

    @staticmethod
    @abstractmethod
    async def get_converter_coin_symbol_by_id(
        converter_id: str,
    ) -> CoinSymbols:
        """..."""


from anycoin.response_models import CoinQuotes  # noqa: E402
