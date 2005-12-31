import reader
import strongsmapping
from lexicon import Lexicon
from tischreader import TischReader
import linearreader
from manual_analyses import ManualAnalyses

byzbasedir = "/home/ulrikp/build/GNT/www-byztxt-com"
WHParsedBasedir = "/projects/Tischendorf/Tisch/text/WHParsed"
tischbasedir = "/projects/Tischendorf/Tisch/text/Unparsed"
AccentedTischbasedir = "/projects/Tischendorf/Tisch/text/Accented"
ClintYaleAccentedTischbasedir = "/home/ulrikp/Ongoing/ClintYale4/OLB"
tisch_out_basedir = "."

def myambiguityfinder(w):
    return "/" in str(w.Strongs1) or "/" in w.parsing or w.parsing==""

def read_W27Var_NA27_MT():
    dir=WHParsedBasedir
    suffix = "WHP"
    rd = reader.Reader(dir, suffix)
    rd.read_MT_NA27()
    return rd

def read_W27Var_NA27():
    dir=WHParsedBasedir
    suffix = "WHP"
    rd = reader.Reader(dir, suffix)
    rd.read_NT(reader.read_na27_only)
    return rd

def read_Stephanus():
    dir=byzbasedir + "/Stephens-TR-Parsed-with-Scrivener-Variants"
    suffix = "TRP"
    rd = reader.Reader(dir, suffix)
    rd.read_NT(reader.read_stephens)
    return rd

def read_Stephanus_writeMQL():
    dir=byzbasedir + "/Stephens-TR-Parsed-with-Scrivener-Variants"
    suffix = "TRP"
    rd = reader.Reader(dir, suffix)
    rd.read_NT_write_MQL("Stephens.mql", reader.read_stephens, False)
    return rd

def read_Stephanus_MT():
    dir=byzbasedir + "/Stephens-TR-Parsed-with-Scrivener-Variants"
    suffix = "TRP"
    rd = reader.Reader(dir, suffix)
    rd.read_MT(reader.read_stephens)
    return rd

def read_Byzantine():
    dir = byzbasedir + "/Byzantine-Parsed-text"
    suffix = "BZP"
    rd = reader.Reader(dir, suffix)
    rd.read_NT(reader.read_wh_only)
    return rd

def read_Byzantine_writeMQL():
    dir = byzbasedir + "/Byzantine-Parsed-text"
    suffix = "BZP"
    rd = reader.Reader(dir, suffix)
    rd.read_NT_write_MQL("Byzantine.mql", reader.read_wh_only, False)
    return rd

def read_WH():
    dir=WHParsedBasedir
    suffix = "WHP"
    rd = reader.Reader(dir, suffix)
    rd.read_NT(reader.read_wh_only)
    return rd

def read_WH_MT():
    dir=WHParsedBasedir
    suffix = "WHP"
    rd = reader.Reader(dir, suffix)
    rd.read_MT(reader.read_wh_only)
    return rd

def read_WH_writeMQL():
    dir=WHParsedBasedir
    suffix = "WHP"
    rd = reader.Reader(dir, suffix)
    rd.read_NT_write_MQL("WH.mql", reader.read_wh_only, False)
    return rd

def read_WH_writeMQL_oldstyle():
    dir=WHParsedBasedir
    suffix = "WHP"
    rd = reader.Reader(dir, suffix)
    rd.read_NT_write_MQL("WH11.mql", reader.read_wh_only, True)

def read_W27Var_write_SFM():
    dir=WHParsedBasedir
    suffix = "WHP"
    rd = reader.Reader(dir, suffix)
    rd.read_NT_write_SFM()

def read_WH_add_lemmas():
    dir = WHParsedBasedir
    suffix = "WHP"
    whrd = reader.Reader(dir, suffix)
    whrd.read_NT_write_SFM()

def read_Tischendorf():
    dir = tischbasedir
    suffix = ""
    rd = reader.Reader(dir, suffix)
    rd.read_NT(reader.read_tischendorf)
    return rd


def read_Tischendorf():
    dir = tischbasedir
    suffix = ""
    rd = reader.Reader(dir, suffix)
    rd.read_NT(reader.read_tischendorf)
    return rd

def read_AccentedTischendorf():
    dir = AccentedTischbasedir
    suffix = ""
    rd = reader.Reader(dir, suffix)
    rd.read_NT_AccentedTischendorf()
    return rd


def read_AccentedTischendorf_write_StrippedLinear():
    dir = AccentedTischbasedir
    suffix = ""
    rd = reader.Reader(dir, suffix)
    rd.read_NT_AccentedTischendorf_write_stripped_linear()
    return rd

