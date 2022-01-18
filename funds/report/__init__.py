import pandas as pd

from funds.asset import Bond, Share


class FundReport(object):
    """ Base class and interface for reports of funds
    -------
    Attributes
    ----------
    isin: str
        ISIN number of the fund
    date: Date
        Publication date of the report
    assets: List<Assets>
        List of Securites of which the fund is comprised
    """
    @property
    def name(self):
        return self._name

    @property
    def isin(self):
        return self._isin

    @property
    def date(self):
        return self._date

    @property
    def assets(self):
        return self._assets

    @property
    def bonds(self):
        return [b for b in self._assets if isinstance(b, Bond)]

    @property
    def shares(self):
        return [b for b in self._assets if isinstance(b, Share)]

    def __init__(self, isin, name, date):
        self._isin = isin
        self._name = name
        self._date = date
        self._assets = []

    def total_percentage(self):
        total = 0
        for s in self.assets:
            total += s.percentage
        return total

    def to_df(self):
        payload = []
        for s in self._assets:
            s_dict = {}
            s_dict["position_name"] = self.name
            s_dict["position"] = self.isin
            s_dict["percentage_of_asset"] = s.percentage
            s_dict["name"] = s.name
            s_dict["isin"] = s.isin
            if isinstance(s, Bond):
                s_dict["type"] = "bond"
                s_dict["kupon"] = s.kupon
                s_dict["due"] = s.due
            else:
                s_dict["type"] = "share"
                s_dict["kupon"] = None
                s_dict["due"] = None
            payload.append(s_dict)
        return pd.DataFrame(payload)
