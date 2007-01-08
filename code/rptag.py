#
#  Copyright (c) 2005 by Ulrik Petersen
#  All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#
#  - Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
#  - Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
#  - Neither the name "Ulrik Petersen" nor the names of any contributors
#    may be used to endorse or promote products derived from this
#    software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#  HOLDERS OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
#  INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
#  BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
#  OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#  ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
#  TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
#  USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
#  DAMAGE
#

import re

def get_enum_from_dict(dict, str):
    if str == "NA":
        return str
    else:
        if dict is psp_dict:
            return dict[str][0]
        else:
            return dict[str]

def printMQL(f, feature_name, str, dict):
    if str == "NA":
        return
    else:
        print >>f, "  %s:=%s;" % (feature_name, get_enum_from_dict(dict, str))

def cmp_longer_first(str1, str2):
    i1 = 0
    i2 = 0
    lasts1 = len(str1)-1
    lasts2 = len(str2)-1
    while i1 != lasts1 and i2 != lasts2:
        c1 = str1[i1]
        c2 = str2[i2]
        if c1 != c2:
            if c1 < c2:
                return -1
            else:
                return 1
        i1 += 1
        i2 += 1

    if lasts1 == lasts2:
        return 0
    elif lasts1 < lasts2:
        return 1
    else:
        return -1
    
def get_re_from_dict(dict):
    rstr = ""
    keys = dict.keys()
    keys.sort(cmp_longer_first)
    for k in keys:
        rstr += "(^" + k + ")|"
    return re.compile(rstr[0:-1])

def parse_re(regex, str):
    m = regex.match(str)
    if m != None:
        result = str[m.start():m.end()]
        remainder = regex.sub('', str, 1)
        return result, remainder
    else:
        return "", str
        

def parse_suffix(str, rptag):
    suffix, remainder = parse_re(rptag.suffix_re, str)
    if suffix != "":
        rptag.suffix = suffix
    return remainder

def parse_extra(str, rptag):
    extra, remainder = parse_re(rptag.extra_re, str)
    if extra != "":
        rptag.extra = extra
    return remainder

def parse_psp_indeclinable(str, rptag):
    remainder = parse_suffix(str, rptag)
    return remainder

def parse_case(str, rptag):
    case, remainder = parse_re(rptag.case_re, str)
    if case != "":
        rptag.case = case
    return remainder

def parse_number(str, rptag):
    number, remainder = parse_re(rptag.number_re, str)
    if number != "":
        rptag.number = number
    return remainder

def parse_gender(str, rptag):
    gender, remainder = parse_re(rptag.gender_re, str)
    if gender != "":
        rptag.gender = gender
    return remainder

def parse_gender_number(str, rptag):
    remainder = parse_number(str, rptag)
    remainder = parse_gender(remainder, rptag)
    return remainder

def parse_psp_noun_like(str, rptag):
    remainder = parse_case(str, rptag)
    remainder = parse_gender_number(remainder, rptag)
    if remainder != "":
        remainder = parse_suffix(remainder, rptag)
    return remainder

def parse_person(str, rptag):
    person, remainder = parse_re(rptag.person_re, str)
    if person != "":
        rptag.person = person
    else:
        rptag.person = "3"
    return remainder


def parse_psp_pronoun(str, rptag):
    remainder = parse_person(str, rptag)
    if rptag.person == "3":
        remainder = parse_case(remainder, rptag)
        remainder = parse_number(remainder, rptag)
        remainder = parse_gender(remainder, rptag)
    else:
        remainder = parse_case(remainder, rptag)
        remainder = parse_number(remainder, rptag)
    if remainder != "":
        remainder = parse_suffix(remainder, rptag)
    return remainder

def parse_psp_pronoun_2(str, rptag):
    remainder = parse_person(str, rptag)
    remainder = parse_case(remainder, rptag)
    remainder = parse_number(remainder, rptag)
    remainder = parse_gender(remainder, rptag)
    if remainder != "":
        remainder = parse_suffix(remainder, rptag)
    return remainder

def parse_tense(str, rptag):
    tense, remainder = parse_re(rptag.tense_re, str)
    if tense != "":
        rptag.tense = tense
    return remainder

