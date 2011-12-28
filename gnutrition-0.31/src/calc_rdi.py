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
#

# Ian's code to compute the RDIs

# General RDI tables 
# Reference: Bender, D.A. and Bender, A.E., `Nutrition: a reference handbook'
# 1st ed., Oxford University Press, 1997, ISBN 0-19-262368-0. All page numbers
# are for this book 
# Unless otherwise stated, American values are chosen where Bender gives
# a choice, and the lower value is generally chosen where a range is
# given.
# FIXME: more data on cholesterol, fatty acids and fibre
# FIXME: wouldn't it be better to put all this into a database table?

factor = {
    'CHO': 2, 'FAT': 1, 'ENERGY': 9, 'SUGAR': 10, 'M_UNSAT_FAT': 76,
    'P_UNSAT_FAT': 77, 'SAT_FAT': 52, 'LINO': 63, 'A_LINO': 64, 'MET': 38,
    'CYS': 39, 'PHE': 40, 'TYR': 41, 'EN_KCAL': 4, 'KJ2KCAL': 0.24,
    'EN_CHO': 4.27, 'EN_FAT': 9.0 
}

# energy consumption varies according to activity. Values
# presented here represent a "sedentary lifestyle" ;-)
#
# for children: kJ per kg by body weight up to age 10
# for adults: much more interesting. First BMR (basal metabolic rate)
# is computed using the equation A (weight) + B, where A and B are
# dependent upon the age and sex. (pg 82) The BMR is converted into energy
# requirements by a fourth variable C, also age- and sex-dependent (pg 89)*/
#
# energy_dict = {key: value}
# value = [( age, male, female)]
energy_dict = { 
    'child': [ (0, 410, 410), (1, 414, 431), (2, 414, 406), 
        (3, 393, 377), (4, 377, 364), (5, 364, 352), (6, 352, 331),
        (7, 331, 301), (8, 306, 276), (9, 285, 247)],
    'A': [(10, 0.0732, 0.0510), (18, 0.0640, 0.0615), (30, 0.0485, 0.0364),
        (60, 0.0565, 0.0439)],
    'B': [(10, 2.72, 3.12), (18, 2.84, 2.08), (30, 3.67, 3.47),
        (60, 2.04, 2.49)],
    'C': [(10, 1.74, 1.59), (11, 1.67, 1.55), (12, 1.61, 1.51), 
        (13, 1.56, 1.47), (14, 1.49, 1.46), (15, 1.44, 1.47), 
        (16, 1.40, 1.48), (17, 1.40, 1.50), (18, 1.41, 1.42), 
        (60, 1.40, 1.40)] 
}


