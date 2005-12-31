variant_none = 0
variant_first = 1
variant_second = 2

def variant2string(v):
    if v == variant_none:
        return "none"
    elif v == variant_first:
        return "var_first"
    elif v == variant_second:
        return "var_second"
    else:
        raise Exception("Error: variant unknown in variant2string(%s)" % str(v))

