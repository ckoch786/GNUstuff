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

import gobject
import gtk

import gnutr_widgets
import date_widget

def MyImageMenuItem( label_text, stock_image):
    return gnutr_widgets.GnutrImageMenuItem( label_text, stock_image)

class PlanWinUI:
    def __init__( self):
        self.create_menubar()
        self.create_toolbar()
        self.create_pane()

    def create_menubar( self):
        self.menubar_box = gtk.HandleBox()
        menubar = gtk.MenuBar()
        self.menubar_box.add( menubar)

        file_menu_item = gtk.MenuItem( '_File')
        edit_menu_item = gtk.MenuItem( '_Edit')
        view_menu_item = gtk.MenuItem( '_View')
        settings_menu_item = gtk.MenuItem( '_Settings')
        help_menu_item = gtk.MenuItem( '_Help')

        file_menu = gtk.Menu()
        self.save_item = MyImageMenuItem( '_Save', 'gtk-save')
        separator1 = gtk.SeparatorMenuItem()
        self.exit_item = MyImageMenuItem( '_Quit', 'gtk-quit')
        file_menu.add( self.save_item)
        file_menu.add( separator1)
        file_menu.add( self.exit_item)
        file_menu_item.set_submenu( file_menu)

        edit_menu = gtk.Menu()
        self.add_item = MyImageMenuItem( '_Add', 'gtk-add')
        self.edit_item = MyImageMenuItem( '_Edit', 'gtk-edit')
        self.delete_item = MyImageMenuItem( '_Delete', 'gtk-delete')
        edit_menu.add( self.add_item)
        edit_menu.add( self.edit_item)
        edit_menu.add( self.delete_item)
        edit_menu_item.set_submenu( edit_menu)

        view_menu = gtk.Menu()
        self.plan_view_item = MyImageMenuItem( '_Plan', 'gnutr-plan')
        self.recipe_view_item = MyImageMenuItem( '_Recipe', 'gnutr-recipe')
        self.food_view_item = MyImageMenuItem( '_Food', 'gnutr-food')
        view_menu.add( self.plan_view_item)
        view_menu.add( self.recipe_view_item)
        view_menu.add( self.food_view_item)
        view_menu_item.set_submenu( view_menu)

        settings_menu = gtk.Menu()
        self.nutr_goal_item = MyImageMenuItem( 'Nutrient _Goal', 'gtk-properties')
        settings_menu.add( self.nutr_goal_item)
        settings_menu_item.set_submenu( settings_menu)

        help_menu = gtk.Menu()
        self.manual_item = MyImageMenuItem( '_Contents', 'gtk-help')
        self.about_item = MyImageMenuItem( '_About', 'gtk-about')
        help_menu.add( self.manual_item)
        help_menu.add( self.about_item)
        help_menu_item.set_submenu( help_menu)

        menubar.add( file_menu_item)
        menubar.add( edit_menu_item)
        menubar.add( view_menu_item)
        menubar.add( settings_menu_item)
        menubar.add( help_menu_item)

        self.menubar_box.show_all()

    def create_toolbar( self):
        self.toolbar_box = gtk.HandleBox()
        toolbar = gnutr_widgets.GnutrToolbar()
        tooltips = gtk.Tooltips()
        self.toolbar_box.add( toolbar)

        self.save_button = toolbar.append_button( 'gtk-save', 'Save', tooltips, 'Save meal plan')

        sep = gtk.SeparatorToolItem()
        toolbar.insert(sep, -1)

        self.add_button = toolbar.append_button( 'gtk-add', 'Add', tooltips, 'Add food or recipe')
        self.edit_button = toolbar.append_button( 'gtk-undo', 'Edit', tooltips, 'Edit recipe or food')
        self.delete_button = toolbar.append_button( 'gtk-remove', 'Delete', tooltips, 'Delete selected recipe or food')

        sep = gtk.SeparatorToolItem()
        toolbar.insert(sep, -1)

        self.compute_button = toolbar.append_button( 'gtk-execute', 'Compute', tooltips, 'Compute nutritient composition')

#        icon6 = gtk.Image() 
#        icon6.set_from_stock( 'gtk-execute', gtk.ICON_SIZE_LARGE_TOOLBAR)
#        self.graph_button = toolbar.append_item( 'Graph',
#            'Graph of nutrient composition', None, icon6, None, None)

#        icon7 = gtk.Image() 
#        icon7.set_from_stock( 'gtk-execute', gtk.ICON_SIZE_LARGE_TOOLBAR)
#        self.graph_button = toolbar.append_item( 'Variation',
#            'Graph of variation of nutrient composition', None, icon7, 
#            None, None)

        self.toolbar_box.show_all()

    def create_pane( self):
        self.pane = gtk.Table( 2, 2, False)
        self.pane.set_border_width( 5)
        self.pane.set_row_spacings( 5)
        self.pane.set_col_spacings( 5)

        label1 = gtk.Label( 'Date')
        label1.set_alignment( 1.0, 0.5)
        self.pane.attach( label1, 0, 1, 0, 1, gtk.FILL, 0, 0, 0)

        self.date = date_widget.MyDateEntry()
        self.pane.attach( self.date, 1, 2, 0, 1, 
            gtk.EXPAND | gtk.FILL, 0, 0, 0)

        scrolledwindow1 = gtk.ScrolledWindow()
        scrolledwindow1.set_shadow_type( gtk.SHADOW_IN)
        self.pane.attach( scrolledwindow1, 0, 2, 1, 2, 
            gtk.EXPAND | gtk.FILL, gtk.EXPAND | gtk.FILL, 0, 0)

        self.treemodel = gtk.ListStore( gobject.TYPE_STRING,
            gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING,
            gobject.TYPE_OBJECT)

        self.treeview = gtk.TreeView( self.treemodel)
        self.treeview.set_rules_hint( True)

        self.selection = self.treeview.get_selection()
        self.selection.set_mode( gtk.SELECTION_SINGLE)

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn( 'Time', renderer, text=0)
#        column.set_sizing( gtk.TREE_VIEW_COLUMN_RESIZEABLE)
        self.treeview.append_column( column)
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn( 'Amount', renderer, text=1)
#        column.set_sizing( gtk.TREE_VIEW_COLUMN_RESIZEABLE)
        self.treeview.append_column( column)
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn( 'Measure', renderer, text=2)
#        column.set_sizing( gtk.TREE_VIEW_COLUMN_RESIZEABLE)
        self.treeview.append_column( column)
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn( 'Recipe or Food', renderer, text=3)
#        column.set_sizing( gtk.TREE_VIEW_COLUMN_RESIZEABLE)
        self.treeview.append_column( column)

        scrolledwindow1.add( self.treeview)

        self.pane.show_all()
