############################################################################
#%% class
from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import pandas as pd
#from tabulate import tabulate
import os
import datetime
from random import choice
import json
#import numpy as np
import requests

# define a webdriver
def open_browser():
    chrome_path = r'/Users/song/GoogleDrive_SMU/MAS/Alternative Data/WebScrapping/chromedriver'
    ip_table_path = r'/Users/song/GoogleDrive_SMU/MAS/Alternative Data/WebScrapping/ip_table.json'
    
    ip_table = pd.read_json(ip_table_path, orient='records')
    m = choice(list(ip_table.index))
    random_ip = str(ip_table.loc[m, 'IP Address']) + ':' + str(ip_table.loc[m, 'Port'])
    service_args = [
            '--proxy=' + random_ip + ':9999',
            '--proxy-type=socks5'
            ]
    driver = webdriver.Chrome(chrome_path, service_args = service_args)
    driver.implicitly_wait(100)
    driver.set_page_load_timeout(300)
    return driver

# define a search function
def find_tag_by_text(soup, tag_name, text):
    tags = soup.find_all(tag_name)
    for tag in tags:
        if tag.name == tag_name and text == tag.text.strip():
            break
    return tag
#%%
homepage = 'https://www.propertyguru.com.sg'
queenstown = 'https://www.propertyguru.com.sg/property-for-sale?freetext=queenstown'
driver = open_browser()
driver.get(queenstown)
#%%
soup_level_1 = BeautifulSoup(driver.page_source, 'lxml')
ul = soup_level_1.find('ul', attrs = {'class':'listing-items'})
lis = ul.find_all('li', attrs = {'class':'listing-item'})
hrefs = [li.find(lambda tag: tag.name =='a' and tag['href'])['href'] for li in lis]
urls = list(map(lambda x: homepage + x, hrefs))

#%%
class MalaysiaTodayScraper():
    def __init__(self, path, DAILY_LIMIT = 100):
        self.driver = open_browser()
        self.NEWS_channel = 'malaysia-today'
        self.homepage = 'http://www.malaysia-today.net/'
        self.DAILY_LIMIT = DAILY_LIMIT
        self.path = path

    def get_links(self):
        self.driver.get(self.homepage)
        soup_level_1 = BeautifulSoup(self.driver.page_source, 'lxml')
        article_urls = []
        while True:            
            articles = soup_level_1.find_all('article')
            article_urls += [article.find('h2', attrs = {'class':'title'}).find('a')['href'] for article in articles]
            if len(article_urls) >= self.DAILY_LIMIT:
                break
            try:
                next_page_anchor = soup_level_1.find('a', attrs = {'class':'next page-numbers'})
                next_url = next_page_anchor['href']
                print(next_url)
                print('Next page...')
                self.driver.get(next_url)
                soup_level_1 = BeautifulSoup(self.driver.page_source, 'lxml')
            except:
                print('Cannot go to next page...')
                break
        return article_urls

    def get_data(self, article_urls):
        df_data = pd.DataFrame()
        for idx, url in enumerate(article_urls[:self.DAILY_LIMIT]):
            print(idx, ' of ', self.DAILY_LIMIT)
            print(url)
            try:
                df_data.loc[idx, 'url'] = url
                try:
                    r = requests.get(url, timeout = 10000)
                    soup_level_2 = BeautifulSoup(r.content, "html.parser")
                    sub_article = soup_level_2.find('article')
                    df_data.loc[idx, 'title'] = sub_article.find('h1', attrs = {'class':'single-post-title'}).text.strip()
                except:
                    self.driver.get(url)
                    soup_level_2 = BeautifulSoup(self.driver.page_source, 'lxml')
                    sub_article = soup_level_2.find('article')
                    df_data.loc[idx, 'title'] = sub_article.find('h1', attrs = {'class':'single-post-title'}).text.strip() 
                div = sub_article.find('div', attrs = {'class':'entry-content clearfix single-post-content'})
                ps = div.find_all('p')
                paragraphs = '\n'.join([p.text.strip() for p in ps])
                df_data.loc[idx, 'content'] = paragraphs       
            except:
                print('article not existing anymore')
                continue
            try:
                span = soup_level_2.find('span',attrs = {'class':'post-author-name'})
                b = span.find('b')
                df_data.loc[idx, 'author'] = b.text.strip()
            except:
                df_data.loc[idx, 'author'] = str(None)
            try:
                last_update = sub_article.find('time')
                df_data.loc[idx, 'update time'] = last_update['datetime']
            except:
                df_data.loc[idx, 'update time'] = str(None)
        try:
            self.driver.quit()
        except:
            pass
        return df_data
#%%   
if __name__ == '__main__':
    
    MTS_path = '/Users/song/GoogleDrive_SMU/MAS/Alternative Data/WebScrapping/Malaysia-today'
    MTS = MalaysiaTodayScraper(MTS_path, DAILY_LIMIT = 100)
    article_urls_MTS = MTS.get_links()
    df_data_MTS = MTS.get_data(article_urls_MTS)
    data_today_MTS = save_as_json(MTS.NEWS_channel, MTS.homepage, df_data_MTS, MTS.path)
