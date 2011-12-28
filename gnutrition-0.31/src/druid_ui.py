# gnutrition - a nutrition and diet analysis program.
# Copyright( C) 2000-2002 Edgar Denny (edenny@skyweb.net)
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
import getpass

class DruidPage:
    def __init__( self, page_num):
        self.vbox = gtk.VBox()
        self.vbox.set_border_width( 5)

        # Welcome
        if page_num == 0:
            label1 = gtk.Label( 'Welcome to Gnutrition!')
            label1.set_alignment( 0.0, 0.5)
            self.vbox.pack_start( label1, False, False, 5)

            label2 = gtk.Label( 'You seem to be running Gnutrition for the first time.\n\nThe following steps will set up Gnutrition by asking a few simple questions. Before you start, you will need to have the MySQL database system installed in your system. You will also need to know the MySQL root username and password.')
            label2.set_alignment( 0.0, 0.5)
            label2.set_line_wrap( True)
            label2.set_justify( gtk.JUSTIFY_FILL)
            self.vbox.pack_start( label2, False, False, 5)

        # Database Create
        elif page_num == 1:
            table1 = gtk.Table( 2, 5, False)
            table1.set_row_spacings( 5)
            table1.set_col_spacings( 5)
            self.vbox.pack_start( table1, True, True, 0)

            label1 = gtk.Label( 'Database Creation.') 
            label1.set_alignment( 0.0, 0.5)
            table1.attach( label1, 0, 2, 0, 1, gtk.FILL, 0, 0, 0)

            label2 = gtk.Label( 
                'Enter the root username and password for MySQL.') 
            label2.set_alignment( 0.0, 0.5)
            table1.attach( label2, 0, 2, 1, 2, gtk.FILL, 0, 0, 0)

            label3 = gtk.Label( 'MySQL root username') 
            label3.set_alignment( 1.0, 0.5)
            table1.attach( label3, 0, 1, 2, 3, gtk.FILL, 0, 0, 0)

            self.root_user_entry = gtk.Entry()
            table1.attach( self.root_user_entry, 1, 2, 2, 3, 
                gtk.FILL | gtk.EXPAND, 0, 0, 0)

            label4 = gtk.Label( 'MySQL root password') 
            label4.set_alignment( 1.0, 0.5)
            table1.attach( label4, 0, 1, 3, 4, gtk.FILL, 0, 0, 0)

            self.root_pass_entry = gtk.Entry()
            self.root_pass_entry.set_visibility( False);
            table1.attach( self.root_pass_entry, 1, 2, 3, 4, 
                gtk.FILL | gtk.EXPAND, 0, 0, 0)

            label5 = gtk.Label( 'When you press the "Next" button Gnutrition will check to see if the Gnutrition Database is already installed. If not, Gnutrition will install it for you.') 
            label5.set_alignment( 0.0, 0.5)
            label5.set_line_wrap( True)
            label5.set_justify( gtk.JUSTIFY_FILL)
            table1.attach( label5, 0, 2, 4, 5, gtk.FILL, 0, 0, 0)

            label6 = gtk.Label( 'This may take some time.') 
            label6.set_alignment( 0.0, 0.5)
            table1.attach( label6, 0, 2, 5, 6, gtk.FILL, 0, 0, 0)

        # Error in Database Creation
        elif page_num == 2:
            label1 = gtk.Label( 'Error: Database Creation Failed!')
            label1.set_alignment( 0.0, 0.5)
            self.vbox.pack_start( label1, False, False, 5)

            label2 = gtk.Label( 'The installation of the Gnutrition Database has failed.')
            label2.set_alignment( 0.0, 0.5)
            self.vbox.pack_start( label2, False, False, 5)

            label2 = gtk.Label( 'Please go back and check that the MySQL root username and password are correct.')
            label2.set_alignment( 0.0, 0.5)
            label2.set_line_wrap( True)
            self.vbox.pack_start( label2, False, False, 5)

        # User Setup
        elif page_num == 3:
            table1 = gtk.Table( 2, 4, False)
            table1.set_row_spacings( 5)
            table1.set_col_spacings( 5)
            self.vbox.pack_start( table1, True, True, 0)

            label1 = gtk.Label( 'User Setup.')
            label1.set_alignment( 0.0, 0.5)
            table1.attach( label1, 0, 2, 0, 1, gtk.FILL, 0, 0, 0)

            label2 = gtk.Label( 'In order to access the database you need to create a normal MySQL username and password. Specify your choice below. Gnutrition will remember them for you.')
            label2.set_alignment( 0.0, 0.5)
            label2.set_line_wrap( True)
            label2.set_justify( gtk.JUSTIFY_FILL)
            table1.attach( label2, 0, 2, 1, 2, gtk.FILL, 0, 0, 0)

            label3 = gtk.Label( 'MySQL username') 
            label3.set_alignment( 1.0, 0.5)
            table1.attach( label3, 0, 1, 2, 3, gtk.FILL, 0, 0, 0)

            self.user_entry = gtk.Entry()
            self.user_entry.set_text( getpass.getuser())
            table1.attach( self.user_entry, 1, 2, 2, 3, 
                gtk.FILL | gtk.EXPAND, 0, 0, 0)

            label4 = gtk.Label( 'MySQL password') 
            label4.set_alignment( 1.0, 0.5)
            table1.attach( label4, 0, 1, 3, 4, gtk.FILL, 0, 0, 0)

            self.pass_entry = gtk.Entry()
            self.pass_entry.set_visibility( False)
            table1.attach( self.pass_entry, 1, 2, 3, 4, 
                gtk.FILL | gtk.EXPAND, 0, 0, 0)

        # Error in User Setup
        elif page_num == 4:
            label1 = gtk.Label( 'Error: User Setup Failed.')
            label1.set_alignment( 0.0, 0.5)
            self.vbox.pack_start( label1, False, False, 5)

            label2 = gtk.Label( 'Unable to connect to the database.')
            label2.set_alignment( 0.0, 0.5)
            self.vbox.pack_start( label2, False, False, 5)

            label3 = gtk.Label( 'If you have connected to the database before, go back to the previous page and check that your password is correct.')
            label3.set_alignment( 0.0, 0.5)
            label3.set_line_wrap( True)
            label3.set_justify( gtk.JUSTIFY_FILL)
            self.vbox.pack_start( label3, False, False, 5)

            label4 = gtk.Label( 'If you are connecting to the database for the very first time, it may be that someone else has already chosen the same user name as you. Try going back and chosing another one.')
            label4.set_alignment( 0.0, 0.5)
            label4.set_line_wrap( True)
            label4.set_justify( gtk.JUSTIFY_FILL)
            self.vbox.pack_start( label4, False, False, 5)

        # Personal Details
        elif page_num == 5:
            table1 = gtk.Table( 3, 7, False)
            table1.set_row_spacings( 5)
            table1.set_col_spacings( 5)
            self.vbox.pack_start( table1, True, True, 0)

            label1 = gtk.Label( 'Personal Details.')
            label1.set_alignment( 0.0, 0.5)
            table1.attach( label1, 0, 3, 0, 1, gtk.FILL, 0, 0, 0)

            label2 = gtk.Label( 'Gnutrition will compute a recommended dietary intake for you, based upon your age and weight. Later, you may adjust the computed values to suit you own personal goals.')
            label2.set_alignment( 0.0, 0.5)
            label2.set_line_wrap( True)
            label2.set_justify( gtk.JUSTIFY_FILL)
            table1.attach( label2, 0, 3, 1, 2, gtk.FILL, 0, 0, 0)

            label3 = gtk.Label( 'Name')
            label3.set_alignment( 1.0, 0.5)
            table1.attach( label3, 0, 1, 2, 3, gtk.FILL, 0, 0, 0)

            self.name_entry = gtk.Entry()
            table1.attach( self.name_entry, 1, 2, 2, 3, 
                gtk.FILL | gtk.EXPAND, 0, 0, 0)

            label4 = gtk.Label( 'Age')
            label4.set_alignment( 1.0, 0.5)
            table1.attach( label4, 0, 1, 3, 4, gtk.FILL, 0, 0, 0)

            self.age_entry = gtk.Entry()
            table1.attach( self.age_entry, 1, 2, 3, 4, 
                gtk.FILL | gtk.EXPAND, 0, 0, 0)

            label5 = gtk.Label( 'Weight')
            label5.set_alignment( 1.0, 0.5)
            table1.attach( label5, 0, 1, 4, 5, gtk.FILL, 0, 0, 0)

            self.weight_entry = gtk.Entry()
            table1.attach( self.weight_entry, 1, 2, 4, 5, 
                gtk.FILL | gtk.EXPAND, 0, 0, 0)

            self.weight_combo = gtk.combo_box_new_text()
            self.weight_combo.append_text('lbs')
            self.weight_combo.append_text('kg')
            self.weight_combo.set_active(0)
            table1.attach( self.weight_combo, 2, 3, 4, 5, 
                0, 0, 0, 0)

            label6 = gtk.Label( 'Gender')
            label6.set_alignment( 1.0, 0.5)
            table1.attach( label6, 0, 1, 5, 6, gtk.FILL, 0, 0, 0)

            hbox1 = gtk.HBox()
            self.male_button = gtk.RadioButton( None, 'Male')
            hbox1.pack_start( self.male_button, False, False, 0)
            self.female_button = gtk.RadioButton( self.male_button, 'Female')
            hbox1.pack_start( self.female_button, False, False, 0)
            table1.attach( hbox1, 1, 3, 5, 6, gtk.FILL, 0, 0, 0)
            self.male_button.set_active( True)

            label7 = gtk.Label( 'Pysiology')
            label7.set_alignment( 1.0, 0.5)
            table1.attach( label7, 0, 1, 6, 7, gtk.FILL, 0, 0, 0)

            self.physiol_hbox = gtk.HBox()
            self.preg_button = gtk.RadioButton( None, 'Pregnant')
            self.physiol_hbox.pack_start( self.preg_button, 
                False, False, 0)
            self.lac_button = gtk.RadioButton( self.preg_button, 'Lactating')
            self.physiol_hbox.pack_start( self.lac_button, 
                False, False, 0)
            self.neither_button = gtk.RadioButton( self.preg_button, 'Neither')
            self.physiol_hbox.pack_start( self.neither_button, 
                False, False, 0)
            table1.attach( self.physiol_hbox, 1, 3, 6, 7, gtk.FILL, 0, 0, 0)

            self.male_button.connect( 'toggled', self.on_male_button_toggled)
            self.on_male_button_toggled( None)

        # Error in Personal Details
        elif page_num == 6:
            label1 = gtk.Label( 'Error: Personal Details Setup Failed.')
            label1.set_alignment( 0.0, 0.5)
            self.vbox.pack_start( label1, False, False, 5)

            label2 = gtk.Label( 'The name you have chosen in the Personal Details page is already in the database for another user.')
            label2.set_alignment( 0.0, 0.5)
            label2.set_line_wrap( True)
            label2.set_justify( gtk.JUSTIFY_FILL)
            self.vbox.pack_start( label2, False, False, 5)

            label2 = gtk.Label( 'Please go back and select another Name.')
            label2.set_alignment( 0.0, 0.5)
            self.vbox.pack_start( label2, False, False, 5)

        # Finish
        elif page_num == 7:
            label1 = gtk.Label( 'Gnutrition has been successfully set up.')
            label1.set_alignment( 0.0, 0.5)
            self.vbox.pack_start( label1, False, False, 5)

            label2 = gtk.Label( 'Now press the "Finish" button to start Gnutrition.')
            label2.set_alignment( 0.0, 0.5)
            self.vbox.pack_start( label2, False, False, 5)

        self.vbox.show_all()

    def on_male_button_toggled( self, w, d=None):
        if self.male_button.get_active():
            self.physiol_hbox.set_sensitive( False)
        else:
            self.physiol_hbox.set_sensitive( True)

