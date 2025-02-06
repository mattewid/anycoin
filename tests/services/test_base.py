from anycoin.services.base import BaseAPIService


def test__repr__():
    service = BaseAPIService()
    assert repr(service) == ('BaseAPIService(***)')


def test__str__():
    service = BaseAPIService()
    assert str(service) == ('BaseAPIService(***)')
