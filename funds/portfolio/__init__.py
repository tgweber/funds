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
            r',',
            r'\^',
            r'[',
            r']',
            r'/',
        ]
        self.erase = re.compile(r'{}'.format('|'.join(self._erase)))

        self._normalization_endings = \
            [
                r"v?\d+$", "nk", "[a-zA-Z]{0,1}", "ost", "grp", "and",
                "144a" "[taiwan]", "co", "kgaa", "ag"
                "aandelen op naam eo", "ab",
                "ag", "akt", "aktien", "as", "asa",
                "bond", "bv", "chf", "class", "co", "corp", "corporation",
                "dl", "emtn", "eur", "fin", "free",
                "government", "group", "hldg", "holding", "holdings",
                "inc", "inh", "inhaber", "ltd",
                "motors", "nam", "namen", "namens", "namensakt", "non voting",
                "nv", "st", "on", "pcl", "plc", "rc", "reg",
                "registered", "reit", "actions", "nominatives", "sa",
                "sdi", "regs", "se", "sf", "shares",
                "shs", "strahlen und medizintechnik",
                "vorzugsakt", "st",
                "vorzugsaktien", "vz", "wi", "str", "med",
             ]
        self._endings = \
            re.compile(r"( ({})(^|\.)*)+$".format("|".join(
                self._normalization_endings)))

        # order matters
        find_replace = [
            [r"\xad", ' '],
            [r'-', ' '],
            [r'\.', ' '],
            [r'&', ' and '],
            [r'applied mat($|\s+)', 'applied materials'],
            [r'phillips 66', 'phillips sixtysix'],
            [r'( laboratories)|( labs)', ' lab'],
            [r' com(\s+|$)', '.com '],
            [r' bk$', 'banking'],
        ]
        self._find_replace = [
            (re.compile(find), replace) for (find, replace) in find_replace
        ]

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

    def normalize(self):
        if len(self.df) > 0:
            # create
            self.df["normalized_name"] = \
                self.df["name"].apply(self.normalize_create)
            # erase
            self.df["normalized_name"] = \
                self.df["normalized_name"].apply(self.normalize_erase)
            # replace
            self.df["normalized_name"] = \
                self.df["normalized_name"].apply(self.normalize_replace)
            # endings
            self.df["normalized_name"] = \
                self.df["normalized_name"].apply(self.normalize_endings)
            # create sid
            self.df["sid"] = \
                self.df.groupby("normalized_name")["sid"].transform('first')
            # calculate portfolio global weights
            self.df["sid_total_weight"] = self.df.groupby("sid").agg(
                sid_total_weight=pd.NamedAgg(column='weight', aggfunc='sum')
            )

    def normalize_create(self, string):
        return " ".join(string.lower().split())

    def normalize_erase(self, string):
        return re.sub(self.erase, '', string)

    def normalize_replace(self, string):
        return_string = string
        for (find, replace) in self._find_replace:
            return_string = re.sub(find, replace, return_string)
        return " ".join(return_string.split())

    def normalize_endings(self, string):
        return " ".join(re.sub(self._endings, '', string).split())
