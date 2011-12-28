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
import install
import gnutr_widgets

def MyImageMenuItem( label_text, stock_image):
    return gnutr_widgets.GnutrImageMenuItem( label_text, stock_image)

class RecipeWinUI:
    def __init__( self):
        self.create_menubar()
        self.create_toolbar()
        self.create_pane()

    def create_menubar( self):
        self.menubar_box = gtk.HandleBox()

        menubar = gtk.MenuBar()
        self.menubar_box.add( menubar)

        file_menu_item = gtk.MenuItem( '_File')
        file_menu = gtk.Menu()
        file_menu.set_accel_path( '<main>/File')

        self.clear_item = MyImageMenuItem( '_Clear', 'gtk-clear')
        self.open_item = MyImageMenuItem( '_Open', 'gtk-open')
        self.save_item = MyImageMenuItem( '_Save', 'gtk-save')
        self.save_as_item = MyImageMenuItem( 'E_xport...', 'gtk-save-as')
        separator = gtk.SeparatorMenuItem()
        self.exit_item = MyImageMenuItem( '_Quit', 'gtk-quit')

        file_menu.add( self.clear_item)
        file_menu.add( self.open_item)
        file_menu.add( self.save_item)
        file_menu.add( self.save_as_item)
        file_menu.add( separator)
        file_menu.add( self.exit_item)
        file_menu_item.set_submenu( file_menu)

        edit_menu_item = gtk.MenuItem( '_Edit')
        edit_menu = gtk.Menu()
        
        self.add_food_item = MyImageMenuItem( '_Add Food', 'gtk-add')
        self.edit_food_item = MyImageMenuItem( '_Edit Food', 'gtk-edit')
        self.delete_food_item = MyImageMenuItem( '_Delete Food', 'gtk-delete')

        edit_menu.add( self.add_food_item)
        edit_menu.add( self.edit_food_item)
        edit_menu.add( self.delete_food_item)
        edit_menu_item.set_submenu( edit_menu)

        view_menu_item = gtk.MenuItem( '_View')
        view_menu = gtk.Menu()

        self.plan_item = MyImageMenuItem( '_Plan', 'gnutr-plan')
        self.recipe_item = MyImageMenuItem( '_Recipe', 'gnutr-recipe')
        self.food_item = MyImageMenuItem( '_Food', 'gnutr-food')

        view_menu.add( self.recipe_item)
        view_menu.add( self.plan_item)
        view_menu.add( self.food_item)
        view_menu_item.set_submenu( view_menu)

        settings_menu_item = gtk.MenuItem( '_Settings')
        settings_menu = gtk.Menu()
        self.nutrient_goal_item = MyImageMenuItem( 'Nutrient _Goal', 
            'gtk-properties')
        self.hide_instr_item = gtk.CheckMenuItem( 'Hide Recipe _Instructions')
        settings_menu.add( self.nutrient_goal_item)
        settings_menu.add( self.hide_instr_item)
        settings_menu_item.set_submenu( settings_menu)

        help_menu_item = gtk.MenuItem( '_Help')
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


        self.open_button = toolbar.append_button( 'gtk-open', "Open", tooltips, "Open recipe from database")
        self.save_button = toolbar.append_button( 'gtk-save', "Save", tooltips, "Save recipe to database")
        self.clear_button = toolbar.append_button( 'gtk-refresh', "Clear", tooltips, "Clear recipe")

        sep = gtk.SeparatorToolItem()
        toolbar.insert( sep, -1)

        self.add_button = toolbar.append_button( 'gtk-add', "Add", tooltips, "Add food to recipe")
        self.delete_button = toolbar.append_button( 'gtk-remove', "Delete", tooltips, "Delete food from recipe")
        self.edit_button = toolbar.append_button( 'gtk-undo', "Edit", tooltips, "Edit food in recipe")

        sep = gtk.SeparatorToolItem()
        toolbar.insert( sep, -1)

        self.nutr_button = toolbar.append_button( 'gtk-execute', "Nutrients", tooltips, "Display recipe nutrient totals")
        self.goal_button = toolbar.append_button( 'gtk-properties', "Goals", tooltips, "Nutrition goals")

