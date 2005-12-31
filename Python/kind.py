kind_word = 0
kind_number = 1
kind_parsing = 2
kind_pipe = 3
kind_parens = 4
kind_unknown = 5

def recognize(str):
    if str[0] in "0123456789":
        return kind_number
    elif str[0] == "|":
        return kind_pipe
    elif str[0] == "{":
        return kind_parsing
    elif str[0] == "(":
        return kind_parens
    elif str[0] in "abcdefghihjklmnopqrstuvwxyz[]<>":
        return kind_word
    else:
        return kind_unknown


kStrongs = 0
kANLEX = 1

kOLB = 0
kBETA = 1
kUnicode = 2

