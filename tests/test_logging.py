"""
Tests amati/logging.py
"""

from amati.logging import Log, LogMixin
from amati.validators.generic import GenericObject
from amati.validators.reference_object import Reference, ReferenceModel

reference1: Reference = ReferenceModel(title="Test", url="https://example.com")

reference2: Reference = ReferenceModel(title="Test", url="https://a.com")

references: Reference = [reference1, reference2]


class Model1(GenericObject):
    value: str

    def test_log(self):
        LogMixin.log(Log(message="Model1", type=ValueError, reference=reference1))


class Model2(GenericObject):
    value: str

    def test_log(self):
        LogMixin.log(Log(message="Model2", type=ValueError, reference=references))


def test_writer():
    with LogMixin.context():
        model1 = Model1(value="a")
        model1.test_log()
        assert LogMixin.logs == [
            Log(message="Model1", type=ValueError, reference=reference1)
        ]

        model2 = Model2(value="b")
        model2.test_log()
        assert LogMixin.logs == [
            Log(message="Model1", type=ValueError, reference=reference1),
            Log(message="Model2", type=ValueError, reference=references),
        ]