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

import gobject
import gtk

class PlanAddDlgUI:
    def __init__( self):
        self.dialog = gtk.Dialog( title='Nutrient Composition',
#            flags=gtk.DIALOG_MODAL,
            buttons=( gtk.STOCK_HELP, gtk.RESPONSE_HELP,
                gtk.STOCK_OK, gtk.RESPONSE_OK,
                gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))
        self.dialog.set_default_response( gtk.RESPONSE_OK)

        self.notebook = gtk.Notebook()
        self.notebook.set_border_width( 5)
        self.dialog.vbox.pack_start( self.notebook, True, True, 0)

        self.recipe_box = gtk.VBox( False, 0)
        self.notebook.append_page( self.recipe_box, gtk.Label( 'Recipe Search'))

        self.fd_txt_box = gtk.VBox( False, 0)
        self.notebook.append_page( self.fd_txt_box, gtk.Label( 'Food Search by Text'))

        self.fd_nutr_box = gtk.VBox( True, 0)
        self.notebook.append_page( self.fd_nutr_box, gtk.Label( 'Food Search by Nutrient'))
