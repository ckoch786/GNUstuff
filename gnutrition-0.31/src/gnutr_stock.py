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

import gtk
import install

def create_stock():
    drct = install.dir + '/pixmaps/'
    recipe_pixbuf = gtk.gdk.pixbuf_new_from_file( drct + 'cake.png')
    plan_pixbuf = gtk.gdk.pixbuf_new_from_file( drct + 'plan.png')
    food_pixbuf = gtk.gdk.pixbuf_new_from_file( drct + 'banana.png')

    recipe_iconset = gtk.IconSet( recipe_pixbuf)
    plan_iconset = gtk.IconSet( plan_pixbuf)
    food_iconset = gtk.IconSet( food_pixbuf)

    icon_factory = gtk.IconFactory()
    icon_factory.add( 'gnutr-recipe', recipe_iconset)
    icon_factory.add( 'gnutr-plan', plan_iconset)
    icon_factory.add( 'gnutr-food', food_iconset)

    icon_factory.add_default()

    gtk.stock_add(( 
        ('gnutr-recipe', '_Recipe', gtk.gdk.MOD1_MASK, ord( "r"), "uk"), 
        ('gnutr-plan', '_Plan', gtk.gdk.MOD1_MASK, ord( "p"), "uk"), 
        ('gnutr-food', '_Food', gtk.gdk.MOD1_MASK, ord( "f"), "uk")))

create_stock()
