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

import gobject
import gtk
import gnutr_widgets

def MyImageMenuItem( label_text, stock_image):
    return gnutr_widgets.GnutrImageMenuItem( label_text, stock_image)

class FoodWinUI:
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
        self.exit_item = MyImageMenuItem( '_Quit', 'gtk-quit')
        file_menu.add( self.exit_item)
        file_menu_item.set_submenu( file_menu)

        edit_menu = gtk.Menu()
        self.clear_item = MyImageMenuItem( '_Clear', 'gtk-clear')
        edit_menu.add( self.clear_item)
        edit_menu_item.set_submenu( edit_menu)

        view_menu = gtk.Menu()
        self.plan_view_item = MyImageMenuItem( '_Plan', 'gnutr-plan')
        self.recipe_view_item = MyImageMenuItem( '_Recipe', 'gnutr-recipe')
        self.food_view_item = MyImageMenuItem( '_Food', 'gnutr_food')
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

        self.clear_button = toolbar.append_button( 'gtk-clear', 'Clear', tooltips, 'Clear food data')

        sep = gtk.SeparatorToolItem()
        toolbar.insert(sep, -1)

        self.select_button = toolbar.append_button( 'gtk-find', 'Select', tooltips, 'Select food from database')
        self.compute_button = toolbar.append_button( 'gtk-execute', 'Compute', tooltips, 'Compute nutrition composition')

        sep = gtk.SeparatorToolItem()
        toolbar.insert(sep, -1)
        
        self.pref_button = toolbar.append_button( 'gtk-preferences', 'Goals', tooltips, 'Nutritient goal')

#        icon5 = gtk.Image() 
#        icon5.set_from_stock( 'gtk-execute', gtk.ICON_SIZE_LARGE_TOOLBAR)
#        self.graph_button = toolbar.append_item( 'Graph',
#            'Graph of nutrient composition', None, icon5, None, None)

        self.toolbar_box.show_all()

    def create_pane( self):
        self.pane = gtk.Table( 3, 5, False)
        self.pane.set_border_width( 5)
        self.pane.set_row_spacings( 5)
        self.pane.set_col_spacings( 5)

        label1 = gtk.Label( 'Selected food')
        label1.set_alignment( 1, 0.5)
        self.pane.attach( label1, 0, 1, 0, 1, gtk.FILL,0, 0, 0)

        self.food_entry = gtk.Entry()
        self.food_entry.set_property( 'editable', False)
        self.food_entry.set_property( 'can-focus', False)
        self.pane.attach( self.food_entry, 1, 5, 0, 1, 
            gtk.EXPAND | gtk.FILL, 0, 0, 0)

        label2 = gtk.Label( '')
        label2.set_text_with_mnemonic( '_Amount')
        label2.set_alignment( 1, 0.5)
        self.pane.attach( label2, 0, 1, 1, 2, gtk.FILL, 0, 0, 0)

        self.amount_entry = gtk.Entry()
        self.pane.attach( self.amount_entry, 1, 2, 1, 2, 
            gtk.EXPAND | gtk.FILL, 0, 0, 0)

        label3 = gtk.Label( '   ')
        label3.set_alignment( 1, 0.5)
        self.pane.attach( label3, 2, 3, 1, 2, gtk.FILL, 0, 0, 0)

        label4 = gtk.Label( '')
        label4.set_text_with_mnemonic( '_Measure')
        label4.set_alignment( 1, 0.5)
        self.pane.attach( label4, 3, 4, 1, 2, gtk.FILL, 0, 0, 0)

        self.msre_combo = gnutr_widgets.GnutrComboBox()
        self.pane.attach( self.msre_combo, 4, 5, 1, 2, 
            gtk.EXPAND | gtk.FILL, 0, 0, 0)

        scrolledwindow1 = gtk.ScrolledWindow()
        scrolledwindow1.set_policy( gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        self.pane.attach( scrolledwindow1, 0, 5, 2, 3, gtk.EXPAND | gtk.FILL, 
            gtk.EXPAND | gtk.FILL, 0, 0)

        viewport1 = gtk.Viewport()
        viewport1.set_shadow_type( gtk.SHADOW_IN)
        scrolledwindow1.add( viewport1)

        self.notebook_container = gtk.HBox( False, 0)
        viewport1.add( self.notebook_container)

        self.pane.show_all()
