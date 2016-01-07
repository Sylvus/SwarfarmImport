# Swarfarm Import
<br />
This script can be used to import your monsters into swarfarm (http://swarfarm.com/). In order to do this you need a csv file with all your monsters. You can easily generate one by using this project: https://github.com/kakaroto/SWParser
<br />
The following fields can be found at the top of the import file and need to be filled in by you:<br />
USERNAME = 'Your user name here'<br />
PASSWORD = 'Your password here'<br />
CSV_FILE = 'id-monsters.csv'<br />
DELETE_CURRENT_MONS = True<br />
<br />
You can also write the csv file by yourself. The layout should look like this:<br />
<br />
Monster id,name,level,Stars,<br />
1,Camilla,40,6,<br />
2,Soha,35,5<br />
3,Undine (Water),35,5<br />
4,Raoq,35,5 <br />
...
