import string
from variant import *
from kind import *
import re
from morphgnt import convert
import rptag
from lexicon import Lexicon
from morphgnt import booknames
import unicodedata

state_surface = 0
state_strongs1 = 1
state_strongs2 = 2
state_parsing = 3

OLBtoBETAtrans = string.maketrans("abgdezhyiklmnxoprsvtufcqw", "ABGDEZHQIKLMNCOPRSSTUFXYW")
OLBtoGALATIAtrans = string.maketrans("abgdezhyiklmnxoprsvtufcqw", "abgdezjqiklmnxoprsvtufcyw")
BETAtoGALATIAtrans = string.maketrans("ABGDEZHQIKLMNCOPRSSTUFXYW", "abgdezjqiklmnxoprsvtufcyw")
MixedCaseBETAtoBETAtrans = string.maketrans("AaBbGgDdEeZzHhQqIiKkLlMmNnCcOoPpRrSsJjTtUuFfXxYyWw", "AABBGGDDEEZZHHQQIIKKLLMMNNCCOOPPRRSSSSTTUUFFXXYYWW")

BETAtoOLBtrans = string.maketrans("ABGDEZHQIKLMNCOPRSTUFXYW", "abgdezhyiklmnxoprstufcqw")



reolbstrip = re.compile("[\\[\\]<>]+")
#reaccentsstrip = re.compile("[/+\\|\\(\\)\\\\=\[\],.;':]+")
reaccentsstrip = re.compile("[/+\\|\\(\\)\\\\=,.;':\*]+")

reUpperCaseBETA = re.compile(r'([A-Z])')
reMoveDiacriticsBETA = re.compile(r'\*([AEHIOUW])([\(\)][/=\\|]*)')
reMoveBreathingRhoBETA = re.compile(r'\*R([\(\)])')

alternate_spellings = { "SAMAREITWN" : "SAMARITWN" ,
                        "OUTWS" : "OUTW",
                        "ERRANTISEN" : "ERANTISEN",
                        "AXRIS" : "AXRI",
                        "ALLA" : "ALL",
                        "EORAKA" : "EWRAKA"}

