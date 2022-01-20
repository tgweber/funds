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
            r'\[',
            r'\]',
            r'/',
            r'\*',
        ]
        self.erase = re.compile(r'{}'.format('|'.join(self._erase)))

        self._to_space = [
            r"\xad",
            r'-',
            r'\.'
        ]
        self.to_space = re.compile(r'{}'.format('|'.join(self._to_space)))

        self._normalization_endings = \
            [
                r"v?\d+", "[a-zA-Z]{0,1}", "144a",
                "aandelen", "ab", "actions", "and", "adr",
                "ag", "akt", "aktien", "aktier", "as", "asa", "au",
                "bank", "bhd", "bond", "bv",
                "chf", "cl", "class",
                "co", "cos", "companies",
                "corp", "corporation", "cv",
                "de", "dl",
                "emtn", "eo", "eur",
                "femsa", "fin", "finanzas", "free", "frn",
                "government",
                "groip", "groep?", "group", "grp",
                "hbc", "hldg", "holding", "holdings",
                "idec", "inc", "inh", "inhaber",
                "kgaa",
                "ltd", "limited",
                "med", "motors",
                "naam", "nam", "namen", "namens", "namensakt", "namn",
                "nk", "non voting", "nominatives", "nv", "nvdr",
                "on", "op", "ost",
                "pcl", "plc", "perpetual",
                "rc", "reg", "regs", "registered", "rg", "reit",
                "sa", "sab", "sdi", "se", "sf", "shares",
                "shs", "st", "stapled security",
                "str", "strahlen und medizintechnik", "sub",
                "usa",
                "vorzugsakt", "vorzugsaktien", "vot", "vz",
                "wi",
             ]
        self._endings = \
            re.compile(r"( ({})(^|\.)*)+$".format("|".join(
                self._normalization_endings)))

        # order matters
        find_replace = [
            [r'&', ' and '],
            [r'applied mat($|\s+)', 'applied materials'],
            [r'phillips 66', 'phillips sixtysix'],
            [r'( laboratories)|( labs)', ' lab'],
            [r' com(\s+|$)', '.com '],
            [r' bk$', ' banking'],
            [r'asian\s*d?\s*dev(elopment)?\s*(banking)?.*',
                'asian development banking'],
            [r' amr$', ' amro'],
            [r'^software$', 'software ag'],
            [r' ny ', ' new york '],
            [r'systms', 'systems'],
            [r'bnp par$', 'bnp paribas'],
            [r'borgwarner', 'borg warner'],
            [r'cisco sys$', 'cisco systems'],
            [r'citigp', 'citigroup'],
            [r'city developments', 'city development'],
            [r'cppib cap(it)?$', 'cppib capital'],
            [r'^e on$', 'e.on'],
            [r'^east jap(an)?( railway)?$', 'east japan railway'],
            [r' hlth', ' health'],
            [r'(^fresenius)$|frs med care', 'fresenius medical care'],
            [r'^iberdrola international$', 'iberdrola'],
            [r'intl flavors and frag', 'international flavors and fragrances'],
            [r'johnson controls(( intl$)|( international$))',
                'johnson controls'],
            [r'^jpm($|organ ch$)', 'jpmorgan chase'],
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
            # to-space
            self.df["normalized_name"] = \
                self.df["normalized_name"].apply(self.normalize_space)
            # replace
            self.df["normalized_name"] = \
                self.df["normalized_name"].apply(self.normalize_replace)
            # endings
            self.df["normalized_name"] = \
                self.df["normalized_name"].apply(self.normalize_endings)
            # replace
            self.df["normalized_name"] = \
                self.df["normalized_name"].apply(self.normalize_replace)
            # isin
            self._isin_lookup = self.df.groupby("isin").apply(
                lambda x: x["normalized_name"].value_counts().index[0])
            self.df["normalized_name"] = \
                self.df.apply(self.normalize_isin, axis=1)
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

    def normalize_space(self, string):
        return " ".join(re.sub(self.to_space, ' ', string).split())

    def normalize_endings(self, string):
        return " ".join(re.sub(self._endings, '', string).split())

    def normalize_isin(self, asset):
        if asset.get("isin") is None:
            return asset.get("normalized_name")
        return self._isin_lookup.loc[asset.get("isin")]
