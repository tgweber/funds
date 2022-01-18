#!/usr/bin/env python

"""Tests for `funds` package."""

from datetime import datetime

from funds.report.factory import \
        PDFFundReportFactory, \
        PDFParser, RowParser, \
        get_bond

from tests.util import get_fixtures, iterate_pages


def test_get_bond():
    assert get_bond("bname 0.6123% 12/04/2929") == \
        ["bname",
         0.6123,
         datetime.strptime("12/04/2929",
                           "%d/%m/%Y")]
    assert get_bond("bname 0.6123% 12.04.2929") == \
        ["bname",
         0.6123,
         datetime.strptime("12.04.2929",
                           "%d.%m.%Y")]

    assert get_bond("bname 0.6123% (12/04/2929)") == \
        ["bname",
         0.6123,
         datetime.strptime("12.04.2929",
                           "%d.%m.%Y")]
    assert get_bond("bname 0.6123% 1243") == ["bname", 0.6123, None]
    assert get_bond("bname 0,6123% 1243") == ["bname", 0.6123, None]
    assert get_bond("Danone 1.0% 21-Perp") == ["Danone", 1.0, None]
    assert get_bond(
        "4.0000 % Energiekontor Finanzanlagen Anleihe (2024/26-39)") == \
        ["Energiekontor Finanzanlagen Anleihe", 4.0, None]
    assert get_bond("7.2500 % Hylea Group S.A. EO-Anl. 2017(22)") == \
        ["Hylea Group S.A. EO-Anl.", 7.25, None]
    assert get_bond(
        "6.5000 % DE-VAU-GE Gesundkostwerk Dt. IHS (2023/2025)") == \
        ["DE-VAU-GE Gesundkostwerk Dt. IHS", 6.5, None]
    assert get_bond("6.7500 % SoWiTec group GmbH IHS. (2021/2023)") == \
        ["SoWiTec group GmbH IHS.", 6.75, None]


def test_pdf_creation_classic_1():
    config = get_fixtures("classic")
    iterate_pages([65, 64], config)

    fundReport = PDFFundReportFactory.create(config)
    assert str(fundReport.date) == "2022-01-18 00:00:00"

    assert fundReport.assets[0].name == "Sims Ltd."
    assert fundReport.assets[0].percentage == 0.73
    assert fundReport.assets[-1].name == "Unite Group Plc."
    assert fundReport.assets[-1].percentage == 0.35
    assert "{:.2f}".format(fundReport.total_percentage()) == "94.01"
    assert len(fundReport.bonds) == 0
    assert len(fundReport.shares) == len(fundReport.assets)


def test_pdf_creation_growing_1():
    config = get_fixtures("growing")
    iterate_pages([36, 69, 19], config)
    fundReport = PDFFundReportFactory.create(config)
    assert len(fundReport.assets) == 124
    assert fundReport.assets[0].name == "IDP Education Ltd."
    assert fundReport.assets[0].percentage == 0.46
    assert fundReport.assets[-1].name == "Gland Pharma Ltd."
    assert fundReport.assets[-1].percentage == 1.32
    assert "{:.1f}".format(fundReport.total_percentage()) == "96.8"


def test_pdf_creation_rock_1():
    iterate_pages([30, 75, 15], get_fixtures("rock"))


def test_pdf_creation_klima_1():
    iterate_pages([33, 69, 46], get_fixtures("klima"))


def test_pdf_creation_ms_1():
    config = get_fixtures("murphy")
    fundReport = PDFFundReportFactory.create(config)
    assert len(fundReport.shares) == 31
    assert len(fundReport.bonds) == 12
    assert len(fundReport.assets) == 43
    iterate_pages([39, 4], config)


def test_pdf_creation_swisscanto_1():
    config = get_fixtures("swisscanto")
    pages_len = [25, 34, 38, 34, 43, 48, 38, 46, 41, 36, 36, 43, 51, 47, 18,
                 21, 5]
    iterate_pages(pages_len, config)

    b = RowParser.parse(PDFParser.parse(config["file"],
                                        config["format"],
                                        5,
                                        5)[1],
                        config["format"])
    assert b.name == "Danone"
    fundReport = PDFFundReportFactory.create(config)

    assert len(fundReport.assets) == 604
    assert len(fundReport.shares) == 81
    assert len(fundReport.bonds) == 523


