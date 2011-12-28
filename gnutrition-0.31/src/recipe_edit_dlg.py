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

import gtk
import recipe_edit_dlg_ui
import gnutr
import help

class RecipeEditDlg:
    def __init__( self, app):
        self.ui = recipe_edit_dlg_ui.RecipeEditDlgUI()
        self.app = app

        self.ui.dialog.connect( 'response', self.on_response)

    def show( self, recipe):
        self.recipe = recipe
        self.ui.dialog.vbox.show_all()
        self.ui.recipe_entry.set_text( recipe.desc)
        self.ui.num_serv_entry.set_text( str( recipe.num_portions))
        self.ui.dialog.run()

    def on_response( self, w, r, d=None):
        if r == gtk.RESPONSE_HELP:
            help.open( '')
        elif r == gtk.RESPONSE_OK:
            try:
                self.recipe.num_portions = \
                    float( self.ui.num_serv_entry.get_text())
            except ValueError:
                gnutr.Dialog( 'error', 
                    'The number of portions must be a number.')
            self.app.base_win.plan.replace_recipe( self.recipe)
            self.ui.dialog.hide()
        elif r == gtk.RESPONSE_CANCEL or r == gtk.RESPONSE_DELETE_EVENT:
            self.ui.dialog.hide()
