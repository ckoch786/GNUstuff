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

import MySQLdb
import install
import warnings

class Database:
    _shared_state = {}
    def __init__( self, uname=None, pword=None):
        self.__dict__ = self._shared_state
        if self._shared_state:
            return

	# supress warning on "DROP TABLE IF EXISTS" for temp tables
        warnings.filterwarnings("ignore", "Unknown table.*_temp")
        
        self.db = MySQLdb.Connect( user=uname, passwd=pword)

#        self.cursor = self.db.cursor( MySQLdb.cursors.CursorNW)
	self.cursor = self.db.cursor( )
        self.user = uname

#    def connect( self, uname, pword):
#        try:
#            self.db = MySQLdb.Connect( user=uname, passwd=pword)
#            self.cursor = self.db.cursor()
#            self.user = uname
#        except:
#            return 0
#        return 1

    def change_user( self, uname, pword, dbase): 
        try:
            self.db = MySQLdb.Connect( user=uname, passwd=pword, db=dbase)
            self.cursor = self.db.cursor()
            self.user = uname
        except:
            return 0
        return 1

    def initialize( self):
        try:
            self.cursor.execute( 'SHOW DATABASES')
            list_db = self.cursor.fetchall()
        except:
#            import sys
#            import traceback
#            traceback.print_exc()
#            sys.exit()
            pass

        match = 0
        for b in list_db:
            if b[0] == 'gnutr_db':
                match = 1
        if match == 1: 
            return 0

        self.query( 'CREATE DATABASE gnutr_db')
        self.query( 'USE gnutr_db')

        # create fd_group table
        self.create_load_table( "CREATE TABLE fd_group " + 
            "( fd_gp SMALLINT( 4) UNSIGNED NOT NULL, " + 
            "gp_desc CHAR( 60) NOT NULL, " + 
            "INDEX (fd_gp)) " +
            "ENGINE=InnoDB", 'fd_group')

        # create measure table
        self.create_load_table( "CREATE TABLE measure " + 
            "( msre_no MEDIUMINT( 5) UNSIGNED NOT NULL, " + 
            "msre_desc CHAR( 120) NOT NULL, " + 
            "INDEX( msre_no) ) " +
            "ENGINE=InnoDB", 'measure')

        # create nutr_def table
        self.create_load_table( "CREATE TABLE nutr_def " + 
            "( nutr_no SMALLINT(3) UNSIGNED NOT NULL, " + 
            "units CHAR(6) NOT NULL, " +
            "tagname CHAR(20) NOT NULL, " +
            "nutr_desc CHAR(60) NOT NULL, " +
            "INDEX (nutr_no) ) " +
            "ENGINE=InnoDB", 'nutr_def')

        # create food_des table
        self.create_load_table( "CREATE TABLE food_des " +
            "( fd_no SMALLINT( 5) UNSIGNED NOT NULL, " + 
            "fd_gp SMALLINT( 4) UNSIGNED NOT NULL, " + 
            "fd_desc CHAR( 200) NOT NULL, " + 
            "short_desc CHAR( 60) NOT NULL, " + 
            "refuse_desc CHAR( 45), " + 
            "refuse FLOAT( 2,0), " + 
            "sci_name CHAR( 60), " + 
            "n_factor FLOAT( 5,3), " + 
            "pro_factor FLOAT( 5,3), " + 
            "fat_factor FLOAT( 5,3), " + 
            "cho_factor FLOAT( 5,3), " + 
            "INDEX (fd_no), INDEX (fd_gp) " +
#            ",CONSTRAINT fk_food_des_fd_group FOREIGN KEY fk_food_des_fd_gp (fd_gp) REFERENCES fd_group(fd_gp)) " +
            ") ENGINE=InnoDB", 'food_des')

        # create nut_data table
        self.create_load_table( "CREATE TABLE nut_data " + 
            "( fd_no SMALLINT( 5) UNSIGNED NOT NULL, " + 
            "nutr_no SMALLINT( 3) UNSIGNED NOT NULL, " + 
            "nutr_val FLOAT( 10,3) NOT NULL, " + 
            "sample_ct FLOAT( 5,0) NOT NULL, " + 
            "std_error FLOAT( 8,3), " + 
            "src_cd CHAR( 2) NOT NULL, " +
            "INDEX (fd_no, nutr_no) " +
#            ",CONSTRAINT fk_nut_data_food_des FOREIGN KEY (fd_no) REFERENCES food_des(fd_no), " +
#            "CONSTRAINT fk_nut_data_nutr_def FOREIGN KEY (fd_no) REFERENCES nutr_def(nutr_no) " +
            ") " +
            "ENGINE=InnoDB", 'nut_data')

        # create weight table
        self.create_load_table( "CREATE TABLE weight " +
            "( fd_no SMALLINT(5) UNSIGNED NOT NULL, " +
            "msre_no MEDIUMINT(5) UNSIGNED NOT NULL, " +
            "wgt_val FLOAT(9,2), " +
            "INDEX (fd_no, msre_no) " +
#            ",CONSTRAINT fk_weight_measure FOREIGN KEY (msre_no) REFERENCES measure(msre_no) " +
            ")ENGINE=InnoDB", 'weight')

        # create recipe table
        self.create_table( "CREATE TABLE recipe " +
            "( recipe_no MEDIUMINT(6) UNSIGNED NOT NULL AUTO_INCREMENT, " +
            "recipe_name CHAR(200) NOT NULL, " +
            "no_serv SMALLINT(4) UNSIGNED NOT NULL, " +
            "no_ingr SMALLINT(4) UNSIGNED NOT NULL, " +
            "category_no TINYINT(3) UNSIGNED NOT NULL, " +
            "PRIMARY KEY (recipe_no), " +
            "INDEX (recipe_name( 20), category_no)) " +
            "ENGINE=InnoDB")

        # create ingredient table
        self.create_table( "CREATE TABLE ingredient " + 
            "( recipe_no MEDIUMINT(6) NOT NULL, " + 
            "amount FLOAT(7,2) NOT NULL, " +
            "msre_no MEDIUMINT(5) UNSIGNED NOT NULL, " +
            "fd_no SMALLINT(5) UNSIGNED NOT NULL, " +
            "INDEX (recipe_no)) " +
            "ENGINE=InnoDB")

        # create recipe category table
        self.create_load_table( "CREATE TABLE category " +
            "( category_no TINYINT(3) UNSIGNED NOT NULL, " +
            "category_desc CHAR(40) NOT NULL, " +
            "INDEX (category_no)) " +
            "ENGINE=InnoDB", 'category')

        # create recipe preparation table
        self.create_table( "CREATE TABLE preparation " +
            "( recipe_no MEDIUMINT( 6) UNSIGNED NOT NULL, " +
            "prep_time CHAR( 50), " +
            "prep_desc TEXT, " +
            "INDEX (recipe_no)) " +
            "ENGINE=InnoDB")

        # create person table
        self.create_table( "CREATE TABLE person " +
            "( person_no SMALLINT(6) UNSIGNED NOT NULL AUTO_INCREMENT " +
            "PRIMARY KEY, " +
            "person_name CHAR(100), INDEX person_name (person_name(10)), " +
            "user_name CHAR(50)) " +
            "ENGINE=InnoDB")

        # create food_plan table
        self.create_table( "CREATE TABLE food_plan " +
            "( person_no SMALLINT(6) UNSIGNED NOT NULL, " +
            "date DATE NOT NULL, " +
            "time TIME NOT NULL, " +
            "amount FLOAT(7,2) NOT NULL, " +
            "msre_no MEDIUMINT(5) UNSIGNED NOT NULL, " +
            "fd_no SMALLINT(5) UNSIGNED NOT NULL) " +
            "ENGINE=InnoDB")

        # create recipe_plan table
        self.create_table( "CREATE TABLE recipe_plan " +
            "( person_no SMALLINT(6) UNSIGNED NOT NULL, " +
            "date DATE NOT NULL, " +
            "time TIME NOT NULL, " +
            "no_portions FLOAT(7,2) NOT NULL, " +
            "recipe_no MEDIUMINT(6) UNSIGNED NOT NULL) " +
            "ENGINE=InnoDB")

        # create nutr_goal table
        self.create_table( "CREATE TABLE nutr_goal " +
            "( person_no SMALLINT(6) UNSIGNED NOT NULL, " +
            "nutr_no SMALLINT(3) UNSIGNED NOT NULL, " +
            "goal_val FLOAT(11,4) NOT NULL) " +
            "ENGINE=InnoDB")
        self.cursor.close()
        self.cursor = self.db.cursor()
        return 1

    def query( self, query):
        try:
            self.cursor.execute( query)
        except MySQLdb.Error, sqlerr:
            print 'Error :', sqlerr, '\nquery:', query

            self.cursor.execute('SHOW ERRORS');
            print self.get_result()
            import traceback
            import sys
            traceback.print_exc()
            sys.exit()
    def get_result( self):
        result = self.cursor.fetchall()
        if not result:
            print 'No result'
        return result

    def get_row_result( self):
        result = self.cursor.fetchall()
        if not result:
            print 'No result'
            return None
        if len( result) == 1:
            return result[0]
        print 'Error: not a single row'
        return None

    def get_single_result( self):
        result = self.cursor.fetchall()
        if not result:
            print 'No result'
            return None
        if len( result) == 1:
            if len( result[0] ) == 1:
                return result[0][0]
        print 'Error: not a single value'
        return None

    def create_table( self, query):
        self.query( query)

    def create_load_table( self, query, table):
        self.query( query)
        fn = install.dir + '/data/' + table + '.txt'
        self.query( "LOAD DATA LOCAL INFILE '"+ fn + "' " +
            "INTO TABLE " + table + " FIELDS TERMINATED BY '^'")
        print "table created: ", table

    def add_user( self, user, password):
        self.query( "GRANT USAGE ON *.* TO " + user +
            "@localhost IDENTIFIED BY '" + password + "'")
        self.query( "GRANT ALL ON gnutr_db.* TO " + user + 
            "@localhost IDENTIFIED BY '" + password + "'")
        self.query( "FLUSH PRIVILEGES")

    def delete_db( self):
        self.query( "DROP DATABASE gnutr_db")
