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

import string
import time

import gobject
import gtk

import plan_win_ui
import gnutr
import gnutr_consts
import database
import person
import help

class PlanWin:
    def __init__( self, app, parent):
        self.ui = plan_win_ui.PlanWinUI()
        self.app = app
        self.db = database.Database()
        self.person = person.Person()
        self.parent = parent

        self.connect_signals()
        self.update()

    def get_current_date( self):
        self.db.query( "SELECT CURDATE()")
        return self.db.get_single_result()

    def connect_signals( self):
        self.ui.save_button.connect( 'clicked', self.on_save_released)
        self.ui.add_button.connect( 'clicked', self.on_add_released)
        self.ui.delete_button.connect( 'clicked', self.on_delete_released)
        self.ui.edit_button.connect( 'clicked', self.on_edit_released)
        self.ui.compute_button.connect( 'clicked', self.on_compute_released)

        self.ui.save_item.connect( 'activate', self.on_save_released)
        self.ui.exit_item.connect( 'activate', lambda w: gtk.main_quit())
        self.ui.add_item.connect( 'activate', self.on_add_released)
        self.ui.delete_item.connect( 'activate', self.on_delete_released)
        self.ui.edit_item.connect( 'activate', self.on_edit_released)
        self.ui.recipe_view_item.connect( 'activate', self.on_recipe_activate)
        self.ui.food_view_item.connect( 'activate', self.on_food_activate)
        self.ui.nutr_goal_item.connect( 'activate', self.on_nutr_goal_activate)
        self.ui.manual_item.connect( 'activate', self.on_manual_activate)
        self.ui.about_item.connect( 'activate', self.on_about_activate)

        self.ui.selection.connect( 'changed', self.on_selection_changed)
        self.ui.date.connect( 'date-changed', self.on_date_changed)

    def on_manual_activate( self, w, d=None):
        help.open( '')

    def on_add_released( self, w, d=None):
        (model, iter) = self.ui.selection.get_selected()
        if not iter:
            gnutr.Dialog( 'warn', 'No time selected.', self.parent)
            return
        if not hasattr( self, 'plan_add_dlg'):
            import plan_add_dlg
            self.plan_add_dlg = plan_add_dlg.PlanAddDlg( self.app)
        self.plan_add_dlg.show()

    def on_date_changed( self, w, d=None):
        self.update()

    def on_selection_changed( self, selection, d=None):
        (model, iter) = selection.get_selected()
        if iter:
            date_str = self.ui.date.entry.get_text()
            if not date_str:
                gnutr.Dialog( 'warn', 'You must select a date before\n' +
                    'you can select a time.', self.parent)

    def on_save_released( self, w, d=None):
        dlg = gnutr.Dialog( 'question',
            'The old plan will be overwritten by the new one.\n' +
            'Are you sure you want to do this?', self.parent)
        reply = dlg.run()
        if reply == gtk.RESPONSE_YES:
            self.save_plan()
            dlg.destroy()
        else:
            dlg.destroy()

    def on_delete_released( self, w, d=None):
        (model, iter) = self.ui.selection.get_selected()
        if not iter:
            gnutr.Dialog( 'warn', 'You must select a recipe or food to delete.',
                self.parent)
            return
        
        date = self.ui.date.entry.get_text()

        data = model.get_value( iter, 4)
        if data:
            if isinstance( data, gnutr.Ingredient):
                self.delete_from_plan_temp_db( date, food=data) 
            elif isinstance( data, gnutr.Recipe):
                self.delete_from_plan_temp_db( date, recipe=data) 
            else:
                return
            model.set_value( iter, 1, '')
            model.set_value( iter, 2, '')
            model.set_value( iter, 3, '')
            model.set_value( iter, 4, gobject.GObject())
        else:
            return

    def on_edit_released( self, w, d=None):
        (model, iter) = self.ui.selection.get_selected()
        if not iter:
            gnutr.Dialog( 'warn', 'You must select a recipe or food to edit.',
                self.parent)
            return

        data = model.get_value( iter, 4)
        if isinstance( data, gnutr.Ingredient):
            if not hasattr( self, 'food_edit_dlg'):
                import food_edit_dlg
                self.food_edit_dlg = food_edit_dlg.FoodEditDlg( self.app)
            self.food_edit_dlg.show( data, gnutr_consts.PLAN)
        elif isinstance( data, gnutr.Recipe):
            if not hasattr( self, 'recipe_edit_dlg'):
                import recipe_edit_dlg
                self.recipe_edit_dlg = recipe_edit_dlg.RecipeEditDlg( self.app)
            self.recipe_edit_dlg.show( data)

    def replace_recipe( self, recipe):
        date = self.ui.date.entry.get_text()
        (model, iter) = self.ui.selection.get_selected()
        if not iter:
            return
        model.set_value( iter, 1, recipe.num_portions)
        model.set_value( iter, 4, recipe)
        self.edit_plan_temp_db( date, recipe=recipe)

    def replace_food( self, food):
        date = self.ui.date.entry.get_text()
        (model, iter) = self.ui.selection.get_selected()
        if not iter:
            return
        model.set_value( iter, 1, food.amount)
        model.set_value( iter, 2, food.msre_desc)
        model.set_value( iter, 4, food)
        self.edit_plan_temp_db( date, food=food)

    def on_compute_released( self, w, d=None):
        if not hasattr( self, 'plan_compute_dlg'):
            import plan_compute_dlg
            self.plan_compute_dlg = plan_compute_dlg.PlanComputeDlg( self.app)
        self.plan_compute_dlg.show()

    def on_recipe_activate( self, w, d=None):
        self.app.base_win.on_recipe_button_released( None)

    def on_food_activate( self, w, d=None):
        self.app.base_win.on_food_button_released( None)

    def on_nutr_goal_activate( self, w, d=None):
        if not hasattr( self, 'nutr_goal_dlg'):
            import nutr_goal_dlg
            self.nutr_goal_dlg = nutr_goal_dlg.NutrGoalDlg()
        self.nutr_goal_dlg.show()

    def on_about_activate( self, w, d=None):
        reply = self.app.base_win.ui.about_dlg.run()
        if reply == gtk.RESPONSE_CANCEL or reply == gtk.RESPONSE_DELETE_EVENT:
            self.app.base_win.ui.about_dlg.hide()

    def set_times( self):
        for i in range( 24):
            iter = self.ui.treemodel.append()
            self.ui.treemodel.set_value( iter, 0, str(i) + ':00')
            iter = self.ui.treemodel.append()
            self.ui.treemodel.set_value( iter, 0, '')

    def get_time_of_day( self):
        (model, iter1) = self.ui.selection.get_selected()
        if not iter1:
            return ''

        time_string = model.get_value( iter1, 0)
        if time_string:
            return time_string

        # Can't seem to iterate backwards through a list store!
        # if blank text, we want the next cell with text
        while iter1:
            time_string_next = model.get_value( iter1, 0)
            if time_string_next:
                break
            iter1 = model.iter_next( iter1)

        # Now we want the hour before
        text_list = string.split( time_string_next, ':')
        return str( int( text_list[0]) - 1) + ':00'

    def iter_for_time( self, time_string1):
        iter = self.ui.treemodel.get_iter_root()
        pos = 0
        while iter:
            value = self.ui.treemodel.get_value( iter, 0)
            if value:
                value_list = string.split( value, ':')
                if int( value_list[0]) < 10:
                    #time_string2 = '0' + value + ':00'
                    time_string2 = value + ':00'
                else:
                    time_string2 = value + ':00'
                if time_string1 == time_string2:
                    return iter, pos
            pos = pos + 1
            iter = self.ui.treemodel.iter_next( iter)
        return iter, pos

    def update( self):
        date = self.ui.date.entry.get_text()

        self.ui.treemodel.clear()
        self.set_times()

        food_list = self.get_foods_for_date( date)
        recipe_list = self.get_recipes_for_date( date)

        for recipe in recipe_list:
            iter, pos = self.iter_for_time( recipe.time)
            
            # is there already a recipe or food in either of the two
            # rows available for the time? If both occupied create a
            # new one.
            text = self.ui.treemodel.get_value( iter, 3)
            if not text:
                self.ui.treemodel.set_value( iter, 1, recipe.num_portions)
                self.ui.treemodel.set_value( iter, 3, recipe.desc)
                self.ui.treemodel.set_value( iter, 4, recipe)
                continue

            ret = self.ui.treemodel.iter_next( iter)
            if ret:
                text = self.ui.treemodel.get_value( iter, 3)
                if not text:
                    self.ui.treemodel.set_value( iter, 1, recipe.num_portions)
                    self.ui.treemodel.set_value( iter, 3, recipe.desc)
                    self.ui.treemodel.set_value( iter, 4, recipe)
                    continue

            iter = self.ui.treemodel.insert( pos + 2)
            self.ui.treemodel.set_value( iter, 1, recipe.num_portions)
            self.ui.treemodel.set_value( iter, 3, recipe.desc)
            self.ui.treemodel.set_value( iter, 4, recipe)

        for food in food_list:
            iter, pos = self.iter_for_time( food.time)

            # is there already a recipe or food in either of the two
            # rows available for the time? If both occupied create a
            # new one.
            text = self.ui.treemodel.get_value( iter, 3)
            if not text:
                self.ui.treemodel.set_value( iter, 1, food.amount)
                self.ui.treemodel.set_value( iter, 2, food.msre_desc)
                self.ui.treemodel.set_value( iter, 3, food.food_desc)
                self.ui.treemodel.set_value( iter, 4, food)
                continue

            ret = self.ui.treemodel.iter_next( iter)
            if ret:
                text = self.ui.treemodel.get_value( iter, 3)
                if not text:
                    self.ui.treemodel.set_value( iter, 1, food.amount)
                    self.ui.treemodel.set_value( iter, 2, food.msre_desc)
                    self.ui.treemodel.set_value( iter, 3, food.food_desc)
                    self.ui.treemodel.set_value( iter, 4, food)
                    continue

            iter = self.ui.treemodel.insert( pos + 2)
            self.ui.treemodel.set_value( iter, 1, food.amount)
            self.ui.treemodel.set_value( iter, 2, food.msre_desc)
            self.ui.treemodel.set_value( iter, 3, food.food_desc)
            self.ui.treemodel.set_value( iter, 4, food)

    def get_foods_for_date( self, date):
        if not hasattr( self, 'store'):
            import store
            self.store = store.Store()

        self.db.query( "SELECT time, amount, msre_no, fd_no " +
            "FROM food_plan_temp WHERE date = '%s'" %( date))
        result = self.db.get_result()

        food_list = []
        for time, amount, msre_num, food_num in result:
            food = gnutr.Ingredient()
            food.time = str( time)
            food.amount = amount
            food.msre_num = msre_num
            food.food_num = food_num
            food.food_desc = self.store.fd_num2desc[food.food_num]
            food.msre_desc = self.store.msre_num2desc[food.msre_num]
            food_list.append( food)
        return food_list

    def get_recipes_for_date( self, date):
        self.db.query( "SELECT time, no_portions, " +
            "recipe.recipe_no, recipe_name FROM recipe_plan_temp, recipe " +
            "WHERE date = '" + date + "' AND " +
            "recipe_plan_temp.recipe_no = recipe.recipe_no")
        result = self.db.get_result()

        recipe_list = []
        for time, num_portions, recipe_num, recipe_desc in result:
            recipe = gnutr.Recipe()
            recipe.time = str( time)
            recipe.num_portions = num_portions
            recipe.num = recipe_num
            recipe.desc = recipe_desc
            recipe_list.append( recipe)
        return recipe_list

    def get_recipes_for_time( self, time, date):
        ret = []
        recipe_list = self.get_recipes_for_date( date)
        for recipe in recipe_list:
            if int( string.split( recipe.time, ':')[0]) == \
                int( string.split( time, ':')[0]):
                ret.append( recipe)
        return ret

    def get_foods_for_time( self, time, date):
        ret = []
        food_list = self.get_foods_for_date( date)
        for food in food_list:
            if int( string.split( food.time, ':')[0]) == \
                int( string.split( time, ':')[0]):
                ret.append( food)
        return ret

    def delete_from_plan_temp_db( self, date, food=None, recipe=None):
        if food:
            self.db.query( "DELETE FROM food_plan_temp WHERE " +
                "date = '%s' AND time = '%s' AND fd_no = '%d'"
                %( date, food.time, food.food_num))
        else:
            self.db.query( "DELETE FROM recipe_plan_temp WHERE " +
                "date = '%s' AND time = '%s' AND recipe_no = '%d'" 
                %( date, recipe.time, recipe.num))

    def edit_plan_temp_db( self, date, food=None, recipe=None):
        if food:
            self.db.query( "SELECT * FROM food_plan_temp WHERE " +
                "date = '%s' AND time = '%s' AND fd_no = '%d'"
                %( date, food.time, food.food_num))
            data = self.db.get_result()
            # FIXME: catches a bug where two foods have the same name,
            # date and time. At present can't distinguish between them
            if len( data) > 1:
                person_num, date2, time, amount, msre_num, food_num = data[0]
            else:
                ((person_num, date2, time, amount, msre_num, food_num),) = \
                data

            self.db.query( "DELETE FROM food_plan_temp WHERE " +
                "date = '%s' AND time = '%s' AND fd_no = '%d'"
                %( date, food.time, food.food_num))

            self.db.query( "INSERT INTO food_plan_temp VALUES ( " +
                "'%d', '%s', '%s', '%s', '%d', '%d')"
                %( person_num, date2, time, food.amount, food.msre_num,
                    food_num))
        else:
            self.db.query( "SELECT * FROM recipe_plan_temp WHERE " +
                "date = '%s' AND time = '%s' AND recipe_no = '%d'" 
                %( date, recipe.time, recipe.num))
            data = self.db.get_result()
            # FIXME: catches a bug where two recipes have the same name,
            # date and time. At present can't distinguish between them
            if len( data) > 1:
                person_num, date2, time, num_portions, recipe_num = data[0]
            else:
                ((person_num, date2, time, num_portions, recipe_num),) = data

            self.db.query( "DELETE FROM recipe_plan_temp WHERE " +
                "date = '%s' AND time = '%s' AND recipe_no = '%d'" 
                %( date, recipe.time, recipe.num))

            self.db.query( "INSERT INTO recipe_plan_temp VALUES ( " +
            "'%d', '%s', '%s', '%s', '%d')"
                %( person_num, date2, time, recipe.num_portions, recipe_num))

    def save_plan( self):
        person_num = self.person.get_person_num()

        # delete old plan
        self.db.query( "DELETE FROM food_plan WHERE person_no = '%d'" 
            %( person_num))
        self.db.query( "DELETE FROM recipe_plan WHERE person_no = '%d'" 
            %( person_num))

        # transfer from tempory to stored table
        # FIXME: for plans that span a large time, this is inefficient
        self.db.query( "SELECT * FROM food_plan_temp")
        plan_list = self.db.get_result()

        for person_num, date, time, amount, msre_num, food_num in plan_list:
            self.db.query( "INSERT INTO food_plan VALUES ( " +
                "'%d', '%s', '%s', '%f', '%d', '%d' )"
                %( person_num, date, time, amount, msre_num, food_num))

        self.db.query( "SELECT * FROM recipe_plan_temp")
        recipe_list = self.db.get_result()

        for person_num, date, time, num_portions, recipe_num in recipe_list:
            self.db.query( "INSERT INTO recipe_plan VALUES ( " +
                "'%d', '%s', '%s', '%f', '%d')"
                %( person_num, date, time, num_portions, recipe_num))

    def add_recipe( self, recipe):
        date = self.ui.date.entry.get_text()
        time = self.get_time_of_day()
        recipe_list = self.get_recipes_for_time( time, date)
        for r in recipe_list:
            if r.num == recipe.num:
                gnutr.Dialog( 'error', 'Cannot have the same recipe twice\n' +
                    'for the same day and time.')
                return
        person_num = self.person.get_person_num()

        self.db.query( "INSERT INTO recipe_plan_temp VALUES ( " +
            "'%d', '%s', '%s', '%f', '%d' )"
            %( person_num, date, time, recipe.num_portions, recipe.num))
        self.update()

    def add_food( self, food):
        date = self.ui.date.entry.get_text()
        time = self.get_time_of_day()
        food_list = self.get_foods_for_time( time, date)
        for f in food_list:
            if f.food_num == food.food_num:
                gnutr.Dialog( 'error', 'Cannot have the same food twice\n' +
                    'for the same day and time.', self.parent)
                return
        person_num = self.person.get_person_num()

        # Note: the temporary table is used
        self.db.query( "INSERT INTO food_plan_temp VALUES ( " +
            "'%d', '%s', '%s', '%f', '%d', '%d' )"
            %( person_num, date, time, food.amount, food.msre_num, 
            food.food_num))
        self.update()
