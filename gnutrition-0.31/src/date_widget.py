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

import gobject
import gtk

class MyPopup:
    def __init__( self, my_widget):
        self.win = gtk.Window( gtk.WINDOW_POPUP)
        self.my_widget = my_widget
        self.win.set_resizable( False)
        self.is_visible = False
        self.vbox = gtk.VBox()
        self.vbox.show()
        self.win.add( self.vbox)
        self.calendar = gtk.Calendar()
        self.calendar.thaw()
        self.calendar.show()
        self.gdk_parent_win = None
        self.vbox.pack_start( self.calendar, False, False, 0)

    def show( self, x, y):
        if self.is_visible == False:
            self.move( x, y)
            self.is_visible = True
        else:
            self.is_visible = False
            self.win.hide()

    def move( self, x, y):
        self.win.realize()
        if not self.gdk_parent_win:
            self.gdk_parent_win = self.vbox.get_parent_window()
        dum1, dum2, w, dum3 = self.win.get_allocation()
        self.gdk_parent_win.move( x - w, y)
        self.win.show()

class MyDateEntry( gtk.HBox):
    __gsignals__ = {
        'date-changed': (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE,
        (gobject.TYPE_OBJECT,))
    }
    def __init__( self):
        gtk.HBox.__init__( self)
        self.__gobject_init__()

        self.entry = gtk.Entry()
        self.entry.set_property( 'editable', False)
        self.entry.show()
        self.pack_start( self.entry, True, True, 0)
        self.button = gtk.Button()
        self.button.show()
        self.parent_win = None
        arrow = gtk.Arrow( gtk.ARROW_DOWN, gtk.SHADOW_OUT)
        arrow.show()
        self.button.add( arrow)
        self.pack_start( self.button, False, True, 0)

        self.popup = MyPopup( self)
        self.on_day_selected( None)

        self.button.connect( 'clicked', self.on_button_released)
        self.popup.calendar.connect( 'day-selected', self.on_day_selected)

    def set_pos_calendar( self):
        x0, y0 = self.parent_win.get_root_origin()
        x1, y1, w1, h1, d1 = self.parent_win.get_geometry()
        x2, y2, w2, h2 = self.button.get_allocation()
        return (x0 + x1 + x2 + w2, y0 + y1 + y2 + h2)
        
    def on_expose_event( self, win, e, d=None):
        if self.popup.is_visible == True:
            x, y = self.set_pos_calendar()
            self.popup.move( x, y)

    def on_button_released( self, w, d=None):
        if not self.parent_win:
            self.parent_win = self.get_parent_window()
            self.parent_widget = self.parent
            self.parent_widget.connect( 'expose_event', self.on_expose_event)
        x, y = self.set_pos_calendar()
        self.popup.show( x, y)

    def on_day_selected( self, w, d=None):
        y, m, d = self.popup.calendar.get_date()
        self.entry.set_text( '%d-%d-%d' % ( y, m + 1, d))
        self.emit( 'date-changed', self)

gobject.type_register( MyDateEntry)
