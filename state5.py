STATE5_NOT_DICT = {
    "0" : "1",
    "1" : "0",
    "D" : "D'",
    "D'": "D",
    "u" : "u",
}

STATE5_AND_DICT = {
    "0" : {"0":"0",  "1":"0",  "D":"0",  "D'":"0",  "u":"0"},
    "1" : {"0":"0",  "1":"1",  "D":"D",  "D'":"D'", "u":"u"},
    "D" : {"0":"0",  "1":"D",  "D":"D",  "D'":"0",  "u":"u"},
    "D'": {"0":"0",  "1":"D'", "D":"0",  "D'":"D'", "u":"u"},
    "u" : {"0":"0",  "1":"u",  "D":"u",  "D'":"u",  "u":"u"},
}

STATE5_OR_DICT = {
    "0" : {"0":"0",  "1":"1",  "D":"D",  "D'":"D'", "u":"u"},
    "1" : {"0":"1",  "1":"1",  "D":"1",  "D'":"1",  "u":"1"},
    "D" : {"0":"D",  "1":"1",  "D":"D",  "D'":"1",  "u":"u"},
    "D'": {"0":"D'", "1":"1",  "D":"1",  "D'":"D'", "u":"u"},
    "u" : {"0":"u",  "1":"1",  "D":"u",  "D'":"u",  "u":"u"},
}

STATE5_XOR_DICT = {
    "0" : {"0":"0",  "1":"1",  "D":"D",  "D'":"D'", "u":"u"},
    "1" : {"0":"1",  "1":"0",  "D":"D'", "D'":"D",  "u":"u"},
    "D" : {"0":"D",  "1":"D'", "D":"0",  "D'":"1",  "u":"u"},
    "D'": {"0":"D'", "1":"D",  "D":"1",  "D'":"0",  "u":"u"},
    "u" : {"0":"u",  "1":"u",  "D":"u",  "D'":"u",  "u":"u"},
}

def _s5_and(a,b):
    return STATE5_AND_DICT[a][b]
    
def _s5_or(a,b):
    return STATE5_OR_DICT[a][b]

def _s5_xor(a,b):
    return STATE5_XOR_DICT[a][b]

def S5_AND(*args):
    state = args[0]
    for bit in args[1:]:
        state = _s5_and(state, bit)
    return state

def S5_OR(*args):
    state = args[0]
    for bit in args[1:]:
        state = _s5_or(state, bit)
    return state

def S5_XOR(*args):
    state = args[0]
    for bit in args[1:]:
        state = _s5_xor(state, bit)
    return state

def S5_NOT(a):
    return STATE5_NOT_DICT[a]

def S5_NAND(*args):
    return STATE5_NOT_DICT[S5_AND(*args)]

def S5_NOR(*args):
    return STATE5_NOT_DICT[S5_OR(*args)]

def S5_XNOR(*args):
    return STATE5_NOT_DICT[S5_AND(*args)]

def _and(a,b):
    return a if a == b else '0'

def _or(a,b):
    return a if a == b else '1'

def _xor(a,b):
    return '0' if a == b else '1'

def AND(*args):
    return '0' if '0' in args else '1'

def OR(*args):
    return '1' if '1' in args else '0'

def XOR(*args):
    return '1' if args.count('1') % 2 == 1 else '0'

def _is_s5(*args) -> bool:
    return "D" in args or "D'" in args or "u" in args

def SMART_AND(*args):
    return S5_AND(*args) if _is_s5(*args) else AND(*args)

def SMART_OR(*args):
    return S5_OR(*args) if _is_s5(*args) else OR(*args)

def SMART_XOR(*args):
    return S5_XOR(*args) if _is_s5(*args) else XOR(*args)
