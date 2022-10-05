.PHONY: report clean all

TESTINS := $(wildcard report/testins/*.txt)
TESTOUTS := $(TESTINS:report/testins/%.txt=report/testouts/%.txt)
SRC := $(wildcard *.py)
SUBSRC := $(SRC:%=report/submit/%)

report: report/submit/report.pdf $(SUBSRC)

report/submit/report.pdf: report/trash/report.pdf
	mkdir -p report/submit
	cp report/trash/report.pdf report/submit/

report/trash/report.pdf: report/report.tex $(SRC) $(TESTOUTS)
	mkdir -p report/trash
	latexmk report/report.tex -pdf -outdir=report/trash

report/testouts/%.txt: report/testins/%.txt $(SRC)
	python3 main.py < $< > $@

report/submit/%.py: %.py
	cp $< $@

clean:
	rm -rf report/trash/* report/testouts/* report/submit/*
