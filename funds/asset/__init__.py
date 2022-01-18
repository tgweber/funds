class Assets(object):
    """ Base class and interface for securites comprising a fund
    -------
    Attributes
    ----------
    isin: str
        ISIN number of the asset
    name: str
        Name of the asset
    percentage: float
        Percentage of this asset compared to the comprising fund
    """
    @property
    def isin(self):
        return self._isin

    @property
    def name(self):
        return self._name

    @property
    def percentage(self):
        return self._percentage

    def __init__(self, name, percentage, isin="xxx"):
        self._name = name
        self._percentage = percentage
        self._isin = isin


class Bond(Assets):
    """ """
    @property
    def kupon(self):
        return self._kupon

    @property
    def due(self):
        return self._due

    def __init__(self, name, percentage, kupon, due, isin="xxx"):
        super(Bond, self).__init__(name, percentage, isin)
        self._kupon = kupon
        self._due = due
        self._isin = isin


class Share(Assets):
    """ """
