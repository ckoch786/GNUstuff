#  gnutrition - a nutrition and diet analysis program.
#  Copyright( C) 2000-2002 Edgar Denny (edenny@skyweb.net)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
#v This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import os
import stat
import gtk

import save_as
import gnutr_widgets

class FileSelectDlg:
    def __init__( self):
        self.save_as = save_as.SaveAs()
        self.dlg = gtk.FileSelection( 'Save Recipe As...')
        self.dlg.set_filename( os.environ['HOME'] + '/')
        self.dlg.connect( 'response', self.on_response)

        hbox1 = gtk.HBox()
        self.dlg.main_vbox.pack_start( hbox1, False, True, 5)
        label1 = gtk.Label( 'Save Recipe As') 
        hbox1.pack_start( label1, False, True, 5)

# what's this supposed to do?
#         option_menu1 = gtk.OptionMenu()
#         menu = gtk.Menu()
#         menuitem1 = gtk.MenuItem( 'HTML (.html)')
#         # FIXME: send a bug report to pygtk
#         gtk.MenuShell.append( menu, menuitem1)
#         option_menu1.set_menu( menu)

        option_menu1 = gnutr_widgets.GnutrComboBox((( 'HTML (.html)',),), 0)
        
        hbox1.pack_start( option_menu1, True, True, 0)
        self.dlg.main_vbox.show_all()

    def show( self, recipe, nutr_list, pcnt_cal):
        self.recipe = recipe
        self.nutr_list = nutr_list
        self.pcnt_cal = pcnt_cal
        self.dlg.run()

    def valid_filename( self, fn):
        if not fn:
            return 0
        if os.access( fn, os.F_OK):
            mode = os.stat( fn)[stat.ST_MODE]
            if mode:
                if stat.S_ISDIR( mode):
                    return 0
        return 1

    def on_response( self, w, r, d=None):
        if r == gtk.RESPONSE_OK:
            fn = self.dlg.get_filename()
            if self.valid_filename( fn):
                self.save_as.html( self.recipe, self.nutr_list, self.pcnt_cal, 
                    fn)
                self.dlg.hide()
        elif r == gtk.RESPONSE_CANCEL or r == gtk.RESPONSE_DELETE_EVENT:
            self.dlg.hide()
