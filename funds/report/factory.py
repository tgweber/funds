from datetime import datetime
import fitz
import re
import regex

from funds.report import FundReport
from funds.asset import Bond, Share


class PDFFundReportFactory(object):
    """ Factory from PDF for fund reports

    Methods

    ------
    create(config_path) -> FundReport
        Factory method returning a FundReport object appropriate
        for the given type and payload
    """

    def create(config):
        """ Creates a FundReport object according to the config

        Parameters
        ----------
        config_path: dict
            * file (path to PDF file)
            * format (format for the PDF file to detect rows)
            * pages
                * min: page number (0-based) to start parsing (included)
                * max: page number (0-based) to end parsing (included)

        Returns
        -------
        FundReport: The created fund report
        """
        if "date" in config.keys():
            date = datetime.strptime(config["date"], "%Y-%m-%d")
        else:
            date = PDFParser.get_date(config["file"])

        fundReport = FundReport(config["isin"], config["name"], date)
        for row in PDFParser.parse(
            config["file"],
            config["format"],
            config["pages"]["min"],
            config["pages"]["max"]
        ):
            fundReport.assets.append(RowParser.parse(row, config["format"]))
        return fundReport


class PDFParser(object):
    def get_date(file_path):
        with fitz.open(file_path) as doc:
            return datetime.strptime(
                doc.metadata["creationDate"][2:10], "%Y%m%d")

    def parse(file_path, row_format, min_page, max_page):
        rows = []
        r = get_regex(row_format)
        pages = range(min_page, max_page + 1)
        with fitz.open(file_path) as doc:
            for page in pages:
                rows.extend(
                    [row for row in regex.findall(r,
                                                  doc[page].get_text(
                                                      "block"))])
        return rows


class RowParser(object):
    def parse(row, row_format):
        if '|' in row_format:
            sec_type = "share"
            isin = None
            kupon = None
            due = None
            for idx, col in enumerate(row_format.split('|')):
                payload = " ".join(row[idx].strip().split())
                if col[0] == 'N':
                    name = payload
                elif col[0] == 'P':
                    percentage = float(payload.replace(",", "."))
                elif col[0] == 'I':
                    isin = payload
                elif col[0] == 'X' or col[0] == 'B':
                    [name, kupon, due] = get_bond(payload)
                    if kupon is None and due is None:
                        sec_type = "share"
                    else:
                        sec_type = "bond"
        if sec_type == "bond":
            asset = Bond(name, percentage, kupon, due, isin)
        else:
            asset = Share(name, percentage, isin)
        return asset


def get_regex(string):
    if '|' in string:
        regex_parts = []
        switch_types = {
            # Large numbers are used in the row parser
            # name of a share
            'N': r'(?=.*[a-zA-Z])(\S+(?:\ *\S+)*)',
            # name of a share or a bond (complex)
            'X': r'(?=.*[a-zA-Z])(.+)',
            # a float that is also the percentage
            'P': r'([0-9]{1,2}(?:\.|,)[0-9]+)',
            # an ISIN number maybe invalid (ending with M)
            'I': r'([A-Z]{2}[A-Z0-9]{9}[0-9M])',
            # a Bond
            'B': r"""(.*\s+                             # Bond name
                (?:(?:\d(?:\.\d{1,3}){0,1}%)\s*){0,1}   # kupon
                (?:
                    (?:\d\d/\d\d/\d\d\d\d)              # date
                    |.*\(ISIN.*)).*                     # or: (ISIN number)
            """,
            # Small numbers are just to match only rows
            # (the information is not used)
            # standard separator
            '|': r'[\n\r\s]+',
            # a currency
            'c': r'({})'.format(get_currencies_matcher()),
            # an integer
            'i': r'([0-9]{1,3}(?:\ *(?:\.|,){0,1}[0-9]{3})*)',
            # any float
            'f': r'([0-9]{1,3}(?:(?:\.|,)[0-9]{3})*(?:,|.[0-9]+)*)',
            # any string
            's': r'(?=.*[a-zA-Z])(.+)',
        }
        # TODO: Try to turn these into lookups to switch_types
        switch_look = {
            "ubs": r'[0-9]{{1,3}}(?:\.[0-9]{{3}})+\s*(?:{})\s*'.format(
                get_currencies_matcher()
            ),
            "xt1": r',\d\d[\n\r\s]',
            "ish": r'(?:{})\s*'.format(get_currencies_matcher()),
            "2sh": r'\d+,\d+',
            "riz": r'\d+\.\d+[\n\r\s]+',
        }

        for column in string.split('|'):
            regex_part = switch_types[column[0]]
            # place a look(ahead|behind)-directive before the type
            if "(" in column:
                [look_instructor, key] = column[2:].split('&')
                regex_part = "(?{}{}){}".format(look_instructor,
                                                switch_look[key],
                                                regex_part)
            # place a look(ahead|behind)-directive after the type
            elif ")" in column:
                [look_instructor, key] = column[2:].split('&')
                regex_part = "{}(?{}{})".format(regex_part,
                                                look_instructor,
                                                switch_look[key])
            # the name contains a specific amount of newlines,
            # a number following _ specifies how many
            elif '_' in column:
                if column[0] == 'B':
                    regex_part = r"""
                        (\S+(:?\ *\S+)*(:?\n){{0,{}}}\S+(:?\ *\S+)*\s+ # name
                        (?:(?:\d(?:\.\d{{1,3}}){{0,1}}%)\s*){{0,1}}    # kupon
                        (?:
                            (?:\d\d/\d\d/\d\d\d\d).*                   # date
                            |.*\(ISIN\s+.*\)                           # isin
                        ))
                    """.format(column[2:3])
                elif column[0] == 'N':
                    regex_part = r"""
                        ((?=.*[a-zA-Z])\S+(?:\ *\S+)*\ *(?:\n){{0,{}}}.*)
                    """.format(column[2:3])
            # contains a specific amount of space + newlines,
            # a number following ~ specifies how many
            elif '~' in column:
                regex_part = r'([^\n]+(?:(?:\ \n){{{}}}){{0,1}}.*)'.format(
                    column[2:3])
            # contains a single char that could be an alternate for the type
            elif '?' in column:
                regex_part = '(?:' + regex_part + '|' + column[2:3] + ')'

            regex_parts.append(regex_part)
        return regex.compile(switch_types['|'].join(regex_parts), re.X,
                             re.VERBOSE)