alternate_Tischendorf_spellings = { "DAUID" : [ "DAUEID" ],
                                    "OZIAN" : [ "OZEIAN" ],
                                    "OZIAS" : [ "OZEIAS" ],
                                    "AXAS" : [ "AXAZ" ],
                                    "IWSIAN" : [ "IWSEIAN" ],
                                    "IWSIAS" : [ "IWSEIAS" ],
                                    "ELIAKIM" : [ "ELIAKEIM" ],
                                    "AXIM" : [ "AXEIM" ],
                                    "MATQAN" : [ "MAQQAN" ],
                                    "MARIAN" : [ "MARIAM" ],
                                    "MARIA" : [ "MARIAM" ],
                                    "PASIN" : [ "PASI" ],
                                    "NAZARET" : [ "NAZAREQ" ],
                                    "NEFQALIM" : [ "NEFQALEIM" ],
                                    "ALIEIS" : [ "ALEEIS" ],
                                    "ELQETW" : [ "ELQATW" ], # This is correct!
                                    "DUSIN" : [ "DUSI" ],
                                    "EKATONTARXOS" : [ "EKATONTARXHS" ],
                                    "HNEWXQHSAN" : [ "ANEWXQHSAN" ],
                                    "SAMAREITWN" : [ "SAMARITWN" ],
                                    "APOKTEINONTWN" : [ "APOKTENNONTWN" ],
                                    "DE" : [ "D" ],
                                    "HLIAS" : [ "HLEIAS" ],
                                    "BHQSAIDA" : [ "BHQSAIDAN" ],
                                    "EUDOKHSEN" : [ "HUDOKHSEN" ],
                                    "NINEUITAI" : [ "NINEUEITAI" ],
                                    "ERRIYAN" : [ "ERIYAN" ],
                                    "HLIAN" : [ "HLEIAN" ],
                                    "SULLALOUNTES" : [ "SUNLALOUNTES" ],
                                    "HLIA" : [ "HLEIA" ],
                                    "PALIGGENESIA" : [ "PALINGENESIA" ],
                                    "BASTASASIN" : [ "BASTASASI" ],
                                    "IERIXW" : [ "IEREIXW" ],
                                    "RABBI" : [ "RABBEI" ],
                                    "GEQSHMANI" : [ "GEQSHMANEI" ],
                                    "GUNAICIN" : [ "GUNAICI" ],
                                    "PILATW" : [ "PEILATW" ],
                                    "PILATOS" : [ "PEILATOS" ],
                                    "PIEIN" : [ "PEIN" ],
                                    "ELWI" : [ "HLEI" ],
                                    "SABAXQANI" : [ "SABAXQANEI" ],
                                    "PILATON" : [ "PEILATON" ],
                                    "ADDI" : [ "ADDEI" ],
                                    "AGOUSIN" : [ "AGOUSI" ],
                                    "AGALLIATE" : [ "AGALLIASQE" ], # Could also be indicative, but only occurs once, in an imperative context
                                    "ALL" : [ "ALLA" ],
                                    "ANAIDEIAN," : [ "ANAIDIAN" ],
                                    "EKAQARISQH" : [ "EKAQERISQH" ],
                                    "EIDAN" : [ "IDAN" ],
                                    "IEROSOLUMITAI" : [ "IEROSOLUMEITAI" ], 
                                    "SULLUPOUMENOS" : [ "SUNLUPOUMENOS" ],
                                    "SUMPNIGOUSIN" : [ "SUNPNIGOUSIN" ],
                                    "THLAUGWS" : [ "DHLAUGWS" ],  # This is correct, according to ANLEX.
                                    "ALAZONEIA" : [ "ALAZONIA" ],
                                    "ALAZONEIAIS" : [ "ALAZONIAIS" ],
                                    "ANAIDEIAN" : [ "ANAIDIAN" ],
                                    "ANTIPAS" : [ "ANTEIPAS" ],
                                    "AREION" : [ "ARION" ],
                                    "AREIOU" : [ "ARIOU" ],
                                    "AREOPAGITHS" : [ "AREOPAGEITHS" ],
                                    "ARRABWNA" : [ "ARABWNA" ],
                                    "ARSESIN" : [ "ARRESIN" ],
                                    "ASUGKRITON" : [ "ASUNKRITON" ],
                                    "ATTALEIAN" : [ "ATTALIAN" ],
                                    "BENIAMIN" : [ "BENIAMEIN" ],
                                    "DIELIPEN" : [ "DIELEIPEN" ],
                                    "DOULEIAN" : [ "DOULIAN" ],
                                    "DOULEIAS" : [ "DOULIAS" ],
                                    "ECEKREMATO" : [ "ECEKREMETO" ], # Strange! But it is not a textual error (LU 19:48.11)
                                    "EGGEGRAMMENH" : [ "ENGEGRAMMENH" ],
                                    "EGGEGRAPTAI" : [ "ENGEGRAPTAI" ],
                                    "EGKAINIA" : [ "ENKAINIA" ],
                                    "EGKAKEIN" : [ "ENKAKEIN" ],
                                    "EGKAKWMEN" : [ "ENKAKWMEN" ],
                                    "EGKAQETOUS" : [ "ENKAQETOUS" ],
                                    "EGKATALEIYEIS" : [ "ENKATALEIYEIS" ],
                                    "EGKATELEIFQH" : [ "ENKATELEIFQH" ],
                                    "EGKATELIPEN" : [ "ENKATELIPEN" ],
                                    "EGKATOIKWN" : [ "ENKATOIKWN" ],
                                    "EGKAUXASQAI" : [ "ENKAUXASQAI" ],
                                    "EGKEKAINISTAI" : [ "ENKEKAINISTAI" ],
                                    "EGKENTRISAI" : [ "ENKENTRISAI" ],
                                    "EGKENTRISQHSONTAI" : [ "ENKENTRISQHSONTAI" ],
                                    "EGKOPHN" : [ "EKKOPHN" ], # This is NOT a textual error. However, it is also not wrong, according to ANLEX. 1CO 9:12.22
                                    "EGKOPTESQAI" : [ "ENKOPTESQAI" ],
                                    "EGKOPTW" : [ "ENKOPTW" ],
                                    "EGKRINAI" : [ "ENKRINAI" ],
                                    "EIDEN" : [ "IDEN" ],
                                    "ANWRQWQH" : [ "ANORQWQH" ],  # This is OK, according to Perseus...
                                    "ANOIGHSETAI" : [ "ANOIXQHSETAI" ], # This is OK, according to ANLEX.
                                    "APODW" : [ "APODOI" ], # NOTE: Is this a textual error? "APODW|" ... Nope, it's not a textual error (1TH 5:15), but I am going to parse it as APODW| anyway.  The things that Perseus calls it are not helpful.
                                    "APOKTEINEI" : [ "APOKTENNEI" ],
                                    "EIDWLEIW" : [ "EIDWLIW" ],
                                    "EILIKRINEIA" : [ "EILIKRINIA" ],
                                    "EILIKRINEIAS" : [ "EILIKRINIAS" ],
                                    "EMPERIPATHSW" : [ "ENPERIPATHSW" ],
                                    "FARMAKEIA" : [ "FARMAKIA" ],
                                    "GALATIAN" : [ "GALLIAN" ],
                                    "IEROSOLUMITWN" : [ "IEROSOLUMEITWN" ],
                                    "ISRAHLITAI" : [ "ISRAHLEITAI" ],
                                    "ISRAHLITHS" : [ "ISRAHLEITHS" ],
                                    "IWANNH" : [ "IWANNEI" ],
                                    "KAISAREIA" : [ "KAISARIA" ],
                                    "KAISAREIAN" : [ "KAISARIAN" ],
                                    "KAISAREIAS" : [ "KAISARIAS" ],
                                    "KATAKRINW" : [ "KATAKREINW" ],
                                    "KATEKRINEN" : [ "KATEKREINEN" ],
                                    "KAUDA" : [ "KLAUDA" ],
                                    "KIS" : [ "KEIS" ],
                                    "KOLAKEIAS" : [ "KOLAKIAS" ],
                                    "KUBEIA" : [ "KUBIA" ],
                                    "LAODIKEIA" : [ "LAODIKIA" ],
                                    "LAODIKEIAN" : [ "LAODIKIAN" ],
                                    "LAODIKEIAS" : [ "LAODIKIAS" ],
                                    "LEUI" : [ "LEUEI" ],
                                    "LEUIN" : [ "LEUEIN" ],
                                    "LEUIS" : [ "LEUEIS" ],
                                    "LEUITAS" : [ "LEUEITAS" ],
                                    "LEUITHS" : [ "LEUEITHS" ],
                                    "LEUITIKHS" : [ "LEUEITIKHS" ],
                                    "MAGEIAIS" : [ "MAGIAIS" ],
                                    "MAQQAT" : [ "MAQQAQ" ],
                                    "MELXI" : [ "MELXEI" ],
                                    "MEQODEIAN" : [ "MEQODIA" ],
                                    "MEQODEIAS" : [ "MEQODIAS" ],
                                    "MURA" : [ "MURRA" ],
                                    "NINEUITAIS" : [ "NINEUEITAIS" ],
                                    "ORNIS" : [ "ORNIC" ],
                                    "PAIDEIAN" : [ "PAIDIAN" ],
                                    "PAIDEIAS" : [ "PAIDIAS" ],
                                    "PALIGGENESIAS" : [ "PALINGENESIAS" ],
                                    "PANDOXEION" : [ "PANDOKION" ], # NOTE: The textual apparatus lets one assume that it is OK to analyze as though it were PANDOXEION.
                                    "PILATOU" : [ "PEILATOU" ],
                                    "QRHSKEIA" : [ "QRHSKIA" ],
                                    "QRHSKEIAS" : [ "QRHSKIAS" ],
                                    "SAMAREIAN" : [ "SAMARIAN" ],
                                    "SAMAREIA" : [ "SAMARIA" ],
                                    "SAMAREIAS" : [ "SAMARIAS" ],
                                    "SEIROIS" : [ "SIROIS" ],
                                    "SELEUKEIAN" : [ "SELEUKIAN" ],
                                    "SEMEIN" : [ "SEMEEIN" ],
                                    "SOLOMWN" : [ "SALWMWN" ],
                                    "SUGKAKOPAQHSON" : [ "SUNKAKOPAQHSON" ],
                                    "SUGKAKOUXEISQAI" : [ "SUNKAKOUXEISQAI" ],
                                    "SUGKALEI" : [ "SUNKALEI" ],
                                    "SUGKALESAMENOS" : [ "SUNKALESAMENOS" ],
                                    "SUGKALESASQAI" : [ "SUNKALESASQAI" ],
                                    "SUGKALOUSIN" : [ "SUNKALOUSIN" ],
                                    "SUGKAQHMENOI" : [ "SUNKAQHMENOI" ],
                                    "SUGKAQHMENOS" : [ "SUNKAQHMENOS" ],
                                    "SUGKAQISANTWN" : [ "SUNKAQISANTWN" ],
                                    "SUGKATABANTES" : [ "SUNKATABANTES" ],
                                    "SUGKATAQESIS" : [ "SUNKATAQESIS" ],
                                    "SUGKATATEQEIMENOS" : [ "SUNKATATIQEIMENOS" ],
                                    "SUGKATEYHFISQH" : [ "SUNKATEYHFISQH" ],
                                    "SUGKLEIOMENOI" : [ "SUNKLEIOMENOI" ],
                                    "SUGKLHRONOMA" : [ "SUNKLHRONOMA" ],
                                    "SUGKLHRONOMOI" : [ "SUNKLHRONOMOI" ],
                                    "SUGKLHRONOMWN" : [ "SUNKLHRONOMWN" ],
                                    "SUGKOINWNEITE" : [ "SUNKOINWNEITE" ],
                                    "SUGKOINWNHSANTES" : [ "SUNKOINWNHSANTES" ],
                                    "SUGKOINWNHSHTE" : [ "SUNKOINWNHSHTE" ],
                                    "SUGKOINWNOS" : [ "SUNKOINWNOS" ],
                                    "SUGKOINWNOUS" : [ "SUNKOINWNOUS" ],
                                    "SUGKRINAI" : [ "SUNKRINAI" ],
                                    "SUGKRINONTES" : [ "SUNKRINONTES" ],
                                    "SUGKUPTOUSA" : [ "SUNKUPTOUSA" ],
                                    "SUGXAIREI" : [ "SUNXAIREI" ],
                                    "SUGXAIRETE" : [ "SUNXAIRETE" ],
                                    "SUGXAIRW" : [ "SUNXAIRW" ],
                                    "SUGXUNNETAI" : [ "SUNXUNNETAI" ],

                                    "SULLALHSAS" : [ "SUNLALHSAS" ],
                                    "SULLAMBANOU" : [ "SUNLAMBANOU" ],
                                    "SUMBALLOUSA" : [ "SUNBALLOUSA" ],
                                    "SUMBIBAZOMENON" : [ "SUNBIBAZOMENON" ],
                                    "SUMMARTUREI" : [ "SUNMARTUREI" ],
                                    "SUMMARTUROUSHS" : [ "SUNMARTUROUSHS" ],
                                    "SUMMETOXA" : [ "SUNMETOXA" ],
                                    "SUMMETOXOI" : [ "SUNMETOXOI" ],
                                    "SUMMIMHTAI" : [ "SUNMIMHTAI" ],
                                    "SUMMORFIZOMENOS" : [ "SUNMORFIZOMENOS" ],
                                    "SUMMORFON" : [ "SUNMORFON" ],
                                    "SUMPAQHSAI" : [ "SUNPAQHSAI" ],
                                    "SUMPARAGENOMENOI" : [ "SUNPARAGENOMENOI" ],
                                    "SUMPARAGENOMENOI" : [ "SUNPARAGENOMENOI" ],
                                    "SUMPARAKLHQHNAI" : [ "SUNPARAKLHQHNAI" ],
                                    "SUMPARALABEIN" : [ "SUNPARALABEIN" ],
                                    "SUMPARALABONTES" : [ "SUNPARALABONTES" ],
                                    "SUMPARALABWN" : [ "SUNPARALABWN" ],
                                    "SUMPARALAMBANEIN" : [ "SUNPARALAMBANEIN" ],
                                    "SUMPARONTES" : [ "SUNPARONTES" ],
                                    "SUMPASXEI" : [ "SUNPASXEI" ],
                                    "SUMPASXOMEN" : [ "SUNPASXOMEN" ],
                                    "SUMPLHROUSQAI" : [ "SUNPLHROUSQAI" ],
                                    "SUMPNIGONTAI" : [ "SUNPNIGONTAI" ],
                                    "SUMPOLITAI" : [ "SUNPOLITAI" ],
                                    "SUMYUXOI" : [ "SUNYUXOI" ],
                                    "SUNEILHFEN" : [ "SUNEILHFIA" ],
                                    "SUSSHMON" : [ "SUNSHMON" ],
                                    "SUSSWMA" : [ "SUNSWMA" ],
                                    "SUSTAURWQENTOS" : [ "SUNTAURWQENTOS" ],
                                    "SUSTOIXEI" : [ "SUNSTOIXEI" ],
                                    "SUSTRATIWTHN" : [ "SUNSTRATIWTHN" ],
                                    "SUSXHMATIZESQE" : [ "SUNSXHMATIZESQE" ],
                                    "SUZHN" : [ "SUNZHN" ],
                                    "SUZUGE" : [ "SUNZUGE" ],
                                    "TESSARA" : [ "TESSERA" ],
                                    "XORAZIN" : [ "XORAZEIN" ],
                                    "XEROUBIN" : [ "XEROUBEIN" ],
                                    "XALKHDWN" : [ "XALKEDWN" ],
                                    "SUGKLHRONOMOI" : [ "SUNKLHRONOMOI" ],
                                    "HLIOU" : [ "HLEIA", "HLEIOU" ],
                                    "HLI" : [ "HLEI" ],
                                    "ESLI" : [ "ESLEI" ],
                                    "AKATAPASTOUS" : [ "AKATAPAUSTOUS" ],
                                    "ANAPEIROUS" : [ "ANAPHROUS" ],
                                    "APAGWN" : [ "APAGAGWN" ],
                                    "ARSENES" : [ "ARRENES" ],


                                    "QA" : [ "AQA" ],
                                    "EIDWLOLATRIAS" : [ "EIDWLOLATREIAS" ],
                                    "EIDWLOLATRIA" : [ "EIDWLOLATREIA" ],
                                    "IERON" : [ "EIERON" ],   # NOTE: This is not a textual error (1st instance of Joh 8:2.)
                                    "EQAUMASEN" : [ "EQAUMAZEN" ],
                                    "ERRANTISEN" : [ "ERANTISEN" ],
                                    "ERRUSATO" : [ "ERUSATO" ],
                                    "ERRUSQHN" : [ "ERUSQHN" ],
                                    "ESQIONTES" : [ "ESQONTES" ],
                                    "HUXONTO" : [ "EUXONTO" ],
                                    "HMISIA" : [ "HMISEIA" ],
                                    "HSSON" : [ "HTTON" ],
                                    "EUDOKHSAN" : [ "HUDOKHSAN" ],
                                    "EUDOKHSAS" : [ "HUDOKHSAS" ],
                                    "IAIROS" : [ "IAEIROS" ],
                                    "IWRIM" : [ "IWREIM" ],
                                    "KAKOPAQIAS" : [ "KAKOPAQEIAS" ],
                                    "LOGEIAI" : [ "LOGIAI" ],
                                    "LOGEIAS" : [ "LOGIAS" ],
                                    "MARANA" : [ "MARAN" ],
                                    "MASTOIS" : [ "MASQOIS" ],
                                    "MELITHNH" : [ "MELITH" ],
                                    "MEQODEIAN" : [ "MEQODIAN" ],
                                    "MULINON" : [ "MULON" ],
                                    "NHRI" : [ "NHREI" ],
                                    "OIKTIRHSW" : [ "OIKTEIRHSW" ],
                                    "OIKTIRW" : [ "OIKTEIRW" ],
                                    "EGGISEI" : [ "EGGIEI" ],
                                    "ENEBRIMWNTO" : [ "ENEBRIMOUNTO" ],
                                    "SAPFIROS" : [ "SAPFEIROS" ],
                                    "EIDON" : [ "IDON" ],
                                    "KEGXREAIS" : [ "KENXREAIS" ],
                                    "KOLLOURION" : [ "KOLLURION" ],
                                    "SUNISTANONTES" : [ "SUNISTANTES" ],
                                    # "PEPTWKAN" : [ "PEPWKAN" ], # NOTE: This is not true!
                                    "KATEIRGASATO" : [ "KATHRGASATO" ],
                                    "EIRGASANTO" : [ "HRGASANTO" ],
                                    "APEIQOUSIN" : [ "APEIQOUSI" ],   # Note: This is ambiguous as to V-PAI-3P or V-PAP-DPM, but I assume it's the same as in WH.
                                    "ALUSESIN" : [ "ALUSESI" ], 
                                    "APELUSEN" : [ "APELUSE" ], 
                                    "ASEBESIN" : [ "ASEBESI" ], 
                                    "ASEBH" : [ "ASEBHN" ], 
                                    "AXRI" : [ "AXRIS" ], 
                                    "DEHSESIN" : [ "DEHSESI" ], 
                                    "DIASWSWSIN" : [ "DIASWSWSI" ], 
                                    "DUNAMESIN" : [ "DUNAMESI" ], 
                                    "EDOCEN" : [ "EDOCE" ], 
                                    "ELABEN" : [ "ELABE" ], 
                                    "ELAXEN" : [ "ELAXE" ], 
                                    "EQESIN" : [ "EQESI" ], 
                                    "ESQHSESIN" : [ "ESQHSESI" ], 
                                    "EXOUSIN" : [ "EXOUSI" ], 
                                    "EXWSIN" : [ "EXWSI" ], 
                                    "GINWSKOUSIN" : [ "GINWSKOUSI" ],   # Note: This is ambiguous between V-PAI-3P and V-PAP-DPM, but I will assume that it is the same as in WH.
                                    "HLQEN" : [ "HLQE" ], 
                                    "ISASIN" : [ "ISASI" ], 
                                    "KATELIPEN" : [ "KATELIPE" ], 
                                    "KLIMASIN" : [ "KLIMASI" ], 
                                    "MEXRI" : [ "MEXRIS" ], 
                                    "OUTWS" : [ "OUTW" ], 
                                    "PARADEDWKOSIN" : [ "PARADEDWKOSI" ], 
                                    "PNEUMASIN" : [ "PNEUMASI" ], 
                                    "ROMFA" : [ "ROMFAN" ], 
                                    "TERASIN" : [ "TERASI" ], 
                                    "TIMWSIN" : [ "TIMWSI" ],   # Note: This is ambiguous between V-PAI-3P and V-PAS-3P, but I will assume it is the same as in WH.
                                    "XALWSIN" : [ "XALWSI" ], 
                                    "XEIRA" : [ "XEIRAN" ], 
                                    "ZWSIN" : [ "ZWSI" ],   # Note: This is ambiguous between V-PAI-3P and V-PAS-3P, but I will assume it is the same as in WH.
                                    "QELWSIN" : [ "QELWSI" ],
                                    "EPEGNWKOSIN" : [ "EPEGNWKOSI" ],
                                    "HGAPHKOSIN" : [ "HGAPHKOSI" ],
                                    "EIXEN" : [ "EIXE" ],
                                    "KRIQWSIN" : [ "KRIQWSI" ],
                                    "SUGXARHTE" : [ "SUNXARHTE" ],
                                    "SUZHTEIN" : [ "SUNZHTEIN" ],
                                    "SUMMAQHTAIS" : [ "SUNMAQHTAIS" ],
                                    "SUSTAURWQENTOS" : [ "SUNSTAURWQENTOS" ],
                                    "EMPROSQEN" : [ "ENPROSQEN" ],
                                    "SMURNAN" : [ "ZMURNAN" ],
                                    "SMURNH" : [ "ZMURNH" ],
#                                    "" : [ "" ],
#                                    "" : [ "" ],

                                   }

