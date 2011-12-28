#  gnutrition - a nutrition and diet analysis program.
#  Copyright( C) 2000 - 2002 Edgar Denny (edenny@skyweb.net)
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

import gtk
import plan_add_dlg_ui
import gnutr_consts
import food_srch_dlg
import recipe_srch_dlg
import help

class PlanAddDlg:
    def __init__( self, app):
        self.ui = plan_add_dlg_ui.PlanAddDlgUI()
        self.app = app

        self.food_srch_dlg = food_srch_dlg.FoodSrchDlg( self.app)
        self.recipe_srch_dlg = recipe_srch_dlg.RecipeSrchDlg( self.app)

        self.recipe_srch_dlg.ui.container.reparent( self.ui.recipe_box)
        self.ui.recipe_box.set_child_packing( 
            self.recipe_srch_dlg.ui.container, False, False,
            0, gtk.PACK_START)

        self.food_srch_dlg.ui.box_txt.reparent( self.ui.fd_txt_box)
        self.ui.fd_txt_box.set_child_packing( 
            self.food_srch_dlg.ui.box_txt, False, False,
            0, gtk.PACK_START)

        self.food_srch_dlg.ui.table_nutr.reparent( self.ui.fd_nutr_box)
        self.ui.fd_nutr_box.set_child_packing( 
            self.food_srch_dlg.ui.table_nutr, True, True,
            0, gtk.PACK_START)

        self.ui.dialog.connect( 'response', self.on_response)
        self.food_srch_dlg.ui.dialog.connect( 'hide', self.on_hide)

    def show( self):
        self.ui.dialog.vbox.show_all()
        self.ui.dialog.run()

    def on_hide( self, w, d=None):
        self.ui.dialog.hide()

    def on_response( self, w, r, d=None):
        if r == gtk.RESPONSE_HELP:
            help.open( '')

        elif r == gtk.RESPONSE_OK:
            if not hasattr( self, 'recipe_srch_res_dlg'):
                import recipe_srch_res_dlg
                self.recipe_srch_res_dlg = \
                    recipe_srch_res_dlg.RecipeSrchResDlg( self.app)
                self.recipe_srch_res_dlg.ui.dialog.connect( 'hide', 
                    self.on_hide)

            if not hasattr( self, 'food_srch_res_dlg'):
                import food_srch_res_dlg
                self.food_srch_res_dlg = \
                    food_srch_res_dlg.FoodSrchResDlg( self.app)
                self.food_srch_res_dlg.ui.dialog.connect( 'hide', 
                    self.on_hide)

            num = self.ui.notebook.get_current_page()
            if num == 0:# recipe
                srch_list = self.recipe_srch_dlg.get_search_match()
                if not srch_list: 
                    return
                self.recipe_srch_res_dlg.show( srch_list, gnutr_consts.PLAN)
            elif num == 1:  # food by text
                srch_list = self.food_srch_dlg.search_by_text()
                if not srch_list: 
                    return
                self.food_srch_res_dlg.show( srch_list, gnutr_consts.PLAN)
            else:   # food by nutrient
                srch_list = self.food_srch_dlg.search_by_text()
                if not srch_list: 
                    return
                self.food_srch_res_dlg.show( srch_list, gnutr_consts.PLAN)

        elif r == gtk.RESPONSE_CANCEL or r == gtk.RESPONSE_DELETE_EVENT:
            self.ui.dialog.hide()
