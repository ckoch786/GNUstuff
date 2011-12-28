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

nutr_data_list = [
    # macro-nutrients
    [203, 'Protein (g)', 0, 0, 1, 1, 2], 
    [204, 'Total Fat (g)', 0, 0, 1, 2, 3], 
    [205, 'Carbohydrates (g)', 0, 0, 1, 3, 4],
    [601, 'Cholesterol (mg)', 0, 0, 1, 4, 5], 
    [208, 'Calories (kcal)', 0, 0, 1, 5, 6],
    [606, 'Saturated Fat (g)', 0, 2, 3, 1, 2],
    [645, 'Mono-Unsaturated Fat (g)', 0, 2, 3, 2, 3 ], 
    [646, 'Poly-Unsaturated Fat (g)', 0, 2, 3, 3, 4], 
    [291, 'Fiber (g)', 0, 2, 3, 4, 5], 
    [268, 'Energy (kJ)', 0, 2, 3, 5, 6], 
    # micro-nutrients
#    [392, 'A( IU)', 1, 0, 1, 1, 2], 
    [318, 'A (mg RE)', 1, 0, 1, 1, 2], 
    [394, 'E (mg ATE)', 1, 0, 1, 2, 3], 
    [401, 'C (mg)', 1, 0, 1, 3, 4],
    [404, 'Thiamin (mg)', 1, 0, 1, 4, 5], 
    [405, 'Riboflavin (mg)', 1, 0, 1, 5, 6],
    [406, 'Niacin (mg)', 1, 0, 1, 6, 7],
    [410, 'Panto. Acid (mg)', 1, 0, 1, 7, 8],
    [415, 'B6 (mg)', 1, 0, 1, 8, 9], 
    [417, 'Folate (mcg)', 1, 0, 1, 9, 10],
    [418, 'B12 (mcg)', 1, 0, 1, 10, 11], 
    [301, 'Calcium (mg)', 1, 2, 3, 1, 2],
    [303, 'Iron (mg)', 1, 2, 3, 2, 3],
    [304, 'Magnesium (mg)', 1, 2, 3, 3, 4],
    [305, 'Phosphorus (mg)', 1, 2, 3, 4, 5],
    [306, 'Potassium (mg)', 1, 2, 3, 5, 6],
    [307, 'Sodium (mg)', 1, 2, 3, 6 , 7], 
    [309, 'Zinc (mg)', 1, 2, 3, 7, 8],
    [312, 'Copper (mg)', 1, 2, 3, 8, 9],
    [315, 'Maganese (mg)', 1, 2, 3, 9, 10],
    [317, 'Selenium (mcg)', 1, 2, 3, 10, 11],
    # proteins
    [501, 'Tryptophan (g)', 2, 0, 1, 1, 2], 
    [502, 'Threonine (g)', 2, 0, 1, 2, 3],
    [503, 'Isoleucine (g)', 2, 0, 1, 3, 4],
    [504, 'Leucine (g)', 2, 0, 1, 4, 5], 
    [505, 'Lysine (g)', 2, 0, 1, 5, 6],
    [505, 'Methionine (g)', 2, 0, 1, 6, 7],
    [506, 'Cysteine (g)', 2, 0, 1, 7, 8],
    [507, 'Phenylalanine (g)', 2, 0, 1, 8, 9],
    [508, 'Tyrosine (g)', 2, 0, 1, 9, 10],
    [510, 'Valine (g)', 2, 2, 3, 1, 2],
    [511, 'Arginine (g)', 2, 2, 3, 2, 3],
    [512, 'Histidine (g)', 2, 2, 3, 3, 4], 
    [513, 'Alanine (g)', 2, 2, 3, 4, 5], 
    [514, 'Aspartic Acid (g)', 2, 2, 3, 5, 6], 
    [515, 'Glutamic Acid (g)', 2, 2, 3, 6, 7],
    [516, 'Glycine (g)', 2, 2, 3, 7, 8], 
    [517, 'Proline (g)', 2, 2, 3, 8, 9],
    [518, 'Serine (g)', 2, 2, 3, 9, 10],
    # fats
    [607, '4:0 (g)', 3, 0, 1, 1, 2],  
    [608, '6:0 (g)', 3, 0, 1, 2, 3],
    [609, '8:0 (g)', 3, 0, 1, 3, 4],
    [610, '10:0 (g)', 3, 0, 1, 4, 5],
    [611, '12:0 (g)', 3, 0, 1, 5, 6],
    [612, '14:0 (g)', 3, 0, 1, 6, 7],
    [613, '16:0 (g)', 3, 0, 1, 7, 8],
    [614, '18:0 (g)', 3, 0, 1, 8, 9],
    [615, '20:0 (g)', 3, 0, 1, 9, 10],
    [617, '18:1 (g)', 3, 0, 1, 10, 11],
    [618, '18:2 (g)', 3, 0, 1, 11, 12],
    [619, '18:3 (g)', 3, 0, 1, 12, 13],
    [620, '20:4 (g)', 3, 0, 1, 13, 14],
    [621, '22:6 (g)', 3, 2, 3, 1, 2], 
    [624, '22:0 (g)', 3, 2, 3, 2, 3],
    [625, '14:1 (g)', 3, 2, 3, 3, 4],
    [626, '16:1 (g)', 3, 2, 3, 4, 5],
    [627, '18:4 (g)', 3, 2, 3, 5, 6],
    [628, '20:1 (g)', 3, 2, 3, 6, 7],
    [629, '20:5 (g)', 3, 2, 3, 7, 8],
    [630, '22:1 (g)', 3, 2, 3, 8, 9],
    [631, '22:5 (g)', 3, 2, 3, 9, 10],
    [652, '15:0 (g)', 3, 2, 3, 10, 11],
    [653, '17:0 (g)', 3, 2, 3, 11, 12],
    [654, '24:0 (g)', 3, 2, 3, 12, 13],
    # miscelaneous
    [207, 'Ash (g)', 4, 0, 1, 1, 2],
    [221, 'Alcohol (g)', 4, 0, 1, 2, 3],
    [255, 'Water (g)', 4, 0, 1, 3, 4], 
    [636, 'Phytosterols (mg)', 4, 0, 1, 4, 5],
    [263, 'Theobromine (mg)', 4, 2, 3, 1, 2],
    [262, 'Caffeine (mg)', 4, 2, 3, 2, 3],
    [269, 'Sugars, total (g)', 4, 2, 3, 3, 4]
]