tischendorfLexicon = Lexicon()
tischendorfLexicon.primeWithTischendorf()



def TischSpellingDifferenceOK(BETA_selfsurface, BETA_tischsurface):
    try:
        if BETA_tischsurface in alternate_Tischendorf_spellings[BETA_selfsurface]:
            return 1
        else:
            return 0
    except KeyError:
        return 0

def olbstrip(olbword):
    return reolbstrip.sub("", OLBtoBETAtranslate(olbword.qere_noaccents))

def RemoveAccents(surface):
    return reaccentsstrip.sub("", surface)

def OLBtoBETAtranslate(str):
    return str.translate(OLBtoBETAtrans)

def BETAtoOLBtranslate(str):
    newstr = str.translate(BETAtoOLBtrans)
    try:
        if newstr[-1] == "s":
            newstr[-1] = "v"
    except:
        pass
    return newstr

def OLBtoGALATIAtranslate(str):
    return str.translate(OLBtoGALATIAtrans)

def BETAtoGALATIAtranslate(str):
    return str.translate(BETAtoGALATIAtrans)

def MixedCaseBETAtoBETAtranslate(str):
    return str.translate(MixedCaseBETAtoBETAtrans)

def MixedCaseBETAtoBETAtranslateWithStar(str):
    newstr = reUpperCaseBETA.sub(r'*\1', str)
    newstr = reMoveDiacriticsBETA.sub(r'*\2\1', newstr)
    newstr = reMoveBreathingRhoBETA.sub(r'*\1R', newstr)
    newstr = newstr.replace("(*", "*(").replace("(/*", "*(/").replace("(\\*", "*(\\").replace("(=*", "*(=").replace(")*", "*)").replace(")/*", "*)/").replace(")\\*", "*)\\").replace(")=*", "*)=")
    return newstr.translate(MixedCaseBETAtoBETAtrans)

