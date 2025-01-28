from dataclasses import dataclass
from enum import Enum


@dataclass
class CoinItem:
    value: str
    name: str


class CoinSymbols(Enum):
    btc = CoinItem('btc', 'Bitcoin')
    eth = CoinItem('eth', 'Ethereum')
    xrp = CoinItem('xrp', 'XRP')
    usdt = CoinItem('usdt', 'Tether')
    sol = CoinItem('sol', 'Solana')
    bnb = CoinItem('bnb', 'BNB')
    doge = CoinItem('doge', 'Dogecoin')
    usdc = CoinItem('usdc', 'USDC')
    ada = CoinItem('ada', 'Cardano')
    trx = CoinItem('trx', 'Tron')
    avax = CoinItem('avax', 'Avalanche')
    ton = CoinItem('ton', 'Toncoin')
    not_ = CoinItem('not', 'Notcoin')
    shib = CoinItem('shib', 'Shiba Inu')
    dot = CoinItem('dot', 'Polkadot')
    ltc = CoinItem('ltc', 'Litecoin')
    bch = CoinItem('bch', 'Bitcoin Cash')
    pepe = CoinItem('pepe', 'Pepe')
    pol = CoinItem('pol', 'Polygon')

    def __new__(cls, item):
        obj = object.__new__(cls)
        obj._value_ = item.value
        obj._name = item.name
        return obj

    @property
    def name(self):
        return self._name


class QuoteSymbols(Enum):
    usd = CoinItem('usd', 'United States Dollar')
    eur = CoinItem('eur', 'Euro')
    brl = CoinItem('brl', 'Brazilian Real')
    rub = CoinItem('rub', 'Russian ruble')
    bdt = CoinItem('bdt', 'Bangladeshi taka')

    def __new__(cls, item):
        obj = object.__new__(cls)
        obj._value_ = item.value
        obj._name = item.name
        return obj

    @property
    def name(self):
        return self._name
