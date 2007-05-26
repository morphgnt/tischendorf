DERIVED_FILES = lemmatable_utf8.txt lemmatable_ANLEX_utf8.txt \
                lemmatable_SBL.txt lemmatable_ANLEX_SBL.txt

CLEANFILES = *~ $(DERIVED_FILES)


all: $(DERIVED_FILES)


clean:
	rm -f $(CLEANFILES)


lemmatable_utf8.txt: lemmatable.txt toutf8.py
	python toutf8.py < lemmatable.txt > lemmatable_utf8.txt

lemmatable_ANLEX_utf8.txt: lemmatable_ANLEX.txt toutf8.py
	python toutf8.py < lemmatable_ANLEX.txt > lemmatable_ANLEX_utf8.txt


lemmatable_SBL.txt: lemmatable.txt toSBL.py
	python toSBL.py < lemmatable.txt > lemmatable_SBL.txt

lemmatable_ANLEX_SBL.txt: lemmatable_ANLEX.txt toSBL.py
	python toSBL.py < lemmatable_ANLEX.txt > lemmatable_ANLEX_SBL.txt
