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
import druid_ui
import config
import person
import calc_rdi
import database
import nutr_goal_dlg

class Druid:
    def __init__( self, app):
        self.app = app
        self.ui = druid_ui.DruidUI()
        self.connect_signals()

    def connect_signals( self):
        self.ui.cancel_button.connect( 'clicked', self.on_cancel)
        self.ui.next_button.connect( 'clicked', self.on_next)
        self.ui.back_button.connect( 'clicked', self.on_back)

    def show( self):
        self.ui.dialog.show_all()

    def on_cancel( self, w, d=None):
        self.ui.dialog.hide()
        gtk.main_quit()
        return 0

    def on_next( self, w, d=None):
        if self.ui.page_num == 0:
            self.ui.set_page( 1)

        # Database Create
        elif self.ui.page_num == 1:
            uname = self.ui.page_list[1].root_user_entry.get_text()
            pword = self.ui.page_list[1].root_pass_entry.get_text()
            if (not uname) or (not pword):
                return
            try:
                self.db = database.Database( uname, pword)
            except Exception, ex:
                self.ui.set_page(2)
                return
            
            self.db.initialize()
            
            # no error, so skip over page_db_error
            self.ui.set_page( 3)
            return

        # User Setup
        elif self.ui.page_num == 3:
            uname = self.ui.page_list[3].user_entry.get_text()
            pword = self.ui.page_list[3].pass_entry.get_text()
            if (not uname) or (not pword):
                return
            success = self.user_setup( uname, pword)
            if not success:
                self.ui.set_page( 4)
                return
            self.db.change_user( uname, pword, 'gnutr_db')

            # does the user have an entry in the person table?
            self.person = person.Person()
            person_name = self.person.get_name( uname)
            if person_name:
                config.set_key_value( 'Name', person_name)
                self.person.setup()

                self.ui.set_page( 7)
                return
            self.ui.set_page( 5)
            return

        # Personal details
        elif self.ui.page_num == 5:
            name = self.ui.page_list[5].name_entry.get_text()
            age = self.ui.page_list[5].age_entry.get_text()
            weight_txt = self.ui.page_list[5].weight_entry.get_text()
            if (not name) or (not age) or (not weight_txt):
                return
            weight = float( weight_txt)

            config.set_key_value( 'Name', name)
            self.person.add_name( name)
            self.person.setup()

            if self.ui.page_list[5].weight_combo.get_active() == 0:
                # convert from pounds to kilos
                weight = weight * 0.4536
            female = self.ui.page_list[5].female_button.get_active()
            if female == 1:
                pregnant = self.ui.page_list[5].preg_button.get_active()
                lactating = self.ui.page_list[5].lac_button.get_active()
            else:
                pregnant = 0
                lactating = 0

            list = calc_rdi.compute( age, weight, female, pregnant, lactating)
            self.nutr_goal_dlg = nutr_goal_dlg.NutrGoalDlg()
            self.nutr_goal_dlg.save_goal( list)

            self.ui.set_page( 7)
            return

        # Finish
        elif self.ui.page_num == 7:
            self.ui.dialog.hide()
            self.app.startup()
           
    def user_setup( self, uname, pword):
        # check to see if user name is already in mysql.user and that the
        # password is correct
        if self.user_name_exists( uname):
            if self.password_match( uname, pword):
                # add the info to the config file.
                config.set_key_value( 'Username', uname)
                config.set_key_value( 'Password', pword)
                # check to see if user can access 'gnutr_db'
                if not self.user_db_access( uname):
                    # grant privileges to user
                    self.db.add_user( uname, pword)
            else:
                return 0
        else:
            self.db.add_user( uname, pword)
            config.set_key_value( 'Username', uname)
            config.set_key_value( 'Password', pword)
        return 1

    def user_name_exists( self, uname):
        self.db.query( "USE mysql")
        self.db.query( "SELECT User FROM user WHERE " +
            "User = '" + uname + "'")
        name = self.db.get_single_result()
        if not name:
            return 0
        return 1

    def password_match( self, uname, pword):
        # check to see if the password is correct
        self.db.query( "SELECT Password FROM user WHERE " +
            "User = '" + str( uname) + "'")
        result1 = self.db.get_single_result()
        self.db.query( "SELECT PASSWORD( '" + str( pword) + "')")
        result2 = self.db.get_single_result()
        if result1 == result2:
            return 1;
        return 0

    def user_db_access( self, uname):
        # does the user have access to the gnutr_db?
        self.db.query( "SELECT Db FROM db WHERE " +
            "User = '" + str( uname) + "'")
        result = self.db.get_result()
        for db_name in result:
            if db_name[0] == 'gnutr_db':
                return 1
        return 0

    def on_back( self, w, d=None):
        # skip back over page_db_error
        if self.ui.page_num == 3:
            self.ui.set_page( 1)
        elif self.ui.page_num == 5:
            self.ui.set_page( 3)
        elif self.ui.page_num == 7:
            self.ui.set_page( 5)
        else:
            self.ui.set_page( self.ui.page_num - 1)
