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

class FoodSrchResDlgUI:
    def __init__( self):
        self.dialog = gtk.Dialog( title='Food Search Result', 
            flags=gtk.DIALOG_MODAL, 
            buttons=( gtk.STOCK_HELP, gtk.RESPONSE_HELP, gtk.STOCK_OK,
            gtk.RESPONSE_OK, gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))
        self.dialog.set_default_response(gtk.RESPONSE_OK)

        table = gtk.Table( 4, 3, False)
        table.set_border_width( 5)
        table.set_row_spacings( 5)
        table.set_col_spacings( 5)
        self.dialog.vbox.pack_start( table, True, True, 0)

        self.tree = gtk.TreeStore( gobject.TYPE_STRING, gobject.TYPE_INT) 
        self.treeview = gtk.TreeView( self.tree)

        self.selection = self.treeview.get_selection()
        self.selection.set_mode( gtk.SELECTION_SINGLE)

        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_policy( gtk.POLICY_ALWAYS, gtk.POLICY_ALWAYS)
        scrolled_window.set_shadow_type( gtk.SHADOW_IN)
        scrolled_window.add( self.treeview)
        scrolled_window.set_size_request( 400, 200)
        
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn( 'Food', renderer, text=0)
        self.treeview.append_column( column)

        table.attach( scrolled_window, 0, 4, 0, 1, 
            gtk.FILL | gtk.EXPAND, gtk.FILL | gtk.EXPAND, 0, 0)

        label1 = gtk.Label( 'Selected food')
        label1.set_alignment( 1, 0.5)
        table.attach( label1, 0, 1, 1, 2, gtk.FILL, 0, 0, 0)

        self.food_entry = gtk.Entry()
        self.food_entry.set_property( 'editable', False)
        self.food_entry.set_property( 'can-focus', False)
        self.food_entry.set_activates_default( True)
        table.attach( self.food_entry, 1, 4, 1, 2, 
            gtk.FILL | gtk.EXPAND, 0, 0, 0)

        self.amount_label = gtk.Label( '')
        self.amount_label.set_text_with_mnemonic( '_Amount')
        self.amount_label.set_alignment( 1, 0.5)
        table.attach( self.amount_label, 0, 1, 2, 3, gtk.FILL, 0, 0, 0)

        self.amount_entry = gtk.Entry()
        self.amount_label.set_mnemonic_widget( self.amount_entry)
        self.amount_entry.set_activates_default( True)
        table.attach( self.amount_entry, 1, 2, 2, 3, 
            gtk.FILL | gtk.EXPAND, 0, 0, 0)
        
        self.msre_label = gtk.Label( '')
        self.msre_label.set_text_with_mnemonic( '_Measure')
        self.msre_label.set_alignment( 1, 0.5)
        table.attach( self.msre_label, 2, 3, 2, 3, gtk.FILL, 0, 0, 0)

        self.combo = gnutr_widgets.GnutrComboBox()
        self.msre_label.set_mnemonic_widget( self.combo)
        table.attach( self.combo, 3, 4, 2, 3, 
            gtk.FILL | gtk.EXPAND, 0, 0, 0)
