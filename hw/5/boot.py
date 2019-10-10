"""
Baseline utilities: must be loaded before anything else.
"""


class Pretty:
    """A class that pretty prins itself, attributes sorted alphabetically,
    ignoring 'private' attributes (those starting with '_')."""

    def __repr__(i):
        pairs = sorted([(k, v) for k, v in i.__dict__.items()
                        if k[0] != "_"])
        pre = i.__class__.__name__ + '{'

        def q(z):
            if isinstance(z, str): return "'%s'" % z
            if callable(z): return "fun(%s)" % z.__name__
            return str(z)

        return pre + ", ".join([('%s=%s' % (k, q(v)))
                                for k, v in pairs]) + '}'


class o(Pretty):
    "Class for names attributes"

    def __init__(i, **d):
        "Fast specification of attributes and their defaults."
        i.d().update(**d)

    def d(i):
        "Convenience method, shortcut access to internal dictionary."
        return i.__dict__

    def cloner(i):
        "Return something that can make new things of this type."
        return i.__class__
