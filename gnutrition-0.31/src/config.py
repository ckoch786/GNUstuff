#  gnutrition - a nutrition and diet analysis program.
#  Copyright( C) 2000 - 2002 Edgar Denny (edenny@skyweb.net)
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
#

import shelve
import os

dir = os.environ['HOME'] + '/.gnutrition'
fn = dir + '/config'

if not os.access( dir, os.F_OK):
    os.mkdir( dir)

def get_value( key):
    db = shelve.open( fn, 'c')
    try:
        value = db[key]
    except KeyError:
        value = None
    db.close()
    return value

def set_key_value( key, value):
    db = shelve.open( fn)
    db[key] = value
    db.close()
