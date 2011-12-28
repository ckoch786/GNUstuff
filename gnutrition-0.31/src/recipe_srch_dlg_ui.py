#  Gnutrition - a nutrition and diet analysis program.
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

import gobject
import gtk
import gnutr_widgets

class RecipeSrchDlgUI:
    def __init__( self):
        self.dialog = gtk.Dialog( title='Recipe Search',
            flags=gtk.DIALOG_MODAL,
            buttons=( gtk.STOCK_HELP, gtk.RESPONSE_HELP,
                      gtk.STOCK_OK, gtk.RESPONSE_OK,
                      gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))
        self.dialog.set_resizable( False)
        self.dialog.set_default_response( gtk.RESPONSE_OK)

        self.container = gtk.HBox( False, 0)
        self.dialog.vbox.pack_start( self.container, True, True, 0)

        vbox1 = gtk.VBox( False, 0)
        self.container.pack_start( vbox1, True, True, 0)

        hbox2 = gtk.HBox( True, 0)
        hbox2.set_border_width( 5)
        vbox1.pack_start( hbox2, True, False, 0)

        label1 = gtk.Label( 'Recipe Category')
        label1.set_alignment( 1.0, 0.5)
        label1.set_padding( 10, 0)
        hbox2.pack_start( label1, False, True, 0)

        self.category_combo = gnutr_widgets.GnutrComboBox()
        hbox2.pack_start( self.category_combo, True, True, 0)

        frame1 = gtk.Frame( 'Text in Recipe Name to Match')
        frame1.set_border_width( 5)
        vbox1.pack_start( frame1, True, True, 0)

        hbox3 = gtk.HBox( True, 0)
        hbox3.set_border_width( 5)
        frame1.add( hbox3)

        label2 = gtk.Label( 'Regular Expression')
        label2.set_alignment( 1.0, 0.5)
        label2.set_padding( 10, 0)
        hbox3.pack_start( label2, False, True, 0)

        self.reg_expr_entry = gtk.Entry()
        self.reg_expr_entry.set_activates_default(True)
        hbox3.pack_start( self.reg_expr_entry, True, True, 0)
