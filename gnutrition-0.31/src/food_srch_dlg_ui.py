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

import gobject
import gtk
import gnutr_widgets

class FoodSrchDlgUI:
    def __init__( self):
        self.dialog = gtk.Dialog( title='Food Search', flags=gtk.DIALOG_MODAL,
            buttons=( gtk.STOCK_HELP, gtk.RESPONSE_HELP,
                      gtk.STOCK_OK, gtk.RESPONSE_OK,
                      gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))
        self.dialog.set_default_response( gtk.RESPONSE_OK)

        self.notebook = gtk.Notebook()
        self.dialog.vbox.pack_start( self.notebook, True, True, 0)
        self.notebook.set_border_width( 5)

        self.container_txt = gtk.VBox( False, 0)
        self.notebook.append_page( self.container_txt, gtk.Label( 'Name Search'))

        self.box_txt = gtk.VBox( False, 5)
        self.container_txt.pack_start( self.box_txt, False, False, 0)
        self.box_txt.set_border_width( 5)

        hbox13 = gtk.HBox( True, 0)
        self.box_txt.pack_start( hbox13, True, True, 0)

        label37 = gtk.Label( '')
        label37.set_text_with_mnemonic( 'Food _group')
        hbox13.pack_start( label37, True, True, 5)
        label37.set_alignment( 1, 0.5)

        self.txt_fg_combo = gnutr_widgets.GnutrComboBox()
        label37.set_mnemonic_widget( self.txt_fg_combo)
        hbox13.pack_start( self.txt_fg_combo, True, True, 0)

        hbox14 = gtk.HBox( True, 0)
        self.box_txt.pack_start( hbox14, True, True, 0)
        hbox14.set_border_width( 5)

        label38 = gtk.Label( '')
        label38.set_text_with_mnemonic( '_Search for')
        hbox14.pack_start( label38, True, True, 5)
        label38.set_alignment( 1, 0.5)

        self.food_name_entry = gtk.Entry()
        label38.set_mnemonic_widget( self.food_name_entry)
        hbox14.pack_start( self.food_name_entry, True, True, 0)
        self.food_name_entry.set_activates_default(True)

        hbox15 = gtk.HBox( True, 0)
        self.box_txt.pack_start( hbox15, True, True, 0)
        hbox15.set_border_width( 5)

        hbox15.pack_start( gtk.Label( ''), True, True, 0)
        
        self.use_regex_check = gtk.CheckButton( 'Use _regular expressions')
        hbox15.pack_start( self.use_regex_check, True, True, 0)

        self.container_table = gtk.VBox( False, 0)
        self.notebook.append_page( self.container_table, gtk.Label( 'Nutritient Search'))

        self.table_nutr = gtk.Table( 7, 4, False)
        self.container_table.pack_start( self.table_nutr, True, True, 0)
        self.table_nutr.set_border_width( 5)
        self.table_nutr.set_row_spacings( 5)
        self.table_nutr.set_col_spacings( 5)

        label40 = gtk.Label( '')
        label40.set_text_with_mnemonic( 'Food _group')
        self.table_nutr.attach( label40, 0, 1, 0, 1, gtk.FILL, 0, 0, 0)
        label40.set_alignment( 1, 0.5)

        label41 = gtk.Label( '')
        label41.set_text_with_mnemonic( 'Nor_malize per')
        self.table_nutr.attach( label41, 0, 1, 1, 2, gtk.FILL, 0, 0, 0)
        label41.set_alignment( 0, 1)

        self.nutr_fg_combo = gnutr_widgets.GnutrComboBox()
        label40.set_mnemonic_widget( self.nutr_fg_combo)
        self.table_nutr.attach( self.nutr_fg_combo, 1, 4, 0, 1, 
            gtk.EXPAND|gtk.FILL, 0, 0, 0)

        label42 = gtk.Label( '')
        label42.set_markup( '<b>Nutrients to search for</b>')
        self.table_nutr.attach( label42, 0, 4, 3, 4, gtk.FILL, 0, 0, 0)
        label42.set_alignment( 0, 0.5)

        label43 = gtk.Label( '')
        label43.set_text_with_mnemonic( '_Nutrient')
        self.table_nutr.attach( label43, 0, 1, 4, 5, gtk.FILL, 0, 0, 0)
        label43.set_alignment( 1, 0.5)

        self.nutr_combo = gnutr_widgets.GnutrComboBox()
        label43.set_mnemonic_widget( self.nutr_combo)
        self.table_nutr.attach( self.nutr_combo, 1, 2, 4, 5, 
            gtk.EXPAND|gtk.FILL, 0, 0, 0)

        label45 = gtk.Label( '')
        label45.set_text_with_mnemonic( '_Constraint')
        self.table_nutr.attach( label45, 2, 3, 4, 5, 
            gtk.EXPAND|gtk.FILL, 0, 0, 0)
        label45.set_alignment( 1, 0.5)

        constraint_spin_adj = gtk.Adjustment( 1, -5, 5, 1, 1, 1)
        self.constraint_spin = gtk.SpinButton( constraint_spin_adj, 1, 0)
        label45.set_mnemonic_widget( self.constraint_spin)
        self.table_nutr.attach( self.constraint_spin, 3, 4, 4, 5, 
            gtk.FILL, 0, 0, 0)
        self.constraint_spin.set_activates_default( True)

        label44 = gtk.Label( '')
        label44.set_text_with_mnemonic( 'Number of _foods')
        self.table_nutr.attach( label44, 2, 3, 1, 2, 
            gtk.EXPAND|gtk.FILL, 0, 0, 0)
        label44.set_alignment( 1, 0.5)

        table2 = gtk.Table( 3, 1, False)
        self.table_nutr.attach( table2, 3, 4, 6, 7, 
            gtk.FILL, gtk.EXPAND|gtk.FILL, 0, 0)
        table2.set_row_spacings( 5)

        self.delete_button = gtk.Button( label='_Delete')
        table2.attach( self.delete_button, 0, 1, 1, 2, gtk.FILL, 0, 0, 0)

        self.add_button = gtk.Button( label='_Add')
        table2.attach( self.add_button, 0, 1, 0, 1, 
            gtk.EXPAND | gtk.FILL, 0, 0, 0)

        self.num_foods_entry = gtk.Entry()
        label44.set_mnemonic_widget( self.num_foods_entry)
        self.table_nutr.attach( self.num_foods_entry, 3, 4, 1, 2, 
            gtk.FILL, 0, 0, 0)
        self.num_foods_entry.set_size_request( 80, -1)
        self.num_foods_entry.set_activates_default( True)

        scrolledwindow1 = gtk.ScrolledWindow()
        scrolledwindow1.set_size_request( -1, 120)
        self.table_nutr.attach( scrolledwindow1, 0, 3, 6, 7,
            gtk.EXPAND | gtk.FILL, gtk.EXPAND | gtk.FILL, 0, 0)

        self.treemodel = gtk.ListStore( gobject.TYPE_STRING,
            gobject.TYPE_INT)
        self.treeview = gtk.TreeView( self.treemodel)
        self.treeview.set_rules_hint( True)

        self.selection = self.treeview.get_selection()
        self.selection.set_mode( gtk.SELECTION_SINGLE)

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn( 'Nutrient', renderer, text=0)
        self.treeview.append_column( column)
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn( 'Constraint', renderer, text=1)
        self.treeview.append_column( column)
        scrolledwindow1.add( self.treeview)

        self.norm_combo = gnutr_widgets.GnutrComboBox((( 'calorie',), ( 'gram',)), 0)
        label41.set_mnemonic_widget( self.norm_combo)
        self.table_nutr.attach( self.norm_combo, 1, 2, 1, 2, 
            gtk.FILL, 0, 0, 0)

