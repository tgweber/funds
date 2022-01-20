#!/usr/bin/env python

"""Tests for `funds` package."""
import pytest

from funds.report.factory import PDFFundReportFactory
from funds.portfolio import Portfolio

from tests.util import get_fixtures


def test_portfolio_0():
    p = Portfolio()

    funds = [
        "ageing",
        "amundi",
        "avesco",
        "bond_gov",
        "bond_green",
        "classic",
        "digitalisation",
        "earth",
        "growing",
        "klima",
        "lyxor_energy",
        "mobility",
        "murphy",
        "pictet",
        "rize",
        "rock",
        "swisscanto",
        "tecdax",
        "ubs",
        "wisdomtree",
        "xtrackers_msci",
        "xtrackers_wi",
    ]
    for fund in funds:
        p.add_position(PDFFundReportFactory.create(get_fixtures(fund)),
                       get_fixtures(fund))
    assert len(p.positions) == 22
    assert "normalized_name" in p.df.columns
    assert "sid_total_weight" in p.assets.columns
    assert p.assets.loc[:, "sid_total_weight"].sum() < 100
    assert p.assets.loc[:, "sid_total_weight"].sum() > 90
    double_entries = \
        len(p.df.loc[:, "normalized_name"].value_counts().where(
            lambda x: x > 1).dropna())
    assert len(p.assets) + double_entries <= len(p.df)

    for e in p._erase:
        assert len(p.df[p.df["normalized_name"].str.contains(e)]) == 0
    for f in p._find_replace:
        import pprint
        pprint.pprint(f)
        assert len(p.df[p.df["normalized_name"].str.contains(f[1])]) > 0
    for e in p._normalization_endings:
        if e == "ag":
            continue
        assert len(p.df[p.df["normalized_name"].str.contains(
            " {}$".format(e))]) == 0
    # edge cases:
    assert len(p.df[p.df["normalized_name"].str.contains(
        "asian d development")]) == 0
    assert len(p.df[p.df["normalized_name"].str.contains(
        "bank of ny mellon")]) == 0
    assert len(p.df[p.df["normalized_name"].str.contains(
        "bnp paribas$")]) > 5
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^boliden$")]) > 2
    assert len(p.df[p.df["normalized_name"].str.contains(
        "cisco systems")]) > 2
    assert len(p.df[p.df["normalized_name"].str.contains(
        "citigroup")]) > 2
    assert len(p.df[p.df["normalized_name"].str.contains(
        "city developments")]) == 0
    assert len(p.df[p.df["normalized_name"].str.contains(
        "cppib capital$")]) > 2
    assert len(p.df[p.df["normalized_name"].str.contains(
        "e.on")]) > 0
    assert len(p.df[p.df["normalized_name"].str.contains(
        "east japan railway")]) == 3
    assert len(p.df[p.df["normalized_name"].str.contains(
        "eckert and ziegler")]) == 3


def test_portfolio_1():
    p = Portfolio()
    with pytest.raises(ValueError):
        p.df.to_csv()
    p.add_position(
        PDFFundReportFactory.create(get_fixtures("classic")),
        get_fixtures("classic"))

    p.add_position(PDFFundReportFactory.create(get_fixtures("growing")),
                   get_fixtures("growing"))
    assert len(p.positions) == 2
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
    for e in p._normalization_endings:
        print(e)
        assert len(p.df[p.df["normalized_name"].str.contains(
            " {}$".format(e))]) == 0


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
    assert len(p.df[p.df["normalized_name"].str.contains(r"\d+$")]) == 0
    double_entries = \
        len(p.df.loc[:, "normalized_name"].value_counts().where(
            lambda x: x > 1).dropna())
    assert double_entries == 7
    assert len(p.assets) == len(p.df) - double_entries


def test_portfolio_5():
    p = Portfolio()
    p.add_position(PDFFundReportFactory.create(get_fixtures("digitalisation")),
                   get_fixtures("digitalisation"))
    assert len(p.df[p.df["normalized_name"].str.endswith("'a'")]) == 0


def test_portfolio_6():
    p = Portfolio()
    p.add_position(PDFFundReportFactory.create(get_fixtures("swisscanto")),
                   get_fixtures("swisscanto"))
    assert len(p.df[p.df["normalized_name"] == ("applied materials")]) == 2
    p.add_position(PDFFundReportFactory.create(get_fixtures("xtrackers_msci")),
                   get_fixtures("xtrackers_msci"))
    p.add_position(PDFFundReportFactory.create(get_fixtures("bond_green")),
                   get_fixtures("bond_green"))
    assert len(p.df[p.df["normalized_name"].str.contains("\xad")]) == 0
    assert len(p.df[p.df["normalized_name"].str.endswith(" lab")]) == 3
    assert len(p.df[p.df["normalized_name"].str.contains("laboratories")]) == 0
    assert len(p.df[p.df["normalized_name"].str.contains("labs")]) == 0
    p.add_position(PDFFundReportFactory.create(get_fixtures("digitalisation")),
                   get_fixtures("digitalisation"))
    assert len(p.df[p.df["normalized_name"].str.contains("amazon com")]) == 0
