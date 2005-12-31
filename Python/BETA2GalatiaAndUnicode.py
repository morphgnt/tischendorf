# beta2GalatiaAndUnicode.py
#
# Version 2004-11-23 with changes by ulrikp 2005-03-19
#
# James Tauber
# http://jtauber.com/
#
# You are free to redistribute this, but please inform me of any errors
#
#
# Modified by Ulrik Petersen to do BETA to SIL Galatia as well
# http://ulrikp.org
#
# SIL Galatia is a beautiful Greek font, freely available here:
# http://http://scripts.sil.org/cms/scripts/page.php?site_id=nrsi&item_id=SILGrk_home
#
# Ulrik Petersen makes his changes available under the same conditions
# as James Tauber did above.
#
# USAGE:
#
# trie = beta2unicodeTrie()
# beta = "LO/GOS\n";
# unicode, remainder = trie.convert(beta)
#
# - to get final sigma, string must end in \n
# - remainder will contain rest of beta if not all can be converted



class Trie:
    def __init__(self):
        self.root = [None, {}]

    def add(self, key, value):
        curr_node = self.root
        for ch in key:
            curr_node = curr_node[1].setdefault(ch, [None, {}])
        curr_node[0] = value

    def find(self, key):
        curr_node = self.root
        for ch in key:
            try:
                curr_node = curr_node[1][ch]
            except KeyError:
                return None
        return curr_node[0]

    def findp(self, key):
        curr_node = self.root
        remainder = key
        for ch in key:
            try:
                curr_node = curr_node[1][ch]
            except KeyError:
                return (curr_node[0], remainder)
            remainder = remainder[1:]
        return (curr_node[0], remainder)

    def convert(self, keystring):
        valuestring = ""
        key = keystring
        while key:
            value, key = self.findp(key)
            if not value:
                return (valuestring, key)
            valuestring += value
        return (valuestring, key)

