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

template1 = """<html>
  <head>
    <title>%s</title>
    <meta name="Author" content="Edgar Denny">
    <meta http-equiv="Content-Type" content="text/html">
  </head>
  <body bgcolor="#ffffff" text="#000000" link="#00008b" vlink="#8b0000" alink="#ff0000">
  <p><center><h1>%s</h1></center></p>
    <p><h2>Ingredients</h2>Number of Servings : %s</p>
    <table width="90%%" cellpadding="5" border=1 frame="void">
      <tr>
        <td>Amount</td><td>Measure</td><td>Ingredient</td>
      </tr> 
"""

template2 = """      <tr>
        <td>%d</td><td>%s</td><td>%s</td>
      </tr> 
"""

template3 = """    </table>
  </p>
"""

template4 = """  <p><h2>Preparation</h2></p>
  <table width="90%%" cellpadding="5" border=1 frame="void">
    <tr><td>
      <pre style="font-family: serif">%s</pre>
    </td></tr>
  </table>
"""

template5 = """  <p>
    <table border="1" width="90%%" cellpadding="5" frame="void">
      <colgroup span="4">
        <col width="25%%">
        <col width="25%%">
        <col width="25%%">
        <col width="25%%">
      </colgroup>
      <tr>
        <td colspan=4>%s</td>
      </tr>
"""
template6 = """    <tr>
      <td>%s</td><td>%.3f</td><td>%s</td><td>%.3f</td>
    </tr>
"""

template7 = """    <tr>
      <td>%s</td><td>%.3f</td>
    </tr>
"""

class SaveAs:
    def __init__( self):
        pass

    def value( self, num):
        for nutr_num, nutr_val in self.nutr_list:
            if nutr_num == num:
                return nutr_val;
        return 0.0

    def html( self, recipe, nutr_list, pcnt_cal, fn):
        self.nutr_list = nutr_list
        f = file( fn, 'w')
        f.write( template1 %( recipe.desc, recipe.desc, recipe.num_serv))
        for ingr in recipe.ingr_list:
            f.write( template2 %( ingr.amount, ingr.msre_desc, ingr.food_desc))
        f.write( template3)

        if ( recipe.prep_desc):
            f.write( template4 % ( recipe.prep_desc))

        f.write( '<p><h2>Nutrient Composition (Per Serving)</h2></p>\n')

        f.write( template5 % ('Macro-Nutrients'))
        f.write( template6 %( 'Protein (g)', self.value( 203), 
            'Saturated Fat (g)', self.value( 606)))
        f.write( template6 %( 'Total Fat (g)', self.value( 204), 
            'Mono-Unsaturated Fat (g)', self.value( 645)))
        f.write( template6 %( 'Carbohydrates (g)', self.value( 205), 
            'Poly-Unsaturated Fat (g)', self.value( 646)))
        f.write( template6 %( 'Cholesterol (mg)', self.value( 601), 
            'Fiber (g)', self.value( 291)))
        f.write( template6 %( 'Calories (kcal)', self.value( 208), 
            'Energy (kJ)', self.value( 268)))
        f.write ( template3)

        f.write( template5 %( 'Micro-Nutrients'))
        f.write( template6 %( 'A (mg RE)', self.value( 318),
            'Calcium (mg)', self.value( 301)))
        f.write( template6 %( 'E (mg ATE)', self.value( 394),
            'Iron (mg)', self.value( 303)))
        f.write( template6 %( 'C (mg)', self.value( 401),
            'Magnesium (mg)', self.value( 304)))
        f.write( template6 %( 'Thiamin (mg)', self.value( 404),
            'Phosphorus (mg)', self.value( 305)))
        f.write( template6 %( 'Riboflavin (mg)', self.value( 405),
            'Potassium (mg)', self.value( 306)))
        f.write( template6 %( 'Niacin (mg)', self.value( 406),
            'Sodium (mg)', self.value( 307)))
        f.write( template6 %( 'Panto. Acid (mg)', self.value( 410),
            'Zinc (mg)', self.value( 309)))
        f.write( template6 %( 'B6 (mg)', self.value( 415),
            'Copper (mg)', self.value( 312)))
        f.write( template6 %( 'Folate (cmg)', self.value( 417),
            'Manganese (mg)', self.value( 315)))
        f.write( template6 %( 'B12 (cmg)', self.value( 418),
            'Selenium (mcg)', self.value( 317)))
        f.write ( template3)

        f.write( template5 % ( 'Percentage of Calories'))
        f.write( template6 %( 'Protein', pcnt_cal[0],
            'Fat', pcnt_cal[1]))
        f.write( template7 %( 'Carbohydrates', pcnt_cal[2]))
        f.write ( template3)
        f.write( '</html>\n')
        f.close()
