<script language="php">
/*
* submit-recipe PHP script run on SourceForge to process submitted recipes *
* Copyright( C) 2001 Ian Haywood (ihaywood@gnu.org)                        *
*                                                                          *
* This program is free software: you can redistribute it and/or modify     *
* it under the terms of the GNU General Public License as published by     *
* the Free Software Foundation, either version 3 of the License, or        *
* (at your option) any later version.                                      *
*                                                                          *
* This program is distributed in the hope that it will be useful,          *
* but WITHOUT ANY WARRANTY; without even the implied warranty of           *
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            *
* GNU General Public License for more details.                             *
*                                                                          *
* You should have received a copy of the GNU General Public License        *
* along with this program.  If not, see <http://www.gnu.org/licenses/>.    *
*/
function chk_string ($string)
{ /* vets strings for illegal chars and length */
	if (strlen ($string) > 10000)
	{
		echo "GNUTR_DB_ERRORString too long";
		exit;
	}
	$string = str_replace ("\t", "\\t", $string); /* escape tabs */
	$string = str_replace ("\n", "\\n", $string); /* escape newlines */
	return $string;
}

$number_file = fopen ("/home/groups/g/gn/gnutrition/db/no_recipes", "r+");
if (! $number_file)
{
	echo "GNUTR_DB_ERRORCould not open file";
	exit;
}
if (! flock ($number_file, 2))
{
	echo "GNUTR_DB_ERRORCould not get lock";
	exit;
}
$recipe_file = fopen ("/home/groups/g/gn/gnutrition/db/recipe", "a");
$ingred_file = fopen ("/home/groups/g/gn/gnutrition/db/ingredient", "a");
$prep_file = fopen ("/home/groups/g/gn/gnutrition/db/preparation", "a");

$number = fgets ($number_file, 10);
$newnum = $number + 1;
rewind ($number_file);
fputs ($number_file, $newnum);

$i = 0;
$amount = "amount" . $i;
while (isset ($$amount)) 
{
        $msre = "msre" . $i;
        $food_no = "food_no" . $i;
        fputs ($ingred_file, $newnum . "\t" . chk_string ($$amount) . "\t" .
        chk_string ($$msre) . "\t" . chk_string ($$food_no) . "\n");
        $i = $i + 1;
        $amount  = "amount" . $i;
}
$no_ingr = $i 

fputs ($recipe_file, $newnum . "\t" . chk_string ($recipe_name) . "\t" 
. chk_string ($no_serv) . "\t" . $no_ingr . "\t" . chk_string ($cat_no)  
. "\n");

fputs ($prep_file, $newnum . "\t" . "NULL" . "\t" . $ingr_prep . "\n");

fclose ($ingred_file);
fclose ($recipe_file);
fclose ($prep_file);
flock ($number_file, 3);
fclose ($number_file);
echo "GNUTR_DB_OK";
</script>