def get_bond(payload):
    regex_parts = [
        # leave 0 blank
        r'',
        # match bond's name:
        r'([a-zA-Z .-]+)',
        # match bond's kupon:
        r'(\d(?:(?:\.|,)\d{1,4}){0,1})\s*%',
        # match bond's due date:
        r'\(*(\d{1,2}(?:/|\.)\d{1,2}(?:/|\.)\d{2,4})\)*'
    ]

    runs = [
        [r'{}(?:\s+|\.){}\s*(?:\d\d-){{0,1}}{}.*', 1, 2, 3],
        [r'{}\s+{}\s*{}.*',                        2, 1, 3],
        [r'{}(?:\s+|\.){}.*{}',                    1, 2, 0],
        [r'{}\s+{}.*{}',                           2, 1, 0],
        [r'{}(?:\s+|\.){}(?:\d\d-){{0,1}}{}.*',    1, 0, 2],
        [r'{}',                                    1, 0, 0]
    ]
    bkupo = None
    bdate = None
    for run in runs:
        regex = run[0].format(
            regex_parts[run[1]],
            regex_parts[run[2]],
            regex_parts[run[3]]
        )
        m = re.search(regex, payload)
        if m:
            name_match = m.group(run[1]).strip()
            kupo_match = m.group(run[2])
            date_match = m.group(run[3])
            if run[2] > 0 and kupo_match:
                bkupo = float(kupo_match.replace(',', '.'))
            if run[3] > 0 and date_match:
                for date_format in [
                    "%d.%m.%y",
                    "%d.%m.%Y",
                    "%d/%m/%y",
                    "%d/%m/%Y"
                ]:
                    try:
                        bdate = datetime.strptime(date_match, date_format)
                    except ValueError:
                        continue
                    if bdate is not None:
                        break
            return [name_match, bkupo, bdate]


def get_currencies_matcher():
    currencies = [
        "AED", "AFN", "ALL", "AMD", "ANG", "ANG", "AOA", "ARS", "AUD", "AWG",
        "AZN", "BAM", "BBD", "BDT", "BGN", "BHD", "BIF", "BMD", "BND", "BOB",
        "BOV", "BRL", "BSD", "BTN", "BWP", "BYN", "BZD", "CAD", "CDF", "CHE",
        "CHF", "CHW", "CLF", "CLP", "CNY", "COP", "COU", "CRC", "CUC", "CUP",
        "CVE", "CZK", "DJF", "DKK", "DOP", "DZD", "EGP", "ERN", "ETB", "EUR",
        "FJD", "FKP", "GBP", "GEL", "GHS", "GIP", "GMD", "GNF", "CNH", "GTQ",
        "GYD", "HKD", "HNL", "HRK", "HTG", "HUF", "IDR", "ILS", "INR", "IQD",
        "IRR", "ISK", "JMD", "JOD", "JPY", "KES", "KGS", "KHR", "KMF", "KPW",
        "KRW", "KWD", "KYD", "KZT", "LAK", "LBP", "LKR", "LRD", "LSL", "LYD",
        "MAD", "MDL", "MGA", "MKD", "MMK", "MNT", "MOP", "MRU", "MUR", "MVR",
        "MWK", "MXN", "MXV", "MYR", "MZN", "NAD", "NGN", "NIO", "NOK", "NPR",
        "NZD", "NZD", "OMR", "PAB", "PEN", "PGK", "PHP", "PKR", "PLN", "PYG",
        "QAR", "RON", "RSD", "RUB", "RWF", "SAR", "SBD", "SCR", "SDG", "SEK",
        "SGD", "SHP", "SLL", "SOS", "SRD", "SSP", "STN", "SVC", "SYP", "SZL",
        "THB", "TJS", "TMT", "TND", "TOP", "TRY", "TTD", "TWD", "TZS", "UAH",
        "UGX", "USD", "USN", "UYI", "UYU", "UYW", "UZS", "VES", "VND", "VUV",
        "WST", "XAF", "XAG", "XAU", "XBA", "XBB", "XBC", "XBD", "XCD", "XDR",
        "XOF", "XPD", "XPF", "XPT", "XSU", "XTS", "XUA", "XXX", "YER", "ZAR",
        "ZMW", "ZWL"
    ]
    return '|'.join(currencies)
