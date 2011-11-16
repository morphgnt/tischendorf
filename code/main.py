import reader
import strongsmapping
from lexicon import Lexicon
from tischreader import TischReader
import linearreader
from manual_analyses import ManualAnalyses
import kind

try:
    import psyco
    psyco.full()
except:
    pass

WHParsedBasedir = "../text/whparsed"
tischbasedir = "../text/unaccented"
AccentedTischbasedir = "../text/accented"
ClintYaleAccentedTischbasedir = "/home/ulrikp/Ongoing/ClintYale4/OLB"
tisch_out_basedir = "."
AccentedWHbasedir = "../../westcott-hort-accented/Flat/BETA"

def myambiguityfinder(w):
    return "/" in str(w.Strongs1) or "/" in w.parsing or w.parsing==""

def read_W27Var_NA27():
    dir=WHParsedBasedir
    suffix = "WHP"
    rd = reader.Reader(dir, suffix)
    rd.read_NT(reader.read_na27_only)
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

def read_WHB():
    dir=AccentedWHbasedir
    suffix = "WHB"
    rd = reader.Reader(dir, suffix)
    rd.read_NT(reader.read_AccentedTischendorf)
    return rd

def read_WH_writeMQL():
    rd = read_W27Var_NA27()
    rd.applyMappings()
    rd.write_MQL("WH.mql", False)
    return rd

def read_WH_writeMQL_oldstyle():
    rd = read_WH()
    rd.applyMappings()
    rd.write_MQL("WH11.mql", True)
    return rd

def read_W27Var_write_SFM():
    rd = read_W27Var_NA27()
    rd.applyMappings()
    rd.write_SFM()

def read_Tischendorf():
    dir = tischbasedir
    suffix = ""
    rd = reader.Reader(dir, suffix)
    rd.read_NT(reader.read_tischendorf)
    return rd


def read_Tischendorf_MT():
    dir = tischbasedir
    suffix = ""
    rd = reader.Reader(dir, suffix)
    rd.read_MT(reader.read_tischendorf)
    return rd


def read_AccentedTischendorf():
    dir = AccentedTischbasedir
    suffix = ""
    rd = reader.Reader(dir, suffix)
    rd.read_NT(reader.read_AccentedTischendorf)
    return rd


def read_AccentedTischendorf_MT():
    dir = AccentedTischbasedir
    suffix = ""
    rd = reader.Reader(dir, suffix)
    rd.read_MT(reader.read_AccentedTischendorf)
    return rd


def read_AccentedTischendorf_write_StrippedLinear():
    rd = read_AccentedTischendorf()
    rd.applyMappings()
    rd.write_StrippedLinear()
    return rd

def read_WH_write_WHLinear():
    rd = read_WH()
    rd.applyMappings()
    rd.write_WHLinear()
    return rd

def read_ClintYaleAccentedTischendorf_write_linear():
    dir = ClintYaleAccentedTischbasedir
    suffix = ""
    rd = reader.Reader(dir, suffix)
    rd.read_NT(reader.read_AccentedTischendorf)
    rd.write_Linear()
    return rd

def read_AccentedTischendorf_write_linear():
    rd = read_AccentedTischendorf()
    rd.write_Linear()
    return rd

def read_TSP():
    dir="."
    suffix = "TSP"
    rd = linearreader.LinearReader(dir, suffix)
    rd.read_NT(reader.read_wh_only)
    return rd

def read_TSP_writeMQL():
    rd = read_TSP()
    rd.applyLemma(kind.kANLEX)
    rd.parse_sentences_and_clauses()
    rd.write_MQL("tischendorfmorph.mql", False) # False = bUseOldStyle
    return rd

def read_TSP_writeOSIS():
    rd = read_TSP()
    rd.applyLemma(kind.kANLEX)
    rd.parse_sentences_and_clauses()
    rd.write_OSIS("tischendorfmorph.osis.xml")
    return rd

