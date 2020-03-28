'''
   Version: 0.3
   Author: Leroy van der Steenhoven

   Description:
        This script will get the Root-Me points, rank and challenges completed for the users in "members"

    You'll need the following:
        Python 3.x
        Requests            pip3 install requests
        Beautiful-soup      pip3 install beautifulsoup4
        prettytable         pip3 install prettytable
'''
import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable
import time
import datetime

# Members for which you want scores
members = ['pve', 'Aadsterken', 'netmin', 'lazydoe99', 'Ferran-Tufan', 'bulluk', 'BacVic', 'arriver']

# URLs needed
ranking_URL = 'https://www.root-me.org/'
ranking_SVG = 'IMG/rubon98.svg?1575185394'.lower()
points_SVG = 'squelettes/img/valid.svg?1566650916'.lower()
challenges_SVG = 'IMG/rubon5.svg?1575185394'.lower()
compromises_SVG = 'IMG/rubon196.svg?1575185394'.lower()
present_Class = 'class="grayscale'.lower()

# Make a table
score_Table = PrettyTable()
score_Table.field_names = ['User', 'Global Rank', 'Points', 'Challenges', 'Compromises', 'Measurement date']

# Get the score of every member
for member in members:
    # Wait a split-second between members, else the webpage will ratelimit
    time.sleep(0.5)

    # Get their profile page
    profile = requests.get(str(ranking_URL + str(member) + '?lang=en'))

    # Parse the HTML using beautifulsoup4
    soup =  BeautifulSoup(profile.content, 'html.parser')

    # The page lacks proper ID's so get all h3 elements
    elements = soup.find_all('h3')

    # Make a list to later add as a row in the table #1 is global rank #2 is points, #3 is challenges, #4 is compromises and #5 the date
    member_Stats = [str(member), 'Unknown', 'Unknown','Unknown', 'Unknown', '{}'.format(datetime.date.today())]

    # Go through the elements one by one and check for two things: the overal rank SVG and the points SVG, those lines are needed.
    for element in elements:
        # Lower the likely already lowered element
        element = str(element).lower()
        # Check if it's a grayscale element, some SVGs are used on different places too
        if present_Class in element:
            soup_2 = BeautifulSoup(element, 'html.parser')
            if ranking_SVG in element:
                member_Stats[1] = str(soup_2.find('h3').text).strip()
            elif points_SVG in element:
                member_Stats[2] = str(soup_2.find('h3').text).strip()
            elif challenges_SVG in element:
                member_Stats[3] = str(soup_2.find('h3').text).strip()
            elif compromises_SVG in element:
                member_Stats[4] = str(soup_2.find('h3').text).strip()
    # Add member to scoring table with known and unkown stats
    score_Table.add_row(member_Stats)

# Print results
print(score_Table)
