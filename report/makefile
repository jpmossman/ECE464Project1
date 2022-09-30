report.pdf: trash/report.pdf
	cp trash/report.pdf ./

trash/report.pdf:
	mkdir -p trash
	latexmk report.tex -pdf -outdir=trash
