from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta


url = 'https://www.ontario.ca/page/how-ontario-is-responding-covid-19'

#stop firefox from actually opening 
options = Options()
options.headless = True

# download geckodriver.exe and change path
driver = webdriver.Firefox(options=options, executable_path=r'C:\Program Files\Geckodriver\geckodriver.exe')
driver.get(url)


# wait for page to load all features
time.sleep(30)


# get page html
html = driver.page_source
soup = BeautifulSoup(html, features='lxml')


# get table data
all_data = []
data = []

for table in soup.find_all('table', attrs={'class':'numeric full-width'}):
    rows = table.tbody.find_all('tr')
    
    for row in rows:
        elements = row.find_all('td')
        elements = [val.text.strip().split('\n')[0] for val in elements]
        data.append([val for val in elements if val])
        
    all_data.append(data)
    data = []

# close driver
driver.quit()

# get yesterday's date (data is from previous day)
date = datetime.strftime(datetime.now() - timedelta(1), "%m/%d/%Y")


# get data as a pandas dataframe
df1 = pd.DataFrame(np.array(all_data[0])[[0,1,2,6],0])
df2 = pd.DataFrame(all_data[1])
df3 = pd.DataFrame(np.array(all_data[2])[[0,2]])
df4 = pd.DataFrame(all_data[3])

# remove commas from numbers
df1[0] = df1[0].str.replace(',', '')
df2[0] = df2[0].str.replace(',', '')
df3[0] = df3[0].str.replace(',', '')
df4[0] = df4[0].str.replace(',', '')

df = pd.concat([df1, df2, df3, df4])

# get data from previous days from csv
data = np.genfromtxt(r'Ontario Covid19 data.csv', delimiter=',', encoding="utf-8-sig", dtype=None)
data = pd.DataFrame(data[1:, :], columns=data[0])

#add new data and save to csv
data.insert(1,date, df.to_numpy().astype(int), allow_duplicates=True)
data.to_csv(r'Ontario Covid19 data.csv', index=False)

