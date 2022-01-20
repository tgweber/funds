from funds.report.factory import PDFParser
from pprint import pprint


def get_fixtures(key):
    fixtures = {
        "classic": {
            "name": "classic",
            "isin": "classic",
            "file": "./tests/artefacts/classic_test.pdf",
            "format": "N|c|i|f|P",
            "weight": 5,
            "pages":
                {"min": 0, "max": 1}
        },
        "growing": {
            "name": "growing",
            "isin": "growing",
            "file": "./tests/artefacts/growing_test.pdf",
            "format": "N|c|i|f|P",
            "weight": 5,
            "pages":
                {"min": 0, "max": 2}
        },
        "rock": {
            "name": "rock",
            "isin": "rock",
            "file": "./tests/artefacts/rock_test.pdf",
            "format": "N|c|i|f|P",
            "weight": 5,
            "pages":
                {"min": 0, "max": 2}
        },
        "klima": {
            "name": "klima",
            "isin": "klima",
            "file": "./tests/artefacts/klima_test.pdf",
            "format": "N|c|i|f|P",
            "weight": 5,
            "pages":
                {"min": 0, "max": 2}
        },
        "swisscanto": {
            "date": "2021-09-30",
            "name": "swisscanto",
            "isin": "something",
            "file": "./tests/artefacts/swisscanto_test.pdf",
            "format": "I|X|i|c|i|i|P",
            "pages":
                {"min": 0, "max": 16},
            "weight": 4
        },
        "murphy":  {
            "date": "2021-09-30",
            "name": "murphy",
            "isin": "something",
            "file": "./tests/artefacts/murphyspitz_test.pdf",
            "format": "X|I|i|c|f|f|P",
            "pages":
                {"min": 0, "max": 1},
            "weight": 3
        },
        "pictet": {
            "date": "2021-09-30",
            "name": "pictet",
            "isin": "pictet",
            "file": "./tests/artefacts/pictet_test.pdf",
            "format": "N|c|f|f|P",
            "pages":
                {"min": 0, "max": 2},
            "weight": 2
        },
        "bond_gov": {
            "date": "2021-09-30",
            "name": "bond_gov",
            "isin": "bond_gov",
            "file": "./tests/artefacts/bond_gov_test.pdf",
            "format": "c|i|B|i|P",
            "pages":
                {"min": 0, "max": 6},
            "weight": 5
        },
        "bond_green": {
            "date": "2021-09-30",
            "name": "bond_green",
            "isin": "bond_green",
            "file": "./tests/artefacts/bond_green_test.pdf",
            "format": "P|i|i|c|B_1|i",
            "pages":
                {"min": 0, "max": 10},
            "weight": 5
        },
        "tecdax": {
            "date": "3000-01-01",
            "weight": "5",
            "name": "tecdax",
            "isin": "DE0005933972",
            "file": "./tests/artefacts/tecdax_test.pdf",
            "format": "N_1|I|s|i|i|i?-|c|f|f|P",
            "pages":
                {"min": 0, "max": 0},
        },
        "avesco": {
            "date": "3000-01-02",
            "weight": "5",
            "name": "avesco",
            "isin": "DE000A1J9FJ5",
            "file": "./tests/artefacts/avesco_test.pdf",
            "format": "N|I|s|i|i|i|c|f|f|P",
            "pages":
                {"min": 0, "max": 1}
        },
        "ubs": {
            "date": "3000-01-02",
            "weight": "5",
            "name": "ubs",
            "isin": "ubs",
            "file": "./tests/artefacts/ubs_test.pdf",
            "format": "N)<!&ubs|i|i|P",
            "pages":
                {"min": 0, "max": 13}
        },
        "xtrackers_msci": {
            "date": "3000-01-02",
            "weight": "5",
            "name": "xtrackers_msci",
            "isin": "xtrackers_msci",
            "file": "./tests/artefacts/xtrackers_msci_test.pdf",
            "format": "N|i|c|i|i|P",
            "pages":
                {"min": 0, "max": 4}
        },
        "xtrackers_wi": {
            "date": "3000-01-02",
            "weight": "5",
            "name": "xtrackers_wi",
            "isin": "xtrackers_wi",
            "file": "./tests/artefacts/xtrackers_wi_test.pdf",
            "format": "i|N(<!&xt1|i|P",
            "pages":
                {"min": 0, "max": 3}
        },
        "ageing": {
            "date": "3000-01-02",
            "weight": "5",
            "name": "ageing",
            "isin": "ageing",
            "file": "./tests/artefacts/ageing_test.pdf",
            "format": "c|i|N~5|i(<!&ish|P(=&2sh",
            "pages":
                {"min": 0, "max": 5}
        },
        "digitalisation": {
            "date": "3000-01-02",
            "weight": "5",
            "name": "digitalisation",
            "isin": "digitalisation",
            "file": "./tests/artefacts/digitalisation_test.pdf",
            "format": "c|i|N~5|i(<!&ish|P(=&2sh",
            "pages":
                {"min": 0, "max": 3}
        },
        "wisdomtree": {
            "date": "3000-01-02",
            "weight": "5",
            "name": "wisdomtree",
            "isin": "wisdomtree",
            "file": "./tests/artefacts/wisdomtree_test.pdf",
            "format": "i|N(<!&riz|i|P",
            "pages":
                {"min": 0, "max": 5}
        },
        "amundi": {
            "date": "3000-01-02",
            "weight": "5",
            "name": "amundi",
            "isin": "amundi",
            "file": "./tests/artefacts/amundi_test.pdf",
            "format": "N|f|f|P",
            "pages":
                {"min": 0, "max": 3}
        },
        "lyxor_energy": {
            "date": "3000-01-02",
            "weight": "5",
            "name": "lyxor_energy",
            "isin": "lyxor_energy",
            "file": "./tests/artefacts/lyxor_energy_test.pdf",
            "format": "I|N_1|s|f|f|c|P",
            "pages":
                {"min": 0, "max": 1}
        },
        "earth": {
            "date": "3000-01-02",
            "weight": "5",
            "name": "earth",
            "isin": "earth",
            "file": "./tests/artefacts/earth_test.pdf",
            "format": "N|I|s|i|i|i|c|f|f|P",
            "pages":
                {"min": 0, "max": 1}
        },
        "rize": {
            "date": "3000-01-02",
            "weight": "5",
            "name": "rize",
            "isin": "rize",
            "file": "./tests/artefacts/rize_test.pdf",
            "format": "i|N(<!&riz|i|P",
            "pages":
                {"min": 0, "max": 2}
        },
        "mobility": {
            "date": "3000-01-02",
            "weight": "5",
            "name": "mobility",
            "isin": "mobility",
            "file": "./tests/artefacts/mobility_test.pdf",
            "format": "P|i|i|c|N|i",
            "pages":
                {"min": 0, "max": 1}
        },

    }
    return fixtures.get(key, None)


def iterate_pages(pages, config):
    for index, page in enumerate(
        range(config["pages"]["min"],
              config["pages"]["max"] + 1)):
        page_as_rows = PDFParser.parse(config["file"],
                                       config["format"],
                                       page,
                                       page)
        pprint(page_as_rows)
        print("Page checked  : {}".format(page))
        print("Assets counted: {}".format(len(page_as_rows)))
        print("Assets speced : {}".format(pages[index]))

        assert len(page_as_rows) == pages[index]
