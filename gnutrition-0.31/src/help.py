#  gnutrition - a nutrition and diet analysis program.
#  Copyright( C) 2000-2002 Edgar Denny (edenny@skyweb.net)
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

import webbrowser
import install
import os
import string

def test_access( file):
    path_list = string.split( os.environ['PATH'], ':')
    for p in path_list:
        if os.path.exists( p):
            a = os.access( p + '/' + file, os.F_OK | os.X_OK)
            if a:
                return 1
    return 0

def get_browser():
    browser_list = ['galeon', 'mozilla', 'lynx']
    for b in browser_list:
        if test_access( b):
            browser = webbrowser.GenericBrowser( b + ' %s')
            webbrowser.register( b, None, browser)
            return b
    print 'No Web browser found.'
    return ''

def open( html_page):
    url = 'file://' + install.dir + '/doc/' + html_page

    if selected_browser:
        controller = webbrowser.get( selected_browser)
        controller.open( url)

selected_browser = get_browser()
