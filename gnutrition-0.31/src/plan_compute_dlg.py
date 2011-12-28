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

import string
import gtk
import plan_compute_dlg_ui
import gnutr
import gnutr_consts
import database
import help

class PlanComputeDlg:
    def __init__( self, app):
        self.ui = plan_compute_dlg_ui.PlanComputeDlgUI()
        self.app = app
        self.db = database.Database()

        self.ui.dialog.connect( 'response', self.on_response)

    def show( self):
        self.ui.dialog.vbox.show_all()
        self.ui.dialog.show()

    def start_later_than_end( self, start, end):
        date_split1 = string.split( start, '-')
        date_split2 = string.split( end, '-')
        if int( date_split1[0]) > int( date_split2[0]):    # year
            return 1
        if int( date_split1[1]) > int( date_split2[1]):    # month
            return 1
        if int( date_split1[2]) > int( date_split2[2]):    # day
            return 1
        return 0

    def on_response( self, w, r, d=None):
        if r == gtk.RESPONSE_HELP:
            help.open( '')
            
        elif r == 1:
            start_date = self.ui.start_date.entry.get_text()
            end_date = self.ui.end_date.entry.get_text()
            if self.start_later_than_end( start_date, end_date):
                gnutr.Dialog( 'error', 'The start date is later\n' +
                    'than the end date.')
                return

            avg = self.ui.avg_rad_button.get_active()
            result = self.compute( start_date, end_date, avg)
            if not hasattr( self, 'nutr_composition_dlg'):
                import nutr_composition_dlg
                self.nutr_composition_dlg = \
                    nutr_composition_dlg.NutrCompositionDlg()
            self.nutr_composition_dlg.show( nutr_list=result)

        elif r == gtk.RESPONSE_CANCEL or r == gtk.RESPONSE_DELETE_EVENT:
            self.ui.dialog.hide()

    def compute( self, start_date, end_date, avg):
        tot_list = self.initialize_tot_list()

        # get recipes in plan within the dates
        self.db.query( "SELECT recipe_no, no_portions FROM " +
            "recipe_plan_temp WHERE date >='%s' AND date <='%s'" 
            %( start_date, end_date))
        result = self.db.get_result()

        for recipe_num, num_portions in result:
            self.add_recipe_to_total( tot_list, recipe_num, num_portions)

        # get foods in plan within the dates
        self.db.query( "SELECT amount, msre_no, fd_no FROM " +
            "food_plan_temp WHERE date >='%s' AND date <='%s'" 
            %( start_date, end_date))
        result = self.db.get_result()

        for amount, msre_num, fd_num in result:
            self.add_food_to_total( tot_list, amount, msre_num, fd_num)

        if avg:
            self.divide_total_by_no_days( tot_list, start_date, end_date)
        return tot_list

    def initialize_tot_list( self):
        if not hasattr( self, 'store'):
            import store
            self.store = store.Store()
        tot_list = []
        for nutr_no in self.store.nutr_num_list:
            tot_list.append( (nutr_no, 0.000))
        return tot_list

    def divide_total_by_no_days( self, tot_list, start_date, end_date):
        self.db.query( "SELECT TO_DAYS('%s')" %( start_date))
        days_start = self.db.get_single_result()
        self.db.query( "SELECT TO_DAYS('%s')" %( end_date))
        days_end = self.db.get_single_result()
        days_diff = float( days_end - days_start + 1L)
        for i in range( len( tot_list)):
            nutr_no, nutr_val = tot_list[i]
            avg = nutr_val / days_diff
            tot_list[i] = ( nutr_no, avg)

    def get_ingredients( self, recipe_num):
        self.db.query(  "SELECT amount, msre_no, fd_no FROM " +
            "ingredient WHERE recipe_no = '%d'" %( recipe_num))
        return self.db.get_result()

    def get_food_nutrients( self, food_num):
        self.db.query( "SELECT nutr_no, nutr_val FROM nut_data " +
            "WHERE fd_no = '%d'" %( food_num))
        return self.db.get_result()

    def get_gm_per_measure( self, food_num, msre_num):
        if int( msre_num) == 99999:
            return 1.0
        self.db.query( "SELECT wgt_val FROM weight WHERE " +
            "fd_no = '%d' AND msre_no = '%d'" %( food_num, msre_num))
        return float( self.db.get_single_result())

    def add_food_nutr_comp( self, tot_list, food_num, amount, gm_per_msre):
        fd_nutr_list = self.get_food_nutrients( food_num)
        for i in range( len( tot_list)):
            tot_nutr_num, tot_nutr_val = tot_list[i]
            for fd_nutr_num, fd_nutr_val in fd_nutr_list:
                if fd_nutr_num == tot_nutr_num:
                    total = tot_nutr_val
                    total = total + ( amount * gm_per_msre *
                        fd_nutr_val / 100.0)
                    tot_list[i] = (tot_nutr_num, total)
                    break

    def add_recipe_to_total( self, tot_list, recipe_num, num_portions):
        ingr_list = self.get_ingredients( recipe_num)
        self.db.query(  "SELECT no_serv FROM recipe WHERE " +
            "recipe_no = '%d'" %( recipe_num))
        num_serv = float( self.db.get_single_result())
        for amount, msre_num, fd_num in ingr_list:
            tot_amount = amount * num_portions / num_serv
            gm_per_msre = self.get_gm_per_measure( fd_num, msre_num)
            self.add_food_nutr_comp( tot_list, fd_num, tot_amount, gm_per_msre)

    def add_food_to_total( self, tot_list, amount, msre_no, fd_no):
        gm_per_msre = self.get_gm_per_measure( fd_no, msre_no)
        self.add_food_nutr_comp( tot_list, fd_no, amount, gm_per_msre)
