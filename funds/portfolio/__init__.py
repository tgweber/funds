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
        self._normalization_endings = \
            ["sdi", "inc", "corp", "sa", "s.a", "se", "ltd",
             "on", "o.n", "shs", "reg", "shs", "registered",
             "asa", "plc", "corporation", "ag & co kgaa", "ag & co. kgaa",
             "co", "ag", "nv", "holding", "a", "c", "holdings",
             "inhaber", "namens", "shares", "bond",
             "government", "motors", "o.st", "vorzugsaktien", "H",
             "inh", "akt", "vorzugsakt", "vorzugsakt.o.st.o.n.",
             "aktien", "namens", "aandelen op naam eo  ,01", "hldg",
             "str. u.med.ag", "&co.kgaa", "n.v", "ag & co. kgaa", "sf 10",
             "sf 14,15", "eur 1", "s.a. actions nominatives", "nam",
             "strahlen  und medizintechnik", "a/s", "[taiwan]", "&", "a.s",
             "as", "vz", "pcl", "reit", "non voting", "b", "free", "ab",
             "chf"]
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
            self.df["normalized_name"] = self.df["name"].str.lower().apply(
                lambda x: re.sub(r'\(|\)', '', x)).str.replace("-", " ")
            self.df["normalized_name"] = self.df["normalized_name"].apply(
                lambda x: x.replace('\xad', ' ').strip())

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


def get_normalization(df, ending):
    return df["normalized_name"].apply(
        lambda x: x[:-(len(ending)+1)].strip()
        if x.endswith(" {}".format(ending)) else x)
