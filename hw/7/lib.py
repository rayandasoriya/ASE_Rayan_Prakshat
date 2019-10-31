"""
Misc standard Python tricks
"""

import random, sys, re, os
from the import *

# -------------------------------------------------
# standard shortcuts

r = random.random
seed = random.seed
isa = isinstance


def first(l):
    "first in a list"
    return l[0]


def last(l):
    "last in a list"
    return l[-1]


def isNum(x):
    "checks for numbers"
    return isa(x, (float, int))


def same(x):
    "do nothing"
    return x


# -------------------------------------------------
# string stuff

def atom(x):
    "coerce x into the right kind of atom"
    try:
        return int(x)
    except:
        try:
            return float(x)
        except:
            return x


# -------------------------------------------------
# sorted list

def ordered(lst, key=same):
    "Sort things, but ignore any 'THE.char.skip' entries."
    return sorted([x for x in lst if key(x) != THE.char.skip])


# -------------------------------------------------
# some convenient iterators

def words(f):
    "iterate over words in a file"
    with open(f) as fp:
        for line in fp:
            for word in line.strip().split():
                yield word


def string(s):
    "iterate over lines from a string"
    for line in s.splitlines():
        yield line


def file(f):
    "iterate over lines in a file"
    with open(f) as fp:
        for line in fp:
            yield line.strip()


# -------------------------------------------------
# error handling

def now(t, m):
    "maybe complain and exit"
    if not t:
        sys.stderr.write('#E> ' + str(m) + '\n')
        sys.exit()


# -------------------------------------------------
# cli tricks

def cli():
    "Allow command lines args to update fields in the THE object"
    args = [thing(x) for x in sys.argv[1:]]
    what = {}
    groups = THE.d()
    while args:
        arg = args.pop(0)
        if arg in groups:
            what = groups[arg].d()
        else:
            now(isa(arg, str) and arg[0] == "-", "bad flag '%s'" % arg)
            arg = arg[1:]
            now(arg in what, "%s not one of %s" % (arg, list(what.keys())))
            old = what[arg]
            if isa(old, bool):
                what[arg] = not what[arg]
            else:
                val = args.pop(0)
                now(type(old) == type(val),
                    "'%s' value not of type '%s'" % (arg, type(old)))
                what[arg] = val
    return THE
