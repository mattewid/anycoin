from anycoin.services.base import BaseAPIService


def test_repr():
    service = BaseAPIService()
    assert repr(service) == ('BaseAPIService(***)')
