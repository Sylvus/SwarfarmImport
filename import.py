# This script can be used to import your monsters into swarfarm
# http://swarfarm.com/
# In order to do this you need a csv file with all your monsters.
# You can easily generate one by using this project:
# https://github.com/kakaroto/SWParser

# The following fields need to be filled in by you.
USERNAME = 'user'
PASSWORD = 'password'
CSV_FILE = 'id-monsters.csv'
DELETE_CURRENT_MONS = True # Replace with False if you want to keep your swarfarm mons.

##############################
# Start of the program #######
##############################
#
# please do not modify anything if you don't know what you are doing.
#
import sys
import requests
# You may need to install BeautifulSoup see:
# http://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup
# On linux: apt-get install python-bs4
from bs4 import BeautifulSoup
import csv

client = requests.session()

url_login = 'https://swarfarm.com/login/'
url_profile = 'https://swarfarm.com/profile/' + USERNAME + '/'
url_inventory = url_profile + 'monster/inventory/'

# Retrieve the CSRF token first
client.get(url_login)  # sets cookie
csrftoken = client.cookies['csrftoken']

login_data = {'csrfmiddlewaretoken': csrftoken,
              'username': USERNAME,
              'password': PASSWORD}

# Log in
r = client.post(url_login, data=login_data, headers=dict(Referer=url_login))

print('Login: ', r.reason)

# Find the CSV file and load all the mons
monsters = []
with open(CSV_FILE, 'r') as csvfile:
  reader = csv.DictReader(csvfile, delimiter=',')
  for row in reader:
    monsters.append({'name': row['name'].replace('(','').replace(')',''), 'level': row['level'], 'stars': row['Stars']})

# OPTIONAL: Delete all current mons
if (DELETE_CURRENT_MONS):
  r = client.get(url_inventory)
  soup = BeautifulSoup(r.content)
  for button in soup.findAll('button', {'class': 'monster-delete'}):
    mon_id = button['data-instance-id']
    url_delete = url_profile + 'monster/delete/' + mon_id + '/'
    r = client.get(url_delete, params={'delete': 'delete', 'instance_id': mon_id})
    print('Deleting: ', r.reason)

# Get the correct IDs
for mon in monsters:
  mon_name = mon['name']
  url_search = 'https://swarfarm.com/autocomplete/MonsterAutocomplete/'
  r = client.get(url_search, params={'q': mon_name})
  print('Looking up ID: ', r.status_code, r.reason)
  soup = BeautifulSoup(r.content)
  divs = soup.findAll('div')
  selection = 0
  if (len(divs) > 1):
    if (divs[1].find('span').text == mon_name):
      selection = 1

  mon_id = int(divs[selection]['data-value'])
  mon['id'] = mon_id

# Add the mons
url_add = url_profile + 'monster/bulk_add/'
# Retrieve the CSRF token first
client.get(url_add)
csrftoken = client.cookies['csrftoken']

mon_data = {'csrfmiddlewaretoken': csrftoken,
            'form-TOTAL_FORMS': len(monsters),
            'form-INITIAL_FORMS': 0,
            'form-MIN_NUM_FORMS': 0,
            'form-MAX_NUM_FORMS': len(monsters),
            'submit': 'Submit'}
counter = 0
for mon in monsters:
  prefix = 'form-' + str(counter) + '-'
  mon_data[prefix + 'monster-autocomplete'] = ''
  mon_data[prefix + 'monster'] = int(mon['id'])
  mon_data[prefix + 'stars'] = int(mon['stars'])
  mon_data[prefix + 'level'] = int(mon['level'])
  counter = counter + 1

r = client.post(url_add, data=mon_data, headers=dict(Referer=url_add))

print("Adding ", r.reason)
print("Done.")