def beta2unicodeTrie():
    t = Trie()

    t.add("*A",      u"\u0391")
    t.add("*B",      u"\u0392")
    t.add("*G",      u"\u0393")
    t.add("*D",      u"\u0394")
    t.add("*E",      u"\u0395")
    t.add("*Z",      u"\u0396")
    t.add("*H",      u"\u0397")
    t.add("*Q",      u"\u0398")
    t.add("*I",      u"\u0399")
    t.add("*K",      u"\u039A")
    t.add("*L",      u"\u039B")
    t.add("*M",      u"\u039C")
    t.add("*N",      u"\u039D")
    t.add("*C",      u"\u039E")
    t.add("*O",      u"\u039F")
    t.add("*P",      u"\u03A0")
    t.add("*R",      u"\u03A1")
    t.add("*S",      u"\u03A3")
    t.add("*T",      u"\u03A4")
    t.add("*U",      u"\u03A5")
    t.add("*F",      u"\u03A6")
    t.add("*X",      u"\u03A7")
    t.add("*Y",      u"\u03A8")
    t.add("*W",      u"\u03A9")

    t.add("A",      u"\u03B1")
    t.add("B",      u"\u03B2")
    t.add("G",      u"\u03B3")
    t.add("D",      u"\u03B4")
    t.add("E",      u"\u03B5")
    t.add("Z",      u"\u03B6")
    t.add("H",      u"\u03B7")
    t.add("Q",      u"\u03B8")
    t.add("I",      u"\u03B9")
    t.add("K",      u"\u03BA")
    t.add("L",      u"\u03BB")
    t.add("M",      u"\u03BC")
    t.add("N",      u"\u03BD")
    t.add("C",      u"\u03BE")
    t.add("O",      u"\u03BF")
    t.add("P",      u"\u03C0")
    t.add("R",      u"\u03C1")

    t.add("S\n",    u"\u03C2")
    t.add("S'",     u"\u03C2'")
    t.add("S,",     u"\u03C2,")
    t.add("S.",     u"\u03C2.")
    t.add("S:",     u"\u03C2:")
    t.add("S;",     u"\u03C2;")
    t.add("S]",     u"\u03C2]")
    t.add("S@",     u"\u03C2@")
    t.add("S_",     u"\u03C2_")
    t.add("S",      u"\u03C3")

    t.add("T",      u"\u03C4")
    t.add("U",      u"\u03C5")
    t.add("F",      u"\u03C6")
    t.add("X",      u"\u03C7")
    t.add("Y",      u"\u03C8")
    t.add("W",      u"\u03C9")

    t.add("I+",     U"\u03CA")
    t.add("U+",     U"\u03CB")

    t.add("A)",     u"\u1F00")
    t.add("A(",     u"\u1F01")
    t.add("A)\\",   u"\u1F02")
    t.add("A(\\",   u"\u1F03")
    t.add("A)/",    u"\u1F04")
    t.add("A(/",    u"\u1F05")
    t.add("E)",     u"\u1F10")
    t.add("E(",     u"\u1F11")
    t.add("E)\\",   u"\u1F12")
    t.add("E(\\",   u"\u1F13")
    t.add("E)/",    u"\u1F14")
    t.add("E(/",    u"\u1F15")
    t.add("H)",     u"\u1F20")
    t.add("H(",     u"\u1F21")
    t.add("H)\\",   u"\u1F22")
    t.add("H(\\",   u"\u1F23")
    t.add("H)/",    u"\u1F24")
    t.add("H(/",    u"\u1F25")
    t.add("I)",     u"\u1F30")
    t.add("I(",     u"\u1F31")
    t.add("I)\\",   u"\u1F32")
    t.add("I(\\",   u"\u1F33")
    t.add("I)/",    u"\u1F34")
    t.add("I(/",    u"\u1F35")
    t.add("O)",     u"\u1F40")
    t.add("O(",     u"\u1F41")
    t.add("O)\\",   u"\u1F42")
    t.add("O(\\",   u"\u1F43")
    t.add("O)/",    u"\u1F44")
    t.add("O(/",    u"\u1F45")
    t.add("U)",     u"\u1F50")
    t.add("U(",     u"\u1F51")
    t.add("U)\\",   u"\u1F52")
    t.add("U(\\",   u"\u1F53")
    t.add("U)/",    u"\u1F54")
    t.add("U(/",    u"\u1F55")
    t.add("W)",     u"\u1F60")
    t.add("W(",     u"\u1F61")
    t.add("W)\\",   u"\u1F62")
    t.add("W(\\",   u"\u1F63")
    t.add("W)/",    u"\u1F64")
    t.add("W(/",    u"\u1F65")

    t.add("A)=",    u"\u1F06")
    t.add("A(=",    u"\u1F07")
    t.add("H)=",    u"\u1F26")
    t.add("H(=",    u"\u1F27")
    t.add("I)=",    u"\u1F36")
    t.add("I(=",    u"\u1F37")
    t.add("U)=",    u"\u1F56")
    t.add("U(=",    u"\u1F57")
    t.add("W)=",    u"\u1F66")
    t.add("W(=",    u"\u1F67")

    t.add("*A)",     u"\u1F08")
    t.add("*)A",     u"\u1F08")
    t.add("*A(",     u"\u1F09")
    t.add("*(A",     u"\u1F09")
    #
    t.add("*(\A",    u"\u1F0B")
    t.add("*A)/",    u"\u1F0C")
    t.add("*)/A",    u"\u1F0C")
    t.add("*A(/",    u"\u1F0D")
    t.add("*(/A",    u"\u1F0D")
    t.add("*A(=",    u"\u1F0F")
    t.add("*(=A",    u"\u1F0F")
    t.add("*E)",     u"\u1F18")
    t.add("*)E",     u"\u1F18")
    t.add("*E(",     u"\u1F19")
    t.add("*(E",     u"\u1F19")
    #
    t.add("*(\E",    u"\u1F1B")
    t.add("*E)/",    u"\u1F1C")
    t.add("*)/E",    u"\u1F1C")
    t.add("*E(/",    u"\u1F1D")
    t.add("*(/E",    u"\u1F1D")

    t.add("*H)",     u"\u1F28")
    t.add("*)H",     u"\u1F28")
    t.add("*H(",     u"\u1F29")
    t.add("*(H",     u"\u1F29")
    t.add("*H)\\",   u"\u1F2A")
    t.add(")\\*H",   u"\u1F2A")
    t.add("*)\\H",    u"\u1F2A")
    #
    t.add("*H)/",    u"\u1F2C")
    t.add("*)/H",    u"\u1F2C")
    #
    t.add("*)=H",    u"\u1F2E")
    t.add("(/*H",    u"\u1F2F")
    t.add("*(/H",    u"\u1F2F")
    t.add("*I)",     u"\u1F38")
    t.add("*)I",     u"\u1F38")
    t.add("*I(",     u"\u1F39")
    t.add("*(I",     u"\u1F39")
    #
    #
    t.add("*I)/",    u"\u1F3C")
    t.add("*)/I",    u"\u1F3C")
    #
    #
    t.add("*I(/",    u"\u1F3F")
    t.add("*(/I",    u"\u1F3F")
    #
    t.add("*O)",     u"\u1F48")
    t.add("*)O",     u"\u1F48")
    t.add("*O(",     u"\u1F49")
    t.add("*(O",     u"\u1F49")
    #
    #
    t.add("*(\O",    u"\u1F4B")
    t.add("*O)/",    u"\u1F4C")
    t.add("*)/O",    u"\u1F4C")
    t.add("*O(/",    u"\u1F4F")
    t.add("*(/O",    u"\u1F4F")
    #
    t.add("*U(",     u"\u1F59")
    t.add("*(U",     u"\u1F59")
    #
    t.add("*(/U",    u"\u1F5D")
    #
    t.add("*(=U",    u"\u1F5F")
    
    t.add("*W)",     u"\u1F68")
    t.add("*)W",     u"\u1F68")
    t.add("*W(",     u"\u1F69")
    t.add("*(W",     u"\u1F69")
    #
    #
    t.add("*W)/",    u"\u1F6C")
    t.add("*)/W",    u"\u1F6C")
    t.add("*W(/",    u"\u1F6F")
    t.add("*(/W",    u"\u1F6F")

    t.add("*A)=",    u"\u1F0E")
    t.add("*)=A",    u"\u1F0E")
    t.add("*A(=",    u"\u1F0F")
    t.add("*W)=",    u"\u1F6E")
    t.add("*)=W",    u"\u1F6E")
    t.add("*W(=",    u"\u1F6F")
    t.add("*(=W",    u"\u1F6F")

    t.add("A\\",    u"\u1F70")
    t.add("A/",     u"\u1F71")
    t.add("E\\",    u"\u1F72")
    t.add("E/",     u"\u1F73")
    t.add("H\\",    u"\u1F74")
    t.add("H/",     u"\u1F75")
    t.add("I\\",    u"\u1F76")
    t.add("I/",     u"\u1F77")
    t.add("O\\",    u"\u1F78")
    t.add("O/",     u"\u1F79")
    t.add("U\\",    u"\u1F7A")
    t.add("U/",     u"\u1F7B")
    t.add("W\\",    u"\u1F7C")
    t.add("W/",     u"\u1F7D")

    t.add("A)/|",   u"\u1F84")
    t.add("A(/|",   u"\u1F85")
    t.add("H)|",    u"\u1F90")
    t.add("H(|",    u"\u1F91")
    t.add("H)/|",   u"\u1F94")
    t.add("H)=|",   u"\u1F96")
    t.add("H(=|",   u"\u1F97")
    t.add("W)|",    u"\u1FA0")
    t.add("W(=|",   u"\u1FA7")

    t.add("A=",     u"\u1FB6")
    t.add("H=",     u"\u1FC6")
    t.add("I=",     u"\u1FD6")
    t.add("U=",     u"\u1FE6")
    t.add("W=",     u"\u1FF6")

    t.add("I\\+",   u"\u1FD2")
    t.add("I/+",    u"\u1FD3")
    t.add("I+/",    u"\u1FD3")
    t.add("U\\+",   u"\u1FE2")
    t.add("U/+",    u"\u1FE3")

    t.add("A|",     u"\u1FB3")
    t.add("A/|",    u"\u1FB4")
    t.add("H|",     u"\u1FC3")
    t.add("H/|",    u"\u1FC4")
    t.add("W|",     u"\u1FF3")
    t.add("W|/",    u"\u1FF4")
    t.add("W/|",    u"\u1FF4")

    t.add("A=|",    u"\u1FB7")
    t.add("H=|",    u"\u1FC7")
    t.add("W=|",    u"\u1FF7")

    t.add("R(",     u"\u1FE5")
    t.add("*R(",    u"\u1FEC")
    t.add("*(R",    u"\u1FEC")

    t.add("R)",     u"\u1FE4")
    t.add("*R)",    u"\u03A1\u0313")
    t.add("*)R",    u"\u03A1\u0313")


