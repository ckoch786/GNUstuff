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

import food_win_ui
import gnutr
import gnutr_consts
import store
import nutr_composition_dlg
import help

class FoodWin:
    def __init__( self, app, parent):
        self.ui = food_win_ui.FoodWinUI()
        self.app = app
        self.parent = parent

        self.nutr_comp_dlg = nutr_composition_dlg.NutrCompositionDlg()
        self.ui.hbox = self.nutr_comp_dlg.ui.hbox
        self.ui.hbox.reparent( self.ui.notebook_container)
        self.ui.notebook_container.show_all()
        self.store = store.Store()

        self.connect_signals()

    def connect_signals( self):
        self.ui.exit_item.connect( 'activate', lambda w: gtk.main_quit())
        self.ui.clear_item.connect( 'activate', self.on_clear_released)
        self.ui.plan_view_item.connect( 'activate', self.on_plan_activate)
        self.ui.recipe_view_item.connect( 'activate', self.on_recipe_activate)
        self.ui.nutr_goal_item.connect( 'activate', self.on_goals_released)
        self.ui.manual_item.connect( 'activate', self.on_manual_activate)
        self.ui.about_item.connect( 'activate', self.on_about_activate)

        self.ui.select_button.connect( 'clicked', self.on_select_released)
        self.ui.clear_button.connect( 'clicked', self.on_clear_released)
        self.ui.compute_button.connect( 'clicked', self.on_compute_released)
        self.ui.pref_button.connect( 'clicked', self.on_goals_released)

        self.ui.food_entry.connect( 'changed', self.on_food_entry_changed)

    def on_food_entry_changed( self, w, d=None):
        self.nutr_comp_dlg.reset()

    def on_plan_activate( self, w, d=None):
        self.app.base_win.on_plan_button_released( None)

    def on_manual_activate( self, w, d=None):
        help.open( '')
        
    def on_recipe_activate( self, w, d=None):
        self.app.base_win.on_recipe_button_released( None)
        
    def on_about_activate( self, w, d=None):
        r = self.app.base_win.ui.about_dlg.run()
        if r == gtk.RESPONSE_CANCEL or r == gtk.RESPONSE_DELETE_EVENT:
            self.app.base_win.ui.about_dlg.hide()

    def on_select_released( self, w, d=None):
        if not hasattr( self, 'food_srch_dlg'):
            import food_srch_dlg
            self.food_srch_dlg = food_srch_dlg.FoodSrchDlg( self.app)
        self.food_srch_dlg.show( gnutr_consts.FOOD)

    def on_clear_released( self, w, d=None):
        self.ui.food_entry.set_text( '')
        self.ui.msre_combo.clear_rows()
        self.ui.amount_entry.set_text( '')
        self.nutr_comp_dlg.reset()

    def on_compute_released( self, w, d=None):
        fd_desc = self.ui.food_entry.get_text()
        if not fd_desc: 
            return
        fd_num = self.store.fd_desc2num[fd_desc]
        msre_desc = self.ui.msre_combo.get_active_text()
        msre_num = self.store.msre_desc2num[msre_desc]
        try:
            amount = float( self.ui.amount_entry.get_text())
        except ValueError:
            gnutr.Dialog( 'error', 'The amount must be a number.', self.parent)
        self.nutr_comp_dlg.compute_food( amount, msre_num, fd_num)

    def on_goals_released( self, w, d=None):
        if not hasattr( self, 'nutr_goal_dlg'):
            import nutr_goal_dlg
            self.nutr_goal_dlg = nutr_goal_dlg.NutrGoalDlg()
        self.nutr_goal_dlg.show()

    def update( self, ingr):
        msre_model = self.store.get_msre_desc_tuples( ingr.food_num)
        self.ui.msre_combo.set_rows( msre_model)
        self.ui.msre_combo.set_active(0)
        self.ui.food_entry.set_text( ingr.food_desc)
        self.ui.amount_entry.set_text( '1.00')
