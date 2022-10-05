.PHONY: report clean all

TESTINS := $(wildcard report/testins/*.txt)
TESTOUTS := $(TESTINS:report/testins/%.txt=report/testouts/%.txt)

report: report/submit/report.pdf

report/submit/report.pdf: report/trash/report.pdf
	mkdir -p report/submit
	cp report/trash/report.pdf report/submit/

report/trash/report.pdf: report/report.tex $(TESTOUTS)
	mkdir -p report/trash
	latexmk report/report.tex -pdf -outdir=report/trash

report/testouts/%.txt: report/testins/%.txt
	python3 main.py < $< > $@

clean:
	rm -rf report/trash/* report/testouts/*
