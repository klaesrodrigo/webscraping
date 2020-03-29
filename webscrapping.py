import requests
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json


# Pega o conteúdo HTML a partir de uma URL
url = "https://stats.nba.com/players/traditional/?PerMode=Totals&Season=2019-20&SeasonType=Regular%20Season&sort=PLAYER_NAME&dir=-1"
top10ranking = {}

rankings = {
    '3points': {'field': 'FG3M', 'label': '3PM'},
    'points': {'field': 'PTS', 'label': 'PTS'},
    'assistants': {'field': 'AST', 'label': 'AST'},
    'rebounds': {'field': 'REB', 'label': 'REB'},
    'steals': {'field': 'STL', 'label': 'STL'},
    'blocks': {'field': 'BLK', 'label': 'BLK'},
}

def buildRank(type):
    field = rankings[type]['field']
    label = rankings[type]['label']

    # Busca  conteúdo pelo elemento
    driver.find_element_by_xpath(
        f"//div[@class='nba-stat-table']//div//table//thead//tr//th[@data-field='{field}']").click()
    element = driver.find_element_by_xpath("//div[@class='nba-stat-table']//div//table")
    html_content = element.get_attribute('outerHTML')
    
    # Parsea o conteúdo html
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find(name='table')

    # Estrutura o conteúdo em data frame
    df_full = pd.read_html( str(table) )[0].head(10)

    df = df_full[['Unnamed: 0', 'PLAYER', 'TEAM', label]]
    df.columns = ['pos', 'player', 'team', 'total']

    # Tranbsformar data frame em  um dicionário
    return df.to_dict('records')

option = Options()
# option.headless = True
driver = webdriver.Firefox()

driver.get(url)
time.sleep(4)

# Transforma em JSON

for k in rankings:
    top10ranking[k] = buildRank(k)

driver.close()
driver.quit()

js = json.dumps(top10ranking)

fp = open('ranking.json', 'w')
fp.write(js)
fp.close()