# gnutrition - a nutrition and diet analysis program.
# Copyright (C) 2001-2002 Edgar Denny (edenny@skyweb.net)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

prefix		= /usr/local
exec_prefix	= ${prefix}
bindir		= ${exec_prefix}/bin
datadir		= ${datarootdir}/gnutrition
datarootdir 	= ${prefix}/share
INSTALL		= /usr/bin/install -c
DISTNAME	= gnutrition-0.6
PYTHON		= /usr/bin/python



SUBDIRS = src data pixmaps doc rpm debian

files = AUTHORS autogen.sh COPYING gnutrition.desktop py-compile \
	Changelog configure install-sh INSTALL configure.in \
	run-gnutrition.py.in Makefile.in README

all:
	for dir in $(SUBDIRS); do \
		${MAKE} -C $$dir all; \
	done

install: all mkinstalldirs
	for dir in $(SUBDIRS); do \
		${MAKE} -C $$dir install; \
	done
	mkdir -p ${bindir}
	${INSTALL} run-gnutrition.py ${bindir}/gnutrition
	mkdir -p ${prefix}/gnome/apps/Applications/
	${INSTALL} -m 644 gnutrition.desktop ${prefix}/gnome/apps/Applications/

mkinstalldirs:
	mkdir -p ${bindir}
	mkdir -p ${datadir}

clean:
	for dir in $(SUBDIRS); do \
		${MAKE} -C $$dir clean; \
	done

uninstall:
	for dir in $(SUBDIRS); do \
		${MAKE} -C $$dir uninstall; \
	done
	rm -rf ${bindir}/gnutrition
	rm -rf ${datadir}

distclean: clean deb-clean rpm-clean
	for dir in $(SUBDIRS); do \
		rm -f $$dir/Makefile; \
	done
	rm -f config.status config.cache config.log
	rm -f install-stamp build-stamp
	rm -f Makefile run-gnutrition.py
	rm -f config.cache config.log config.status
	rm -f src/install.py

deb:
	dpkg-buildpackage -rfakeroot -us -uc

dist: clean
	rm -rf $(DISTNAME)
	mkdir -p $(DISTNAME)
	cp $(files) $(DISTNAME)
	for dir in $(SUBDIRS); do \
		mkdir -p $(DISTNAME)/$$dir; \
		cp -r $$dir/* $(DISTNAME)/$$dir; \
	done
	tar --gzip --create --file=../$(DISTNAME).tar.gz $(DISTNAME)
	rm -rf $(DISTNAME)

release: dist
	${MAKE} deb
	${MAKE} rpm

deb-clean:
	rm -rf debian/gnutrition
	rm -f debian/*.debhelper
	rm -f debian/files
	rm -f debian/substvars

rpm-spec:
	./configure --prefix=/tmp/tmpgnutrition/usr
	${MAKE}
	${MAKE} install
	(find /tmp/tmpgnutrition -type f; find /tmp/tmpgnutrition -type l) \
		| ${PYTHON} rpm/remove_prefix.py > rpm/files.list
	rm -rf /tmp/tmpgnutrition

rpm: rpm-spec dist
	cp ../$(DISTNAME).tar.gz /usr/src/redhat/SOURCES
	rpm -ba rpm/gnutrition.spec

rpm-clean:
	rm -f rpm/gnutrition.spec
	rm -f rpm/files.list