# rdi_dict = {key: value}
# key = nutr_no
# value =  ( by_weight, pregnancy, lactation, [( age, male, female)])
rdi_dict = {
    203: ( 1, 6, 17.5,
        [ (0.3, 1.85, 1.85), (0.58, 1.65, 1.65), (0.83, 1.48, 1.48),
            (1.0, 1.26, 1.26), (1.5, 1.17, 1.17), (2, 1.13, 1.13),
            (3, 1.09, 1.09), (4, 1.06, 1.06), (5, 1.02, 1.02),
            (6, 1.01, 1.01), (9, 0.99, 0.99), (10, 0.99, 1),
            (11, 0.98, 0.98), (12, 1, 0.96), (13, 0.97, 0.94),
            (14, 0.96, 0.90), (15, 0.92, 0.87), (16, 0.90, 0.83),
            (17, 0.86, 0.80), (18, 0.75, 0.75)] ),
    291: ( 0, 0, 0,
        [ (18, 30, 30)] ),
    301: ( 0, 400, 400,
        [ (0, 400, 400), (0.5, 600, 600), (1, 800, 800), 
            (11, 1200, 1200), (25, 800, 800) ]),
    303: ( 0, 15, 0,
        [ (0, 6, 6), (0.5, 10, 10), (11, 12, 15), 
            (19, 10, 15), (51, 10, 10) ]),
    304: ( 0, 40, 75,
        [ (0, 40, 40), (0.5, 60, 60), (1, 80, 80), (4, 120, 120),
            (7, 170, 170), (11, 270, 280), (15, 400, 300), (19, 350, 280) ]),
    305: ( 0, 400, 400,
        [ (0, 300, 300), (0.5, 500, 500), (1, 800, 800), (11, 1200, 1200),
            (25, 800, 800)]),
    306: ( 0, 0, 0,
        [ (0, 500, 500), (0.5, 700, 700), (1, 1000, 1000), (2, 1400, 1400),
            (6, 1600, 1600), (10, 2000, 2000)]),
    307: ( 0, 0, 0, 
        [ (0, 120, 120), (0.5, 200, 200), (1, 225, 225), (2, 300, 300),
            (6, 400, 400), (10, 500, 500)]),
    309: ( 0, 3, 7,
        [ (0, 5, 5), (1, 10, 10), (11, 15, 12)]),
    312: ( 0, 0, 0.3,
        [ (0, 0.4, 0.4), (0.5, 0.6, 0.6), (1, 0.7, 0.7), (4, 1.0, 1.0),
                         (11, 1.5, 1.5)]),
    315: ( 0, 0, 0, 
        [(0, 0.3, 0.3), (0.5, 0.6, 0.6), (1, 0.7, 0.7), (4, 1.0, 1.0),
                         (11, 1.5, 1.5)]),
    317: ( 0, 10, 20, 
        [(0, 10, 10), (0.5, 15, 15), (1, 20, 20), (7, 30, 30),
                         (11, 40, 45), (15, 50, 50), (19, 70, 55)]),
    392: ( 0, 0, 500,
        [(0, 375, 365), (1, 400, 400), (4, 500, 500), (7, 700, 700),
                         (11, 1000, 800)]),
    394: ( 0, 2, 2,
        [(0, 3, 3), (0.5, 4, 4), (1, 6, 6), (4, 7, 7), (11, 10, 8)]),
    401: ( 0, 10, 35,
        [(0, 30, 30), (0.5, 35, 35), (1, 40, 40), (4, 45, 45),
                         (11, 50, 50), (15, 60, 60)]),
    404: ( 0, 0.4, 0.5,
        [(0, 0.3, 0.3), (0.5, 0.4, 0.4), (1, 0.7, 0.7), (4, 0.9, 0.9),
            (7, 1.0, 1.0), (11, 1.3, 1.1), (15, 1.5, 1.1), (51, 1.2, 1.1),
            (-1, 0, 0)]),
    405: ( 0, 0.3, 0.5,
        [(0, 0.4, 0.4), (0.5, 0.5, 0.5), (1, 0.8, 0.8), (4, 1.1, 1.1),
            (7, 1.2, 1.2), (11, 1.5, 1.3), (15, 1.8, 1.3), (19, 1.7, 1.3),
            (51, 1.4, 1.3)]),
    406: ( 0, 2, 5,
        [(0, 5, 5), (0.5, 6, 6), (1, 9, 9), (4, 12, 12), (7, 13, 13),
            (11, 17, 15), (15, 20, 15), (19, 19, 15), (51, 15, 13)]),
    410: ( 0, 0, 0,
        [(0, 2, 2), (0.5, 3, 3), (7, 4, 4)]),
    415: ( 0, 0.6, 0.5,
        [(0, 0.3, 0.3), (0.5, 0.5, 0.5), (1, 0.7, 0.7), (4, 1.1, 1.1),
            (7, 1.4, 1.4), (11, 1.7, 1.4), (15, 2.0, 1.5), (19, 2.0, 1.6)]),
    417: ( 0, 220, 100,
        [(0, 25, 25), (0.5, 35, 35), (1, 50, 50), (4, 75, 75),
            (7, 100, 100), (11, 150, 150), (15, 200, 180)]),
    418: ( 0, 0.2, 0.6,
        [(0, 0.3, 0.3), (0.5, 0.5, 0.5), (1, 0.7, 0.7), (4, 1, 1),
            (7, 1.4, 1.4), (11, 2.0, 2.0)]),
    501: ( 1, 0, 0,
        [(0.25, 17, 17), (2, 12.5, 12.5), (10, 3.5, 3.5)]),
    502: ( 1, 0, 0,
        [(0.25, 87, 87), (2, 37, 37), (10, 28, 28), (18, 7, 7)]),
    503: ( 1, 0, 0,
        [(0.25, 70, 70), (2, 31, 31), (10, 28, 28), (18, 10, 10)]),
    504: ( 1, 0, 0,
        [(0.25, 161, 161), (2, 73, 73), (10, 44, 44), (18, 14, 14)]),
    505: ( 1, 0, 0,
        [(0.25, 103, 103), (2, 64, 64), (10, 44, 44), (18, 12, 12)]),
    506: ( 1, 0, 0,
        [(0.25, 58, 58), (2, 27, 27), (10, 22, 22), (18, 13, 13)]),
    508: ( 1, 0, 0,
        [(0.25, 125, 125), (2, 69, 69), (10, 22, 22), (18, 14, 14)]),
    510: ( 1, 0, 0,
        [(0.25, 93, 93), (2, 38, 38), (10, 25, 25), (18, 10, 10)]),
    512: ( 1, 0, 0,
        [(0, 8, 8)]),
    601: ( 0, 0, 0,
        [(18, 300, 300)]) 
}

