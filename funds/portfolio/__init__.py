import pandas as pd
import re


class PortfolioPosition(object):
    def __init__(self, fundReport, config):
        self.fundReport = fundReport
        self.weight = float(config["weight"])


class PortfolioPositions(object):
    def __init__(self):
        self._positions = []

    def __iter__(self):
        return self._positions.__iter__()

    def __len__(self):
        return self._positions.__len__()

    def add(self, p):
        self._positions.append(p)


class Portfolio(object):
    def __init__(self):
        self.positions = PortfolioPositions()
        self._df = None
        self._erase = [
            r'"',
            r'\'',
            r'\(',
            r'\)',
        ]
        self._find_replace = [
            [r'applied mat($|\s+)', 'applied materials'],
            [r'( laboratories)|( labs)', ' lab'],
            [r' com($|\s+)', '.com '],
            [r"\xad", ' '],
            [r'-', ' '],
        ]
        self._normalization_endings = \
            [
                "&",
                "&co.kgaa",
                "144a"
                "H",
                "[taiwan]",
                "a",
                "a.s",
                "a/s",
                "aandelen op naam eo  ,01",
                "ab",
                "ag & co kgaa",
                "ag & co. kgaa",
                "ag",
                "akt",
                "aktien",
                "as",
                "asa",
                "b",
                "bond",
                "bv",
                "c",
                "chf",
                "class",
                "co",
                "corp",
                "corporation",
                "dl  ,54945",
                "emtn regs v142024",
                "eur 1",
                "fin",
                "free",
                "government",
                "group",
                "hldg",
                "holding",
                "holdings",
                "v122022",
                "inc",
                "inc^/*",
                "inh",
                "inhaber",
                "ltd",
                "motors",
                "n.v",
                "nam",
                "namen",
                "namens",
                "non voting",
                "nv",
                "o.n",
                "o.st",
                "on",
                "pcl",
                "plc",
                "rc  ,10",
                "reg",
                "registered",
                "reit",
                "s.a",
                "s.a. actions nominatives",
                "sa",
                "sa/nv",
                "sdi",
                "se regs",
                "se",
                "sf 10",
                "sf 14,15",
                "shares",
                "shs",
                "str. u.med.ag",
                "strahlen und medizintechnik",
                "v142021",
                "vorzugsakt",
                "vorzugsakt.o.st.o.n",
                "vorzugsaktien",
                "vz",
                "wi",
             ]
        self._ending_chars = ["", "^", "."]

    def add_position(self, fundReport, config):
        self.positions.add(PortfolioPosition(fundReport, config))
        if self._df is not None:
            self._df.drop(["sid", "position_weight"], axis=1)
        self._df = pd.concat([self._df, fundReport.to_df()], ignore_index=True)
        self.df["sid"] = range(0, len(self.df))
        self.df["position_weight"] = 0
        for p in self.positions:
            self.df.loc[self.df["position"] ==
                        p.fundReport.isin, "position_weight"] = p.weight
        self.rebalance()
        self.normalize()

    def rebalance(self):
        if len(self._df) > 0:
            weights_total = sum([p.weight for p in self.positions])
            self.df["weight"] = \
                self.df.loc[:, "percentage_of_asset"] \
                * self.df.loc[:, "position_weight"]
            self.df["weight"] = self.df["weight"]/weights_total

    @property
    def df(self):
        if self._df is None:
            raise ValueError("This portfolio has no position in it")
        return self._df

    @property
    def assets(self):
        group = self.df.groupby("sid")
        return group[["normalized_name",
                      "sid_total_weight"]].first().reset_index()

    @property
    def shares(self):
        group = self.df[self.df["type"] == "share"].groupby("sid")
        return group[["normalized_name",
                      "sid_total_weight"]].first().reset_index()

    @property
    def bonds(self):
        group = self.df[self.df["type"] == "bond"].groupby("sid")
        return group[["normalized_name",
                      "sid_total_weight"]].first().reset_index()

    def normalize(self):
        if len(self.df) > 0:
            # create
            self.df["normalized_name"] = \
                self.df["name"].apply(self.normalize_create)
            # replace
            self.df["normalized_name"] = \
                self.df["normalized_name"].apply(self.normalize_replace)
            # erase
            self.df["normalized_name"] = \
                self.df["normalized_name"].apply(self.normalize_erase)

            self.df["sid"] = \
                self.df.groupby("normalized_name")["sid"].transform('first')
            before = self.df.loc[:, "sid"].nunique()
            after = 0
            while before != after:
                before = after
                for ending in self._normalization_endings:
                    for char in self._ending_chars:
                        ending_final = ending + char
                        group = self.df.groupby("normalized_name")["sid"]
                        self.df["sid"] = group.transform('first')
                        self.df["normalized_name"] = get_normalization(
                            self.df, ending_final)
                        after = self.df.loc[:, "sid"].nunique()
            self.df["sid_total_weight"] = self.df.groupby("sid").agg(
                sid_total_weight=pd.NamedAgg(column='weight', aggfunc='sum')
            )

    def normalize_create(self, string):
        return " ".join(string.lower().split())

    def normalize_erase(self, string):
        return re.sub(r'{}'.format('|'.join(self._erase)), '', string)

    def normalize_replace(self, string):
        return_string = string
        for (find, replace) in self._find_replace:
            return_string = re.sub(find, replace, return_string)
        return " ".join(return_string.split())


def get_normalization(df, ending):
    return df["normalized_name"].apply(
        lambda x: x[:-(len(ending)+1)].strip()
        if x.endswith(" {}".format(ending)) else x)
