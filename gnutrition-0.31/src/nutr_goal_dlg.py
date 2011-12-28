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
import nutr_goal_dlg_ui
import gnutr
import person
import help

class NutrGoalDlg:
    def __init__( self):
        self.ui = nutr_goal_dlg_ui.NutrientGoalDlgUI()
        self.connect_signals()
        self.person = person.Person()

    def connect_signals( self):
        self.ui.dialog.connect( 'response', self.on_response)

    def show( self):
        goal_list = self.get_goal()

        for nutr in self.ui.nutr_list:
            nutr.entry.set_text( '0.000')

        for goal_num, goal_val in goal_list:
            for nutr in self.ui.nutr_list:
                if nutr.num == goal_num:
                    nutr.entry.set_text( '%.3f' %( goal_val))
        self.ui.dialog.vbox.show_all()
        self.ui.dialog.run()

    def on_response( self, w, r, d=None):
        if r == gtk.RESPONSE_CANCEL or r == gtk.RESPONSE_DELETE_EVENT: 
            self.ui.dialog.hide()

        elif r == 1:    #save
            goal_list = []
            for nutr in self.ui.nutr_list:
                try:
                    val = float( nutr.entry.get_text())
                except:
                    gnutr.Dialog( 'error', 
                        'Save Failed: A nutrient goal entry\nis not a number.')
                    return
                goal_list.append( ( nutr.num, val))
            self.save_goal( goal_list)

        elif r == gtk.RESPONSE_HELP:
            help.open( '')

    def get_goal( self):
        person_no = self.person.get_person_num()

        self.person.db.query( "SELECT nutr_no, goal_val FROM nutr_goal " + 
            "WHERE person_no = '%d'" % ( person_no))
        goal_list = self.person.db.get_result()

        return goal_list

    def save_goal( self, goal_list):
        person_num = self.person.get_person_num()

        # delete the old goals if necessary
        self.person.db.query( "DELETE FROM nutr_goal " +
            "WHERE person_no = '%d'" % ( person_num))

        for nutr_num, nutr_val in goal_list:
            self.person.db.query( "INSERT INTO nutr_goal VALUES " +
                "('%d', '%d', '%f')" % ( person_num, int(nutr_num), float(nutr_val)))
