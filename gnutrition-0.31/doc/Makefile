# Makefile.in for Gnutrition docs

prefix      = /usr/local
exec_prefix = ${prefix}
bindir      = ${exec_prefix}/bin
datadir     = ${prefix}/share
INSTALL     = /usr/bin/install -c
PACKAGE		= gnutrition
srcdir      = ..

imagefiles = $(wildcard *.jpg)
dist_files = Makefile topic.dat $(imagefiles) gnutrition.sgml
docdir = ${datadir}/gnome/help/${PACKAGE}/C

#all: create-html create-pdf
all: create-html

clean:
	rm -Rf gnutrition/
	rm -f gnutrition.pdf
	rm -f gnutrition.tex gnutrition.aux gnutrition.log gnutrition.out
	rm -Rf DB* # temp dirs created by db2html

install: gnutrition/book1.html 
	mkdir -p $(docdir)/stylesheet-images
	${INSTALL} -m 644 $(imagefiles) $(docdir)
	for i in gnutrition/*.html ; do \
		${INSTALL} -m 644 $$i $(docdir) ; \
	done
	for i in gnutrition/stylesheet-images/*.gif ; do \
		${INSTALL} -m 644 $$i $(docdir)/stylesheet-images ; \
	done
	${INSTALL} -m 644 topic.dat $(docdir)

uninstall:

gnutrition/book1.html: create-html

create-html: gnutrition.sgml $(imagefiles)
	db2html gnutrition.sgml

create-pdf: gnutrition.sgml $(imagefiles)
	db2pdf gnutrition.sgml