#    t.add("~",      u"~")
#    t.add("-",      u"-")
    
#    t.add("(null)", u"(null)")
#    t.add("&", "&")
    
    t.add("0", u"0")
    t.add("1", u"1")
    t.add("2", u"2")
    t.add("3", u"3")
    t.add("4", u"4")
    t.add("5", u"5")
    t.add("6", u"6")
    t.add("7", u"7")
    t.add("8", u"8")
    t.add("9", u"9")
    
    t.add("@", u"@")
    t.add("$", u"$")
    
    t.add(" ", u" ")
    
    t.add(".", u".")
    t.add(",", u",")
    t.add("'", u"'")
    t.add(":", u":")
    t.add(";", u"\u037e")
    t.add("_", u"_")
    t.add("-", u"-")
    

    t.add("[", u"[")
    t.add("]", u"]")

    t.add("[1", u"(")
    t.add("]1", u")")
    
    t.add("[2", u"(")
    t.add("]2", u")")

    t.add("\n", u"")

    t.add("*#2", u"\u03da")  # GREEK (CAPITAL) LETTER STIGMA
    t.add("#2", u"\u03db")   # GREEK SMALL LETTER STIGMA
    
    return t


def beta2GalatiaTrie():
    t = Trie()

    t.add("*A",      "A")
    t.add("*B",      "B")
    t.add("*G",      "G")
    t.add("*D",      "D")
    t.add("*E",      "E")
    t.add("*Z",      "Z")
    t.add("*H",      "J")
    t.add("*Q",      "Q")
    t.add("*I",      "I")
    t.add("*K",      "K")
    t.add("*L",      "L")
    t.add("*M",      "M")
    t.add("*N",      "N")
    t.add("*C",      "X")
    t.add("*O",      "O")
    t.add("*P",      "P")
    t.add("*R",      "R")
    t.add("*S",      "S")
    t.add("*T",      "T")
    t.add("*U",      "U")
    t.add("*F",      "F")
    t.add("*X",      "C")
    t.add("*Y",      "Y")
    t.add("*W",      "W")

    t.add("A",      "a")
    t.add("B",      "b")
    t.add("G",      "g")
    t.add("D",      "d")
    t.add("E",      "e")
    t.add("Z",      "z")
    t.add("H",      "j")
    t.add("Q",      "q")
    t.add("I",      "i")
    t.add("K",      "k")
    t.add("L",      "l")
    t.add("M",      "m")
    t.add("N",      "n")
    t.add("C",      "x")
    t.add("O",      "o")
    t.add("P",      "p")
    t.add("R",      "r")

    t.add("S\n",    "v")
    t.add("S,",     "v,")
    t.add("S'",     "v'")
    t.add("S@",     "v@")
    t.add("S.",     "v.")
    t.add("S:",     "v:")
    t.add("S;",     "v;")
    t.add("S]",     "v]")
    t.add("S",      "s")

    t.add("T",      "t")
    t.add("U",      "u")
    t.add("F",      "f")
    t.add("X",      "c")
    t.add("Y",      "y")
    t.add("W",      "w")

    t.add("I+",     "\xbb")
    t.add("U+",     "\xcb")

    t.add("A)",     "\x87")
    t.add("A(",     "\x83")
    t.add("A)\\",   "\x89")
    t.add("A(\\",   "\x85")
    t.add("A)/",    "\x88")
    t.add("A(/",    "\x84")
    t.add("E)",     "\x9d")
    t.add("E(",     "\x9b")
    t.add("E(\\",   "\x9f")
    t.add("E)/",    "\x9e")
    t.add("E(/",    "\x9c")
    t.add("H)",     "\xd7")
    t.add("H(",     "\xd3")
    t.add("H)\\",   "\xd9")
    t.add("H(\\",   "\xd5")
    t.add("H)/",    "\xd8")
    t.add("H(/",    "\xd4")
    t.add("I)",     "\xb8")
    t.add("I(",     "\xb3")
    t.add("I(\\",   "\xbe")
    t.add("I)/",    "\xb9")
    t.add("I(/",    "\xb4")
    t.add("O)",     "\xec")
    t.add("O(",     "\xe9")
    t.add("O)\\",   "\xce")
    t.add("O(\\",   "\xeb")
    t.add("O)/",    "\xed")
    t.add("O(/",    "\xea")
    t.add("U)",     "\xc7")
    t.add("U(",     "\xc3")
    t.add("U)\\",   "\xc9")
    t.add("U(\\",   "\xc5")
    t.add("U)/",    "\xc8")
    t.add("U(/",    "\xc4")
    t.add("W)",     "\xf7")
    t.add("W(",     "\xf3")
    t.add("W)\\",   "\xf9")
    t.add("W(\\",   "\xf5")
    t.add("W)/",    "\xf8")
    t.add("W(/",    "\xf4")

    t.add("A)=",    "\x8a")
    t.add("A(=",    "\x86")
    t.add("H)=",    "\xda")
    t.add("H(=",    "\xd6")
    t.add("I)=",    "\xba")
    t.add("I(=",    "\xb5")
    t.add("U)=",    "\xca")
    t.add("U(=",    "\xc6")
    t.add("W)=",    "\xfa")
    t.add("W(=",    "\xf6")

    t.add("*A)",     "HA")
    t.add("*)A",     "HA")
    t.add("*A(",     "hA")
    t.add("*(A",     "hA")
    #
    t.add("*(\\A",   "\xaaA")
    t.add("*A)/",    "\xadA")
    t.add("*)/A",    "\xadA")
    t.add("*A(/",    "\xa9A")
    t.add("*(/A",    "\xa9A")

    #
    t.add("*E)",     "HE")
    t.add("*)E",     "HE")
    t.add("*E(",     "hE")
    t.add("*(E",     "hE")
    #
    t.add("*(\\E",   "\xaaE")
    t.add("*E)/",    "\xadE")
    t.add("*)/E",    "\xadE")
    t.add("*E(/",    "\xa9E")
    t.add("*(/E",    "\xa9E")

    t.add("*H)",     "HJ")
    t.add("*)H",     "HJ")
    t.add("*H(",     "hJ")
    t.add("*(H",     "hJ")

    #
    t.add("*H)\\",   "\xaeJ")
    t.add(")\\*H",   "\xaeJ")
    t.add("*)\\H",   "\xaeJ")
    #
    t.add("*H)/",    "\xadJ")
    t.add("*)/H",    "\xadJ")
    #
    t.add("*)=H",    "\xafJ")
    t.add("(/*H",    "\xa9J")
    t.add("*(/H",    "\xa9J")

    #
    t.add("*I)",     "HI")
    t.add("*)I",     "HI")
    t.add("*I(",     "hI")
    t.add("*(I",     "hI")
    #
    #
    t.add("*I)/",    "\xadI")
    t.add("*)/I",    "\xadI")
    t.add("*I(/",    "\xa9I")
    t.add("*(/I",    "\xa9I")
    #
    t.add("*O)",     "HO")
    t.add("*)O",     "HO")
    t.add("*O(",     "hO")
    t.add("*(O",     "hO")

    #
    t.add("*(\\O",   "\xaaO")
    t.add("*O)/",    "\xadO")
    t.add("*)/O",    "\xadO")
    t.add("*O(/",    "\xa9O")
    t.add("*(/O",    "\xa9O")

    #
    t.add("*)U",     "HU")
    t.add("*U)",     "HU")
    t.add("*(U",     "hU")
    t.add("*U(",     "hU")
    #
    t.add("*(/U",    "\xa9U")
    t.add("*U(/",    "\xa9U")
    #
    t.add("*(=U",    "\xabU")
    t.add("*U(=",    "\xabU")
    
    t.add("*W)",     "HW")
    t.add("*)W",     "HW")
    t.add("*W(",     "hW")
    t.add("*(W",     "hW")
    #
    #
    t.add("*W)/",    "\xadW")
    t.add("*)/W",    "\xadW")
    t.add("*W(/",    "\xa9W")
    t.add("*(/W",    "\xa9W")

    t.add("*A)=",    "\xafA")
    t.add("*)=A",    "\xafA")
    t.add("*A(=",    "\xabA")
    t.add("*W)=",    "\xafW")
    t.add("*)=W",    "\xafW")
    t.add("*W(=",    "\xabW")
    t.add("*(=W",    "\xabW")

    t.add("A\\",    "\x81")
    t.add("A/",     "\x80")
    t.add("E\\",    "\x9a")
    t.add("E/",     "\x99")
    t.add("H\\",    "\xd1")
    t.add("H/",     "\xd0")
    t.add("I\\",    "\xb1")
    t.add("I/",     "\xb0")
    t.add("O\\",    "\xe8")
    t.add("O/",     "\xe7")
    t.add("U\\",    "\xc1")
    t.add("U/",     "\xc0")
    t.add("W\\",    "\xf1")
    t.add("W/",     "\xf0")

    t.add("A(/|",   "\x90")
    t.add("A(=|",   "\x92")
    t.add("A(\\|",  "\x91")
    t.add("A(|",    "\x8f")
    t.add("A)|",    "\x93")
    t.add("A)/|",   "\x94")
    t.add("A)=|",   "\x98")
    t.add("A)\\|",  "\x95")
    t.add("H)|",    "\xe3")
    t.add("H(|",    "\xdf")
    t.add("H)/|",   "\xe4")
    t.add("H)=|",   "\xe6")
    t.add("H)\\|",  "\xe5")
    t.add("H(/|",   "\xe0")
    t.add("H(=|",   "\xe2")
    t.add("H(\\|",  "\xe1")
    t.add("W)|",    "\xa5")
    t.add("W(/|",   "\xa1")
    t.add("W(=|",   "\xa3")
    t.add("W(\\|",  "\xa2")
    t.add("W)/|",   "\xa6")
    t.add("W)=|",   "\xa8")
    t.add("W)\\|",  "\xa7")

    t.add("A=",     "\x82")
    t.add("H=",     "\xd2")
    t.add("I=",     "\xb2")
    t.add("U=",     "\xc2")
    t.add("W=",     "\xf2")

    t.add("I\\+",   "\xbd")
    t.add("I+\\",   "\xbd")
    t.add("I/+",    "\xbc")
    t.add("I+/",    "\xbc")
    t.add("U\\+",   "\xcd")
    t.add("U+\\",   "\xcd")
    t.add("U/+",    "\xcc")
    t.add("U+/",    "\xcc")

    t.add("A|",     "\x8b")
    t.add("A/|",    "\x8c")
    t.add("A\\|",   "\x8d")
    t.add("H|",     "\xdb")
    t.add("H/|",    "\xdc")
    t.add("H\\|",   "\xdd")
    t.add("W|",     "\xfb")
    t.add("W/|",    "\xfc")
    t.add("W|/",    "\xfc")
    t.add("W\\|",   "\xfd")
    t.add("W|\\",   "\xfd")

    t.add("A=|",    "\x8e")
    t.add("H=|",    "\xde")
    t.add("W=|",    "\xfe")

    t.add("R(",     "\xbf")
    t.add("*R(",    "hR")
    t.add("*(R",    "hR")

    t.add("R)",     "\xcf")
    t.add("*R)",    "HR")
    t.add("*)R",    "HR")