def parse_voice(str, rptag):
    voice, remainder = parse_re(rptag.voice_re, str)
    if voice != "":
        rptag.voice = voice
    return remainder


def parse_mood(str, rptag):
    mood, remainder = parse_re(rptag.mood_re, str)
    if mood != "":
        rptag.mood = mood
    return remainder


def parse_psp_verb(str, rptag):
    remainder = parse_tense(str, rptag)
    remainder = parse_voice(remainder, rptag)
    remainder = parse_mood(remainder, rptag)
    if rptag.mood in ["R", "P"]:     # participle
        if remainder[0] == "-":
            remainder = remainder[1:]
        remainder = parse_case(remainder, rptag)
        remainder = parse_number(remainder, rptag)
        remainder = parse_gender(remainder, rptag)
    elif rptag.mood in ["I", "S", "O", "M"]: # finite verbs
        if remainder == "":
            #print "UP1: str = '" + str + "'"
            pass
        elif remainder[0] == "-":
            remainder = remainder[1:]
        remainder = parse_person(remainder, rptag)
        remainder = parse_number(remainder, rptag)
    if remainder != "":
        remainder = parse_extra(remainder, rptag)
    return remainder


suffix_dict = {
    "-S" : "superlative",
    "-C" : "comparative",
    "-ABB" : "abbreviated",
    "-I" : "interrogative",
    "-N" : "negative",
    "-ATT" : "attic",
    "-P" : "particle_attached",
    "-K" : "crasis"
    }


case_dict = {
    "N" : "nominative",
    "V" : "vocative",
    "G" : "genitive",
    "D" : "dative",
    "A" : "accusative"
    }




number_dict = {
    "S" : "singular",
    "P" : "plural",
    }


gender_dict = {
    "M" : "masculine",
    "F" : "feminine",
    "N" : "neuter",
    }


tense_dict = {
    "P" : "present",
    "I" : "imperfect",
    "F" : "future",
    "2F" : "second_future",
    "A" : "aorist",
    "2A" : "second_aorist",
    "R" : "perfect",
    "2R" : "second_perfect",
    "L" : "pluperfect",
    "2L" : "second_pluperfect",
    "X" : "no_tense_stated"
    }


voice_dict = {
    "A" : "active",
    "M" : "middle",
    "P" : "passive",
    "E" : "middle_or_passive",
    "D" : "middle_deponent",
    "O" : "passive_deponent",
    "N" : "middle_or_passive_deponent",
    "Q" : "impersonal_active",
    "X" : "no_voice"
    }


mood_dict = {
    "I" : "indicative",
    "S" : "subjunctive",
    "O" : "optative",
    "M" : "imperative",
    "N" : "infinitive",
    "P" : "participle",
    "R" : "imperative_participle"
    }


extra_dict = {
    "-M" : "middle_significance",
    "-C" : "contracted_form",
    "-T"  : "transitive",
    "-A" : "aeolic",
    "-ATT" : "attic",
    "-AP" : "apocopated_form",
    "-IRR" : "irregular_or_impure_form"
    }

person_dict = {
    "1" : "first_person",
    "2" : "second_person",
    "3" : "third_person"
    }

psp_dict = {
  "ADV" : ("adverb", parse_psp_indeclinable),
  "CONJ" : ("conjunction", parse_psp_indeclinable),
  "COND" : ("cond", parse_psp_indeclinable),
  "PRT" : ("particle", parse_psp_indeclinable),
  "PREP" : ("preposition", parse_psp_indeclinable),
  "INJ" : ("interjection", parse_psp_indeclinable),
  "ARAM" : ("aramaic", parse_psp_indeclinable),
  "HEB" : ("hebrew", parse_psp_indeclinable),
  "N-PRI" : ("proper_noun_indeclinable", parse_psp_indeclinable),
  "A-NUI" : ("numeral_indeclinable", parse_psp_indeclinable),
  "N-LI" : ("letter_indeclinable", parse_psp_indeclinable),
  "N-OI" : ("noun_other_type_indeclinable", parse_psp_indeclinable),
  "N-" : ("noun", parse_psp_noun_like),
  "A-" : ("adjective", parse_psp_noun_like),
  "R-" : ("relative_pronoun", parse_psp_pronoun),
  "C-" : ("reciprocal_pronoun", parse_psp_pronoun),
  "D-" : ("demonstrative_pronoun", parse_psp_pronoun),
  "T-" : ("article", parse_psp_noun_like),
  "K-" : ("correlative_pronoun", parse_psp_pronoun),
  "I-" : ("interrogative_pronoun", parse_psp_pronoun),
  "X-" : ("indefinite_pronoun", parse_psp_pronoun),
  "Q-" : ("correlative_or_interrogative_pronoun", parse_psp_pronoun),
  "F-" : ("reflexive_pronoun", parse_psp_pronoun_2),
  "S-" : ("possessive_pronoun", parse_psp_pronoun_2),
  "P-" : ("personal_pronoun", parse_psp_pronoun),
  "V-" : ("verb", parse_psp_verb),
    }



