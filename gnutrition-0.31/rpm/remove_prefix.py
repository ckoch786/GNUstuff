#!/usr/bin/python

#  gnutrition - a nutrition and diet analysis program.  
#  Copyright (C) 2001 Edgar Denny (e.denny@ic.ac.uk)
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

# taken from solfege by Tom Cato Amundsen <tca@gnu.org>

import os, sys, string

prfx = "tmp/tmpgnutrition"

sys.stdout.write( "%defattr( -,root,root)\n")
infile = sys.stdin
while 1:
    s = infile.readline()
    if not s:
        break
    s = '/'+s[:-1][len( prfx)+2:]
    if s:
        sys.stdout.write( s)
        sys.stdout.write( "\n")
