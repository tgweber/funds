#!/usr/bin/env python

"""Tests for `funds` package."""


from funds.report.factory import PDFFundReportFactory
from funds.portfolio import Portfolio

from tests.util import get_fixtures


def test_portfolio_1():
    p = Portfolio()
    p.add_position(
        PDFFundReportFactory.create(get_fixtures("classic")),
        get_fixtures("classic"))
    p.add_position(PDFFundReportFactory.create(get_fixtures("growing")),
                   get_fixtures("growing"))
    assert len(p.positions) == 2
    assert len(p.assets) == 230
    assert len(p.df) == 253
    double_entries = \
        len(p.df.loc[:, "normalized_name"].value_counts().where(
            lambda x: x > 1).dropna())
    assert double_entries == 23
    assert len(p.assets) + double_entries == len(p.df)


def test_portfolio_2():
    p = Portfolio()
    p.add_position(
        PDFFundReportFactory.create(get_fixtures("classic")),
        get_fixtures("classic"))
    assert len(p.positions) == 1
    assert len(p.df) == 129
    p.add_position(PDFFundReportFactory.create(get_fixtures("swisscanto")),
                   get_fixtures("swisscanto"))
    assert len(p.positions) == 2
    assert len(p.df) == 733
    assert len(p.df[p.df["type"] == "bond"]) == 523
    assert len(p.df[p.df["type"] == "share"]) == 210


def test_portfolio_3():
    p = Portfolio()
    p.add_position(PDFFundReportFactory.create(get_fixtures("tecdax")),
                   get_fixtures("tecdax"))
    assert len(p.df) == 30


def test_portfolio_4():
    p = Portfolio()
    p.add_position(PDFFundReportFactory.create(get_fixtures("tecdax")),
                   get_fixtures("tecdax"))
    p.add_position(PDFFundReportFactory.create(get_fixtures("avesco")),
                   get_fixtures("avesco"))
    double_entries = \
        len(p.df.loc[:, "normalized_name"].value_counts().where(
            lambda x: x > 1).dropna())
    assert double_entries == 7
    assert len(p.assets) == len(p.df) - double_entries
