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

import gtk
import food_srch_dlg_ui
import gnutr
import store
import database
import help

# I can pass a class here nad check if it is plan, food, or recipe
class FoodSrchDlg:
    def __init__( self, app):
        self.ui = food_srch_dlg_ui.FoodSrchDlgUI()
        self.connect_signals()
        self.store = store.Store()
        self.db = database.Database()
        self.app = app

        self.ui.txt_fg_combo.set_rows( self.store.fg_desc_tuple, 0)
        self.ui.nutr_fg_combo.set_rows( self.store.fg_desc_tuple, 0)
        self.ui.nutr_combo.set_rows( self.store.nutr_desc_tuples, 0)

    def show( self, view):
        self.ui.food_name_entry.set_text( '')
        self.ui.num_foods_entry.set_text( '40')
        self.ui.constraint_spin.set_value( 1)

        self.view = view
        self.ui.dialog.vbox.show_all()
        self.ui.dialog.run()

    def connect_signals( self):
        self.ui.dialog.connect( 'response', self.on_response)
        self.ui.add_button.connect( 'clicked', self.on_add_released)
        self.ui.delete_button.connect( 'clicked', self.on_delete_released)
        self.ui.treeview.connect( 'key-press-event', self.on_treeview_key_press_event)
        self.ui.treeview.connect( 'button-press-event', self.on_treeview_button_press_event)

    def on_hide( self, w, d=None):
        self.ui.dialog.hide()

    def on_response( self, w, resp, d=None):
        if not hasattr( self, 'food_srch_res_dlg'):
            import food_srch_res_dlg
            self.food_srch_res_dlg = \
            food_srch_res_dlg.FoodSrchResDlg( self.app)
            self.food_srch_res_dlg.ui.dialog.connect( 'hide', self.on_hide)

        if resp == gtk.RESPONSE_HELP:
            help.open( '')
            
        elif resp == gtk.RESPONSE_OK:
            page = self.ui.notebook.get_current_page()
            if page == 0:
                match_list = self.search_by_text()
                if not match_list:
                    gnutr.Dialog( 'warn', 'No matching foods.')
                    return
            else:
                match_list = self.search_by_nutrient()
                if not match_list:
                    gnutr.Dialog( 'warn', 'No matching foods.')
                    return
            self.food_srch_res_dlg.show( match_list, self.view)

        elif resp == gtk.RESPONSE_CANCEL or resp == gtk.RESPONSE_DELETE_EVENT:
            if hasattr( self, 'food_srch_res_dlg'):
                self.food_srch_res_dlg.ui.dialog.hide()
            self.ui.dialog.hide()

    def on_add_released( self, w, d=None):
        nutr_desc = self.ui.nutr_combo.get_active_text()
        constr_val = self.ui.constraint_spin.get_value()

        if self.in_store( nutr_desc):
            gnutr.Dialog( 'warn', 'The nutrient is already in the list.')
            return

        iter = self.ui.treemodel.append()
        self.ui.treemodel.set_value( iter, 0, nutr_desc)
        self.ui.treemodel.set_value( iter, 1, constr_val)

    def on_delete_released( self, w, d=None):
        modell, iter = self.ui.selection.get_selected()
        if not iter:
            gnutr.Dialog( 'warn', 'No nutrient is selected.')
        else:
            self.ui.treemodel.remove( iter)

    def search_by_text( self):
        txt = self.ui.food_name_entry.get_text()
        if not txt:
            return None
        fg_desc = self.ui.txt_fg_combo.get_active_text()

        if self.ui.use_regex_check.get_active():
            where = "fd_desc REGEXP '%s'" % ( txt)
        else:
            where = "fd_desc LIKE '%%%s%%'" % ( txt)
            
        if fg_desc == 'All Foods':
            self.db.query( "SELECT fd_no FROM food_des " +
                "WHERE %s" % ( where))
        else:
            fg_num = self.store.fg_desc2num[ fg_desc]
            self.db.query("SELECT fd_no FROM food_des " +
                "WHERE fd_gp = '%s' AND %s"
                % ( str( fg_num), where))
        result = self.db.get_result()

        food_num_list = []
        for num in result:
            food_num_list.append( num[0])
        return food_num_list

    def search_by_nutrient( self):
        if self.ui.treemodel.iter_n_children( None) == 0:
            return None

        fg_desc = self.ui.nutr_fg_combo.get_active_text()
        norm_by = self.ui.norm_combo.get_active()
        num = self.ui.num_foods_entry.get_text()
        try:
            num_foods = int( num)
        except ValueError:
            gnutr.Dialog( 'warn', 'The number of foods to list is not\n' +
                'specified or is not a number.')
            return None

        constr_list = []
        iter = self.ui.treemodel.get_iter_root()
        ret = True
        while ret:
            nutr_desc = self.ui.treemodel.get_value( iter, 0)
            constr_val = self.ui.treemodel.get_value( iter, 1)
            constr_list.append( ( nutr_desc, constr_val))
            ret = self.ui.treemodel.iter_next( iter)

        result_list = self.search_by_nutr_constr( fg_desc, norm_by, num_foods,
            constr_list)
        return result_list

    def in_store( self, txt1):
        if self.ui.treemodel.iter_n_children( None) == 0:
            return 0
        iter = self.ui.treemodel.get_iter_root()
        ret = True
        while ret:
            txt2 = self.ui.treemodel.get_value( iter, 0)
            if txt1 == txt2:
                return 1
            ret = self.ui.treemodel.iter_next( iter)
        return 0
            
    def search_by_nutr_constr( self, fg_desc, norm_by, num_foods, constr_list):
        nutr_tot_list = []
        dict = self.store.nutr_desc2num
        query =  "( "
        for nutr_desc, constraint in constr_list:
            nutr_num = dict[nutr_desc]
            nutr_tot_list.append( (nutr_num, '0.0', constraint))
            query = query + " nutr_no = '%s' OR" % ( str( nutr_num))
        query = query + " nutr_no = '208' )"

        dict = self.store.fg_desc2num
        if fg_desc == 'All Foods':
            query = ( "SELECT fd_no, nutr_no, nutr_val FROM nut_data " +
                "WHERE " + query)
        else: 
            fg_num = self.store.fg_desc2num[fg_desc]
            query = ( "SELECT nut_data.fd_no, nutr_no, nutr_val FROM " +
                "nut_data, food_des WHERE " +
                "food_des.fd_gp = '" + str( fg_num) + "' AND " +
                "nut_data.fd_no = food_des.fd_no AND " + query)
        self.db.query( query)
        result = self.db.get_result()

        # compute the average nutrient value for each of the nutrients that
        # are a constraints. Will be used to normalize values.
        num_tot_foods = 0
        fd_num_prev = 0
        temp_list = []
        for fd_num, nutr_num, nutr_val in result:
            if len( temp_list) != 0 and fd_num != fd_num_prev:
                self.incr_nutr_values( temp_list, nutr_tot_list, norm_by)
                temp_list[:] = []
                num_tot_foods = num_tot_foods + 1
            temp_list.append( (fd_num, nutr_num, nutr_val))
            fd_num_prev = fd_num
        for i in range( len( nutr_tot_list)):
            nutr_num, nutr_val_tot, constraint = nutr_tot_list[i]
            total = float( nutr_num)/float( num_tot_foods)
            nutr_tot_list[i] = ( nutr_num, str( total), constraint)

        # compute the food score on the basis of the nutrient constraints
        score_list = []
        fd_num_prev = ''
        temp_list = []
        for fd_num, nutr_num, nutr_val in result:
            if len( temp_list) != 0 and fd_num != fd_num_prev:
                fd_score = self.calc_score( temp_list, nutr_tot_list, norm_by)
                temp_list[:] = []
                self.add_to_score_list( score_list, fd_num, fd_score, num_foods)
            temp_list.append( (fd_num, nutr_num, nutr_val))
            fd_num_prev = fd_num

        # return a list just of fd_num
        ret_list = []
        for fd_num, fd_score in score_list:
            ret_list.append( fd_num)
        return ret_list

    def calc_score( self, fd_list, avg_nutr_list, norm_by):
        energy_val = 0.0
        for fd_num, nutr_num, nutr_val in fd_list:
            if nutr_num == 208:
                energy_val = nutr_val

        # ignore those foods whose energy in kcals is undefined
        if energy_val == 0.0:
            return 0.0

        food_score = 0.0
        for fd_num, nutr_num, nutr_val in fd_list:
            for avg_nutr_num, avg_nutr_val, constraint in avg_nutr_list:
                if nutr_num == avg_nutr_num:
                    if norm_by == 0:    # score per calories
                        value = float( nutr_val)/ float( energy_val)
                    else:               # score per weight
                        value = float( nutr_val)

                    # normalize w.r.t the average nutrient value
                    food_score = food_score + ( float( constraint) *
                        value / float( avg_nutr_val))
                    break
        return food_score

    def add_to_score_list( self, score_list, fd_num, fd_score, num_foods):
        length = len( score_list)
        if length < num_foods:
            score_list.append( (fd_num, fd_score))
        else:
            score_lowest = score_list[0]
            j = 0
            for i in range( length):
                num, score = score_list[i]
                if float(score) < score_lowest:
                    score_lowest = float(score)
                    j = i
            if float( fd_score) > score_lowest:
                score_list[j] = ( fd_num, fd_score)
        return score_list

    def incr_nutr_values( self, list_tmp, nutr_tot_list, norm_by):
        energy_val = 0.0
        for fd_num, nutr_num, nutr_val in list_tmp:
            if nutr_num == 208:
                energy_val = nutr_val

        # ignore those foods whose energy in kcals is undefined
        if energy_val == 0.0:
            return

        # sum the nutrient values for the food to the nutrient
        # values. Divide if necessary by the energy in kcals. If
        # not, the values are per 100gm, rather than per kcal.
        for i in range( len( nutr_tot_list)):
            nutr_num_tot, nutr_val_tot, constr = nutr_tot_list[i]
            for fd_num, nutr_num, nutr_val in list_tmp:
                if nutr_num_tot == nutr_num:
                    total = float( nutr_val_tot)
                    if norm_by == 0:    # per calorie
                        total = total + float( nutr_val) / float( energy_val)
                    else:                # per weight
                        total = total + float( nutr_val)
                    nutr_tot_list[i] = ( nutr_num_tot, str( total), constr)

    def on_treeview_key_press_event(self, widget, event):
        if event.keyval == gtk.keysyms.Return:
            widget.get_toplevel().activate_default()
            return True
        return False
    
    def on_treeview_button_press_event(self, widget, event):
        if event.type == gtk.gdk._2BUTTON_PRESS and event.button == 1:
            widget.get_toplevel().activate_default()
            return True
        return False
