
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl, QCoreApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView

import bs4 as bs
from lxml import html

import pandas as pd
import requests
#%%
class Render(QWebEngineView):
    def __init__(self, url):
        self.html = None
            
        #self.app = QApplication(sys.argv)
        
        self.app = QCoreApplication.instance()
        if self.app is None:
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
#%%
# 1. malaysiakini
malaysiakini_link = 'https://www.malaysiakini.com/en/latest/news'
malaysiakini_source = Render(malaysiakini_link).html
#%%
malaysiakini_content = bs.BeautifulSoup(malaysiakini_source, "html.parser")

div = malaysiakini_content.find('div', attrs = {'class':'uk-container'})
article = malaysiakini_content.find('article')
ref = 'https://www.malaysiakini.com/' + article.find('a')['href']
print(ref)
#price = bloomberg_content.find('span', 
#                            attrs = {'class':'priceText__1853e8a5'}).text.strip()

#print(malaysiakini_content)

#%%
import newspaper
from newspaper import Article

content = Article(ref)
content.download()
content.parse()
#%%
print(help(content))
#article = {}
#article['title'] = content.title
#article['text'] = content.text
print(content)