def test_pdf_creation_ubs_1():
    config = get_fixtures("ubs")
    pages_len = [39, 44, 41, 44, 34, 46, 45, 35, 40, 41, 44, 41, 32, 6]
    iterate_pages(pages_len, config)
    a = RowParser.parse(PDFParser.parse(config["file"],
                                        config["format"], 11, 11)[0],
                        config["format"])
    assert a.name == "Tokyo Electron"


def test_pdf_creation_pictet_1():
    config = get_fixtures("pictet")
    pages_len = [22, 34, 1]
    iterate_pages(pages_len, config)
    fundReport = PDFFundReportFactory.create(config)
    assert len(fundReport.assets) == 57
    assert len(fundReport.shares) == 57
    assert fundReport.assets[0].name == "CHRISTIAN HANSEN HOLDING"
    assert fundReport.assets[0].percentage == 0.34
    assert fundReport.assets[-1].name == \
        "PICTET - SHORT-TERM MONEY MARKET USD Z"
    assert fundReport.assets[-1].percentage == 3.22
    assert "{:.2f}".format(fundReport.total_percentage()) == "99.83"


def test_pdf_creation_lyxor_1():
    iterate_pages([25, 14], get_fixtures("lyxor_energy"))


def test_pdf_creation_tecdax_1():
    iterate_pages([30], get_fixtures("tecdax"))


def test_pdf_creation_earth_1():
    iterate_pages([30, 7], get_fixtures("earth"))


def test_pdf_creation_wi_1():
    iterate_pages([55, 38, 51, 45], get_fixtures("xtrackers_wi"))


def test_pdf_creation_msci_1():
    iterate_pages([34, 48, 48, 48, 30], get_fixtures("xtrackers_msci"))


def test_pdf_creation_ageing_1():
    iterate_pages([44, 52, 41, 73, 84, 1], get_fixtures("ageing"))


def test_pdf_creation_digitalisation_1():
    iterate_pages([35, 38, 85, 7], get_fixtures("digitalisation"))


def test_pdf_creation_govbond_1():
    config = get_fixtures("bond_gov")
    iterate_pages([48, 52, 54, 62, 78, 57, 72], config)
    fundReport = PDFFundReportFactory.create(config)
    # 423 is not manually calculated
    assert len(fundReport.assets) == 423
    assert len(fundReport.bonds) == 423
    assert "{:.2f}".format(fundReport.total_percentage()) == "99.09"
    assert fundReport.assets[0].name == "Republic of Austria Government Bond"
    assert fundReport.assets[0].kupon == 0.0
    assert fundReport.assets[0].due.strftime("%Y-%m-%d") == "2022-09-20"
    assert fundReport.assets[0].percentage == 0.01
    assert fundReport.assets[-1].name == "Spain Government Bond"
    assert fundReport.assets[-1].kupon == 6.0
    assert fundReport.assets[-1].due.strftime("%Y-%m-%d") == "2029-01-31"
    assert fundReport.assets[-1].percentage == 0.5


def test_pdf_creation_greenbond_1():
    iterate_pages([44, 43, 44, 43, 43, 43, 44, 43, 39, 40, 33],
                  get_fixtures("bond_green"))


def test_pdf_creation_rize_1():
    iterate_pages([13, 24, 8], get_fixtures("rize"))


def test_pdf_creation_wisdomtree_1():
    iterate_pages([15, 17, 19, 18, 16, 18], get_fixtures("wisdomtree"))


def test_pdf_creation_amundi():
    iterate_pages([95, 102, 95, 80], get_fixtures("amundi"))


def test_pdf_creation_avesco_1():
    iterate_pages([38, 19], get_fixtures("avesco"))


def test_pdf_creation_mobility_1():
    iterate_pages([44, 15], get_fixtures("mobility"))
