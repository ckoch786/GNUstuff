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

class RecipeEditDlgUI:
    def __init__( self):
        self.dialog = gtk.Dialog( title='Edit Food',
                                  flags=gtk.DIALOG_MODAL,
                                  buttons=( gtk.STOCK_HELP, gtk.RESPONSE_HELP,
                                            gtk.STOCK_OK, gtk.RESPONSE_OK,
                                            gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))
        self.dialog.set_default_response( gtk.RESPONSE_OK)

        table = gtk.Table( 2, 2, False)
        table.set_border_width( 5)
        table.set_row_spacings( 5)
        table.set_col_spacings( 5)
        self.dialog.vbox.pack_start( table, True, True, 0)

        label1 = gtk.Label( 'Recipe')
        label1.set_alignment( 1, 0.5)
        table.attach( label1, 0, 1, 0, 1, gtk.FILL, 0, 0, 0)

        label2 = gtk.Label( '')
        label2.set_text_with_mnemonic( '_Number of servings')
        label2.set_alignment( 1, 0.5)
        table.attach( label2, 0, 1, 1, 2, gtk.FILL, 0, 0, 0)

        self.recipe_entry = gtk.Entry()
        self.recipe_entry.set_property( 'editable', False)
        self.recipe_entry.set_property( 'can-focus', False)
        table.attach( self.recipe_entry, 1, 2, 0, 1, 
           gtk.EXPAND| gtk.FILL, 0, 0, 0)

        self.num_serv_entry = gtk.Entry()
        self.num_serv_entry.set_activates_default( True)
        table.attach( self.num_serv_entry, 1, 2, 1, 2, 
           gtk.EXPAND| gtk.FILL, 0, 0, 0)
