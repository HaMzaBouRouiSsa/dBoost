import sys
from math import sqrt

def zeroif(S, X):
    return S if S != None else tuple(tuple(0 for _ in x) for x in X)

def root(X):
    return tuple(tuple(sqrt(xi) for xi in x) for x in X)

def merge(S, X, f, phi):
    return tuple(tuple(phi(si, f(xi)) for si, xi in zip(s, x)) for s, x in zip(S, X))

def id(x):
    return x

def sqr(x):
    return x * x if x != None else None

def not_null(x):
    return x != None

def plus(a, b):
    return a + b if b != None else a

def minus(a, b):
    return a - b if b != None else a

def mul(a, b):
    return a * b if b != None else a

def div0(a, b):
    return a / b if a != None and b != 0 else 0

def tuplify(a, b):
    return (a, b)

def report_progress(nb):
    if nb % 1000 == 0:
        sys.stderr.write(str(nb) + "\r")