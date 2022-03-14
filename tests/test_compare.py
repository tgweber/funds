from funds.portfolio import Portfolio
from funds.report.factory import PDFFundReportFactory

from tests.util import get_fixtures

tecdax = PDFFundReportFactory.create(get_fixtures("tecdax"))
avesco = PDFFundReportFactory.create(get_fixtures("avesco"))


def test_simple_sim():
    p1 = Portfolio()
    p1.add_position(tecdax, 1)
    p2 = Portfolio()
    p2.add_position(avesco, 1)
    assert tecdax.simple_sim(avesco) == 7/80
    assert avesco.simple_sim(tecdax) == tecdax.simple_sim(avesco)
    assert p1.simple_sim(p2) == tecdax.simple_sim(avesco)
    assert p1.simple_sim(p1) == 1
    assert avesco.simple_sim(avesco) == 1


def test_simple_diff():
    p1 = Portfolio()
    p1.add_position(tecdax, 1)
    p2 = Portfolio()
    p2.add_position(avesco, 1)
    assert tecdax.simple_diff(avesco) == 73/80
    assert avesco.simple_diff(tecdax) == tecdax.simple_diff(avesco)
    assert p1.simple_diff(p2) == tecdax.simple_diff(avesco)
    assert p2.simple_diff(p2) == 0
    assert tecdax.simple_diff(tecdax) == 0
