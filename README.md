# Swarfarm Import

This script can be used to import your monsters into swarfarm (http://swarfarm.com/). In order to do this you need a csv file with all your monsters. You can easily generate one by using this project: https://github.com/kakaroto/SWParser

The following fields can be found at the top of the import file and need to be filled in by you:
USERNAME = 'Your user name here'
PASSWORD = 'Your password here'
CSV_FILE = 'id-monsters.csv'
DELETE_CURRENT_MONS = True

You can also write the csv file by yourself. The layout should look like this:
Monster id,name,level,Stars,
1,Camilla,40,6,
2,Soha,35,5
3,Undine (Water),35,5
4,Raoq,35,5
...
