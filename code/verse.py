import sys
import string
from word import *
from variant import *
from kind import *
import reader
from rptag import RobinsonPierpontTag
import re

 

 
text_variant_strongs_parsing_re= re.compile(r'\|\s+([a-z\[\]<>]+)\s+\|\s+([a-z\[\]<>]+)\s+\|([0-9\s]+\{[A-Z0-9\-]+\})\s*')

text_strongs_varparsing_varparsing_re = re.compile(r'(\s+[a-z\[\]<>]+\s+[0-9]+\s+)\|\s+(\{[A-Z0-9\-]+\})\s+\|\s+(\{[A-Z0-9\-]+\})\s+')

text_strongs_vartext_varstrongs_parsing = re.compile(r'\|\s+([a-z\[\]<>]+\s+[0-9]+)\s+\|\s+([a-z\[\]<>]+\s+[0-9]+)\s+\|\s+(\{[A-Z0-9\-]+\})\s+')

text_zerostrongs_re = re.compile(r'\s+0\s+([0-9]+)')

text_variant_strongs_parsing_variant_strongs_parsing = re.compile(r'([a-z\[\]<>]+)\s+\|\s+([0-9]+\s+\{[A-Z0-9\-]+\})\s+\|\s+([0-9]+\s+\{[A-Z0-9\-]+\})\s+\|')

text_strongs_variant_strongs_parsing_variant_strongs_parsing = re.compile(r'([a-z\[\]<>]+\s+[0-9]+)\s+\|\s+([0-9]+\s+\{[A-Z0-9\-]+\})\s+\|\s+([0-9]+\s+\{[A-Z0-9\-]+\})\s+\|')

text_strongs_variant_text_strongs_strongs_variant_parsing = re.compile(r'\|\s+([a-z\[\]<>]+\s+[0-9]+)\s+\|\s+([a-z\[\]<>]+\s+[0-9]+\s+[0-9]+)\s+\|\s+(\{[A-Z0-9\-]+\})\s+')

