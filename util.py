from bs4 import BeautifulSoup
import numpy as np
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
import time
import logging
import re
import random

logger = logging.getLogger(__name__)

delay = 15

def wait(timeout=0):
    #print('waiting %d second....' % timeout)
    if timeout != 0:
        time.sleep(timeout)
    else:    
        time.sleep(delay) 

def isDisplay(el):
    if el:
       if el.is_displayed():
           hi = el.get_attribute("aria-hidden")
           cl = el.get_attribute("class")
           if hi == 'true': return False
           if 'disable' in cl: return False
           return True
    return False       
               
def getMsg(drv):
    xpath = '//div[@role="alert"]'
    els = drv.get_elements(By.XPATH, xpath)    
    for i, el in enumerate(els):        
        cls = el.get_attribute('class')
        if cls is None: continue
        cls = cls.lower()
        if 'hidden' in cls: continue
        if 'notice' in cls or 'message' in cls:
            return el.get_attribute('textContent')   
    return None            
    

def getAns(drv):
    xpath = '//div[@class]'
    els = drv.get_elements(By.XPATH, xpath)    
    for i, el in enumerate(els):        
        cls = el.get_attribute('class')
        if cls is None: continue
        cls = cls.lower()
        if 'complete' in cls and 'page' in cls:
            return el.get_attribute('textContent')
    return None
    
def cleanPopup(drv):

    xpath = '//div[@role="dialog"]//button[@class]'
    attr = {'class': re.compile('.*close.*', re.I)}    
    els = drv.get_elements(By.XPATH, xpath)
    for i, el in enumerate(els):
        try:
            cls = el.get_attribute("class")
            if cls is None: continue
            cls = cls.lower()
            if 'close' in  cls:
                drv.js_click(el)    
        except Exception as e:
            pass         
    
def clickRadio(drv):
    xpath = '//input[@type="radio"]'    
    els = drv.get_elements(By.XPATH, xpath)    
    prev = None
    for i, el in enumerate(els):
        try:            
            if el.get_attribute("name") != prev:                
                drv.js_click(el)
                prev = el.get_attribute("name")
        except Exception as e:
            pass     

def getRadios(drv):
    xpath = '//input[@type="radio"]'    
    els = drv.get_elements(By.XPATH, xpath)    
    ret = dict()
    for i, el in enumerate(els):
        try:
            name = el.get_attribute("name")
            if name not in ret:
                ret[name] = [el]
            else:
                ret[name].append(el)
        except Exception as e:
            pass     
    return ret        

def rndRadio(drv, rds, rand=True):
    for k in rds.keys():
        if rand:
            rnd = random.randint(0, len(rds[k]) - 1)
        else:
            rnd = 0        
        drv.js_click(rds[k][rnd])        
    
def getSelectOption(soup):
    tags = soup.find_all("option")
    return [tag.string.strip() for tag in tags]
    
def clickSelect(drv, num=1):
    xpath='//select'    
    els = drv.get_elements(By.XPATH, xpath)    
    for i, el in enumerate(els):
        try:
            htmlstr = el.get_attribute("outerHTML")
            soup = BeautifulSoup(htmlstr, 'lxml')
            va = getSelectOption(soup)
            if len(va) > num :
                Select(el).select_by_visible_text(va[num])
        except Exception as e:
            pass  

        
def getGoodsUrl(drv, url):

    def check(cls, href):
        try:
            if 'product' not in href.lower():
                if not cls:
                    return False                    
                if 'product' not in cls .lower():
                    return False
            vs =href.split('/')
            ret = re.search(r'^.*\d{3,}|.*\?', vs[-1])
            return ret is not None
        except Exception as e:
            return False     
        
    drv.open_scroll(url)
    wait(2)
    xpath='//a[@href]'    
    els = drv.get_elements(By.XPATH, xpath)    
    for i, el in enumerate(els):    
        href = el.get_attribute("href")
        if href is None: continue
        cls = el.get_attribute("class")
        #if cls is None: continue
        #cls = cls.lower()
        if check(cls, href): 
            return url + href if href[:4] != 'http' else href
    return None        
        
            
