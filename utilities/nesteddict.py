from collections import OrderedDict


class NestedDict(OrderedDict):
    """Implementation of perl's autovivification feature.

    Example:
        obj = AutoVivification()
        obj['key1']['key2']['key3'] = value
    """

    def __getitem__(self, item):
        """."""
        try:
            return OrderedDict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value
