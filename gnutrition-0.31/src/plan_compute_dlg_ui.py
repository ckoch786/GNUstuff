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

import date_widget

class PlanComputeDlgUI:
    def __init__( self):
        self.dialog = gtk.Dialog( title='Nutrient Goal',
#            flags=gtk.DIALOG_MODAL, 
            buttons=( gtk.STOCK_HELP, gtk.RESPONSE_HELP,
            'Compute', 1, gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))

        table1 = gtk.Table( 6, 2, False)
        table1.set_row_spacings( 5)
        table1.set_col_spacings( 5)
        table1.set_border_width( 5)
        self.dialog.vbox.pack_start( table1, True, True, 0)

        label1 = gtk.Label( 'Specify the inclusive dates between which\nthe nutrient totals are to be computed')
        table1.attach( label1, 0, 2, 0, 1, gtk.FILL, 0, 0, 0)

        label2 = gtk.Label( '')
        label2.set_text_with_mnemonic( '_Start date')
        label2.set_alignment( 1.0, 0.5)
        table1.attach( label2, 0, 1, 1, 2, gtk.FILL, 0, 0, 0)

        label3 = gtk.Label( '')
        label3.set_text_with_mnemonic( '_End date')
        label3.set_alignment( 1.0, 0.5)
        table1.attach( label3, 0, 1, 2, 3, gtk.FILL, 0, 0, 0)

        self.start_date = date_widget.MyDateEntry()
        label2.set_mnemonic_widget( self.start_date)
        table1.attach( self.start_date, 1, 2, 1, 2, 
            gtk.FILL | gtk.EXPAND, 0, 0, 0)

        self.end_date = date_widget.MyDateEntry()
        label3.set_mnemonic_widget( self.end_date)
        table1.attach( self.end_date, 1, 2, 2, 3, 
            gtk.FILL | gtk.EXPAND, 0, 0, 0)

        vsep = gtk.VSeparator()
        table1.attach( vsep, 0, 2, 3, 4,  gtk.FILL | gtk.EXPAND, 0, 0, 0)

        self.avg_rad_button = gtk.RadioButton( None, 
            'Compute _daily average nutrient composition')
        table1.attach( self.avg_rad_button, 0, 2, 4, 5,  
            gtk.FILL | gtk.EXPAND, 0, 0, 0)

        self.tot_rad_button = gtk.RadioButton( self.avg_rad_button, 
            'Compute _total nutrient composition')
        table1.attach( self.tot_rad_button, 0, 2, 5, 6,  
            gtk.FILL | gtk.EXPAND, 0, 0, 0)
