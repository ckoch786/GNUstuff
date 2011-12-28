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
import recipe_srch_dlg_ui
import gnutr_consts
import gnutr
import store
import help

class RecipeSrchDlg:
    def __init__( self, app):
        self.ui = recipe_srch_dlg_ui.RecipeSrchDlgUI()
        self.app = app
        self.store = store.Store()

        self.ui.dialog.connect( 'response', self.on_response)
        self.ui.category_combo.set_rows( self.store.cat_desc_tuple, 0)

    def show( self):
        self.ui.dialog.vbox.show_all()
        self.ui.dialog.run()

    def on_response( self, w, r, d=None):
        if r == gtk.RESPONSE_HELP:
            help.open( '')
        elif r == gtk.RESPONSE_OK:
            result_list = self.get_search_match()
            if not result_list:
                gnutr.Dialog( 'warn', 'No recipe found.')
                return

            if not hasattr( self, 'recipe_srch_res_dlg'):
                import recipe_srch_res_dlg
                self.recipe_srch_res_dlg = \
                    recipe_srch_res_dlg.RecipeSrchResDlg( self.app)
                self.recipe_srch_res_dlg.ui.dialog.connect( 'hide', 
                    self.on_hide)
            self.recipe_srch_res_dlg.show( result_list, gnutr_consts.RECIPE)
        elif r == gtk.RESPONSE_CANCEL or r == gtk.RESPONSE_DELETE_EVENT:
            self.ui.dialog.hide()

    def on_hide( self, w, d=None):
        self.ui.dialog.hide()

    def get_search_match( self):
        if not hasattr( self, 'db'):
            import database
            self.db = database.Database()

        cat_desc = self.ui.category_combo.get_active_text()
        assert cat_desc, 'category description is empty'
        srch_text = self.ui.reg_expr_entry.get_text()
        if not srch_text:
            return None;

        if cat_desc == 'All':
            self.db.query( "SELECT recipe_no, recipe_name " +
                "FROM recipe WHERE recipe_name REGEXP '%s'" %(srch_text))
            result_list = self.db.get_result()
        else:
            dict = self.store.cat_desc2num
            cat_num = dict[cat_desc]
            self.db.query( ("SELECT recipe_no, recipe_name " +
                "FROM recipe WHERE category_no = '%d' " +
                "AND recipe_name REGEXP '%s'") %( cat_num, srch_text))
            result_list = self.db.get_result()
        return result_list
