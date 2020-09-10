
url = 'https://www.ontario.ca/page/how-ontario-is-responding-covid-19'

# pip install selenium
# pip install beautifulSoup4
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup

import time

#stop firefox from actually opening 
options = Options()
options.headless = True

# download geckodriver.exe and change path
driver = webdriver.Firefox(firefox_options=options, executable_path=r'C:\\Users\\Mohamed\\Anaconda2\\envs\\pytorch\\Lib\\site-packages\\selenium\\geckodriver.exe')


driver.get(url)


# just incase wait a bit (NOT SURE IF THIS IS NEEDED)
time.sleep(30)

html = driver.page_source

soup = BeautifulSoup(html,features='lxml')


all_data = []
data = []

for table in soup.find_all('table', attrs={'class':'numeric full-width'}):
    
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    
    for row in rows:
        cols = row.find_all('td')
        cols = [val.text.strip() for val in cols]
        data.append([val for val in cols if val])
        
    all_data.append(data)
    data = []
    
print(all_data)
    
    


