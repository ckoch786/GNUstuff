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

import gobject
import gtk

import recipe_srch_res_dlg_ui
import gnutr
import gnutr_consts
import database
import store
import help

class RecipeSrchResDlg:
    def __init__( self, app):
        self.app = app
        self.db = database.Database()
        self.store = store.Store()
        self.ui = recipe_srch_res_dlg_ui.RecipeSrchResDlgUI()
        self.connect_signals()

    def connect_signals( self):
        self.ui.dialog.connect( 'response', self.on_response)
        self.ui.selection.connect( 'changed', self.on_selection_changed)
        self.ui.treeview.connect( 'key-press-event', self.on_treeview_key_press_event)
        self.ui.treeview.connect( 'button-press-event', self.on_treeview_button_press_event)

    def show( self, recipe_list, view):
        self.view = view

        self.ui.num_serv_entry.set_text( '')
        self.ui.recipe_entry.set_text( '')
        self.ui.dialog.set_response_sensitive( 1, True)

        self.ui.treemodel.clear()
        for num, desc in recipe_list:
            iter = self.ui.treemodel.append()
            self.ui.treemodel.set_value( iter, 0, desc)
            self.ui.treemodel.set_value( iter, 1, num)

        self.ui.dialog.vbox.show_all()

        if view == gnutr_consts.RECIPE:
            self.ui.num_serv_entry.hide()
            self.ui.num_serv_label.hide()

        if view == gnutr_consts.PLAN:
            self.ui.dialog.set_response_sensitive( 1, False)

        self.ui.dialog.run()

    def on_selection_changed( self, selection, d=None):
        model, iter = selection.get_selected()
        if iter:
            desc = model.get_value( iter, 0)
            self.ui.recipe_entry.set_text( desc)

    def on_response( self, w, r, d=None):
        if r == gtk.RESPONSE_HELP:
            help.open( '')

        elif r == gtk.RESPONSE_OK:
            recipe = gnutr.Recipe()
            model, iter = self.ui.selection.get_selected()
            if not iter:
                gnutr.Dialog( 'warn', 
                    'A recipe must be selected from the list.')
                return

            recipe.desc = model.get_value( iter, 0)
            recipe.num = model.get_value( iter, 1)
            if not recipe.desc or not recipe.num:
                return

            # FIXME: this should be recipe_win.py and
            # plan_win.py
            if self.view == gnutr_consts.RECIPE:
                self.db.query( "SELECT no_serv, category_no FROM " +
                    "recipe WHERE recipe_no = '%d'" %( recipe.num))
                recipe.num_serv, recipe.cat_num = self.db.get_row_result()
                recipe.cat_desc = self.store.cat_num2desc[ recipe.cat_num]

                self.db.query( "SELECT prep_desc FROM preparation WHERE " +
                    "recipe_no = '%d'" %( recipe.num))
                recipe.prep_desc = self.db.get_single_result()

                self.db.query( "SELECT amount, msre_no, fd_no FROM " +
                    "ingredient WHERE recipe_no = '%d'" 
                    %( recipe.num))
                ingr_list = self.db.get_result()

                recipe.ingr_list = []
                for amount, msre_num, food_num in ingr_list:
                    ingr = gnutr.Ingredient()
                    ingr.amount = amount
                    ingr.food_num = food_num
                    ingr.msre_num = msre_num
                    ingr.food_desc = self.store.fd_num2desc[ food_num]
                    ingr.msre_desc = self.store.msre_num2desc[ msre_num]
                    recipe.ingr_list.append( ingr)

                self.app.base_win.recipe.update( recipe)
                self.ui.dialog.hide()

            elif self.view == gnutr_consts.PLAN:
                try:
                    recipe.num_portions = \
                        float( self.ui.num_serv_entry.get_text())
                except ValueError:
                    gnutr.Dialog( 'error', 
                        'The number of portions must be specified.')
                    return

                self.ui.dialog.hide()
                self.app.base_win.plan.add_recipe( recipe)

        elif r == 1:
            desc = self.ui.recipe_entry.get_text()
            if not desc or len( desc) == 0:
                return
            dlg = gnutr.Dialog( 'question', 
                'You are about to delete a recipe from the database.\n' +
                'Are you sure you want to do this?')
            reply = dlg.run()
            if reply == gtk.RESPONSE_YES:
                self.app.base_win.recipe.delete_recipe( desc)
                model, iter = self.ui.selection.get_selected()
                if not iter:
                    return
                model.remove( iter)
                self.ui.recipe_entry.set_text( '')
                dlg.destroy()
            else:
                dlg.destroy()

        elif r == gtk.RESPONSE_CANCEL:
            self.ui.treemodel.clear()
            self.ui.dialog.hide()

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
            
