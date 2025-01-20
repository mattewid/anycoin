from .._enums import CoinSymbols
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
    async def get_crypto_id_by_coin_symbol(coin_symbol: CoinSymbols) -> str:
        """..."""

    @staticmethod
    async def get_crypto_coin_symbol_by_id(crypto_id: str) -> CoinSymbols:
        """..."""

    @staticmethod
    async def get_converter_id_by_coin_symbol(coin_symbol: CoinSymbols) -> str:
        """..."""

    @staticmethod
    async def get_converter_coin_symbol_by_id(
        converter_id: str,
    ) -> CoinSymbols:
        """..."""

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return f'{self.__class__.__name__}(***)'