class RobinsonPierpontTag:
    def __init__(self, tag):
        self.tag = tag
        self.psp = ""
        self.case = "NA"
        self.number = "NA"
        self.gender = "NA"
        self.suffix = "NA"
        self.tense  = "NA"
        self.voice = "NA"
        self.mood = "NA"
        self.extra = "NA"
        self.person = "NA"
        self.person_re = get_re_from_dict(person_dict)
        self.gender_re = get_re_from_dict(gender_dict)
        self.suffix_re = get_re_from_dict(suffix_dict)
        self.case_re = get_re_from_dict(case_dict)
        self.number_re = get_re_from_dict(number_dict)
        self.gender_re = get_re_from_dict(gender_dict)
        self.tense_re = get_re_from_dict(tense_dict)
        self.voice_re = get_re_from_dict(voice_dict)
        self.mood_re = get_re_from_dict(mood_dict)
        self.extra_re = get_re_from_dict(extra_dict)
        self.psp_re = get_re_from_dict(psp_dict)
        self.parsetag()

    def parsetag(self):
        psp_re = get_re_from_dict(psp_dict)
        self.psp, remainder = parse_re(psp_re, self.tag)
        if remainder == "":
            return
        else:
            remainder = psp_dict[self.psp][1](remainder, self)
            if remainder != "":
                print self.tag, " remainder =", remainder

    def writeMQL(self, f):
        printMQL(f, "psp", self.psp, psp_dict)
        printMQL(f, "case", self.case, case_dict)
        printMQL(f, "number", self.number, number_dict)
        printMQL(f, "gender", self.gender, gender_dict)
        printMQL(f, "suffix", self.suffix, suffix_dict)
        printMQL(f, "tense", self.tense, tense_dict)
        printMQL(f, "voice", self.voice, voice_dict)
        printMQL(f, "mood", self.mood, mood_dict)
        printMQL(f, "extra", self.extra, extra_dict)
        printMQL(f, "person", self.person, person_dict)

    def hasDifferentCNG(self, othertag):
        if self.case <> othertag.case or self.number <> othertag.number or self.gender <> othertag.gender:
            return True
        else:
            return False


t = RobinsonPierpontTag("N-NSF")
t = RobinsonPierpontTag("N-NSF")
t = RobinsonPierpontTag("V-PAI-3S")
t = RobinsonPierpontTag("P-2DS")
t = RobinsonPierpontTag("V-PAN")
t = RobinsonPierpontTag("P-ASF")
t = RobinsonPierpontTag("CONJ")
t = RobinsonPierpontTag("V-PAP-NSM")
t = RobinsonPierpontTag("P-ASM")
t = RobinsonPierpontTag("V-AAN")
t = RobinsonPierpontTag("V-AOI-3S")
t = RobinsonPierpontTag("T-ASM")
t = RobinsonPierpontTag("N-ASM")
t = RobinsonPierpontTag("ADV")
t = RobinsonPierpontTag("N-ASM")
t = RobinsonPierpontTag("P-ASM")
t = RobinsonPierpontTag("V-IAI-3P")
t = RobinsonPierpontTag("N-DPN")
t = RobinsonPierpontTag("CONJ")
t = RobinsonPierpontTag("V-2ADP-DPN")
t = RobinsonPierpontTag("T-GSM")
t = RobinsonPierpontTag("N-GSM")
t = RobinsonPierpontTag("V-ADI-3S")
t = RobinsonPierpontTag("T-NSF")
t = RobinsonPierpontTag("PRT-N")
