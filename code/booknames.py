book_lists = {
    "OLB" : ["MT", "MR", "LU", "JOH", "AC", "RO", "1CO", "2CO",
	     "GA", "EPH", "PHP", "COL", "1TH", "2TH", "1TI", "2TI",
	     "TIT", "PHM", "HEB", "JAS", "1PE", "2PE", "1JO", "2JO", "3JO",
	     "JUDE", "RE"],
    
    "AGNT" : ["matt", "mark", "luke", "john", "acts", "romans",
	      "1cor", "2cor", "gal", "eph", "phil", "col",
	      "1thess", "2thess", "1tim", "2tim", "titus", "philem",
	      "heb", "james", "1peter", "2peter", "1john", "2john",
	      "3john", "jude", "rev"],

    "UBS" : ["mat", "mrk", "luk", "jhn", "act", "rom", "1co", "2co",
	     "gal", "eph", "php", "col", "1th", "2th", "1ti", "2ti",
	     "tit", "phm", "heb", "jas", "1pe", "2pe", "1jn", "2jn", "3jn",
	     "jud", "rev"],

    "OSIS" : ["Matt", "Mark", "Luke", "John", "Acts", "Rom", "1Cor", "2Cor", 
              "Gal", "Eph", "Phil", "Col", "1Thess", "2Thess", "1Tim", "2Tim",
              "Titus", "Phlm", "Heb", "Jas", "1Pet", "2Pet", 
              "1John", "2John", "3John", "Jude", "Rev",
        ],
    "BibleWorks" : [
        "Mat", "Mar", "Luk", "Joh", 
        "Act", 
        "Rom", "1Co", "2Co", 
        "Gal", "Eph", "Phi", "Col", 
        "1Th", "2Th", "1Ti", "2Ti", "Tit", "Phm", 
        "Heb", 
        "Jam", "1Pe", "2Pe", "1Jo", "2Jo", "3Jo", "Jud", 
        "Rev",
    ],
}

OLB2More = {
    "MT"  : ("Matthew", 1),
    "MR"  : ("Mark", 2),
    "LU"  : ("Luke", 3),
    "JOH" : ("John", 4),
    "AC"  : ("Acts", 5),
    "RO"  : ("Romans", 6),
    "1CO" : ("I_Corinthians", 7),
    "2CO" : ("II_Corinthians", 8),
    "GA"  : ("Galatians", 9),
    "EPH" : ("Ephesians", 10),
    "PHP" : ("Philippians", 11),
    "COL" : ("Colossians", 12),
    "1TH" : ("I_Thessalonians", 13),
    "2TH" : ("II_Thessalonians", 14),
    "1TI" : ("I_Timothy", 15),
    "2TI" : ("II_Timothy", 16),
    "TIT" : ("Titus", 17),
    "PHM" : ("Philemon", 18),
    "HEB" : ("Hebrews", 19),
    "JAS" : ("James", 20),
    "1PE" : ("I_Peter", 21),
    "2PE" : ("II_Peter", 22),
    "1JO" : ("I_John", 23),
    "2JO" : ("II_John", 24),
    "3JO" : ("III_John", 25),
    "JUDE": ("Jude", 26),
    "RE"  : ("Revelation", 27)
}

AGNT2OLB = {
    "matt" : "MT",
    "mark" : "MR",
    "luke" : "LU",
    "john" : "JOH",
    "acts" : "AC",
    "romans" : "RO",
    "1cor" : "1CO",
    "2cor" : "2CO",
    "gal" : "GA",
    "eph" : "EPH",
    "phil" : "PHP",
    "col" : "COL",
    "1thess" : "1TH",
    "2thess" : "2TH",
    "1tim" : "1TI",
    "2tim" : "2TI",
    "titus" : "TIT",
    "philem" : "PHM",
    "heb" : "HEB",
    "james" : "JAS",
    "1peter" : "1PE",
    "2peter" : "2PE",
    "1john" : "1JO",
    "2john" : "2JO",
    "3john" : "3JO",
    "jude" : "JUDE",
    "rev" : "RE"
}

def book_list(scheme):
    return book_lists[scheme]

def olb2MQLEnum(olb):
    return OLB2More[olb][0]

def olb2BookNumber(olb):
    return OLB2More[olb][1]


def OSIS2OLB(OSIS):
    index = book_list("OSIS").index(OSIS)
    return book_list("OLB")[index]

def BW2OLB(BW):
    index = book_list("BibleWorks").index(BW)
    return book_list("OLB")[index]

def BookNumber2OLB(book_number):
    return book_list("OLB")[book_number-1]

