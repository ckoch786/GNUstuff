#  gnutrition - a nutrition and diet analysis program.
#  Copyright (C) 2001-2002 Edgar Denny (edenny@skyweb.net)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

prefix      = /usr/local
exec_prefix = ${prefix}
bindir      = ${exec_prefix}/bin
datadir     = ${datarootdir}
datarootdir = ${prefix}/share
INSTALL     = /usr/bin/install -c
srcdir      = ..
pycomp      = ${srcdir}/py-compile



all:
	chmod +x ${pycomp}
	${pycomp} *.py

install:
	mkdir -p ${datadir}/gnutrition/src
	${INSTALL} -m 644 -c *.py *.pyc *.pyo ${datadir}/gnutrition/src

clean:
	rm -f *.pyo *.pyc

uninstall:
	rm -f ${datadir}/gnutrition/src/*.py ${datadir}/gnutrition/src/*.pyo
	rm -rf ${datadir}/gnutrition/src
