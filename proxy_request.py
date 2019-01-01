#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 26 18:11:32 2018

@author: song
"""
#%% create the ip_table
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from random import choice
import os

chrome_path = r'/Users/song/GoogleDrive_SMU/MAS/Alternative Data/WebScrapping/chromedriver'
ip_address_link = 'https://free-proxy-list.net/uk-proxy.html'

driver = webdriver.Chrome(chrome_path)
driver.implicitly_wait(30)

driver.get(ip_address_link)

soup_level_1 = BeautifulSoup(driver.page_source, 'lxml')


datalist = []

for i in range(5):
    try:
        table = soup_level_1.find_all('table')[0]
        df_table = pd.read_html(str(table),header=0)[0]
        df_table.dropna(axis = 0, inplace = True)
        datalist.append(df_table)
        
        button = driver.find_element_by_xpath('//*[@id="proxylisttable_next"]/a')
        button.click()
        soup_level_1=BeautifulSoup(driver.page_source, 'lxml')
    except:
        break
driver.quit()
 
ip_table = pd.concat([pd.DataFrame(datalist[i]) for i in range(len(datalist))],ignore_index=True)
ip_table.drop_duplicates(inplace=True)

json_records = ip_table.to_json(orient='records')

path = os.getcwd()
file = path + '/ip_table.json'
f = open(file,"w")
f.write(json_records)
f.close()

#%%
from selenium import webdriver
from bs4 import BeautifulSoup
from random import choice

ip_table_path = r'/Users/song/GoogleDrive_SMU/MAS/Alternative Data/WebScrapping/ip_table.json'
chrome_path = r'/Users/song/GoogleDrive_SMU/MAS/Alternative Data/WebScrapping/chromedriver'

def open_browser(chrome_path, ip_table_path):

    ip_table = pd.read_json(ip_table_path, orient='records')

    m = choice(list(ip_table.index))
    random_ip = str(ip_table.loc[m, 'IP Address']) + ':' + str(ip_table.loc[m, 'Port'])
    print('random IP address: ', random_ip)
    service_args = [
            '--proxy=' + random_ip + ':9999',
            '--proxy-type=socks5'
            ]   
    
    driver = webdriver.Chrome(chrome_path, service_args = service_args)
    driver.implicitly_wait(10)
    driver.set_page_load_timeout(300)
    return driver

driver = open_browser(chrome_path, ip_table_path)
driver.get('https://us.cnn.com/world')

#soup_level_1 = BeautifulSoup(driver.page_source, 'lxml')
driver.quit()
