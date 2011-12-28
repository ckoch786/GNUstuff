#  Guntrition - a nutrition and diet analysis program.
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

import gtk
import gnutr_consts
import gnutr
import food_edit_dlg_ui
import store
import help

class FoodEditDlg:
    def __init__( self, app):
        self.ui = food_edit_dlg_ui.FoodEditDlgUI()
        self.ui.dialog.connect( 'response', self.on_response)
        self.app = app
        self.store = store.Store()

    def show( self, ingr, view):
        self.view = view
        self.ingr = ingr
        msre_tuple = self.store.get_msre_desc_tuples( ingr.food_num)
        self.ui.combo.set_rows( msre_tuple, 0)
        self.ui.food_entry.set_text( ingr.food_desc)
        self.ui.combo.set_active_text( ingr.msre_desc)
        self.ui.amount_entry.set_text( str( ingr.amount))
        self.ui.dialog.show_all()

    def on_response( self, w, response_id, d=None):
        if response_id == gtk.RESPONSE_HELP:
            help.open( '')
        if response_id == gtk.RESPONSE_OK:
            try:
                self.ingr.amount = float( self.ui.amount_entry.get_text())
            except ValueError:
                gnutr.Dialog( 'error', 'The amount must be a number.')
            self.ingr.msre_desc = self.ui.combo.get_active_text()
            self.ingr.msre_num = self.store.msre_desc2num[self.ingr.msre_desc]

            if self.view == gnutr_consts.RECIPE:
                self.app.base_win.recipe.replace_ingredient( self.ingr)
            else:
                self.app.base_win.plan.replace_food( self.ingr)
            self.ui.dialog.hide()

        if response_id == gtk.RESPONSE_CANCEL:
            self.ui.dialog.hide_all()
