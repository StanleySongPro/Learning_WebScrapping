
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView

import bs4 as bs
from lxml import html

import pandas as pd
import requests

class Render(QWebEngineView):
    def __init__(self, url):
        self.html = None
        self.app = QApplication(sys.argv)
        QWebEngineView.__init__(self)
        self.loadFinished.connect(self._loadFinished)
        #self.setHtml(html)
        self.load(QUrl(url))
        self.app.exec_()

    def _loadFinished(self, result):
        # This is an async call, you need to wait for this
        # to be called before closing the app
        self.page().toHtml(self._callable)

    def _callable(self, data):
        self.html = data
        # Data has been stored, it's safe to quit the app
        self.app.quit()

'''
# test on bloomberg
bloomberg_link = 'https://www.bloomberg.com/quote/SPX:IND'
bloomberg_source = Render(bloomberg_link).html

bloomberg_content = bs.BeautifulSoup(bloomberg_source, "html.parser")

div = bloomberg_content.find('div', 
                            attrs = {'class':'overviewRow__0956421f'})
price = bloomberg_content.find('span', 
                            attrs = {'class':'priceText__1853e8a5'}).text.strip()
print(div)
print(price)
'''

# 1. malaysiakini
malaysiakini_link = 'https://www.malaysiakini.com/en/latest/news'
malaysiakini_source = Render(malaysiakini_link).html

malaysiakini_content = bs.BeautifulSoup(malaysiakini_source, "html.parser")

#div = malaysiakini_content.find('div', 
#                            attrs = {'class':'overviewRow__0956421f'})
#price = bloomberg_content.find('span', 
#                            attrs = {'class':'priceText__1853e8a5'}).text.strip()

print(malaysiakini_content)

# save the news HTML as pickle
import requests
import time
import pickle
import random
import pandas as pd

outFile = open('JCO.txt', 'wb')
pickle.dump(JCO_results, outFile)
outFile.close()

inFile = open('JCO.txt', 'rb')
JCO_JSON = pickle.load(inFile)
inFile.close()

# click inside the href and save the HTML as pickle
# extract news info as dataframe and save as json file 



