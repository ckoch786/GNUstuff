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

import database

class Store:
    _shared_state = {}
    def __init__( self):
        self.__dict__ = self._shared_state
        if self._shared_state:
            return
        self.cat_desc2num = {}
        self.cat_num2desc = {}
        self.cat_desc_list = []
        self.nutr_num_list = []
        self.nutr_desc_list = []
        self.fg_desc_list = []
        self.nutr_desc2num = {} 
        self.nutr_num2desc = {} 
        self.fg_desc2num = {} 
        self.fd_desc2num = {} 
        self.fd_num2desc = {} 
        self.msre_num2desc = {} 
        self.msre_desc2num = {} 

        self.db = database.Database()

        self.create_nutr_num_list()
        self.create_nutr_desc_list()
        self.create_cat_desc_list()
        self.create_fd_group_desc_list()
        self.create_nutr_desc_nutr_no_dict()
        self.create_fd_gp_desc_fd_gp_no_dict()
        self.create_fd_desc_fd_no_dict()
        self.create_msre_no_msre_desc_dict()
        self.create_cat_desc_cat_no_dict()

    def create_cat_desc_cat_no_dict( self):
        self.cat_desc2num['All'] = 0
        self.cat_num2desc[0] = 'All'
        self.db.query( "SELECT category_no, category_desc FROM " +
            "category")
        result = self.db.get_result()
        for num, desc in result:
            self.cat_desc2num[desc] = num
            self.cat_num2desc[num] = desc

    def create_cat_desc_list( self):
        self.db.query( "SELECT category_desc FROM category")
        result = self.db.get_result()
        self.cat_desc_tuple = (('All',),) + result
        self.cat_desc_list.append( 'All')
        for desc in result:
            self.cat_desc_list.append( desc[0])

    def create_nutr_num_list( self):
        self.db.query( "SELECT nutr_no FROM nutr_def")
        result = self.db.get_result()
        for num_tuple in result:
            self.nutr_num_list.append( num_tuple[0])
    
    def create_nutr_desc_list( self):
        self.db.query( "SELECT nutr_desc FROM nutr_def")
        result = self.db.get_result()
        self.nutr_desc_tuples = result
        for desc in result:
            self.nutr_desc_list.append( desc[0])

    def create_fd_group_desc_list( self):
        self.db.query( "SELECT gp_desc FROM fd_group")
        result = self.db.get_result()
        self.fg_desc_tuple = (('All Foods',),) + result
        for desc_tuple in result:
            self.fg_desc_list.append( desc_tuple[0])
        self.fg_desc_list.insert( 0, 'All Foods')

    def create_nutr_desc_nutr_no_dict( self):
        self.db.query( "SELECT nutr_no, nutr_desc FROM nutr_def")
        result = self.db.get_result()
        for num, desc in result:
            self.nutr_desc2num[desc] = num
            self.nutr_num2desc[num] = desc

    def create_fd_gp_desc_fd_gp_no_dict( self):
        self.db.query( "SELECT fd_gp, gp_desc FROM fd_group")
        result = self.db.get_result()
        for num, desc in result:
            self.fg_desc2num[desc] = num

    def create_fd_desc_fd_no_dict( self):
        self.db.query( "SELECT fd_no, fd_desc FROM food_des")
        result = self.db.get_result()
        for num, desc in result:
            self.fd_desc2num[desc] = num
            self.fd_num2desc[num] = desc

    def get_msre_desc_tuples( self, fd_num):
        self.db.query( "SELECT msre_desc FROM measure, weight WHERE " +
            "weight.fd_no = '%d' AND measure.msre_no = weight.msre_no" 
            %( fd_num))
        result = self.db.get_result()
        return (('gm',),) + result
    
    def create_msre_no_msre_desc_dict( self):
        self.db.query( "SELECT msre_no, msre_desc FROM measure")
        result = self.db.get_result()
        for num, desc in result:
            self.msre_num2desc[num] = desc
            self.msre_desc2num[desc] = num
        self.msre_num2desc[99999] = 'gm'
        self.msre_desc2num['gm'] = 99999
