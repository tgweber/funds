#!/usr/bin/env python

"""Tests for `funds` package."""
import pytest

from funds.report.factory import PDFFundReportFactory
from funds.portfolio import Portfolio

from tests.util import get_fixtures, get_full_portfolio

p = get_full_portfolio()


def test_portfolio_0():
    assert len(p.positions) == 23
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
        if "mand" in f[1] or "sand" in f[1] or "tand" in f[1]:
            continue
        assert len(p.df[p.df["normalized_name"].str.contains(f[1])]) > 0
    for e in p._normalization_endings:
        if e == "ag" or "a-z" in e:
            continue
        assert len(p.df[p.df["normalized_name"].str.contains(
            " {}$".format(e))]) == 0


def test_portfolio_edge_0():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "asian d development")]) == 0


def test_portfolio_edge_1():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "bank of ny mellon")]) == 0


def test_portfolio_edge_2():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "bnp paribas$")]) > 5


def test_portfolio_edge_3():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^boliden$")]) > 2


def test_portfolio_edge_4():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "cisco systems")]) > 2


def test_portfolio_edge_5():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "citigroup")]) > 2


def test_portfolio_edge_6():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "city developments")]) == 0


def test_portfolio_edge_7():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "cppib capital$")]) > 2


def test_portfolio_edge_8():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "e.on")]) > 0


def test_portfolio_edge_9():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "east japan railway")]) == 3


def test_portfolio_edge_10():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "eckert and ziegler")]) == 3


def test_portfolio_edge_11():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "encompass health")]) == 2


def test_portfolio_edge_12():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "engie")]) == 11


def test_portfolio_edge_13():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "fresenius medical care")]) == 9


def test_portfolio_edge_14():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^gpt$")]) == 2


def test_portfolio_edge_15():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^hca healthcare$")]) == 3


def test_portfolio_edge_16():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^iberdrola$")]) == 15


def test_portfolio_edge_17():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^ing$")]) == 11


def test_portfolio_edge_18():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "international flavors and fragrances")]) == 3


def test_portfolio_edge_19():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^johnson controls$")]) == 3


def test_portfolio_edge_20():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^jpmorgan chase$")]) == 5


def test_portfolio_edge_21():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^kbc$")]) == 5


def test_portfolio_edge_22():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^kimberly clark$")]) == 4


def test_portfolio_edge_23():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^koninklijke$")]) == 4


def test_portfolio_edge_24():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^kuehne nagel international$")]) == 2


def test_portfolio_edge_25():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^l oreal$")]) == 5


def test_portfolio_edge_26():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "lowes")]) == 4


def test_portfolio_edge_27():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "m and g")]) == 2


def test_portfolio_edge_28():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "m and t")]) == 1


def test_portfolio_edge_29():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^m$")]) == 2


def test_portfolio_edge_30():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^magna international$")]) == 3


def test_portfolio_edge_31():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^marsh and mclennan$")]) == 2


def test_portfolio_edge_32():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^met life$")]) == 10


def test_portfolio_edge_33():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^metro$")]) == 2


def test_portfolio_edge_34():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^minor international$")]) == 3


def test_portfolio_edge_35():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^mitsubishi chemical$")]) == 2


def test_portfolio_edge_36():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^mondelez$")]) == 4


def test_portfolio_edge_37():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^moodys$")]) == 3


def test_portfolio_edge_38():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^morgan stan$")]) == 6


def test_portfolio_edge_39():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^mtr$")]) == 4


def test_portfolio_edge_40():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^natwest$")]) == 5


def test_portfolio_edge_41():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^nexi$")]) == 3


def test_portfolio_edge_42():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^nextera energy$")]) == 3


def test_portfolio_edge_43():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^novo nordisk$")]) == 6


def test_portfolio_edge_44():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^oracle japan$")]) == 2


def test_portfolio_edge_45():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^orion$")]) == 3


def test_portfolio_edge_46():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^orsted$")]) == 7


def test_portfolio_edge_47():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^prudential financial$")]) == 6


def test_portfolio_edge_48():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^ptc therapeutics$")]) == 3


def test_portfolio_edge_49():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^quebec prov$")]) == 7


def test_portfolio_edge_50():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^red electrica$")]) == 4


def test_portfolio_edge_51():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^ritchie brothers auctioneers$")]) == 2


def test_portfolio_edge_52():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^roche$")]) == 7


def test_portfolio_edge_53():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^s and t$")]) == 1


def test_portfolio_edge_54():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^salesforce.com$")]) == 4


def test_portfolio_edge_55():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^sartorius$")]) == 6


def test_portfolio_edge_56():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^sbab banking$")]) == 3