class Nutrient:
    pass

class NutrientGoalDlgUI:
    def __init__( self):
        self.dialog = gtk.Dialog( title='Nutrient Goal',
            flags=gtk.DIALOG_MODAL,
            buttons=( gtk.STOCK_HELP, gtk.RESPONSE_HELP, 
            'gtk-save', 1,
            gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))
        self.dialog.set_resizable( False)

        hbox1 = gtk.HBox( False, 0)
        self.dialog.vbox.pack_start( hbox1, True, True, 0)

        notebook1 = gtk.Notebook()
        notebook1.set_border_width( 5)
        hbox1.pack_start( notebook1, True, True, 0)

        self.table_list = []
        self.table_list.append( gtk.Table( 4, 6, False))
        self.table_list.append( gtk.Table( 4, 11, False))
        self.table_list.append( gtk.Table( 4, 10, False))
        self.table_list.append( gtk.Table( 4, 14, False))
        self.table_list.append( gtk.Table( 4, 5, False))
        
        for i in range( 5):
            self.table_list[i].set_border_width( 5)
            self.table_list[i].set_row_spacings( 5)
            self.table_list[i].set_col_spacings( 5)
            self.table_list[i].attach( gtk.Label( 'Daily Goal'), 1, 2, 0, 1,
                gtk.FILL | gtk.EXPAND, 0, 0, 0)
            self.table_list[i].attach( gtk.Label( 'Daily Goal'), 3, 4, 0, 1,
                gtk.FILL | gtk.EXPAND, 0, 0, 0)
            notebook1.add( self.table_list[i])

        label_list = []
        label0 = gtk.Label( '')
        label0.set_text_with_mnemonic('M_acro-Nutrients')
        label_list.append( label0)
        label1 = gtk.Label( '')
        label1.set_text_with_mnemonic('M_icro-Nutrients')
        label_list.append( label1)
        label2 = gtk.Label( '')
        label2.set_text_with_mnemonic('Ami_no Acids')
        label_list.append( label2)
        label3 = gtk.Label( '')
        label3.set_text_with_mnemonic('Fa_ts')
        label_list.append( label3)
        label4 = gtk.Label( '')
        label4.set_text_with_mnemonic('Misce_llaneous')
        label_list.append( label4)

        for i in range( 5):
            notebook1.set_tab_label( notebook1.get_nth_page( i), label_list[i])

        self.nutr_list = []
        for num, label_text, table_num, l, r, t, b in nutr_data_list:
            nutr = Nutrient()
            nutr.num = num
            nutr.table_num = table_num
            nutr.left = l
            nutr.right = r
            nutr.top = t
            nutr.bottom = b
            nutr.label = gtk.Label( label_text)
            nutr.label.set_alignment( 1.0, 0.5)
            nutr.entry = gtk.Entry()
            self.nutr_list.append( nutr)

        for nutr in self.nutr_list:
            self.table_list[ nutr.table_num].attach( nutr.label,
                nutr.left, nutr.right, nutr.top, nutr.bottom,
                gtk.FILL, 0, 0, 0)
            self.table_list[ nutr.table_num].attach( nutr.entry,
                nutr.left+1, nutr.right+1, nutr.top, nutr.bottom,
                gtk.FILL | gtk.EXPAND, 0, 0, 0)