#        icon9 = gtk.Image()
#        icon9.set_from_stock( 'gtk-execute', gtk.ICON_SIZE_LARGE_TOOLBAR)
#        self.graph_button = toolbar.append_item( "Graph",
#            "Display graph of recipe nutrient totals", None, icon9, 
#            None, None)

        self.toolbar_box.show_all()

    def create_pane( self):
        self.pane = gtk.Table(2, 5, False)
        self.pane.set_border_width( 5)
        self.pane.set_row_spacings( 5)
        self.pane.set_col_spacings( 5)

        label1 = gtk.Label( '')
        label1.set_text_with_mnemonic( '_Recipe name')
        label1.set_alignment( 1.0, 0.5)
        self.pane.attach( label1, 0, 1, 0, 1, gtk.FILL, 0, 0, 0)

        self.recipe_entry = gtk.Entry()
        label1.set_mnemonic_widget( self.recipe_entry)
        self.pane.attach( self.recipe_entry, 1, 5, 0, 1, gtk.FILL | gtk.EXPAND, 
            0, 0, 0)

        label2 = gtk.Label( '')
        label2.set_text_with_mnemonic( '_Category')
        label2.set_alignment( 1.0, 0.5)
        self.pane.attach( label2, 0, 1, 1, 2, gtk.FILL, 0, 0, 0)

        self.category_combo = gnutr_widgets.GnutrComboBox()
        label2.set_mnemonic_widget( self.category_combo)
        self.pane.attach( self.category_combo, 1, 2, 1, 2,
            gtk.FILL | gtk.EXPAND, 0, 0, 0)

        label3 = gtk.Label("   ")
        self.pane.attach( label3, 2, 3, 1, 2, gtk.FILL, 0, 0, 0)

        label4 = gtk.Label( '')
        label4.set_text_with_mnemonic( '_Num. servings')
        label4.set_alignment( 1, 0.5)
        self.pane.attach( label4, 3, 4, 1, 2, gtk.FILL, 0, 0, 0)

        self.num_serv_entry = gtk.Entry()
        label4.set_mnemonic_widget( self.num_serv_entry)
        self.pane.attach( self.num_serv_entry, 4, 5, 1, 2, 
            gtk.FILL | gtk.EXPAND, 0, 0, 0)

        self.vpaned = gtk.VPaned()
        self.pane.attach( self.vpaned, 0, 5, 2, 3, gtk.FILL | gtk.EXPAND,
            gtk.FILL | gtk.EXPAND, 0, 0)

        vbox1 = gtk.VBox( False, 0)
        self.vpaned.pack1( vbox1, True, True)

        self.vbox2 = gtk.VBox( False, 0)
        self.vpaned.pack2( self.vbox2, True, True)

        frame1 = gtk.Frame()
        frame1.set_shadow_type( gtk.SHADOW_IN)
        vbox1.pack_start( frame1, False, False, 0)

        button1 = gtk.Button( label="Ingredients")
        frame1.add( button1)

        frame2 = gtk.Frame()
        frame2.set_shadow_type( gtk.SHADOW_IN)
        self.vbox2.pack_start( frame2, False, False, 0)

        button2 = gtk.Button(label='Recipe Instructions')
        frame2.add( button2)

        scrolledwindow1 = gtk.ScrolledWindow()
        scrolledwindow1.set_policy( gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        vbox1.pack_start( scrolledwindow1, True, True, 0)

        self.treemodel = gtk.ListStore( gobject.TYPE_STRING,
            gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_OBJECT)

        self.treeview = gtk.TreeView( self.treemodel)
        self.treeview.set_rules_hint( True)
        self.selection = self.treeview.get_selection()

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn( 'Amount', renderer, text=0)
        self.treeview.append_column( column)
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn( 'Measure', renderer, text=1)
        self.treeview.append_column( column)
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn( 'Food', renderer, text=2)
        self.treeview.append_column( column)

        scrolledwindow1.add( self.treeview)

        self.scrolledwindow2 = gtk.ScrolledWindow()
        self.scrolledwindow2.set_policy( gtk.POLICY_NEVER, gtk.POLICY_ALWAYS)
        self.vbox2.pack_start( self.scrolledwindow2, True, True, 0)

        self.text_box = gtk.TextView()
        self.text_buffer = gtk.TextBuffer( None)
        self.text_box.set_buffer( self.text_buffer)
        self.text_box.set_editable( True)
        self.text_box.set_cursor_visible( True)

        self.scrolledwindow2.add( self.text_box)

        self.pane.show_all()
