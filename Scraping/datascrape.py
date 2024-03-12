from bs4 import BeautifulSoup as bs
from selenium import webdriver #for dynamically loaded page elements that requests won't read in
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
service = Service('C:/Users/cbarg/Downloads/chromedriver_win32/chromedriver.exe') #if anyone ever dares use this you need to replace this with the path to your own chromedriver or what have you
import time
import re
import numpy as np
import pandas as pd

options = Options()
options.add_argument('disable-infobars')
options.add_argument('--incognito')
options.add_argument("start-maximized")

driver = webdriver.Chrome(service=service, options=options)
URL = 'https://www.nhl.com/stats/teams?aggregate=0&reportType=game&seasonFrom=20052006&seasonTo=20202021&dateFromSeason&gameType=3&filter=gamesPlayed,gte,1&sort=a_gameDate&page=0&pageSize=100'
team = []
date = []
points = []
RW = []
ROW = []
SOW = []
goals = []
goals_against = []
power_play = []
penalty_kill = []
net_ppp = []
net_pkp = []
shots = []
shots_a = []
FOWp = []

for i in range(0, 29):
    driver.get(URL)
    time.sleep(5)
    html = driver.page_source
    soup = bs(html, features='html.parser')
    rows = soup.find_all('div', class_='rt-tr-group')

    for row in rows:
        all_data = row.find_all('div', class_='rt-td')

        team.append(all_data[1].text.strip())
        date.append(all_data[2].text.strip())
        points.append(all_data[8].text.strip())
        RW.append(all_data[10].text.strip())
        ROW.append(all_data[11].text.strip())
        SOW.append(all_data[12].text.strip())
        goals.append(all_data[13].text.strip())
        goals_against.append(all_data[14].text.strip())
        power_play.append(all_data[17].text.strip())
        penalty_kill.append(all_data[18].text.strip())
        net_ppp.append(all_data[19].text.strip())
        net_pkp.append(all_data[20].text.strip())
        shots.append(all_data[21].text.strip())
        shots_a.append(all_data[22].text.strip())
        FOWp.append(all_data[23].text.strip())
    URL = re.sub(f'&page={i}', f'&page={i+1}', URL)

driver.quit()
df = pd.DataFrame(zip(team, date, points, RW, ROW, SOW, goals, goals_against, power_play, penalty_kill, net_ppp, net_pkp, shots, shots_a, FOWp),
    columns = ['team', 'date', 'points', 'RW', 'ROW', 'SOW', 'goals', 'goals_against', 'power_play', 'penalty_kill', 'net_ppp', 'net_pkp', 'shots', 'shots_against', 'FOWp'])

df.to_csv('nhl_playoff_stats.csv')