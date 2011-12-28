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

import string
import gobject
import gtk
import food_srch_res_dlg_ui
import gnutr
import gnutr_consts
import store
import help

class FoodSrchResDlg:
    def __init__( self, app):
        self.ui = food_srch_res_dlg_ui.FoodSrchResDlgUI()
        self.app = app
        self.connect_signals()
        self.store = store.Store()

    def connect_signals( self):
        self.ui.food_entry.connect( 'changed', self.on_food_entry_changed)
        self.ui.dialog.connect( 'response', self.on_response)
        self.ui.selection.connect( 'changed', self.on_selection_changed)
        self.ui.treeview.connect( 'key-press-event', self.on_treeview_key_press_event)
        self.ui.treeview.connect( 'button-press-event', self.on_treeview_button_press_event)

    def on_selection_changed( self, selection, d=None):
        (model, iter) = selection.get_selected()
        if iter:
            food_num = model.get_value( iter, 1)
            if food_num:
                food_desc = self.store.fd_num2desc[ food_num]
                self.ui.food_entry.set_text( food_desc)
            else:
                self.ui.combo.clear_rows()
                self.ui.amount_entry.set_text( '')
                self.ui.food_entry.set_text( '')

    def show( self, food_num_list, view):
        self.view_type = view
        self.ui.combo.clear_rows()
        self.ui.amount_entry.set_text( '')
        self.ui.food_entry.set_text( '')

        self.ui.treeview.freeze_child_notify()
        self.ui.treeview.set_model(None)
        self.create_tree( self.ui.tree, food_num_list)
        self.ui.treeview.set_model(self.ui.tree)
        self.ui.treeview.thaw_child_notify()

        # TODO: need to hide/show amount details depending on view
        self.ui.dialog.vbox.show_all()
        if view == gnutr_consts.FOOD:
            self.ui.combo.hide()
            self.ui.amount_entry.hide()
            self.ui.amount_label.hide()
            self.ui.msre_label.hide()
        self.ui.dialog.run()

    def on_food_entry_changed( self, w, d=None):
        if not self.ui.food_entry.get_text():
            return
        elif self.view_type != gnutr_consts.FOOD:
            (model, iter) = self.ui.selection.get_selected()
            if not iter:
                return
            food_num = model.get_value( iter, 1)
            msre_tuple = self.store.get_msre_desc_tuples( food_num)
            self.ui.combo.set_rows(msre_tuple)

    def on_combo_entry_changed( self, w, d=None):
        self.ui.amount_entry.set_text( '1.0')

    def on_response( self, w, r, d=None):
        if r == gtk.RESPONSE_HELP:
            help.open( '')

        elif r == gtk.RESPONSE_OK:
            (model, iter) = self.ui.selection.get_selected()
            if not iter:
                return

            food_num = model.get_value( iter, 1)

            if not food_num in self.store.fd_num2desc:
                return

            ingr = gnutr.Ingredient()
            ingr.food_num = food_num
            ingr.food_desc = self.store.fd_num2desc[ ingr.food_num]

            if self.view_type != gnutr_consts.FOOD:
                try:
                    ingr.amount = float( self.ui.amount_entry.get_text())
                except ValueError:
                    gnutr.Dialog( 'error', 'The amount must be a number.')

            if (self.view_type == gnutr_consts.PLAN or
                    self.view_type == gnutr_consts.RECIPE):
                ingr.msre_desc = self.ui.combo.get_active_text()
                ingr.msre_num = self.store.msre_desc2num[ ingr.msre_desc]

            if self.view_type == gnutr_consts.PLAN:
                self.ui.dialog.hide()
                self.app.base_win.plan.add_food( ingr)
                self.ui.tree.clear()
            elif self.view_type == gnutr_consts.RECIPE:
                self.app.base_win.recipe.add_ingredient( ingr)
            else:
                self.app.base_win.food.update( ingr)

            if self.view_type != gnutr_consts.PLAN:
                self.ui.dialog.hide()
                self.ui.tree.clear()

        elif r == gtk.RESPONSE_CANCEL or r == gtk.RESPONSE_DELETE_EVENT:
            self.ui.dialog.hide()
            self.ui.tree.clear()

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

    def get_split_list( self, text):
        if '(' not in text:
            return string.split( text, ', ');

        split_list = []
        s_list = string.split( text, ', ')
        i = 0
        length = len( s_list)
        while i < length:
            s = ''
            if '(' in s_list[i]:
                while 1:
                    if s == '':
                        s = s_list[i]
                    else:
                        s = s + ', ' + s_list[i]
                    if ')' in s:
                        break
                    else:
                        i = i + 1
            else:
                s = s_list[i]
            i = i + 1
            split_list.append( s)
        return split_list
       
    def str_num_levels( self, text):
        # str_num_levels( 'Apples, green, big') = 2
        split_list = self.get_split_list( text)
        num_levels = len( split_list) - 1
        return num_levels

    def str_at_level( self, text, level):
        # str_at_level( 'Apples, green, big', level=1) = 'green'
        split_list = self.get_split_list( text)
        if len( split_list) > level:
            return split_list[level]
        else:
            return None

    def str_up_to_level( self, text, level):
        # str_up_to_level( 'Apples, green, big', level=1) = 'Apples, green'
        split_list = self.get_split_list( text)
        if len( split_list) >  level:
            return string.joinfields( split_list[:level+1], ', ')
        else:
            return None

    def str_from_level( self, text, level):
        # str_from_level( 'Apples, green, big', level=1) = 'green, big'
        split_list = self.get_split_list( text)
        if len( split_list) >  level:
            return string.joinfields( split_list[level:], ', ')
        else:
            return None

    def sort_by_matching( self, fd_no_list, level):
        dict = self.store.fd_num2desc
        matching_list = []
        non_matching_list = []
        fd_desc = dict[fd_no_list[0]]
        text_to_match = self.str_up_to_level( fd_desc, level)
        for i in range( 0, len( fd_no_list)):
            fd_no = fd_no_list[i]
            fd_desc = dict[fd_no]
            food_text = self.str_up_to_level( fd_desc, level)
            if food_text == text_to_match:
                matching_list.append( fd_no)
            else:
                non_matching_list.append( fd_no)
        return ( matching_list, non_matching_list)

    def sort_by_level( self, fd_no_list, level):
        dict = self.store.fd_num2desc
        max_level_list = []
        non_max_level_list = []
        for i in range( 0, len( fd_no_list)):
            fd_no = fd_no_list[i]
            fd_desc = dict[fd_no]
            food_level = self.str_num_levels( fd_desc)
            if food_level == level:
                max_level_list.append( fd_no)
            else:
                non_max_level_list.append( fd_no)
        return ( max_level_list, non_max_level_list)

    def create_tree( self, tree, fd_num_list, parent_iter=None, level=0):
        dict = self.store.fd_num2desc

        # don't allow too many branches. If level = 4, make all
        # as siblings without further parents. stop recursion.
        # OR if only 3 or less foods, don't bother with further branches.
        if level > 3 or len( fd_num_list) < 4:
            for fd_num in fd_num_list:
                fd_desc = dict[fd_num]
                node_text = self.str_from_level( fd_desc, level)
                iter = tree.append( parent_iter)
                tree.set_value( iter, 0, node_text)
                tree.set_value( iter, 1, fd_num)
            return

        # sort food list into two: those, whose maximum level is equal
        # to the current maximum level, and the others.
        matching_level_list, non_matching_level_list = self.sort_by_level(
            fd_num_list, level)

        # those foods whose maximum level exceeds the current level can
        # be parents. sort these into two lists: 
        # matching_text - those that have matching text to the first food in
        # the list at the current level, and the non-matching text. 
        if non_matching_level_list:
            matching_text_list, non_matching_text_list = self.sort_by_matching(
                non_matching_level_list, level)

            # if all foods match at level, go up at least one level until
            # there is a non-match
            if len( non_matching_text_list) == 0 and matching_text_list:
                fd_num1 = matching_text_list[0]
                fd_desc1 = dict[fd_num1]

                level_old = level
                match = 0
                while 1:
                    text1 = self.str_at_level( fd_desc1, level)
                    if not text1:
                        return
                    for fd_num2 in matching_text_list:
                        fd_desc2 = dict[fd_num2]
                        text2 = self.str_at_level( fd_desc2, level)
                        if text1 != text2:
                            match = 1
                            break 
                    if match == 1:
                        break
                    level = level + 1
                node_text = self.str_at_level( fd_desc1, level_old)
                for lvl in range( level_old + 1, level, 1):
                    txt = self.str_at_level( fd_desc1, lvl)
                    node_text = node_text + ', ' + txt
                iter = tree.prepend( parent_iter)
                tree.set_value( iter, 0, node_text)
                self.create_tree( tree, matching_text_list, iter, level)
                return

            if matching_text_list:
                if len( matching_text_list) == 1:
                    self.create_tree( tree, matching_text_list, parent_iter, 
                        level)
                else:
                    fd_num = matching_text_list[0]
                    fd_desc = dict[fd_num]
                    # make a node and the node becomes the new parent,
                    # and move onto the next level
                    node_text = self.str_at_level( fd_desc, level)
                    iter = tree.prepend( parent_iter)
                    tree.set_value( iter, 0, node_text)

                    self.create_tree( tree, matching_text_list, iter, level + 1)
            # for the non matching list: repeat at same level and parent 
            # by recursion. 
            if non_matching_text_list:
                self.create_tree( tree, non_matching_text_list, parent_iter, 
                    level)

        # those whose maximum level matches the current level cannot be
        # parents to others, they are siblings to the current parent.
        for fd_num in matching_level_list:
            fd_desc = dict[fd_num]
            node_text = self.str_from_level( fd_desc, level)
            iter = tree.append( parent_iter)
            tree.set_value( iter, 0, node_text)
            tree.set_value( iter, 1, fd_num)
