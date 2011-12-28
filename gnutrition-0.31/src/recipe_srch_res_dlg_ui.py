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

class RecipeSrchResDlgUI:
    def __init__( self):
        self.dialog = gtk.Dialog( 'Recipe Search Result',
            flags=gtk.DIALOG_MODAL,
            buttons=( gtk.STOCK_HELP, gtk.RESPONSE_HELP, 
            gtk.STOCK_OK, gtk.RESPONSE_OK, 
            gtk.STOCK_DELETE, 1,
            gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))
        self.dialog.set_default_response(gtk.RESPONSE_OK)

        scrolled_window1 = gtk.ScrolledWindow()
        scrolled_window1.set_border_width( 5)
        scrolled_window1.set_policy( gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrolled_window1.set_size_request( -1, 150)
        self.dialog.vbox.pack_start( scrolled_window1, True, True, 0)

        self.treemodel = gtk.ListStore( gobject.TYPE_STRING, gobject.TYPE_INT)
        self.treeview = gtk.TreeView( self.treemodel)
        self.selection = self.treeview.get_selection()
        self.selection.set_mode( gtk.SELECTION_SINGLE)
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn( 'Recipe Search Results', renderer, text=0)
        self.treeview.append_column( column)
        scrolled_window1.add( self.treeview)

        table1 = gtk.Table( 2, 2, False)
        table1.set_border_width(5)
        table1.set_row_spacings( 5)
        self.dialog.vbox.pack_start( table1, False, True, 0)

        label1 = gtk.Label( 'Selected Recipe')
        label1.set_alignment( 1, 0.5)
        label1.set_padding( 10, 0)
        table1.attach( label1, 0, 1, 0, 1, gtk.FILL, 0, 0, 0)

        self.recipe_entry = gtk.Entry()
        self.recipe_entry.set_property( 'editable', False)
        self.recipe_entry.set_property( 'can-focus', False)
        self.recipe_entry.set_activates_default( True)
        table1.attach( self.recipe_entry, 1, 2, 0, 1, 
            gtk.EXPAND|gtk.FILL, 0, 0, 0)

        self.num_serv_label = gtk.Label( 'Number of Servings')
        self.num_serv_label.set_alignment( 1, 0.5)
        self.num_serv_label.set_padding( 10, 0)
        table1.attach( self.num_serv_label, 0, 1, 1, 2, gtk.FILL, 0, 0, 0)

        self.num_serv_entry = gtk.Entry()
        self.num_serv_entry.set_activates_default( True)
        table1.attach( self.num_serv_entry, 1, 2, 1, 2,
            gtk.EXPAND|gtk.FILL, 0, 0, 0)

