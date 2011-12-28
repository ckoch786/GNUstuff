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

import config
import gtk

class RunApp:
    def __init__( self):
        if not config.get_value( 'Name'):
            import druid
            self.druid = druid.Druid( self)
            self.druid.show()
        else:
            self.startup()


    def startup( self):
        db_uname = config.get_value( 'Username')
        db_pword = config.get_value( 'Password')

        import database 
        self.db = database.Database( db_uname, db_pword)
        success = self.db.change_user( db_uname, db_pword, 'gnutr_db')

        if success == 0:
            import gnutr
            import sys
            gnutr.Dialog( 'error', 
                'Failed to connect to the database.\n\n' +
                'I suggest that you delete the file\n ' +
                '"~/.gnutrition/config" and run "gnutrition" again.')
            gtk.main_quit()
            sys.exit()

        import store
        self.store = store.Store()

        import person
        self.person = person.Person()
        self.person.setup()

        import base_win
        self.base_win = base_win.BaseWin( self)
        self.base_win.show()

def run_app():
    app = RunApp()
    gtk.main()

run_app()
