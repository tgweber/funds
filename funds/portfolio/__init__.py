import pandas as pd
import re


class PortfolioPosition(object):
    def __init__(self, fundReport, weight):
        self.fundReport = fundReport
        self.weight = float(weight)


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
            r'\*',
            r'\+',
            r'`',
            r'´',
            r'’',
        ]
        self.erase = re.compile(r'{}'.format('|'.join(self._erase)))

        self._to_space = [
            r"\xad",
            r'-',
            r'\.',
            r'/',
        ]
        self.to_space = re.compile(r'{}'.format('|'.join(self._to_space)))

        self._normalization_endings = \
            [
                r"v?\d+", "[a-zA-Z]{0,1}", "144a",
                "aandelen", "ab", "actions", "and", "adr",
                "ag", "akt", "aktien", "aktier", "as", "asa", "au",
                "bank", "bhd", "bond", "bv",
                "cap", "chf", "ci", "cl", "class",
                "co", "cos", "companies", "company",
                "corp", "corporation", "cv",
                "de", "dividende", "dl", "dk", "dsm",
                "emtn", "eo", "epic", "eur",
                "fdg", "femsa", "finanzas", "free", "frn",
                "government",
                "groip", "groep?", "groupe?", "grp",
                "hbc", "hldg", "hlg", "holding", "holdings", "h us",
                "idec", "in", "inc", "inh", "indehaver", "inhaber", "int",
                "kgaa",
                "ltd", "limited",
                "mar", "med", "motors", "mtn",
                "naam", "nam", "namen", "namens", "namensakt", "namn", "navne",
                "new", "nk", "nom", "non voting", "nominatives", "nv", "nvdr",
                "ohne stimmrecht", "on", "op", "ost", "oyj",
                "part", "partners", "pcl", "plc", "perpetual",
                "rc", "reg", "regs", "registered", "reit", "rep",
                "rg", "right",
                "sa", "sab", "sdi", "se", "services", "sf", "sfh", "shares",
                "spa", "shs", "st", "stapled security",
                "str", "strahlen und medizintechnik", "sub", "subord",
                "the",
                r"thb\d+",
                "uts", "usa",
                "vopak", "vorz", "vorzugsakt", "vorzugsaktien",
                "vot", "voting", "vtg", "vz",
                "wi",
             ]
        self._endings = \
            re.compile(r"( ({})(^|\.)*)+$".format("|".join(
                self._normalization_endings)))

        # order matters
        find_replace = [
            [r'^mandg$', 'm and g'],
            [r'^mandt$', 'm and t'],
            [r'^sandt$', 's and t'],
            [r'^tandd$', 't and d'],
            [r'm&g', 'mandg'],
            [r'm&t', 'mandt'],
            [r's&t', 'sandt'],
            [r't&d', 'tandd'],
            [r'&', ' and '],
            [r'applied mat($|\s+)', 'applied materials'],
            [r'phillips 66', 'phillips sixtysix'],
            [r'( laboratories)|( labs)', ' lab'],
            [r'^verizon com$', 'verizon communications'],
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
            [r'^kimberly cl$', 'kimberly clark'],
            [r'kreditanstalt fuer wiederaufbau', 'kfw'],
            [r'^loyds$', 'loyds banking'],
            [r'^loreal$', 'l oreal'],
            [r'^lowe$', 'lowes'],
            [r' intl$', ' international'],
            [r'marsh mc lennan$', 'marsh and mclennan'],
            [r'^metlife$', 'met life'],
            [r'chem$', 'chemical'],
            [r'moody s', 'moodys'],
            [r'mor st$', 'morgan stan'],
            [r'novo nordis$', 'novo nordisk'],
            [r'oracle corp japan$', 'oracle japan'],
            [r'^prudential$', 'prudential financial'],
            [r'^ptc$', 'ptc therapeutics'],
            [r'^quebec$', 'quebec prov'],
            [r'^red eléctrica financiaciones$', 'red electrica'],
            [r' bros ', ' brothers '],
            [r'^salesforce$', 'salesforce.com'],
            [r'^sbab$', 'sbab banking'],
            [r'.*ericsson.*', 'ericsson'],
            [r'telefónica', 'telefonica'],
            [r'telefónica', 'telefonica'],
            [r'tech$', 'technologies'],
            [r'^unibail rodamco.*$', 'unibail rodamco'],
            [r'^unilev$', 'unilever'],
            [r'^united util$', 'united utilities'],
            [r' metal$', ' metals'],
            [r'^yamaha.*$', 'yamaha'],
            [r'^zuerich ver$', 'zurich insurance'],

        ]

        self._find_replace = [
            (re.compile(find), replace) for (find, replace) in find_replace
        ]

    def add_position(self, fundReport, weight):
        self.positions.add(PortfolioPosition(fundReport, weight))
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
    def shared_assets(self):
        return self.df.loc[:, "normalized_name"].value_counts().where(
            lambda x: x > 1).dropna()

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

    def simple_sim(self, other):
        common_count = len(
            self.assets[
                self.assets["normalized_name"].isin(
                    other.assets["normalized_name"]
                )
            ]
        )
        total_assets = \
            pd.concat([self.assets, other.assets])["normalized_name"].nunique()
        return common_count/total_assets

    def simple_diff(self, other):
        return 1 - self.simple_sim(other)

    def weighted_sim(self, other):
        both = self.assets[
            self.assets["normalized_name"].isin(
                other.assets["normalized_name"]
            )
        ]
        both = both.set_index("normalized_name")
        both = both.drop(["sid"], axis=1)
        both = both.rename(columns={"sid_total_weight": "weight1"})
        both["weight2"] = other.assets[
            other.assets["normalized_name"].isin(
                both.index
            )
        ].set_index("normalized_name")["sid_total_weight"]
        normalizer = (
            self.df["sid_total_weight"].sum() +
            other.df["sid_total_weight"].sum()
        )/2
        return both.min(axis=1).sum()/normalizer

    def weighted_diff(self, other):
        return 1 - self.weighted_sim(other)