class Verse:
    def __init__(self, verse_lines, bookname, booknumber):
        self.chapter = self.verse = 0
        self.bookname = bookname
        self.booknumber = booknumber
        self.first_monad = 0
        self.last_monad = 0
        self.current_monad = 0
        self.verse_lines = verse_lines
        self.variant = variant_none
        self.variant_first_monad = 0
        self.words = []

    def getWords(self):
        return self.words
    
    
    def parse_chapter_verse(self, cv):
        #print "UP20: " + self.bookname + " " + cv
        if cv[0] == "[":
            if self.bookname == "Mark":
                self.chapter = 16
                self.verse = 9
            else:
                raise Exception("Verse.parse_chapter_verse: Unknown bookname: " + self.bookname)
        else:
            chap_ver_arr = cv.split(":")
            self.chapter = chap_ver_arr[0]
            self.verse = chap_ver_arr[1]
            #print "%s:%s" % (self.chapter, self.verse)

        
    def encode_word(self, word):
        result = '"'
        for c in word:
            if c == '"':
                result = result + '\\"'
            elif c == "\\":
                result = result + "\\\\"
            else:
                result = result + c
        result += '"'
        return result

    def parse(self, first_monad, read_what):
        # Set member variables
        self.first_monad = self.last_monad = first_monad
        self.current_monad = first_monad

        # Concatenate all lines
        overall_line = " ".join(self.verse_lines)
        #print overall_line

        # Get rid of Zero Strong's
        if text_zerostrongs_re.search(overall_line) != None:
            overall_line = text_zerostrongs_re.sub(r' \1 ', overall_line)

        if text_variant_strongs_parsing_re.search(overall_line) != None:
            overall_line = text_variant_strongs_parsing_re.sub(r'| \1 \3 | \2 \3 | ', overall_line)

        if text_strongs_varparsing_varparsing_re.search(overall_line) != None:
            overall_line = text_strongs_varparsing_varparsing_re.sub(r'| \1 \2 | \1 \3 | ', overall_line)

        if text_strongs_vartext_varstrongs_parsing.search(overall_line) != None:
            overall_line = text_strongs_vartext_varstrongs_parsing.sub(r'| \1 \3 | \2 \3 | ', overall_line)
            
        if text_variant_strongs_parsing_variant_strongs_parsing.search(overall_line) != None:
            sys.stderr.write("UP200!\n")
            overall_line = text_variant_strongs_parsing_variant_strongs_parsing.sub(r'| \1 \2 | \1 \3 | ', overall_line)

        if text_strongs_variant_strongs_parsing_variant_strongs_parsing.search(overall_line) != None:
            sys.stderr.write("UP201!\n")
            overall_line = text_strongs_variant_strongs_parsing_variant_strongs_parsing.sub(r'| \1 \2 | \1 \3 | ', overall_line)

        if text_strongs_variant_text_strongs_strongs_variant_parsing.search(overall_line) != None:
            sys.stderr.write("UP202!\n")
            overall_line = text_strongs_variant_text_strongs_strongs_variant_parsing.sub(r'| \1 \3 | \2 \3 | ', overall_line)
            
            



        # In Romans 16:27, we find the line ends with "{HEB}|".
        # We need this to be "{HEB} |".
        overall_line = overall_line.replace("}|", "} |")

        # Split into words
        line_words = overall_line.split()

        # Parse chapter/verse
        try:
            self.parse_chapter_verse(line_words[0])
        except:
            print overall_line
            raise Exception("Error...")

        # If this is, e.g., the shorter ending of Mark,
        # start at index 0. Otherwise, start at index 1
        if line_words[0][0] == "[":
            index = 0
        else:
            index = 1

        # Strip parens-words.
        # This is things like "(26-61)", indicating that NA27
        # starts the verse here.
        line_word_candidates = []
        for w in line_words[index:]:
            kind = recognize(w)
            if kind == kind_unknown:
                raise Exception("Error in Verse.parse: Unknown word kind: '" + w + "'")
            elif kind == kind_parens:
                pass
            else:
                line_word_candidates.append(w)

        # Parse rest of words
        self.parse_words(line_word_candidates, read_what)

        # If we are doing accented tischendorf, make w.accented_surface and
        # coerce w.surface into OLB.
        if read_what == reader.read_AccentedTischendorf:
            for w in self.words:
                w.makeSurfacesAccentedTischendorf()

        #print "len(self.words) = %d, last_monad - first_monad = %d" % (len(self.words), self.last_monad - self.first_monad)

        if self.last_monad < first_monad:
            print "Error in verse: ", self.bookname, self.chapter, self.verse

        return self.last_monad

    def parse_words(self, words, read_what):
        index = 0
        while index < len(words):
            if words[index] == "|":
                if self.variant == variant_none:
                    self.variant = variant_first
                    self.variant_first_monad = self.current_monad
                    self.first_variant_monad_offset = 0
                elif self.variant == variant_first:
                    self.variant = variant_second
                    self.second_variant_monad_offset = 0
                elif self.variant == variant_second:
                    self.variant = variant_none
                    if read_what == reader.read_wh_only:
                        self.current_monad = self.variant_first_monad + self.first_variant_monad_offset
                    elif read_what == reader.read_na27_only:
                        self.current_monad = self.variant_first_monad + self.second_variant_monad_offset
                    else: # Read both na27 and WH
                        #print "UP2"
                        self.current_monad = self.variant_first_monad + max(self.first_variant_monad_offset, self.second_variant_monad_offset)
                    self.last_monad = self.current_monad
                else:
                    raise Exception("Error: Unknown self.variant")
                index = index+1
            else:
                word_monad = 0
                if self.variant == variant_none:
                    word_monad = self.current_monad
                    self.last_monad = self.current_monad
                    self.current_monad += 1
                elif self.variant == variant_first:
                    word_monad = self.variant_first_monad + self.first_variant_monad_offset
                    self.first_variant_monad_offset += 1
                elif self.variant == variant_second:
                    word_monad = self.variant_first_monad + self.second_variant_monad_offset
                    self.second_variant_monad_offset += 1
                else:
                    raise Exception("Error: Unknown self.variant")
                w = Word(word_monad, self.variant)
                index = w.parse(index, words)
                if read_what == reader.read_wh_only:
                    if self.variant == variant_none or self.variant == variant_first:
                        self.words.append(w)
                elif read_what == reader.read_na27_only:
                    if self.variant == variant_none or self.variant == variant_second:
                        self.words.append(w)
                elif read_what in [reader.read_wh_and_na27,reader.read_tischendorf, reader.read_stephens]:
                    self.words.append(w)
                else:
                    raise Exception("Unknown read_what:" + str(read_what))

    def writeWordsMQL(self, f, bUseOldStyle):
        #print "UP280: %s" % self.getRef()
        for w in self.words:
            w.writeMQL(f, bUseOldStyle)

    def writeMQL(self, f, bUseOldStyle):
        print >>f, "CREATE OBJECT"
        print >>f, "FROM MONADS={" + str(self.first_monad) + "-" + str(self.last_monad) + "}"
        if bUseOldStyle:
            OT = "Verse"
        else:
            OT = ""
        print >>f, "[%s" % OT
        print >>f, "  book:=" + self.bookname + ";"
        print >>f, "  chapter:=" + str(self.chapter) + ";"
        print >>f, "  verse:=" + str(self.verse) + ";"
        print >>f, "]"
        if bUseOldStyle:
            print >>f, "GO"
        print >>f, ""

    def writeSFM(self, f, cur_monad):
        word_index = 1
        for w in self.words:
            w.writeSFM(f, self.booknumber, self.chapter, self.verse, word_index, cur_monad)
            word_index += 1
            cur_monad += 1
        return cur_monad

    def getRef(self):
        return "%s %s:%s" % (self.bookname, str(self.chapter), str(self.verse))

    def addManualAnalysis(self, myref, tischindex, tischverse, manualanalyses):
        thisref = "%s.%d" % (myref, tischindex+1)
        man_anal = manualanalyses.getTuple(thisref)
        #print "UP274: thisref = %s ; man_anal = %s " % (thisref, str(man_anal))
        if man_anal <> None:
            #print "UP275: thisref = %s ; man_anal = %s " % (thisref, str(man_anal))
            tischword = tischverse.words[tischindex]
            tischword.addManualAnalysisInfo(thisref, man_anal)
            return True
        else:
            return False
        

    def compareTischendorf(self, tischverse, tisch_verse_copy, lexicon, manualanalyses):
        bContinue = 1
        whindex = 0

        # First add all we can from manual analysis
        myref = tischverse.get_MORPH_ref(tisch_verse_copy)
        for tischindex in range(0, len(tischverse.words)+1):
            self.addManualAnalysis(myref, tischindex, tischverse, manualanalyses)
        tischindex = 0
        while bContinue:
            if whindex >= len(self.words) or tischindex >= len(tischverse.words):
                #print "UP281: Finished with %s.%d" % (myref, tischindex+1)
                bContinue = 0
            elif (tischverse.words[tischindex]).hasAnalysis():
                # If we have an analysis, just advance tischindex and whindex.
                #print "UP279: %s.%d" % (myref, tischindex+1)
                tischindex += 1
            else:
                tischword = tischverse.words[tischindex]
                whword = self.words[whindex]
                BETA_stripped_tischword = olbstrip(tischword)
                tischlexentry = tischendorfLexicon.getUniqueDefinition(BETA_stripped_tischword)
                if tischlexentry is not None and not lexicon.entryIsAmbiguous(tischlexentry):
                    # If we have a unique tischlexicon entry,
                    # we apply it unconditionally
                    tischword.parsing = tischlexentry[1]
                    tischword.setStrongs(tischlexentry[0])

                if whword.wordMatchesTisch(tischword, tischindex):
                    if not tischword.hasAnalysis(): tischword.addWHInfo(whword)
                    whindex += 1
                    tischindex += 1
                elif tischindex < len(tischverse.words) - 1 and whword.wordMatchesTisch(tischverse.words[tischindex+1], tischindex+1):
                    tischindex += 1
                    tischword = tischverse.words[tischindex]
                    if not tischword.hasAnalysis(): tischword.addWHInfo(whword)
                    whindex += 1
                    tischindex += 1
                elif whindex < len(self.words)-1 and self.words[whindex+1].wordMatchesTisch(tischword, tischindex):
                    whindex += 1
                    whword = self.words[whindex]
                    if not tischword.hasAnalysis(): tischword.addWHInfo(whword)
                    whindex += 1
                    tischindex += 1
                elif tischindex < len(tischverse.words) - 2 and whword.wordMatchesTisch(tischverse.words[tischindex+2], tischindex+2):
                    tischindex += 2
                    tischword = tischverse.words[tischindex]
                    if not tischword.hasAnalysis(): tischword.addWHInfo(whword)
                    whindex += 1
                    tischindex += 1
                elif whindex < len(self.words)-2 and self.words[whindex+2].wordMatchesTisch(tischword, tischindex):
                    whindex += 2
                    whword = self.words[whindex]
                    if not tischword.hasAnalysis(): tischword.addWHInfo(whword)
                    whindex += 1
                    tischindex += 1
                elif tischindex < len(tischverse.words) - 3 and whword.wordMatchesTisch(tischverse.words[tischindex+3], tischindex+3):
                    tischindex += 3
                    tischword = tischverse.words[tischindex]
                    if not tischword.hasAnalysis(): tischword.addWHInfo(whword) 
                    whindex += 1
                    tischindex += 1
                elif whindex < len(self.words)-3 and self.words[whindex+3].wordMatchesTisch(tischword, tischindex):
                    whindex += 3
                    whword = self.words[whindex]
                    if not tischword.hasAnalysis(): tischword.addWHInfo(whword) 
                    whindex += 1
                    tischindex += 1
                elif tischindex < len(tischverse.words) - 4 and whword.wordMatchesTisch(tischverse.words[tischindex+4], tischindex+4):
                    tischindex += 4
                    tischword = tischverse.words[tischindex]
                    if not tischword.hasAnalysis(): tischword.addWHInfo(whword) 
                    whindex += 1
                    tischindex += 1
                elif whindex < len(self.words)-4 and self.words[whindex+4].wordMatchesTisch(tischword, tischindex):
                    whindex += 4
                    whword = self.words[whindex]
                    if not tischword.hasAnalysis(): tischword.addWHInfo(whword) 
                    whindex += 1
                    tischindex += 1
                elif not tischword.hasAnalysis():
                    lexentry = lexicon.getUniqueDefinition(BETA_stripped_tischword)
                    lexnonuniqueentry = lexicon.getNonUniqueDefinition(BETA_stripped_tischword)
                    if tischlexentry != None:
                        if lexicon.entryIsAmbiguous(tischlexentry):
                            print "UP64: NonUniqueTischLexEntry: %s : WH = %s, Tisch = %s" % (self.getRef(), olbstrip(whword), olbstrip(tischword))
                        tischword.parsing = tischlexentry[1]
                        tischword.setStrongs(tischlexentry[0])
                        if self.entriesHaveDifferentCNG(tischword,whword):
                            #print "UP645: %s.%d WH = %s Tisch = %s" %  (self.getRef(), tischindex, olbstrip(whword), olbstrip(tischword))
                            pass
                    elif lexentry != None:
                        tischword.parsing = lexentry[1]
                        tischword.setStrongs(lexentry[0])
                    elif lexnonuniqueentry != None:
                        print "UP61: NonUniqueEntry: %s : WH = %s, Tisch = %s" % (self.getRef(), olbstrip(whword), olbstrip(tischword))
                        tischword.parsing = lexnonuniqueentry[1]
                        tischword.setStrongs(lexnonuniqueentry[0])
                    else:
                        print "\n-----------------------------"
                        print "UP1: %s : WH = %s, Tisch = %s" % (self.getRef(), olbstrip(whword), olbstrip(tischword))
                    whindex += 1
                    tischindex += 1
                else:
                    # If we got here, we had already given it an analysis!
                    whindex += 1
                    tischindex += 1
        
    def get_MORPH_ref(self, verse_copy, bDoVerseCopy = True):
        if verse_copy != "" and bDoVerseCopy:
            base_ref = "%s %d:%d.%s" % (reader.book_list_OLB[self.booknumber-1], int(self.chapter), int(self.verse), verse_copy)
        else:
            base_ref = "%s %d:%d" % (reader.book_list_OLB[self.booknumber-1], int(self.chapter), int(self.verse))
        return base_ref
        
    def write_MORPH_style(self, f, verse_copy, encodingStyle):
        base_ref = self.get_MORPH_ref(verse_copy, False)
        index = 1
        for w in self.words:
            w.write_MORPH_style(f, base_ref, index, True, encodingStyle)
            index += 1

    def write_subset_MORPH_style(self, f, verse_copy, word_predicate, manualanalyses, encodingStyle):
        base_ref = self.get_MORPH_ref(verse_copy)
        index = 1
        for w in self.words:
            thisref = "%s.%d" % (base_ref, index)
            #thisref = "%s" % (base_ref, index)            
            if manualanalyses.getTuple(thisref) <> None or word_predicate(w):
                w.write_MORPH_style(f, base_ref, index, False, encodingStyle)
            index += 1

    def write_StrippedLinear(self, f, verse_copy):
        base_ref = self.get_MORPH_ref(verse_copy)
        index = 1
        for w in self.words:
            w.write_StrippedLinear(f, base_ref, index)
            index += 1

    def write_WHLinear(self, f, verse_copy):
        base_ref = self.get_MORPH_ref(verse_copy)
        index = 1
        for w in self.words:
            w.write_WHLinear(f, base_ref, index)
            index += 1

    def write_Linear(self, f, verse_copy):
        base_ref = self.get_MORPH_ref(verse_copy)
        index = 1
        for w in self.words:
            w.write_Linear(f, base_ref, index)
            index += 1

    def addNonParseTischWords(self, verse_copy, lexicon, manualanalyses):
        myref = self.get_MORPH_ref(verse_copy)
        tischindex = 0
        for tischword in self.words:
            if tischword.hasNoAnalysis():
                thisref = "%s.%d" % (myref, tischindex+1)
                man_anal = manualanalyses.getTuple(thisref)
                if man_anal != None:
                    #print "UP276: thisref = %s ; man_anal = %s " % (thisref, str(man_anal))
                    tischword.addManualAnalysisInfo(thisref, man_anal)
                else:
                    BETA_stripped_tischword = olbstrip(tischword)
                    lexentry = lexicon.getUniqueDefinition(BETA_stripped_tischword)
                    tischlexentry = tischendorfLexicon.getUniqueDefinition(BETA_stripped_tischword)
                    lexnonuniqueentry = lexicon.getNonUniqueDefinition(BETA_stripped_tischword)
                    if tischlexentry != None:
                        if lexicon.entryIsAmbiguous(tischlexentry):
                            print "UP642: NonUniqueTischLexEntry: %s : Tisch = %s" % (self.getRef(), olbstrip(tischword))
                        tischword.parsing = tischlexentry[1]
                        tischword.setStrongs(tischlexentry[0])
                    elif lexentry != None:
                        tischword.parsing = lexentry[1]
                        tischword.setStrongs(lexentry[0])
                    elif lexnonuniqueentry != None:
                        print "UP612: NonUniqueEntry: %s : Tisch = %s" % (self.getRef(), olbstrip(tischword))
                        tischword.parsing = lexnonuniqueentry[1]
                        tischword.setStrongs(lexnonuniqueentry[0])
                    else:
                        print "\n-----------------------------"
                        print "UP12: Analysis not found at all: %s : Tisch = '%s'/'%s'" % (self.getRef(), olbstrip(tischword), tischword)
            tischindex = tischindex + 1
                        
    def entriesHaveDifferentCNG(self,tischword,whword):
        tischtag = RobinsonPierpontTag(tischword.parsing)
        whtag = RobinsonPierpontTag(whword.parsing)
        return tischtag.hasDifferentCNG(whtag)
            
