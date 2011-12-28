import gtk
import gobject

class GnutrComboBox(gtk.ComboBox):
    def __init__(self, rows = None, active = -1):
        gtk.ComboBox.__init__(self)
        
        model = gtk.ListStore(gobject.TYPE_STRING)
        self.set_model(model)
        
        cell = gtk.CellRendererText()
        self.pack_start(cell)
        self.add_attribute(cell, 'text', 0)

        if rows:
            self.set_rows(rows)

        if active > -1:
            self.set_active(active)

    def set_rows(self, rows, active = -1):
        if rows:
            model = self.get_model()
            model.clear()
            for row in rows:
                model.append(row)
            self.set_active(active)

    def clear_rows(self):
        self.get_model().clear()

    def set_active_text(self, text):
        model = self.get_model()
        it = model.get_iter_first()
        while it:
            if model.get_value(it, 0) == text:
                self.set_active_iter(it)
                return True
            it = model.iter_next(it)

class GnutrToolbar( gtk.Toolbar):
    def __init__( self):
        gtk.Toolbar.__init__( self)
        self.set_show_arrow( False)

    def append_button( self, stock_id, label, gtk_tooltips, tooltip):
        icon = gtk.Image()
        icon.set_from_stock( stock_id, gtk.ICON_SIZE_LARGE_TOOLBAR)
        button = gtk.ToolButton( icon, label)
        button.set_tooltip( gtk_tooltips, tooltip)
        self.insert( button, -1)
        return button

class GnutrImageMenuItem(gtk.ImageMenuItem):
    def __init__( self, label_text, stock_image):
        gtk.ImageMenuItem.__init__( self, label_text)
        icon = gtk.Image()
        icon.set_from_stock( stock_image, gtk.ICON_SIZE_MENU)
        self.set_image( icon)


class GnutrComboBoxEntry(gtk.ComboBoxEntry):
    def __init__(self, rows = None):
        gtk.ComboBoxEntry.__init__(self)

        assert False, "Don't use this, it's not working"
        
        model = gtk.ListStore(gobject.TYPE_STRING)
        self.set_model(model)
        self.set_text_column(0)
    
        self.child.connect('changed', self.entry_changed)

        if rows:
            self.set_rows(rows)

    def set_rows(self, rows, active = -1):
        if rows:
            model = self.get_model()
            model.clear()
            for row in rows:
                model.append(row)
            self.set_active(active)

    def entry_changed(self, widget):
        print 'text changed:', widget.get_text()
        self.popup()
        widget.grab_focus()
