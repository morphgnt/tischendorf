import string
from variant import *
from kind import *
import re
from morphgnt import convert
import rptag
from lexicon import Lexicon
from morphgnt import booknames
import unicodedata

#state_surface = 0
#state_strongs1 = 1
#state_strongs2 = 2
#state_parsing = 3

state_none = 0
state_surface = 1
state_strongs1 = 2
state_strongs2 = 3
state_strongs3 = 4
state_parsing = 5
state_alt_strongs1 = 6
state_alt_strongs2 = 7
state_alt_strongs3 = 8
state_alt_parsing = 9


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

alternate_Tischendorf_spellings = { "DAUID" : set(["DAUEID"]),
                                    "OZIAN" : set(["OZEIAN"]),
                                    "OZIAS" : set(["OZEIAS"]),
                                    "AXAS" : set(["AXAZ"]),
                                    "IWSIAN" : set(["IWSEIAN"]),
                                    "IWSIAS" : set(["IWSEIAS"]),
                                    "ELIAKIM" : set(["ELIAKEIM"]),
                                    "AXIM" : set(["AXEIM"]),
                                    "MATQAN" : set(["MAQQAN"]),
                                    "MARIAN" : set(["MARIAM"]),
                                    "MARIA" : set(["MARIAM"]),
                                    "PASIN" : set(["PASI"]),
                                    "NAZARET" : set(["NAZAREQ"]),
                                    "NEFQALIM" : set(["NEFQALEIM"]),
                                    "ALIEIS" : set(["ALEEIS"]),
                                    "ELQETW" : set(["ELQATW"]), # This is correct!
                                    "DUSIN" : set(["DUSI"]),
                                    "EKATONTARXOS" : set(["EKATONTARXHS"]),
                                    "HNEWXQHSAN" : set(["ANEWXQHSAN"]),
                                    "SAMAREITWN" : set(["SAMARITWN"]),
                                    "SAMAREITHS" : set(["SAMARITHS"]),
                                    "SAMAREITIS" : set(["SAMARITIS"]),
                                    "SAMAREITIDOS" : set(["SAMARITIDOS"]),
                                    "SAMAREITAI" : set(["SAMARITAI"]),
                                    "APOKTEINONTWN" : set(["APOKTENNONTWN"]),
                                    "DE" : set(["D"]),
                                    "BHQSAIDA" : set(["BHQSAIDAN"]),
                                    "EUDOKHSEN" : set(["HUDOKHSEN"]),
                                    "NINEUITAI" : set(["NINEUEITAI"]),
                                    "ERRIYAN" : set(["ERIYAN"]),
                                    "HLIAS" : set(["HLEIAS"]),
                                    "HLIAN" : set(["HLEIAN"]),
                                    "HLIA" : set(["HLEIA"]),
                                    "HMIWRON" : set(["HMIWRION"]),
                                    "SULLALOUNTES" : set(["SUNLALOUNTES"]),
                                    "PALIGGENESIA" : set(["PALINGENESIA"]),
                                    "BASTASASIN" : set(["BASTASASI"]),
                                    "IERIXW" : set(["IEREIXW"]),
                                    "RABBI" : set(["RABBEI"]),
                                    "GEQSHMANI" : set(["GEQSHMANEI"]),
                                    "GUNAICIN" : set(["GUNAICI"]),
                                    "PILATW" : set(["PEILATW"]),
                                    "PILATOS" : set(["PEILATOS"]),
                                    "PIEIN" : set(["PEIN"]),
                                    "ELWI" : set(["HLEI"]),
                                    "SABAXQANI" : set(["SABAXQANEI"]),
                                    "PILATON" : set(["PEILATON"]),
                                    "ADDI" : set(["ADDEI"]),
                                    "AGOUSIN" : set(["AGOUSI"]),
                                    "AGALLIATE" : set(["AGALLIASQE"]), # Could also be indicative, but only occurs once, in an imperative context
                                    "ALL" : set(["ALLA"]),
                                    "ANAIDEIAN," : set(["ANAIDIAN"]),
                                    "EKAQARISQH" : set(["EKAQERISQH"]),
                                    "EIDAN" : set(["IDAN"]),
                                    "IEROSOLUMITAI" : set(["IEROSOLUMEITAI"]), 
                                    "SULLUPOUMENOS" : set(["SUNLUPOUMENOS"]),
                                    "SUMPNIGOUSIN" : set(["SUNPNIGOUSIN"]),
                                    "THLAUGWS" : set(["DHLAUGWS"]),  # This is correct, according to ANLEX.
                                    "ALAZONEIA" : set(["ALAZONIA"]),
                                    "ALAZONEIAIS" : set(["ALAZONIAIS"]),
                                    "ANAIDEIAN" : set(["ANAIDIAN"]),
                                    "ANTIPAS" : set(["ANTEIPAS"]),
                                    "AREION" : set(["ARION"]),
                                    "AREIOU" : set(["ARIOU"]),
                                    "AREOPAGITHS" : set(["AREOPAGEITHS"]),
                                    "ARRABWNA" : set(["ARABWNA"]),
                                    "ARSESIN" : set(["ARRESIN"]),
                                    "ASUGKRITON" : set(["ASUNKRITON"]),
                                    "ATTALEIAN" : set(["ATTALIAN"]),
                                    "BENIAMIN" : set(["BENIAMEIN"]),
                                    "DIELIPEN" : set(["DIELEIPEN"]),
                                    "DOULEIAN" : set(["DOULIAN"]),
                                    "DOULEIAS" : set(["DOULIAS"]),
                                    "ECEKREMATO" : set(["ECEKREMETO"]), # Strange! But it is not a textual error (LU 19:48.11)
                                    "EGGEGRAMMENH" : set(["ENGEGRAMMENH"]),
                                    "EGGEGRAPTAI" : set(["ENGEGRAPTAI"]),
                                    "EGKAINIA" : set(["ENKAINIA"]),
                                    "EGKAKEIN" : set(["ENKAKEIN"]),
                                    "EGKAKWMEN" : set(["ENKAKWMEN"]),
                                    "EGKAQETOUS" : set(["ENKAQETOUS"]),
                                    "EGKATALEIYEIS" : set(["ENKATALEIYEIS"]),
                                    "EGKATELEIFQH" : set(["ENKATELEIFQH"]),
                                    "EGKATELIPEN" : set(["ENKATELIPEN"]),
                                    "EGKATOIKWN" : set(["ENKATOIKWN"]),
                                    "EGKAUXASQAI" : set(["ENKAUXASQAI"]),
                                    "EGKEKAINISTAI" : set(["ENKEKAINISTAI"]),
                                    "EGKENTRISAI" : set(["ENKENTRISAI"]),
                                    "EGKENTRISQHSONTAI" : set(["ENKENTRISQHSONTAI"]),
                                    "EGKOPHN" : set(["EKKOPHN"]), # This is NOT a textual error. However, it is also not wrong, according to ANLEX. 1CO 9:12.22
                                    "EGKOPTESQAI" : set(["ENKOPTESQAI"]),
                                    "EGKOPTW" : set(["ENKOPTW"]),
                                    "EGKRINAI" : set(["ENKRINAI"]),
                                    "EIDEN" : set(["IDEN"]),
                                    "ANWRQWQH" : set(["ANORQWQH"]),  # This is OK, according to Perseus...
                                    "ANOIGHSETAI" : set(["ANOIXQHSETAI"]), # This is OK, according to ANLEX.
                                    "APODW" : set(["APODOI"]), # NOTE: Is this a textual error? "APODW|" ... Nope, it's not a textual error (1TH 5:15), but I am going to parse it as APODW| anyway.  The things that Perseus calls it are not helpful.
                                    "APOKTEINEI" : set(["APOKTENNEI"]),
                                    "EIDWLEIW" : set(["EIDWLIW"]),
                                    "EILIKRINEIA" : set(["EILIKRINIA"]),
                                    "EILIKRINEIAS" : set(["EILIKRINIAS"]),
                                    "EMPERIPATHSW" : set(["ENPERIPATHSW"]),
                                    "FARMAKEIA" : set(["FARMAKIA"]),
                                    "GALATIAN" : set(["GALLIAN"]),
                                    "IEROSOLUMITWN" : set(["IEROSOLUMEITWN"]),
                                    "ISRAHLITAI" : set(["ISRAHLEITAI"]),
                                    "ISRAHLITHS" : set(["ISRAHLEITHS"]),
                                    "IWANNH" : set(["IWANNEI"]),
                                    "KAISAREIA" : set(["KAISARIA"]),
                                    "KAISAREIAN" : set(["KAISARIAN"]),
                                    "KAISAREIAS" : set(["KAISARIAS"]),
                                    "KAISARIAS" : set(["KAISAREIAS"]),
                                    "KATAKRINW" : set(["KATAKREINW"]),
                                    "KATEKRINEN" : set(["KATEKREINEN"]),
                                    "KAUDA" : set(["KLAUDA"]),
                                    "KIS" : set(["KEIS"]),
                                    "KOLAKEIAS" : set(["KOLAKIAS"]),
                                    "KUBEIA" : set(["KUBIA"]),
                                    "LAODIKEIA" : set(["LAODIKIA"]),
                                    "LAODIKEIAN" : set(["LAODIKIAN"]),
                                    "LAODIKEIAS" : set(["LAODIKIAS"]),
                                    "LEUI" : set(["LEUEI"]),
                                    "LEUIN" : set(["LEUEIN"]),
                                    "LEUIS" : set(["LEUEIS"]),
                                    "LEUITAS" : set(["LEUEITAS"]),
                                    "LEUITHS" : set(["LEUEITHS"]),
                                    "LEUITIKHS" : set(["LEUEITIKHS"]),
                                    "MAGEIAIS" : set(["MAGIAIS"]),
                                    "MAQQAT" : set(["MAQQAQ"]),
                                    "MELXI" : set(["MELXEI"]),
                                    "MEQODEIAN" : set(["MEQODIA"]),
                                    "MEQODEIAS" : set(["MEQODIAS"]),
                                    "MURA" : set(["MURRA"]),
                                    "NINEUITAIS" : set(["NINEUEITAIS"]),
                                    "ORNIS" : set(["ORNIC"]),
                                    "PAIDEIAN" : set(["PAIDIAN"]),
                                    "PAIDEIAS" : set(["PAIDIAS"]),
                                    "PALIGGENESIAS" : set(["PALINGENESIAS"]),
                                    "PANDOXEION" : set(["PANDOKION"]), # NOTE: The textual apparatus lets one assume that it is OK to analyze as though it were PANDOXEION.
                                    "PESATE" : set(["PESETE"]),
                                    "PILATOU" : set(["PEILATOU"]),
                                    "QRHSKEIA" : set(["QRHSKIA"]),
                                    "QRHSKEIAS" : set(["QRHSKIAS"]),
                                    "SAMAREIAN" : set(["SAMARIAN"]),
                                    "SAMAREIA" : set(["SAMARIA"]),
                                    "SAMAREIAS" : set(["SAMARIAS"]),
                                    "SEIROIS" : set(["SIROIS"]),
                                    "SELEUKEIAN" : set(["SELEUKIAN"]),
                                    "SEMEIN" : set(["SEMEEIN"]),
                                    "SOLOMWN" : set(["SALWMWN"]),
                                    "SUGKAKOPAQHSON" : set(["SUNKAKOPAQHSON"]),
                                    "SUGKAKOUXEISQAI" : set(["SUNKAKOUXEISQAI"]),
                                    "SUGKALEI" : set(["SUNKALEI"]),
                                    "SUGKALESAMENOS" : set(["SUNKALESAMENOS"]),
                                    "SUGKALESASQAI" : set(["SUNKALESASQAI"]),
                                    "SUGKALOUSIN" : set(["SUNKALOUSIN"]),
                                    "SUGKAQHMENOI" : set(["SUNKAQHMENOI"]),
                                    "SUGKAQHMENOS" : set(["SUNKAQHMENOS"]),
                                    "SUGKAQISANTWN" : set(["SUNKAQISANTWN"]),
                                    "SUGKATABANTES" : set(["SUNKATABANTES"]),
                                    "SUGKATAQESIS" : set(["SUNKATAQESIS"]),
                                    "SUGKATATEQEIMENOS" : set(["SUNKATATIQEIMENOS"]),
                                    "SUGKATEYHFISQH" : set(["SUNKATEYHFISQH"]),
                                    "SUGKLEIOMENOI" : set(["SUNKLEIOMENOI"]),
                                    "SUGKLHRONOMA" : set(["SUNKLHRONOMA"]),
                                    "SUGKLHRONOMOI" : set(["SUNKLHRONOMOI"]),
                                    "SUGKLHRONOMWN" : set(["SUNKLHRONOMWN"]),
                                    "SUGKOINWNEITE" : set(["SUNKOINWNEITE"]),
                                    "SUGKOINWNHSANTES" : set(["SUNKOINWNHSANTES"]),
                                    "SUGKOINWNHSHTE" : set(["SUNKOINWNHSHTE"]),
                                    "SUGKOINWNOS" : set(["SUNKOINWNOS"]),
                                    "SUGKOINWNOUS" : set(["SUNKOINWNOUS"]),
                                    "SUGKRINAI" : set(["SUNKRINAI"]),
                                    "SUGKRINONTES" : set(["SUNKRINONTES"]),
                                    "SUGKUPTOUSA" : set(["SUNKUPTOUSA"]),
                                    "SUGXAIREI" : set(["SUNXAIREI"]),
                                    "SUGXAIRETE" : set(["SUNXAIRETE"]),
                                    "SUGXAIRW" : set(["SUNXAIRW"]),
                                    "SUGXUNNETAI" : set(["SUNXUNNETAI"]),

                                    "SULLALHSAS" : set(["SUNLALHSAS"]),
                                    "SULLAMBANOU" : set(["SUNLAMBANOU"]),
                                    "SUMBALLOUSA" : set(["SUNBALLOUSA"]),
                                    "SUMBIBAZOMENON" : set(["SUNBIBAZOMENON"]),
                                    "SUMMARTUREI" : set(["SUNMARTUREI"]),
                                    "SUMMARTUROUSHS" : set(["SUNMARTUROUSHS"]),
                                    "SUMMETOXA" : set(["SUNMETOXA"]),
                                    "SUMMETOXOI" : set(["SUNMETOXOI"]),
                                    "SUMMIMHTAI" : set(["SUNMIMHTAI"]),
                                    "SUMMORFIZOMENOS" : set(["SUNMORFIZOMENOS"]),
                                    "SUMMORFON" : set(["SUNMORFON"]),
                                    "SUMPAQHSAI" : set(["SUNPAQHSAI"]),
                                    "SUMPARAGENOMENOI" : set(["SUNPARAGENOMENOI"]),
                                    "SUMPARAGENOMENOI" : set(["SUNPARAGENOMENOI"]),
                                    "SUMPARAKLHQHNAI" : set(["SUNPARAKLHQHNAI"]),
                                    "SUMPARALABEIN" : set(["SUNPARALABEIN"]),
                                    "SUMPARALABONTES" : set(["SUNPARALABONTES"]),
                                    "SUMPARALABWN" : set(["SUNPARALABWN"]),
                                    "SUMPARALAMBANEIN" : set(["SUNPARALAMBANEIN"]),
                                    "SUMPARONTES" : set(["SUNPARONTES"]),
                                    "SUMPASXEI" : set(["SUNPASXEI"]),
                                    "SUMPASXOMEN" : set(["SUNPASXOMEN"]),
                                    "SUMPLHROUSQAI" : set(["SUNPLHROUSQAI"]),
                                    "SUMPNIGONTAI" : set(["SUNPNIGONTAI"]),
                                    "SUMPOLITAI" : set(["SUNPOLITAI"]),
                                    "SUMYUXOI" : set(["SUNYUXOI"]),
                                    "SUNEILHFEN" : set(["SUNEILHFIA"]),
                                    "SUSSHMON" : set(["SUNSHMON"]),
                                    "SUSSWMA" : set(["SUNSWMA"]),
                                    "SUSTAURWQENTOS" : set(["SUNTAURWQENTOS"]),
                                    "SUSTOIXEI" : set(["SUNSTOIXEI"]),
                                    "SUSTRATIWTHN" : set(["SUNSTRATIWTHN"]),
                                    "SUSXHMATIZESQE" : set(["SUNSXHMATIZESQE"]),
                                    "SUZHN" : set(["SUNZHN"]),
                                    "SUZUGE" : set(["SUNZUGE"]),
                                    "TESSARA" : set(["TESSERA"]),
                                    "TABEIQA" : set(["TABIQA"]),
                                    "XORAZIN" : set(["XORAZEIN"]),
                                    "XEROUBIN" : set(["XEROUBEIN"]),
                                    "XALKHDWN" : set(["XALKEDWN"]),
                                    "SUGKLHRONOMOI" : set(["SUNKLHRONOMOI"]),
                                    "HLIOU" : set(["HLEIA", "HLEIOU"]),
                                    "HLI" : set(["HLEI"]),
                                    "ESLI" : set(["ESLEI"]),
                                    "AKATAPASTOUS" : set(["AKATAPAUSTOUS"]),
                                    "ANAPEIROUS" : set(["ANAPHROUS"]),
                                    "APAGWN" : set(["APAGAGWN"]),
                                    "ARSENES" : set(["ARRENES"]),


                                    "QA" : set(["AQA"]),
                                    "EIDWLOLATRIAS" : set(["EIDWLOLATREIAS"]),
                                    "EIDWLOLATRIA" : set(["EIDWLOLATREIA"]),
                                    "IERON" : set(["EIERON"]),   # NOTE: This is not a textual error (1st instance of Joh 8:2.)
                                    "EQAUMASEN" : set(["EQAUMAZEN"]),
                                    "ERRANTISEN" : set(["ERANTISEN"]),
                                    "ERRUSATO" : set(["ERUSATO"]),
                                    "ERRUSQHN" : set(["ERUSQHN"]),
                                    "ESQIONTES" : set(["ESQONTES"]),
                                    "HUXONTO" : set(["EUXONTO"]),
                                    "HMISIA" : set(["HMISEIA"]),
                                    "HSSON" : set(["HTTON"]),
                                    "EUDOKHSAN" : set(["HUDOKHSAN"]),
                                    "EUDOKHSAS" : set(["HUDOKHSAS"]),
                                    "IAIROS" : set(["IAEIROS"]),
                                    "IWRIM" : set(["IWREIM"]),
                                    "KAKOPAQIAS" : set(["KAKOPAQEIAS"]),
                                    "LOGEIAI" : set(["LOGIAI"]),
                                    "LOGEIAS" : set(["LOGIAS"]),
                                    "MARANA" : set(["MARAN"]),
                                    "MASTOIS" : set(["MASQOIS"]),
                                    "MELITHNH" : set(["MELITH"]),
                                    "MEQODEIAN" : set(["MEQODIAN"]),
                                    "MULINON" : set(["MULON"]),
                                    "NHRI" : set(["NHREI"]),
                                    "OIKTIRHSW" : set(["OIKTEIRHSW"]),
                                    "OIKTIRW" : set(["OIKTEIRW"]),
                                    "EGGISEI" : set(["EGGIEI"]),
                                    "ENEBRIMWNTO" : set(["ENEBRIMOUNTO"]),
                                    "SAPFIROS" : set(["SAPFEIROS"]),
                                    "EIDON" : set(["IDON"]),
                                    "KEGXREAIS" : set(["KENXREAIS"]),
                                    "KOLLOURION" : set(["KOLLURION"]),
                                    "SUNISTANONTES" : set(["SUNISTANTES"]),
                                    # "PEPTWKAN" : set(["PEPWKAN"]), # NOTE: This is not true!
                                    "KATEIRGASATO" : set(["KATHRGASATO"]),
                                    "EIRGASANTO" : set(["HRGASANTO"]),
                                    "APEIQOUSIN" : set(["APEIQOUSI"]),   # Note: This is ambiguous as to V-PAI-3P or V-PAP-DPM, but I assume it's the same as in WH.
                                    "ALUSESIN" : set(["ALUSESI"]), 
                                    "APELUSEN" : set(["APELUSE"]), 
                                    "ASEBESIN" : set(["ASEBESI"]), 
                                    "ASEBH" : set(["ASEBHN"]), 
                                    "AXRI" : set(["AXRIS"]), 
                                    "DEHSESIN" : set(["DEHSESI"]), 
                                    "DIASWSWSIN" : set(["DIASWSWSI"]), 
                                    "DUNAMESIN" : set(["DUNAMESI"]), 
                                    "EDOCEN" : set(["EDOCE"]), 
                                    "ELABEN" : set(["ELABE"]), 
                                    "ELAXEN" : set(["ELAXE"]), 
                                    "EQESIN" : set(["EQESI"]), 
                                    "ESQHSESIN" : set(["ESQHSESI"]), 
                                    "EXOUSIN" : set(["EXOUSI"]), 
                                    "EXWSIN" : set(["EXWSI"]), 
                                    "GINWSKOUSIN" : set(["GINWSKOUSI"]),   # Note: This is ambiguous between V-PAI-3P and V-PAP-DPM, but I will assume that it is the same as in WH.
                                    "HLQEN" : set(["HLQE"]), 
                                    "ISASIN" : set(["ISASI"]), 
                                    "KATELIPEN" : set(["KATELIPE"]), 
                                    "KLIMASIN" : set(["KLIMASI"]), 
                                    "MEXRI" : set(["MEXRIS"]), 
                                    "OUTWS" : set(["OUTW"]), 
                                    "PARADEDWKOSIN" : set(["PARADEDWKOSI"]), 
                                    "PNEUMASIN" : set(["PNEUMASI"]), 
                                    "ROMFA" : set(["ROMFAN"]), 
                                    "TERASIN" : set(["TERASI"]), 
                                    "TIMWSIN" : set(["TIMWSI"]),   # Note: This is ambiguous between V-PAI-3P and V-PAS-3P, but I will assume it is the same as in WH.
                                    "XALWSIN" : set(["XALWSI"]), 
                                    "XEIRA" : set(["XEIRAN"]), 
                                    "ZWSIN" : set(["ZWSI"]),   # Note: This is ambiguous between V-PAI-3P and V-PAS-3P, but I will assume it is the same as in WH.
                                    "QELWSIN" : set(["QELWSI"]),
                                    "EPEGNWKOSIN" : set(["EPEGNWKOSI"]),
                                    "HGAPHKOSIN" : set(["HGAPHKOSI"]),
                                    "EIXEN" : set(["EIXE"]),
                                    "KRIQWSIN" : set(["KRIQWSI"]),
                                    "SUGXARHTE" : set(["SUNXARHTE"]),
                                    "SUZHTEIN" : set(["SUNZHTEIN"]),
                                    "SUMMAQHTAIS" : set(["SUNMAQHTAIS"]),
                                    "SUSTAURWQENTOS" : set(["SUNSTAURWQENTOS"]),
                                    "EMPROSQEN" : set(["ENPROSQEN"]),
                                    "SMURNAN" : set(["ZMURNAN"]),
                                    "SMURNH" : set(["ZMURNH"]),
#                                    "" : [ "" ],
#                                    "" : [ "" ],

                                   }

