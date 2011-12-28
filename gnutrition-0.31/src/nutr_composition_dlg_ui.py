# gnutrition - a nutrition and diet analysis program.
# Copyright( C) 2000-2002 Edgar Denny (edenny@skyweb.net)
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

import nutr_goal_dlg_ui

class Nutrient:
    pass

class NutrCompositionDlgUI:
    def __init__( self):
        self.dialog = gtk.Dialog( title='Nutrient Composition',
            flags=gtk.DIALOG_MODAL,
            buttons=( gtk.STOCK_HELP, gtk.RESPONSE_HELP, 
            gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))
        self.dialog.set_resizable( False)

        self.hbox = gtk.HBox( False, 0)
        self.dialog.vbox.pack_start( self.hbox, True, True, 0)

        notebook1 = gtk.Notebook()
        notebook1.set_border_width( 5)
        self.hbox.pack_start( notebook1, True, True, 0)

        self.table_list = []
        self.table_list.append( gtk.Table( 6, 7, False))
        self.table_list.append( gtk.Table( 6, 11, False))
        self.table_list.append( gtk.Table( 6, 10, False))
        self.table_list.append( gtk.Table( 6, 14, False))
        self.table_list.append( gtk.Table( 6, 5, False))
        
        for i in range( 5):
            self.table_list[i].set_border_width( 5)
            self.table_list[i].set_row_spacings( 5)
            self.table_list[i].set_col_spacings( 5)
            self.table_list[i].attach( gtk.Label( 'Amount'), 1, 2, 0, 1,
                gtk.FILL | gtk.EXPAND, 0, 0, 0)
            self.table_list[i].attach( gtk.Label( '% Daily Goal'), 2, 3, 0, 1,
                gtk.FILL | gtk.EXPAND, 0, 0, 0)
            self.table_list[i].attach( gtk.Label( 'Amount'), 4, 5, 0, 1,
                gtk.FILL | gtk.EXPAND, 0, 0, 0)
            self.table_list[i].attach( gtk.Label( '% Daily Goal'), 5, 6, 0, 1,
                gtk.FILL | gtk.EXPAND, 0, 0, 0)
            notebook1.add( self.table_list[i])

        label_list = []
        label0 = gtk.Label( 'Macro-Nutrients')
        label_list.append( label0)
        label1 = gtk.Label( 'Micro-Nutrients')
        label_list.append( label1)
        label2 = gtk.Label( 'Amino Acids')
        label_list.append( label2)
        label3 = gtk.Label( 'Fats')
        label_list.append( label3)
        label4 = gtk.Label( 'Miscellaneous')
        label_list.append( label4)

        for i in range( 5):
            notebook1.set_tab_label( notebook1.get_nth_page( i), label_list[i])

        self.nutr_list = []
        for data in nutr_goal_dlg_ui.nutr_data_list:
            (num, label_text, table_num, l, r, t, b) = data
            nutr = Nutrient()
            nutr.num = num
            nutr.table_num = table_num
            if l == 2:
                l = l + 1
                r = r + 1
            nutr.left = l
            nutr.right = r
            nutr.top = t
            nutr.bottom = b
            nutr.label = gtk.Label( label_text)
            nutr.label.set_alignment( 1.0, 0.5)
            nutr.entry_amount = gtk.Entry()
            nutr.entry_amount.set_property( 'editable', False)
            nutr.entry_amount.set_size_request( 80, -1)
            nutr.entry_pcnt = gtk.Entry()
            nutr.entry_pcnt.set_property( 'editable', False)
            nutr.entry_pcnt.set_size_request( 80, -1)
            self.nutr_list.append( nutr)

        for nutr in self.nutr_list:
            self.table_list[ nutr.table_num].attach( nutr.label,
                nutr.left, nutr.right, nutr.top, nutr.bottom,
                gtk.FILL | gtk.EXPAND, 0, 0, 0)
            self.table_list[ nutr.table_num].attach( nutr.entry_amount,
                nutr.left+1, nutr.right+1, nutr.top, nutr.bottom,
                gtk.FILL, 0, 0, 0)
            self.table_list[ nutr.table_num].attach( nutr.entry_pcnt,
                nutr.left+2, nutr.right+2, nutr.top, nutr.bottom,
                gtk.FILL, 0, 0, 0)

        table1 = gtk.Table( 6, 2, True)
        table1.set_border_width( 5)
        table1.set_row_spacings( 5)
        table1.set_col_spacings( 5)
        self.table_list[0].attach( table1, 0, 6, 6, 7,
        gtk.FILL | gtk. EXPAND, 0, 0, 0)

        label1 = gtk.Label( 'Percentage of Calories from:')
        table1.attach( label1, 0, 6, 0, 1, gtk.FILL, 0, 0, 0)

        label2 = gtk.Label( 'Protein')
        label2.set_alignment( 1.0, 0.5)
        table1.attach( label2, 0, 1, 1, 2, gtk.FILL | gtk.EXPAND, 0, 0, 0)
        self.protein_entry = gtk.Entry()
        self.protein_entry.set_property( 'editable', False)
        self.protein_entry.set_size_request( 60, -1)
        table1.attach( self.protein_entry, 1, 2, 1, 2, 
            gtk.FILL, 0, 0, 0)

        label2 = gtk.Label( 'Fat')
        label2.set_alignment( 1.0, 0.5)
        table1.attach( label2, 2, 3, 1, 2, gtk.FILL | gtk.EXPAND, 0, 0, 0)
        self.fat_entry = gtk.Entry()
        self.fat_entry.set_property( 'editable', False)
        self.fat_entry.set_size_request( 60, -1)
        table1.attach( self.fat_entry, 3, 4, 1, 2, 
            gtk.FILL, 0, 0, 0)

        label2 = gtk.Label( 'Carbohydrate')
        label2.set_alignment( 1.0, 0.5)
        table1.attach( label2, 4, 5, 1, 2, gtk.FILL | gtk.EXPAND, 0, 0, 0)
        self.carb_entry = gtk.Entry()
        self.carb_entry.set_property( 'editable', False)
        self.carb_entry.set_size_request( 60, -1)
        table1.attach( self.carb_entry, 5, 6, 1, 2, 
            gtk.FILL, 0, 0, 0)