def mangleMQLString(str):
    return str.replace("\\", "\\\\").replace("\"", "\\\"")


class Word:
    def __init__(self, monad, variant):
        self.monad = monad
        self.break_kind = "."   # Can be 'C' for chapter-break, 'P' for paragraph-break, or '.' for no break.
        self.surface = ""       # kethiv (i.e., it is written (in the printed Tischendorf))
        self.qere = ""          # qere (i.e., please read)
        self.accented_surface = ""
        self.parsing = ""
        self.strongslemma = ""
        self.ANLEXlemma = ""
        self.alt_parsing = ""
        self.Strongs1 = -1
        self.Strongs2 = -1
        self.alt_Strongs1 = -1
        self.alt_Strongs2 = -1
        self.altlemma = ""
        self.variant = variant
        self.tag_object = None

    def ends_sentence(self):
	return self.accented_surface[-1] in [".", ";"]

    def isVariant(self):
        return self.variant == variant_second or self.variant == variant_none

    def getStrongs(self):
        lemma = ""
        if self.Strongs1 != -1:
            lemma += str(self.Strongs1)
        if self.Strongs2 != -1:
            lemma += "&" + str(self.Strongs2)
        return lemma

    def getAltStrongs(self):
        lemma = ""
        if self.alt_Strongs1 != -1:
            lemma += str(self.alt_Strongs1)
        if self.alt_Strongs2 != -1:
            lemma += "&" + str(self.alt_Strongs2)
        return lemma

    def setStrongs(self, strongs):
        if "&" in strongs:
            mylist = strongs.split("&")
            self.Strongs1 = int(mylist[0])
            self.Strongs2 = int(mylist[1])
        elif "/" in strongs:
            self.Strongs1 = strongs
        else:
            self.Strongs1 = int(strongs)

    def applyLemma(self, mapping, lemma_kind):
        strongs = self.getStrongs()
        if lemma_kind == kANLEX:
            self.ANLEXlemma = mapping.getLemmaFromStrongs(strongs)
        else:
            self.strongslemma = mapping.getLemmaFromStrongs(strongs)
            altStrongs = self.getAltStrongs()
            if altStrongs != "":
                self.altlemma = mapping.getLemmaFromStrongs(altStrongs)

    def getLemma(self):
        return self.strongslemma

    def writeSFM(self, f, booknumber, chapter, verse, word_index, monad):
        print >>f, self.getSFMReference(f, booknumber, chapter, verse, word_index)
        if self.accented_surface != "":
            surfaceUTF8 = self.accented_surface
        else:
            surfaceUTF8 = self.beta2utf8(OLBtoBETAtranslate(self.surface))
        print >>f, "\\text %s\r" % surfaceUTF8
        print >>f, "\\trans %s %d:%d" % (booknames.book_lists["UBS"][booknumber-1], chapter, verse)
        if len(self.parsing) > 0:
            print >>f, "\\pars %s\r" % self.parsing
        print >>f, "\\monad %d\r" % monad
        if self.ANLEXlemma == "":
            #lemma = "NOLEMMA"
            raise Exception("Error: lemma is empty.")
        else:
            lemma = self.ANLEXlemma
        if lemma != "":
            lemma_encoded = self.beta2utf8(lemma)
            print >>f, "\\lemma %s %s\r" % (self.getStrongs(), lemma_encoded)
        print >>f, "\\re\r"
        print >>f, "\r"

    def beta2galatia(self, beta):
        result = ""
        for s in beta.split(" "):
            # Add '\n' at the end to convert final sigma to real final sigma.
            # The '\n' will be stripped out by the conversion
            galatia, remainder = convert.beta2galatiatrie.convert(s+"\n")
            if remainder != "":
                raise Exception("galatia = '" + galatia +"'\nbeta = " + beta + "\n, and remainder was not empty, but was: '" + remainder + "'")
            result += galatia + " "
        return result[0:-1]

    def beta2utf8(self, beta):
        result = ""
        for s in beta.split(" "):
            # Add '\n' at the end to convert final sigma to real final sigma.
            # The '\n' will be stripped out by the conversion
            utf16 = convert.beta2unicode(s)

            #print (u"'%s' --> '%s'" % (s, utf16)).encode('utf-8')

            # Convert Unicode string to UTF8
            if utf16 == "":
                utf8 = ""
            else:
                utf8 = unicodedata.normalize('NFC', utf16).encode("utf-8")
            
            result += utf8 + " "
        return result[0:-1]

    def getSFMReference(self, f, booknumber, chapter, verse, word_index):
        return "\\rf %02d-%03d-%03d-%03d\r" % (int(booknumber), int(chapter), int(verse), int(word_index))

    def writeMQL(self, f, bUseOldStyle):
        if self.parsing != "":
            self.tag_object = rptag.RobinsonPierpontTag(self.parsing)
        else:
            self.tag_object = None
        print >>f, "CREATE OBJECT"
        print >>f, "FROM MONADS={%d}" % self.monad
        if bUseOldStyle:
            OT = "Word"
        else:
            OT = ""
        print >>f, "[%s" % OT

        if self.accented_surface != "":
            surfaceBETA = self.accented_surface
        else:
            surfaceBETA = OLBtoBETAtranslate(self.surface)
        print >>f, "  surface:=\"%s\";" % mangleMQLString(surfaceBETA)
        print >>f, "  surfaceutf8:=\"%s\";" % mangleMQLString(self.beta2utf8(surfaceBETA))
        print >>f, "  qere:=\"%s\";" % mangleMQLString(self.qere)
        print >>f, "  qereutf8:=\"%s\";" % mangleMQLString(self.beta2utf8(self.qere))
        #print >>f, "  olb_surface:=\"%s\";" % self.surface
        if len(self.parsing) > 0:
            print >>f, "  parsing:=\"%s\";" % self.parsing
        if self.Strongs1 != -1:
            print >>f, "  strongs1:=%s;" % str(self.Strongs1)
        if self.Strongs2 != -1:
            print >>f, "  strongs2:=%s;" % str(self.Strongs2)
        #if len(self.alt_parsing) > 0:
        #    print >>f, "  alt_parsing:=\"%s\";" % self.alt_parsing
        #if self.alt_Strongs1 != -1:
        #    print >>f, "  alt_strongs1:=%s;" % str(self.alt_Strongs1)
        #if self.alt_Strongs2 != -1:
        #    print >>f, "  alt_strongs2:=%s;" % str(self.alt_Strongs2)
        #if self.variant != variant_none:
        #    print >>f, "  is_variant:=%s;" % variant2string(self.variant)
        if self.strongslemma == "":
            lemma = ""
            raise Exception("Error: lemma is empty for word with monad %d and surface %s" % (self.monad, self.surface))
        else:
            lemma = self.strongslemma
        if lemma != "":
            print >>f, "  lemmabeta:=\"%s\";" % lemma
            print >>f, "  lemmautf8:=\"%s\";" % self.beta2utf8(lemma)
        #if self.altlemma != "":
        #    print >>f, "  alt_lemmabeta:=\"%s\";" % self.altlemma
        #    print >>f, "  alt_lemmautf8:=\"%s\";" % self.beta2utf8(self.altlemma)
        if self.tag_object != None:
            self.tag_object.writeMQL(f)
        print >>f, "]"
        if bUseOldStyle:
            print >>f, "GO\n"
        else:
            print >>f, ""

    def writeSFMShort(self, f):
        print >>f, "\\text %s" % OLBtoBETAtranslate(self.surface)
        print >>f, "\\monad %s" % str(self.monad)
        if len(self.parsing) > 0:
            print >>f, "\\pars %s" % self.parsing
        if self.Strongs1 != -1:
            print >>f, "\\str1 %d" % self.Strongs1
        if self.Strongs2 != -1:
            print >>f, "\\str2 %d" % self.Strongs2
        if len(self.alt_parsing) > 0:
            print >>f, "\\altpars %s" % self.alt_parsing
        if self.alt_Strongs1 != -1:
            print >>f, "\\altstr1 %d" % self.alt_Strongs1
        if self.alt_Strongs2 != -1:
            print >>f, "\\altstr2 %d" % self.alt_Strongs2
        print >>f, "\re\n"

    def parseStrongs(self, strongs):
        """This is necessary because "[tou 3588]" occurs in Romans."""
        return strongs.replace(']', '')

    def makeSurfacesAccentedTischendorf(self):
        # Convert surface to BETA for accented_surface,
        # then to OLB for surface. 
        self.accented_surface = MixedCaseBETAtoBETAtranslateWithStar(self.surface)
        self.qere = MixedCaseBETAtoBETAtranslateWithStar(self.qere)
        OLB = BETAtoOLBtranslate(self.accented_surface)
        self.surface = RemoveAccents(OLB)
        self.qere_noaccents = RemoveAccents(BETAtoOLBtranslate(self.qere))

    def parse(self, index, words):
        # Advance if this is parens.
        # This is such things as (26-61) indicating (I think)
        # that NA27 starts the verse here (26:61).

        if recognize(words[index]) == kind_parens:
            index += 1

        state = state_surface
        
        # Read surface
        if not recognize(words[index]) == kind_word:
            raise Exception("Error in words: word[index] is not kind_word:" + str(words[index:]))
        self.surface = words[index]
        if "&" in self.surface:
            [self.surface, self.qere] = self.surface.split("&")
        else:
            self.qere = self.surface
        self.qere_noaccents = RemoveAccents(BETAtoOLBtranslate(self.qere))


        # Advance index
        index += 1

        # If we have gone past the end, return
        if len(words) <= index:
            return index

        # Try next word
        kind = recognize(words[index])
        if kind == kind_number:
            self.Strongs1 = self.parseStrongs(words[index])
            state = state_strongs1
            index += 1

            # In Romans, the text "[tou 3588]" occurs.
            if self.surface[0] == '[' and self.Strongs1[-1] == ']':
                self.surface.append(']')
        elif kind == kind_pipe:
            return index
        elif kind == kind_word:
            # We are not doing parsing or variant, so we have the next surface
            return index
        else:
            raise Exception("Error in Word.parse: 1: Unknown kind:" + str(kind) + "'" +str(words[index]) + "'")

        # Try next word
        kind = recognize(words[index])
        if kind == kind_number:
            self.Strongs2 = self.parseStrongs(words[index])
            state = state_strongs2
            index += 1
        elif kind == kind_parsing:
            if words[index][-1] != "}":
                raise Exception("Error in words: parsing does not end with }: " + str(words[index:]))
            state = state_parsing
            self.parsing = words[index][1:-1] # Strip '{' and '}'
            index += 1
        else:
            raise Exception("Error in Word.parse: 2: Unknown kind:" + str(kind) + " '" +str(words[index]) + "', words = " + str(words))

        # If this is strongs2 state, read the parsing
        if state == state_strongs2:
            # Try next word
            kind = recognize(words[index])

            # It should be parsing at this point
            if kind == kind_parsing:
                if words[index][-1] != "}":
                    raise Exception("Error in words: parsing does not end with }: " + str(words[index:]))
                state = state_parsing
                self.parsing = words[index][1:-1] # Strip '{' and '}'
                index += 1
            else:
                raise Exception("Error in Word.parse: 3: Unknown kind: " + str(kind) + "'" +str(words[index]) + "' " + str(words))

        # So the parsing is read.  The next should either be kind_word
        # or kind_number

        # If we have gone past the end, return
        if len(words) <= index:
            return index

        # Try next word
        kind = recognize(words[index])
        if kind == kind_number:
            self.alt_Strongs1 = words[index]
            state = state_strongs1
            index += 1
        elif kind == kind_word or kind == kind_pipe or kind == kind_parens:
            # If this is a kind_word, kind_pipe or kind_parens,
            # we should return now.
            # If it is a kind_word or a kind_parens, the next word will
            # take care of it.
            # If it is a kind_pipe, the verse will take care of it.
            return index
        else:
            raise Exception("Error in Word.parse: 5: Unknown kind:" + str(kind) + "'" +str(words[index]) + "'... words = " + " ".join(words))

        if not state == state_strongs1:
            raise Exception("Error in Word.parse: 6: Unknown state: " + str(state) + ", please correct the logic.")

        # Try next word
        kind = recognize(words[index])
        if kind == kind_number:
            self.alt_Strongs2 = words[index]
            state = state_strongs2
            index += 1
        elif kind == kind_parsing:
            if words[index][-1] != "}":
                raise Exception("Error in words: parsing does not end with }: " + str(words[index:]))
            state = state_parsing
            self.alt_parsing = words[index][1:-1] # Strip '{' and '}'
            index += 1
        else:
            raise Exception("Error in Word.parse: 7: Unknown kind:" + str(kind) + " '" +str(words[index]) +"'")

        # If this is strongs2 state, read the parsing
        if state == state_strongs2:
            # Try next word
            kind = recognize(words[index])
            # It should be parsing at this point
            if kind == kind_parsing:
                if words[index][-1] != "}":
                    raise Exception("Error in words: parsing does not end with }: " + str(words[index:]))
                state = state_parsing
                self.alt_parsing = words[index][1:-1] # Strip '{' and '}'
                index += 1
            else:
                raise Exception("Error in Word.parse: 8: Unknown kind:" + str(kind) + "'" +str(words[index]) + "'")

        
        # If we have gone past the end, return
        if len(words) <= index:
            return index

        # Otherwise, the next should be a word.
        kind = recognize(words[index])
        if kind == kind_word or kind == kind_pipe:
            return index
        else:
            raise Exception("Error in Word.parse: 9: Unknown kind:" + str(kind) + "'" +str(words[index]) + "'")


        raise Exception("Error in Word.parse: 4: Got too far.  Please redo logic.")

            

    def toStringMQL(self):
        result = ""
        result = result + "CREATE OBJECT\n"
        result = result + "FROM MONADS={%d}" % self.monad
        result = result + "["
        result = result + "  surface:=\"%s\";\n" % OLBtoBETAtranslate(self.surface)
        #result = result + "  olb_surface:=\"%s\";\n" % self.surface
        if len(self.parsing) > 0:
            result = result + "  parsing:=\"%s\";\n" % self.parsing
        if self.Strongs1 != -1:
            result = result + "  strongs1:=%s;\n" % str(self.Strongs1)
        if self.Strongs2 != -1:
            result = result + "  strongs2:=%s;\n" % str(self.Strongs2)
        #if len(self.alt_parsing) > 0:
        #    result = result + "  alt_parsing:=\"%s\";\n" % self.alt_parsing
        #if self.alt_Strongs1 != -1:
        #    result = result + "  alt_strongs1:=%s;\n" % str(self.alt_Strongs1)
        #if self.alt_Strongs2 != -1:
        #    result = result + "  alt_strongs2:=%s;\n" % str(self.alt_Strongs2)
        #if self.variant != variant_none:
        #    result = result + "  is_variant:=%s;\n" % variant2string(self.variant)
        result = result + "]"
        return result

    def toString(self):
        return "%-20s {%-15s %s}" % (self.surface, self.parsing, self.getStrongs())

    def wordMatchesTisch(self, tischword, tischindex):
        tischsurface = olbstrip(tischword)
        BETA_selfsurface = olbstrip(self)
        if BETA_selfsurface == tischsurface:
            return 1
        elif TischSpellingDifferenceOK(BETA_selfsurface, tischsurface):
            return 1
        else:
            return 0
        
    def addWHInfo(self, whword):
        if self.hasNoAnalysis():
            self.parsing = whword.parsing
            self.Strongs1 = whword.Strongs1
            # FIXME: Should we add whword.Strongs2?

    def write_MORPH_style(self, f, base_ref, index, bPrintLemma, encodingStyle):
        ref = "%s.%d" % (base_ref, index)
        #ref = "%s" % base_ref
        if self.parsing == "":
            prs = "NOPARSE"
        else:
            prs = self.parsing
        if self.Strongs1 == -1:
            strongs = "9999"
        elif self.Strongs2 == -1:
            strongs = str(self.Strongs1)
        else:
            strongs = "%s&%s" % (str(self.Strongs1), str(self.Strongs2))
        if self.accented_surface != "":
            surf = self.accented_surface
        else:
            surf = OLBtoBETAtranslate(self.surface)
        qere = self.qere

        if bPrintLemma:
            lemma = self.strongslemma
            ANLEXlemma = self.ANLEXlemma
            if lemma == "":
                print "Error: Strong's lemma for strong's %s does not exist. ref=%s surface=%s prs=%s" % (str(strongs), ref, surf, prs)
                lemma = "NOLEMMA"
                ANLEXlemma = "NOLEMMA"
            if ANLEXlemma == "":
                print "Error: ANLEX lemma for strong's %s does not exist. ref=%s surface=%s prs=%s" % (str(strongs), ref, surf, prs)
                ANLEXlemma = "NOLEMMA"

        if encodingStyle == kBETA:
            pass
        elif encodingStyle == kUnicode:
            lemma = self.beta2utf8(lemma)
            ANLEXlemma = self.beta2utf8(ANLEXlemma)
            surf = self.beta2utf8(surf)
            qere = self.beta2utf8(qere)
        else:
            raise "Error: Unknown encodingStyle parameter = %s" % str(encodingStyle)

        if bPrintLemma:
            print >>f, "%s %s %s %s %s %s %s ! %s" % (ref, self.break_kind, surf, qere, prs, strongs, lemma, ANLEXlemma)
        else:
            print >>f, "%s %s %s %s %s %s %s" % (ref, self.break_kind, surf, qere, prs, strongs)

    def write_StrippedLinear(self, f, base_ref, index):
        ref = "%s" % base_ref
        print >>f, "%s %s" % (ref, RemoveAccents(MixedCaseBETAtoBETAtranslate(self.surface)))

    def write_WHLinear(self, f, base_ref, index):
        ref = "%s" % base_ref
        print >>f, "%s %s" % (ref, OLBtoBETAtranslate(self.surface))

    def write_Linear(self, f, base_ref, index):
        ref = "%s" % base_ref
        if self.accented_surface != "":
            surf = self.accented_surface
        else:
            surf = OLBtoBETAtranslate(self.surface)
        print >>f, "%s %s" % (ref, surf)

    def addManualAnalysisInfo(self, base_ref, man_anal):
        if OLBtoBETAtranslate(self.surface) != man_anal[0]:
            raise Exception("Error: word in manual_analyses.txt '%s %s %s %s' does not match up with surface of this one: '%s'" % (base_ref, man_anal[0], man_anal[1], man_anal[2], self.surface))
        self.parsing = man_anal[1]
        self.setStrongs(man_anal[2])

    def hasNoAnalysis(self):
        if self.parsing == "" or self.Strongs1 == -1:
            return True
        else:
            return False

    def hasAnalysis(self):
        return not self.hasNoAnalysis()

