from collections import defaultdict
import inspect
import time
import utils
import sys

# Rules are functions that take a value (field), and return a tuple of features
# derived from that value. 

rules = defaultdict(list)

def rule(rule):
    sig = inspect.signature(rule)
    params = list(sig.parameters.values())
    
    if len(params) != 1:
        sys.stderr.write("Invalid rule {}".format(rule.__name__))
        sys.exit(1)

    input_type = params[0].annotation
    rules[input_type].append(rule)
    return rule

def descriptions(ruleset):
    descriptions = {}

    for type in ruleset:
        descriptions[type] = []
        for rule in ruleset[type]:
            descriptions[type].extend(inspect.signature(rule).return_annotation)
            
    return descriptions

@rule
def string_case(s: str) -> ("upper case", "lower case", "title case"):
    return (s.isupper(), s.islower(), s.istitle())

@rule
def string_is_digit(s: str) -> ("is digit",):
    return (s.isdigit(),)

@rule
def length(s: str) -> ("length",):
    return (len(s),)

def bits(*positions):
    def _bits(i: int) -> tuple("bit {}".format(pos) for pos in positions):
        return ((i >> pos) & 1 for pos in positions)
    return _bits

def mod(*mods):
    def _mod(i: int) -> tuple("mod {}".format(mod) for mod in mods):
        return (i % mod for mod in mods)
    return _mod

DATE_PROPS = "tm_year", "tm_mon", "tm_mday", "tm_hour", "tm_min", "tm_sec", "tm_wday", "tm_yday"

@rule
def unix2date(timestamp: int) -> DATE_PROPS:
    t = time.gmtime(timestamp)
    return map(lambda a: getattr(t, a), DATE_PROPS)

rule(bits(0, 1, 2, 3, 4, 5))
rule(mod(10))