class DruidUI:
    def __init__( self):
        self.dialog = gtk.Window()
        self.dialog.set_title( 'Gnutrition Druid')
        self.page_num = 0

        vbox1 = gtk.VBox( False, 0)
        vbox1.set_border_width( 2)
        self.dialog.add( vbox1)

        self.container = gtk.VBox()
        self.container.set_border_width( 5)
        vbox1.pack_start( self.container, True, True, 0)

        hsep1 = gtk.HSeparator()
        vbox1.pack_start( hsep1, False, False, 1)

        hbox1 = gtk.HBox( False, 0)
        vbox1.pack_start( hbox1, False, False, 0)

        hbox2 = gtk.HBox( False, 0)
        hbox2.set_border_width( 5)
        hbox1.pack_start( hbox2, True, True, 0)

        self.back_button = gtk.Button()
        button_hbox1 = gtk.HBox( False, 0)
        self.back_button.add( button_hbox1)
        button_icon1 = gtk.Image()
        button_icon1.set_from_stock( 'gtk-go-back', gtk.ICON_SIZE_BUTTON)
        button_hbox1.pack_start( button_icon1, False, False, 0)
        button_label1 = gtk.Label( 'Back')
        button_label1.set_padding( 5, 0)
        button_hbox1.pack_start( button_label1, False, False, 0)
        hbox2.pack_start( self.back_button, False, False, 0)

        self.next_button = gtk.Button()
        self.set_next_button( 0)
        hbox2.pack_start( self.next_button, False, False, 0)

        hbox3 = gtk.HBox( False, 0)
        hbox3.set_border_width( 5)
        hbox1.pack_start( hbox3, False, False, 0)

        self.cancel_button = gtk.Button( stock=gtk.STOCK_CANCEL)
        hbox3.pack_start( self.cancel_button, False, False, 0)

        self.connect_signals()

        self.page_list = []
        for num in range( 8):
            page = DruidPage( num)
            self.page_list.append( page)

        self.back_button.set_sensitive( False)
        self.container.pack_start( self.page_list[0].vbox, True,
            True, 0)

    def connect_signals( self):
        self.dialog.connect( 'destroy', self.on_destroy)

    def on_destroy( self, w, d=None):
        gtk.main_quit()

    def set_page( self, num):
        self.container.remove( self.page_list[self.page_num].vbox)
        self.back_button.set_sensitive( True)
        self.next_button.set_sensitive( True)
        if num == 7:
            self.next_button.remove( self.button_hbox2)
            self.set_next_button( 1)
        else:
            self.next_button.remove( self.button_hbox2)
            self.set_next_button( 0)
        if num == 0:
            self.back_button.set_sensitive( False)
        if num in [ 2, 4, 6]:
            self.next_button.set_sensitive( False)
        self.container.pack_start( self.page_list[num].vbox, 
            True, True, 0)
        self.page_num = num

    def set_next_button( self, flag):
        self.button_hbox2 = gtk.HBox( False, 0)
        self.next_button.add( self.button_hbox2)
        button_icon = gtk.Image()
        if flag == 0:
            button_icon.set_from_stock( 'gtk-go-forward', gtk.ICON_SIZE_BUTTON)
            button_label = gtk.Label( 'Next')
        elif flag == 1:
            button_icon.set_from_stock( 'gtk-apply', gtk.ICON_SIZE_BUTTON)
            button_label = gtk.Label( 'Finish')

        self.button_hbox2.pack_start( button_icon, False, False, 0)
        button_label.set_padding( 5, 0)
        self.button_hbox2.pack_start( button_label, False, False, 0)
        self.next_button.show_all()
