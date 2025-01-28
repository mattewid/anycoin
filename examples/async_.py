import asyncio

from anycoin import AsyncAnyCoin, CoinSymbols, QuoteSymbols
from anycoin.response_models import CoinQuotes
from anycoin.services.coingecko import CoinGeckoService
from anycoin.services.coinmarketcap import CoinMarketCapService

"""
The get_coin_quotes method retrieves-
cryptocurrency quotes from the first-
API service, which in this case is-
CoinMarketCapService. If an error occurs-
and the quote cannot be retrieved, the-
method automatically attempts to fetch the-
quote from the next service, such as-
CoinGeckoService in this example.

Note: You can also use just one API service if you prefer.
"""
api_services = [
    CoinMarketCapService(api_key='<api-key>'),
    CoinGeckoService(api_key='<api-key>'),
]


async def main() -> None:
    anycoin = AsyncAnyCoin(api_services=api_services)

    result: CoinQuotes = await anycoin.get_coin_quotes(
        coins=[
            CoinSymbols.btc,
            CoinSymbols('trx'),  # A string can be passed
        ],
        quotes_in=[QuoteSymbols.usd, QuoteSymbols.eur, QuoteSymbols.brl],
    )
    print(result)


if __name__ == '__main__':
    asyncio.run(main())
