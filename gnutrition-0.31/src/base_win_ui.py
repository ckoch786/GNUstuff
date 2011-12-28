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

import gtk
import install

import gnutr_stock
import gnutr_widgets

class BaseWinUI:
    def __init__( self):
        self.win = gtk.Window( gtk.WINDOW_TOPLEVEL)
        self.win.set_title( 'Gnutrition') 

        vbox1 = gtk.VBox( False, 0)
        self.win.add( vbox1)

        self.menubar_box = gtk.VBox( False, 0)
        vbox1.pack_start( self.menubar_box, False, True, 0)

        self.toolbar_box = gtk.VBox( False, 0)
        vbox1.pack_start( self.toolbar_box, False, True, 0)

        hpaned1 = gtk.HPaned()
#        hpaned1.set_position( 0)
        vbox1.pack_start( hpaned1, True, True, 0)

        vbox2 = gtk.VBox( False, 0)
        hpaned1.pack1( vbox2, False, True)

        frame1 = gtk.Frame()
        frame1.set_border_width( 2)
        frame1.set_shadow_type( gtk.SHADOW_IN)
        vbox2.pack_start( frame1, False, True, 0)

        label1 = gtk.Label( 'View')
        frame1.add( label1)

        frame2 = gtk.Frame()
        frame2.set_border_width( 2)
        frame2.set_shadow_type( gtk.SHADOW_IN)
        vbox2.pack_start( frame2, True, True, 0)

        tooltips = gtk.Tooltips()
        toolbar = gnutr_widgets.GnutrToolbar()
        toolbar.set_orientation( gtk.ORIENTATION_VERTICAL)
        frame2.add( toolbar)

        self.recipe_button = toolbar.append_button( 'gnutr-recipe', 'Recipe', tooltips, 'Switch view to recipe')
        self.plan_button = toolbar.append_button( 'gnutr-plan', 'Plan', tooltips, 'Switch view to plan')
        self.food_button = toolbar.append_button( 'gnutr-food', 'Food', tooltips, 'Switch view to food')

# the original version of the buttons (using the deprecated API) looks
# a bit different, buttons are smaller and have some padding around
# them:

#         vbox4 = gtk.VBox()
#         vbox4.set_border_width( 10)
#         self.recipe_button = gtk.Button()
#         icon2 = gtk.Image()
#         icon2.set_from_stock( 'gnutr-recipe', gtk.ICON_SIZE_LARGE_TOOLBAR)
#         self.recipe_button.add( icon2)
#         self.recipe_button.set_relief( gtk.RELIEF_NONE)
#         vbox4.pack_start( self.recipe_button)

#         label3 = gtk.Label( 'Recipe')
#         vbox4.pack_start( label3)
#         toolbar.append_widget( vbox4, 'Switch view to recipe', None)


        self.pane_box = gtk.HBox( False, 0)
        self.pane_box.set_border_width( 2)
        hpaned1.pack2( self.pane_box, True, True)

        self.win.show_all()

        # about dialog
        self.about_dlg = gtk.Dialog( title='About Nutrition',
            flags=gtk.DIALOG_MODAL, buttons=(gtk.STOCK_CANCEL,
            gtk.RESPONSE_CANCEL))
        self.about_dlg.set_resizable( False)
        about_label = gtk.Label( 
"""Gnutrition %s

(C) 2002 Edgar Denny
Author: Edgar Denny (edenny@skyweb.net)

A Diet and Nutrition Analysis Program.""" % ( install.VERSION))
        about_label.set_justify( gtk.JUSTIFY_CENTER)
        vbox6 = gtk.VBox()
        vbox6.set_border_width( 5)
        vbox6.pack_start( about_label, True, True, 0)
        self.about_dlg.vbox.pack_start( vbox6, True, True, 0)
        self.about_dlg.vbox.show_all()
