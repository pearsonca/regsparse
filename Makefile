
-include local.makefile

SRCS ?= instructions
RESS ?= digests

MKDIRS := ${SRCS} ${RESS}

PYTHON ?= $(shell which python3)

${MKDIRS}:
	mkdir -p $@

check: dictionary.csv
	# TODO check the dictionary file for syntax compliance

ALLSRCS := $(wildcard ${SRCS}/*.pdf)
ALLRESS := $(subst ${SRCS},${RESS},$(ALLSRCS:pdf=csv))

CHROMEDRV := "https://chromedriver.storage.googleapis.com/92.0.4515.107/chromedriver_linux64.zip"

chromedriver:
	wget ${CHROMEDRV} -O tmp.zip
	unzip tmp.zip
	rm tmp.zip

.PRECIOUS: instructions/%.pdf digests/%.csv

instructions/100001p.pdf: regs_dodi.py chromedriver | ${SRCS}
	python3 $^ $(abspath $|)

setup: check instructions/100001p.pdf | ${MKDIRS} chromedriver

cleansrc: | ${SRCS}
	cd $|; rm *.pdf

cleanres: | ${RESS}
	cd $|; rm *.csv

cleanall: cleansrc cleanres

countall: ${ALLRESS}

${RESS}/%.csv: digest.py dictionary.csv ${SRCS}/%.pdf
	${PYTHON} $^ $@

summarize.csv: summarize.R $(wildcard ${RESS}/*.csv) | ${RESS}
	Rscript $< $| $@

summary: summarize.csv