def read_TSP_writeSFM():
    rd = read_TSP()
    rd.applyLemma(kind.kANLEX)
    rd.write_SFM()
    return rd

def read_TSP_writeTUP():
    rd = read_TSP()
    rd.addVersesToVerseDicts()
    rd.write_TUP()
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
    tischrd.writeBooks_MORPH_style(tisch_out_basedir, "TSP", kind.kBETA)
    lexicon = whrd.lexicon
    lexicon.writeLexicon("lexicon_nonunique.txt", False)
    tischlexicon = Lexicon()
    tischrd.produceLexicon(tischlexicon).writeLexicon("tischlexicon_nonunique.txt", False)
    return tischrd

def read_Tischendorf_WH_Matthew_compare_them():
    lexicon = Lexicon()
    tischrd = read_AccentedTischendorf_MT()
    ma = ManualAnalyses("./manual_analyses.txt")
    #whrd = read_WH_writeMQL()
    whrd = read_WH_MT();
    #trstephrd = read_Stephanus()
    #byzrd = read_Byzantine()
    #lexicon = byzrd.produceLexicon(lexicon)
    #lexicon = trstephrd.produceLexicon(lexicon)
    whrd.compareTischendorf(tischrd, lexicon, ma)
    tischrd.applyMappings()    
    tischrd.writeBooks_MORPH_style(tisch_out_basedir, "TSP", kind.kBETA)
    lexicon = whrd.lexicon
    lexicon.writeLexicon("lexicon_nonunique.txt", False)
    tischlexicon = Lexicon()
    tischrd.produceLexicon(tischlexicon).writeLexicon("tischlexicon_nonunique.txt", False)
    return tischrd

def read_Tischendorf_WH_compare_them_writeAmbiguities():
    ma = ManualAnalyses("./manual_analyses.txt")
    tischrd = read_Tischendorf_WH_compare_them()
    tischrd.writeSubset_MORPH_style("out.txt", myambiguityfinder,ma, kind.kBETA)
    return tischrd

def read_Tischendorf_WH_compare_them_writeMQL():
    tischrd = read_Tischendorf_WH_compare_them()
    tischrd.parse_sentences_and_clauses()
    tischrd.write_MQL("tischendorfmorph.mql", False)
    return tischrd

def read_Tischendorf_WH_compare_them_writeSFM():
    tischrd = read_Tischendorf_WH_compare_them()
    tischrd.write_SFM()
    return tischrd

def read_WH_write_lexicon():
    whrd = read_WH();
    lexicon = Lexicon()
    lexicon = whrd.produceLexicon(lexicon)
    lexicon.writeLexicon("lexicon_nonunique.txt", False)
    return whrd

def getSingleStrongsList():
    sm = reader.read_StrongsLemmas()
    sm.getSingleNumberDictionary()

def parseTischendorfBETA():
    tr = TischReader()
    tr.read_BETA_file("./Tischendorf.BETA.txt")
    tr.addVersesToVerseDicts()
    tr.writeAsMORPH(".", "TBA", kind.kBETA)
    return tr

#read_WH_writeMQL()
#read_WH_writeMQL_oldstyle()
#read_W27Var_write_SFM()
#read_Tischendorf()
#read_WH_write_lexicon()
#read_Tischendorf_WH_compare_them_writeAmbiguities()
#getSingleStrongsList()
#parseTischendorfBETA()
#read_AccentedTischendorf_write_StrippedLinear()
#read_WH_write_WHLinear()
#read_Tischendorf_WH_compare_them_writeMQL()
#read_ClintYaleAccentedTischendorf_write_linear()
#read_AccentedTischendorf_write_linear()
#read_Tischendorf_WH_compare_them_writeSFM()
#read_TSP_writeSFM()
#read_WHB()
#read_Tischendorf_WH_Matthew_compare_them()
#read_Tischendorf_WH_compare_them()
#read_TSP_writeTUP()
read_TSP_writeMQL()
#read_TSP_writeOSIS()