def read_ClintYaleAccentedTischendorf_write_linear():
    dir = ClintYaleAccentedTischbasedir
    suffix = ""
    rd = reader.Reader(dir, suffix)
    rd.read_NT_AccentedTischendorf_write_linear()
    return rd

def read_AccentedTischendorf_write_linear():
    dir = AccentedTischbasedir
    suffix = ""
    rd = reader.Reader(dir, suffix)
    rd.read_NT_AccentedTischendorf_write_linear()
    return rd

def read_AccentedTischendorf_writeSFM():
    dir = AccentedTischbasedir
    suffix = ""
    rd = reader.Reader(dir, suffix)
    rd.read_NT_AccentedTischendorf_write_SFM()
    return rd

def read_Tischendorf_MT():
    dir = tischbasedir
    suffix = ""
    rd = reader.Reader(dir, suffix)
    rd.read_MT_Tisch()
    return rd

def read_Tischendorf_writeMQL():
    rd = read_Tischendorf()
    rd.writeMQL("tischendorf.mql", False)

def read_TSP_writeMQL():
    dir="."
    suffix = "TSP"
    rd = linearreader.LinearReader(dir, suffix)
    rd.read_NT_write_MQL("tischendorfmorph.mql", reader.read_wh_only, False)
    return rd

def read_Tischendorf_WH_compare_them():
    lexicon = Lexicon()
    tischrd = read_AccentedTischendorf()
    ma = ManualAnalyses("./manual_analyses.txt")
    #whrd = read_WH_writeMQL()
    whrd = read_WH();
    #trstephrd = read_Stephanus()
    #byzrd = read_Byzantine()
    #lexicon = byzrd.produceLexicon(lexicon)
    #lexicon = trstephrd.produceLexicon(lexicon)
    whrd.compareTischendorf(tischrd, lexicon, ma)
    tischrd.applyMappings()    
    tischrd.writeBooks_MORPH_style(tisch_out_basedir, "TSP")
    lexicon = whrd.lexicon
    lexicon.writeLexicon("lexicon_nonunique.txt", False)
    tischlexicon = Lexicon()
    tischrd.produceLexicon(tischlexicon).writeLexicon("tischlexicon_nonunique.txt", False)
    return tischrd

def read_Tischendorf_WH_compare_them_writeAmbiguities():
    ma = ManualAnalyses("./manual_analyses.txt")
    tischrd = read_Tischendorf_WH_compare_them()
    tischrd.writeSubset_MORPH_style("out.txt", myambiguityfinder,ma)

def read_Tischendorf_WH_compare_them_writeMQL():
    tischrd = read_Tischendorf_WH_compare_them()
    tischrd.writeMQL("tischendorfmorph.mql", False)

def read_Tischendorf_WH_MT_compare_them():
    tischrd = read_Tischendorf_MT()
    whrd = read_WH_MT();
    whrd.compareTischendorf(tischrd, lexicon)
    #tischrd.writeSubset_MORPH_style("out.txt", myambiguityfinder)
    tischrd.applyMappings()    
    lexicon = whrd.lexicon
    lexicon.writeLexicon("lexicon_nonunique.txt", False)
    #tischrd.writeMQL("tischendorfmorph.mql", False)


def read_WH_write_lexicon():
    whrd = read_WH();
    lexicon = Lexicon()
    lexicon = whrd.produceLexicon(lexicon)
    lexicon.writeLexicon("lexicon_nonunique.txt", False)

def getSingleStrongsList():
    sm = strongsmapping.StrongsMapping()
    sm.read("./lemmatable.txt")
    sm.getSingleNumberDictionary()

def parseTischendorfBETA():
    tr = TischReader()
    tr.read_BETA_file("./Tischendorf.BETA.txt")
    tr.addVersesToVerseDicts()
    tr.writeAsMORPH(".", "TBA")


#read_Stephanus()
#read_Stephanus_writeMQL()
#read_Byzantine()
#read_Byzantine_writeMQL()
    

#read_WH_writeMQL()
#read_WH_writeMQL_oldstyle()
#read_W27Var_write_SFM()
#read_Tischendorf()
#read_Tischendorf_writeMQL()
#read_WH_write_lexicon()
#read_Tischendorf_WH_compare_them_writeAmbiguities()
#read_Tischendorf_WH_MT_compare_them()
#read_TSP_writeMQL()
#getSingleStrongsList()
#parseTischendorfBETA()
#read_WH_add_lemmas()
#read_AccentedTischendorf_writeSFM()
#read_AccentedTischendorf_write_StrippedLinear()
#read_Tischendorf_WH_compare_them_writeMQL()
#read_ClintYaleAccentedTischendorf_write_linear()
#read_AccentedTischendorf_write_linear()
read_Tischendorf_WH_compare_them()