def lookup( age_data_list, age, gender):
    for age_data, man_data, woman_data in age_data_list:
        if age >= age_data:
            if gender == 1:
                value = woman_data
            else:
                value = man_data
    return value
    
def normal_rdi( num, age, weight, female, preg, lac):
    by_weight, pregnancy, lactation, age_data_list = rdi_dict[num]
    value = lookup( age_data_list, age, female)
    if by_weight == 1:
        value = value * weight
    if num >= 501 and num <= 512:
        value = value/1000.0
    if preg == 1:
        value = value + pregnancy
    if lac == 1:
        value = value + lactation
    return value

def energy_intake( age, weight, female):
    if age < 10:
        value = lookup( energy_dict['child'], age, female)
    else:
        bmr = ( ( weight * lookup( energy_dict['A'], age, female)) +
            lookup( energy_dict['B'], age, female))
        value = bmr * lookup( energy_dict['C'], age, female)
    value = value * 1000.0    # values in MJ, want kJ
    return value

def compute( age, weight, female, preg, lac):
    rdi_list = []
    energy = energy_intake( age, weight, female)
    rdi_list.append(('268', str( energy)))                           # kj
    energy = energy * factor['KJ2KCAL']
    rdi_list.append(('208', str( energy)))                           # kcal
    rdi_list.append(('269', str( 0.1 * energy/ factor['EN_CHO'])))   # sugar
    rdi_list.append(('204', str( 0.3 * energy/ factor['EN_FAT'])))   # total
    rdi_list.append(('606', str( 0.1 * energy/ factor['EN_FAT'])))   # sat
    rdi_list.append(('645', str( 0.1 * energy/ factor['EN_FAT'])))   # non
    rdi_list.append(('646', str( 0.1 * energy/ factor['EN_FAT'])))   # poly
    rdi_list.append(('618', str( 0.01 * energy/ factor['EN_FAT'])))  # 18:2
    rdi_list.append(('619', str( 0.002 * energy/ factor['EN_FAT']))) # 18.3
    rdi_list.append(('205', str( 0.53 * energy/ factor['EN_CHO'])))  # carbs

    # nutrients that are age, weight, or sex dependent
    for key in rdi_dict.keys():
        value = normal_rdi( key, age, weight, female, preg, lac)
        rdi_list.append( (str( key), str( value)))

    # Cys and Met, can be interconverted by hepatic
    # enzymes, so RDIs are issued for the total.
    # meth and cyst
    value = normal_rdi( 506, age, weight, female, preg, lac)
    rdi_list.append( ('506', str( 0.5 * value)))
    rdi_list.append( ('507', str( 0.5 * value)))
    # phen and tyro
    value = normal_rdi( 508, age, weight, female, preg, lac)
    rdi_list.append( ('508', str( 0.5 * value)))
    rdi_list.append( ('509', str( 0.5 * value)))
    return rdi_list
