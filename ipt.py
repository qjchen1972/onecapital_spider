from bs4 import BeautifulSoup
import numpy as np
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time
import logging
import re

import util

logger = logging.getLogger(__name__)

def _findEleInFrame(drv, call):
    els = drv.get_elements(By.XPATH, '//label[@for]')
    for i, el in enumerate(els):      
        s = el.get_attribute('textContent')
        if s is None: continue
        s = s.lower()
        if(call(s)):
            id = el.get_attribute('for')
            if id is None: continue
            t = '//input[@id=%s]|//select[@id=%s]' %('"'+id+'"','"'+id+'"')
            ob = drv.get_element(By.XPATH, t)
            if ob and  util.isDisplay(ob):
                return ob 
    return None     

#返回el, 外面处理后 需要做switch_to.default_content()    
def _findEle(drv, call):
    el = _findEleInFrame(drv, call)    
    if el is None:
        fms = drv.get_elements(By.XPATH, '//iframe[@class]')
        for i, fm in enumerate(fms):  
            drv.switch_to_frame(fm)
            el = _findEleInFrame(drv, call)
            if el: return el
            drv.switch_to_frame_out()
    return el            
 
#返回select中option项,和instr相似 
def _getOptionStr(el, instr):
    htmlstr = el.get_attribute("outerHTML")
    soup = BeautifulSoup(htmlstr, 'lxml')
    typelist = soup.find_all("option", text=lambda s: instr.lower() in s.lower())
    if len(typelist) < 1: return None
    return typelist[0].string.strip()   
    

def _proc(drv, instr, call, do):
    el = _findEle(drv, call)
    if el is None: return el    
    if do:
        if el.tag_name == 'input':
            drv.clear(el)
            drv.send_value_x(el, instr)
        else:
            va = _getOptionStr(el, instr)
            if va:
                Select(el).select_by_visible_text(va)
    drv.switch_to_frame_out()            
    return el     


#判断是否到了输入信息的页面
def isAddressPage(drv):
    def check(s):
        if 'address' in s and 'email' not in s:
            return True
        return False   
    return _proc(drv, instr='', call=check, do=False) 

    
def email(drv, instr='', do=True):    
    def check(s):        
        if 'email' in s :
            return True
        return False 
    return _proc(drv, instr, check, do)
    

def country(drv, instr='', do=True):
    def check(s):
        if 'country' in s and 'region' in s: 
            return True
        return False   
    return _proc(drv, instr, check, do)
    
def state(drv, instr='', do=True):
    def check(s):
        if 'state' in s: 
            return True
        return False   
    return _proc(drv, instr, check, do)
    
def zipcode(drv, instr='', do=True):
    def check(s):
        if 'zip' in s and 'code' in s:              
            return True
        if 'post' in s and 'code' in s:              
            return True            
        return False   
    return _proc(drv, instr, check, do)
    
def fullname(drv, instr='', do=True):
    def check(s):
        if 'full' in s and 'name' in s:              
            return True
        return False   
    return _proc(drv, instr, check, do)    
    
def address(drv, instr='', do=True):
    def check(s):
        if 'address' in s:
            if 'search' in s or 'email' in s: return False            
            return True
        return False   
    return _proc(drv, instr, check, do)      
    
def city(drv, instr='', do=True):
    def check(s):
        if 'city' in s or 'town' in s:
            return True
        return False   
    return _proc(drv, instr, check, do)
    
def firstname(drv, instr='', do=True):
    def check(s):
        if 'first' in s and 'name' in s:
            return True
        return False   
    return _proc(drv, instr, check, do)    
    
def lastname(drv, instr='', do=True):
    def check(s):
        if 'last' in s and 'name' in s:
            return True
        return False   
    return _proc(drv, instr, check, do)    
    
def phone(drv, instr='', do=True):
    def check(s):
        if 'contact' in s and 'number' in s:
            return True
        if 'phone' in s: return True    
        return False   
    return _proc(drv, instr, check, do) 

def cardnumber(drv, instr='', do=True):
    def check(s):
        if 'card' in s and 'number' in s:
            return True
        return False   
    return _proc(drv, instr, check, do)  

def nameoncard(drv, instr='', do=True):
    def check(s):
        if 'card' in s and 'name' in s and 'on' in s:
            return True
        return False   
    return _proc(drv, instr, check, do)   

def cv2(drv, instr='', do=True):
    def check(s):
        if 'security' in s and 'code' in s:
            return True            
        return False   
    return _proc(drv, instr, check, do)

def expiration(drv, instr='', do=True):
    def check(s):
        if 'expiration' in s and 'date' in s:
            return True            
        return False   
    return _proc(drv, instr, check, do)    
    
def year(drv, instr='', do=True):
    def check(s):
        if 'year' in s:
            return True            
        return False   
    return _proc(drv, instr, check, do)  

def month(drv, instr='', do=True):
    def check(s):
        if 'month' in s or 'date' in s:
            return True            
        return False   
    return _proc(drv, instr, check, do)    
    