def test_portfolio_edge_57():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^shopify$")]) == 3


def test_portfolio_edge_58():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^sig combibloc$")]) == 4


def test_portfolio_edge_59():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^snam$")]) == 3


def test_portfolio_edge_60():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^sncf reseau$")]) == 5


def test_portfolio_edge_61():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^stora enso$")]) == 3


def test_portfolio_edge_62():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^swisscom$")]) == 3


def test_portfolio_edge_63():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^t and d$")]) == 1


def test_portfolio_edge_64():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^ericsson$")]) == 5


def test_portfolio_edge_65():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^telefonica deutschland$")]) == 2


def test_portfolio_edge_66():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^telia$")]) == 4


def test_portfolio_edge_67():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^telus$")]) == 2


def test_portfolio_edge_68():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^trane technologies$")]) == 2


def test_portfolio_edge_69():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^travelers$")]) == 2


def test_portfolio_edge_70():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^ubs$")]) == 8


def test_portfolio_edge_71():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^unibail rodamco$")]) == 5


def test_portfolio_edge_72():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^unilever$")]) == 3


def test_portfolio_edge_73():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^united utilities$")]) == 4


def test_portfolio_edge_74():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^upm kymmene$")]) == 4


def test_portfolio_edge_75():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^verizon communications$")]) == 5


def test_portfolio_edge_76():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^vestas wind systems$")]) == 8


def test_portfolio_edge_77():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^west japan railway$")]) == 5


def test_portfolio_edge_78():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^wheaton precious metals$")]) == 2


def test_portfolio_edge_79():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^yamaha$")]) == 5


def test_portfolio_edge_80():
    assert len(p.df[p.df["normalized_name"].str.contains(
        "^zurich insurance$")]) == 4


def test_portfolio_1():
    p = Portfolio()
    with pytest.raises(ValueError):
        p.df.to_csv()
    p.add_position(
        PDFFundReportFactory.create(get_fixtures("classic")),
        get_fixtures("classic")["weight"])

    p.add_position(PDFFundReportFactory.create(get_fixtures("growing")),
                   get_fixtures("growing")["weight"])
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
        get_fixtures("classic")["weight"])
    for e in p._normalization_endings:
        print(e)
        assert len(p.df[p.df["normalized_name"].str.contains(
            " {}$".format(e))]) == 0


def test_portfolio_3():
    p = Portfolio()
    p.add_position(PDFFundReportFactory.create(get_fixtures("tecdax")),
                   get_fixtures("tecdax")["weight"])
    assert len(p.df) == 30


def test_portfolio_4():
    p = Portfolio()
    p.add_position(PDFFundReportFactory.create(get_fixtures("tecdax")),
                   get_fixtures("tecdax")["weight"])
    p.add_position(PDFFundReportFactory.create(get_fixtures("avesco")),
                   get_fixtures("avesco")["weight"])
    assert len(p.df[p.df["normalized_name"].str.contains(r"\d+$")]) == 0
    double_entries = \
        len(p.df.loc[:, "normalized_name"].value_counts().where(
            lambda x: x > 1).dropna())
    assert double_entries == 7
    assert len(p.assets) == len(p.df) - double_entries


def test_portfolio_5():
    p = Portfolio()
    p.add_position(PDFFundReportFactory.create(get_fixtures("digitalisation")),
                   get_fixtures("digitalisation")["weight"])
    assert len(p.df[p.df["normalized_name"].str.endswith("'a'")]) == 0


def test_portfolio_6():
    p = Portfolio()
    p.add_position(PDFFundReportFactory.create(get_fixtures("swisscanto")),
                   get_fixtures("swisscanto")["weight"])
    assert len(p.df[p.df["normalized_name"] == ("applied materials")]) == 2
    p.add_position(PDFFundReportFactory.create(get_fixtures("xtrackers_msci")),
                   get_fixtures("xtrackers_msci")["weight"])
    p.add_position(PDFFundReportFactory.create(get_fixtures("bond_green")),
                   get_fixtures("bond_green")["weight"])
    assert len(p.df[p.df["normalized_name"].str.contains("\xad")]) == 0
    assert len(p.df[p.df["normalized_name"].str.endswith(" lab")]) == 3
    assert len(p.df[p.df["normalized_name"].str.contains("laboratories")]) == 0
    assert len(p.df[p.df["normalized_name"].str.contains("labs")]) == 0
    p.add_position(PDFFundReportFactory.create(get_fixtures("digitalisation")),
                   get_fixtures("digitalisation")["weight"])
    assert len(p.df[p.df["normalized_name"].str.contains("amazon com")]) == 0