#    t.add("~",      u"~")
#    t.add("-",      u"-")
    
#    t.add("(null)", u"(null)")
#    t.add("&", "&")
    
    t.add("0", "0")
    t.add("1", "1")
    t.add("2", "2")
    t.add("3", "3")
    t.add("4", "4")
    t.add("5", "5")
    t.add("6", "6")
    t.add("7", "7")
    t.add("8", "8")
    t.add("9", "9")
    
    t.add("@", "@")
    t.add("$", "$")
    
    t.add(" ", " ")
    
    t.add(".", ".")
    t.add(",", ",")
    t.add("'", "@")
    t.add(":", ":")
    t.add(";", ";")
    t.add("_", "_")
    t.add("-", "-")

    t.add("[", "[")
    t.add("]", "]")

    t.add("[1", "(")
    t.add("]1", ")")
    
    t.add("[2", "(")
    t.add("]2", ")")
    
    t.add("\n", "")

    t.add("*#2", "v")  # GREEK (CAPITAL) LETTER STIGMA  # FIXME: This is not supposed to be final sigma, but there is no stigma in Galatia.
    t.add("#2", "v")   # GREEK SMALL LETTER STIGMA  # FIXME: This is not supposed to be final sigma, but there is no stigma in Galatia.

    
    return t

#t = beta2unicodeTrie()

#import sys

#for line in file(sys.argv[1]):
#    a, b = t.convert(line)
#    if b:
#        print a.encode("utf-8"), b
#        raise Exception
#    print a.encode("utf-8")


beta2galatiatrie = beta2GalatiaTrie()
beta2unicodetrie = beta2unicodeTrie()
