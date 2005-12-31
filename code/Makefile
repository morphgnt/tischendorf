VERSION = 1.2
ZIPFILES = *.TSP *.TUP README.txt
ZIPFILE = /tmp/Tischendorf-$(VERSION).zip

CLEANFILES = out.txt *~ *.pyc *.TD2 *.TSP *.TUP \
             $(DERIVED_MQLFILES) $(DERIVED_TXTFILES)

DERIVED_MQLFILES = Byzantine.mql Stephens.mql \
                   tischendorfmorph.mql tischendorf.mql \
                   WH11.mql WH.mql whmorph.mql 

DERIVED_TXTFILES = lexicon_nonunique.txt tischlexicon_nonunique.txt

#EMDROSPATH=/opt/EmdrosSQLite120pre140WX
#EMDROSPATH=/var/home/ulrikp/opt/EmdrosSQLite120pre143WX
EMDROSPATH=/var/home/ulrikp/opt/EmdrosSQLite120pre161-O3-noshared-WX-debug

DB = tisch

all:

clean: cleantisch
	rm -f $(CLEANFILES)

$(DB): tischendorfmorph.mql
	-echo "DROP DATABASE $(DB)" | $(EMDROSPATH)/bin/mql 
	echo "CREATE DATABASE $(DB)" | $(EMDROSPATH)/bin/mql 
	$(EMDROSPATH)/bin/mql -d $(DB) GNT_schema_1.2.mql
	$(EMDROSPATH)/bin/mql -d $(DB) -n tischendorfmorph.mql

wh: WH.mql
	-echo "DROP DATABASE wh" | $(EMDROSPATH)/bin/mql
	echo "CREATE DATABASE wh" | $(EMDROSPATH)/bin/mql 
	$(EMDROSPATH)/bin/mql -d wh GNT_schema_1.2.mql
	$(EMDROSPATH)/bin/mql -d wh -n WH.mql


cleantisch:
	-echo "DROP DATABASE $(DB)" | $(EMDROSPATH)/bin/mql 


tischclean: cleantisch

UnAccented: RE.TSP
	rm -rf UnAccented
	mkdir UnAccented
	for f in *.TSP; do NN=`echo $$f | sed -e 's/TSP/SLN/g'`; echo $$f; cat $$f | awk '{ print $$1 " " $$2 " " $$3;}' | sed -e 's/\([0-9]\+:[0-9]\+\).[0-9]\+/\1/' > UnAccented/$$NN; done

.PHONY: Accented

Accented: Accented/RE.SLN
	for f in Accented/*.SLN; do cat $$f | sed -e 's/\([0-9]\+\).[a-z]/\1/' > /tmp/SLN; mv /tmp/SLN $$f; done

zip: README.txt
	rm -f  $(ZIPFILE)
	zip $(ZIPFILE) $(ZIPFILES)

README.txt : ../text/Parsed/README.txt
	cp $< $@

