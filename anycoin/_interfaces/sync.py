import atexit
import threading
from contextlib import ExitStack
from decimal import Decimal
from functools import partial

from anyio.from_thread import BlockingPortal, start_blocking_portal

from .._enums import CoinSymbols, QuoteSymbols
from ..abc import APIService
from ..response_models import CoinQuotes
from .async_ import AsyncAnyCoin


class AnyCoin:
    def __init__(
        self,
        api_services: list[APIService],
    ) -> None:
        self._api_services: list[APIService] = api_services

        if not self._api_services:
            raise RuntimeError('At least one service is required')

        self._async_instance = AsyncAnyCoin(
            api_services=api_services,
        )
        self._lock = threading.Lock()
        self._exit_stack = None
        self._portal = None

    def get_coin_quotes(
        self,
        coins: list[CoinSymbols],
        quotes_in: list[QuoteSymbols],
    ) -> CoinQuotes:
        portal: BlockingPortal = self._get_portal()
        return portal.call(
            partial(
                self._async_instance.get_coin_quotes,
                coins=coins,
                quotes_in=quotes_in,
            )
        )

    def convert_coin(
        self,
        amount: int | float | Decimal,
        from_coin: CoinSymbols | QuoteSymbols,
        to_coin: CoinSymbols | QuoteSymbols,
    ) -> Decimal:
        portal: BlockingPortal = self._get_portal()
        return portal.call(
            partial(
                self._async_instance.convert_coin,
                amount=amount,
                from_coin=from_coin,
                to_coin=to_coin,
            )
        )

    def _get_portal(self) -> BlockingPortal:
        """Thread portal for working with AsyncAnyCoin"""
        with self._lock:
            if self._portal is None:
                if self._exit_stack is None:
                    self._exit_stack = ExitStack()
                    atexit.register(self._exit_stack.close)

                self._portal: BlockingPortal = self._exit_stack.enter_context(
                    start_blocking_portal()
                )

        return self._portal