tischendorfLexicon = Lexicon()
tischendorfLexicon.primeWithTischendorf()



def TischSpellingDifferenceOK(BETA_selfsurface, BETA_tischsurface):
    try:
        if BETA_tischsurface in alternate_Tischendorf_spellings[BETA_selfsurface]:
            return True
        else:
            return False
    except KeyError:
        return False

def olbstrip(olbword):
    return reolbstrip.sub("", OLBtoBETAtranslate(olbword.qere_noaccents))

def olbstrip_surface(olbword):
    return reolbstrip.sub("", OLBtoBETAtranslate(olbword.surface))


def stripolb(str):
    return reolbstrip.sub("", str)

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
        self.qere_noaccents = ""
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

    def has_qere_noaccents(self):
        return self.qere_noaccents != ""

    def ends_sentence(self):
	return self.accented_surface[-1] in [".", ";", ":"]

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
            qere = self.qere
        else:
            surfaceBETA = OLBtoBETAtranslate(stripolb(self.surface))
            qere = OLBtoBETAtranslate(stripolb(self.qere))
        print >>f, "  surface:=\"%s\";" % mangleMQLString(surfaceBETA)
        print >>f, "  surfaceutf8:=\"%s\";" % mangleMQLString(self.beta2utf8(surfaceBETA))
        print >>f, "  qere:=\"%s\";" % mangleMQLString(qere)
        print >>f, "  qereutf8:=\"%s\";" % mangleMQLString(self.beta2utf8(qere))
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
	"""Parses up to the end of this word. Returns the index that points
	one after the end of the word."""

	state = state_none
	LAST_WORD = len(words) - 1
	while True:
	    if index > LAST_WORD:
		return index
	    # Advance if this is parens.
	    # This is such things as (26-61) indicating (I think)
	    # that NA27 starts the verse here (26:61).
	    elif recognize(words[index]) == kind_parens:
		index += 1
	    elif state == state_none:
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

		state = state_surface
	    elif state == state_surface:
		# Try next word
		kind = recognize(words[index])
		if kind == kind_number:
		    self.Strongs1 = int(self.parseStrongs(words[index]))
		    state = state_strongs1
		    # In Romans, the text "[tou 3588]" occurs.
		    if self.surface[0] == '[' and words[index][-1] == ']':
			self.surface += ']'
		    if words[index][-1] == ">":
			self.surface += ">"
		    index += 1
		elif kind in [kind_pipe, kind_VAR, kind_END]:
		    return index
		elif kind == kind_word:
		    # We are not doing parsing or variant, so we have the next surface
		    return index
		else:
		    raise Exception("Error in Word.parse: 1: Unknown kind:" + str(kind) + "'" +str(words[index]) + "'")
	    elif state == state_strongs1:
		# Try next word
		kind = recognize(words[index])
		if kind == kind_number:
		    self.Strongs2 = int(self.parseStrongs(words[index]))
		    state = state_strongs2
		    index += 1
		elif kind == kind_parsing:
		    if words[index][-1] != "}":
			raise Exception("Error in words: parsing does not end with }: " + str(words[index:]))
		    state = state_parsing
		    self.parsing = words[index][1:-1] # Strip '{' and '}'
		    index += 1
		else:
		    raise Exception("Error in Word.parse: 2: Unknown kind:" + str(kind) + " '" +str(words[index]) + "' index=" + str(index) +", words = " + str(words[index:]))
	    elif state == state_strongs2:
		kind = recognize(words[index])
		
		# It should be parsing or Strongs3 at this point
		if kind == kind_parsing:
		    if words[index][-1] != "}":
			raise Exception("Error in words: parsing does not end with }: " + str(words[index:]))
		    state = state_parsing
		    self.parsing = words[index][1:-1] # Strip '{' and '}'
		    index += 1
		elif kind == kind_number:
		    state = state_strongs3
		    self.Strongs3 = self.parseStrongs(words[index])
		    index += 1
		else:
		    raise Exception("Error in Word.parse: 3: Unknown kind: " + str(kind) + "'" +str(words[index]) + "' " + str(words))
	    elif state == state_strongs3:
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
		    raise Exception("Error in Word.parse: 32: Unknown kind: " + str(kind) + "'" +str(words[index]) + "' " + str(words))
	    elif state == state_parsing:
		# So the parsing is read.  The next should either be kind_word
		# or kind_number (but may be state_parsing)

		# If we have gone past the end, return
		if len(words) <= index:
		    return index

		# Try next word
		kind = recognize(words[index])
		if kind == kind_number:
		    self.alt_Strongs1 = int(words[index])
		    state = state_alt_strongs1
		    index += 1
		elif kind == kind_word or kind in [kind_pipe, kind_VAR, kind_END, kind_parens, kind_verse]:
		    # If this is a kind_word, kind_pipe or kind_parens,
		    # we should return now.
		    # If it is a kind_word or a kind_parens, the next word will
		    # take care of it.
		    # If it is a kind_pipe, the verse will take care of it.
		    return index
		elif kind == kind_parsing:
		    if words[index][-1] != "}":
			raise Exception("Error in words: parsing does not end with }: " + str(words[index:]))
		    state = state_alt_parsing
		    self.alt_parsing = words[index][1:-1] # Strip '{' and '}'
		    index += 1
		else:
		    raise Exception("Error in Word.parse: 5: Unknown kind:" + str(kind) + "'" +str(words[index]) + "'")
	    elif state == state_alt_strongs1:
		# Try next word
		kind = recognize(words[index])
		if kind == kind_number:
		    self.alt_Strongs2 = int(words[index])
		    state = state_alt_strongs2
		    index += 1
		elif kind == kind_parsing:
		    if words[index][-1] != "}":
			raise Exception("Error in words: parsing does not end with }: " + str(words[index:]))
		    state = state_alt_parsing
		    self.alt_parsing = words[index][1:-1] # Strip '{' and '}'
		    index += 1
		else:
		    raise Exception("Error in Word.parse: 7: Unknown kind: " + str(kind) + " '" +str(words[index]) +"'" + "\nwords = '%s'" % words)
	    elif state == state_alt_strongs2:
		# Try next word
		kind = recognize(words[index])
		# It should be parsing or number at this point
		if kind == kind_parsing:
		    if words[index][-1] != "}":
			raise Exception("Error in words: parsing does not end with }: " + str(words[index:]))
		    state = state_alt_parsing
		    self.alt_parsing = words[index][1:-1] # Strip '{' and '}'
		    index += 1
		elif kind == kind_number:
		    self.alt_Strongs3 = int(words[index])
		    state = state_alt_strongs3
		    index += 1
		else:
		    raise Exception("Error in Word.parse: 8: Unknown kind:" + str(kind) + "'" +str(words[index]) + "'")
	    elif state == state_alt_strongs3:
		# Try next word
		kind = recognize(words[index])
		# It should be parsing at this point
		if kind == kind_parsing:
		    if words[index][-1] != "}":
			raise Exception("Error in words: parsing does not end with }: " + str(words[index:]))
		    state = state_alt_parsing
		    self.alt_parsing = words[index][1:-1] # Strip '{' and '}'
		    index += 1
		else:
		    raise Exception("Error in Word.parse: 9: Unknown kind:" + str(kind) + "'" +str(words[index]) + "'")
	    elif state == state_alt_parsing:
		# If we have gone past the end, return
		if len(words) <= index:
		    return index
		
		# Otherwise, the next should be a word.
		kind = recognize(words[index])
		if kind == kind_word or kind in [kind_parens, kind_pipe, kind_VAR, kind_END, kind_verse]:
		    return index
		else:
		    raise Exception("Error in Word.parse: 10: Unknown kind:" + str(kind) + "'" +str(words[index]) + "'")


    def parseOld(self, index, words):
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
            return True
        elif TischSpellingDifferenceOK(BETA_selfsurface, tischsurface):
            return True
        else:
            return False
        
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

