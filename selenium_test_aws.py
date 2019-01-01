#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 22 18:43:03 2018

@author: song
"""
import os
from selenium import webdriver
chrome_path = os.getcwd() + '/chromedriver'
#chrome_path = './chromedriver'
options = webdriver.ChromeOptions()                
options.add_argument('--headless')
driver = webdriver.Chrome(desired_capabilities = options.to_capabilities(),
                          executable_path = chrome_path)
driver.get('https://www.google.com')
#driver.quit()
