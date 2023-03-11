from bs4 import BeautifulSoup
import numpy as np
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time
import logging
import re
import numpy as np
import util

logger = logging.getLogger(__name__)


def _findEle(drv, call):
    els = drv.get_elements(By.XPATH, '//button|//a|//input')
    ret = []
    for i, el in enumerate(els):        
        try:
            s = None
            tp = el.get_attribute('type')
            if tp == 'submit':
                s = el.get_attribute('value')
            if not s:    
                s = el.get_attribute('textContent')
            s = s.lower()    
            s = s.replace(" ", "")
            score = call(el, s)
            if score:
                #if util.isDisplay(el):
                ret.append([el, s, score])
        except Exception as e:
            pass        
    return ret     

def _proc(drv, call):
    ret = _findEle(drv, call)
    if not len(ret): return False   
    ret = np.array(ret)
    temp = ret[np.argsort(-ret[:,2])]
    #print(temp)
    #`print(temp[0][1])
    return drv.js_click(temp[0][0])    
    
def enteraddress(drv):
    def check(el, s):
        score = 0
        if 'enter'  in s and 'address'  in s:
            score += 1
            if 'manua' in s:
                score += 1 
            if 'or' in s:
                score += 1
        if score:
            if util.isDisplay(el):
                score += 2            
            if el.tag_name == 'button':
                score += 1                    
        return score
    return _proc(drv, check)

    
def addcart(drv):
    def check(el, s):
        score = 0
        if 'buy' in s:
            score += 1
            if 'now' in s: score += 2 
        if 'add' in s:
            if 'cart' in s or 'basket' in s or 'bag' in s: score += 1            
        if 'checkout' in s:
            score += 1
        if score:
            if util.isDisplay(el):
                score += 2
            if el.tag_name == 'input':
                score += 3            
            if el.tag_name == 'button':
                score += 1                      
        return score
    return _proc(drv, check)    
    
def viewcart(drv):
    def check(el, s):        
        score = 0
        if 'checkout' in s:
            score += 2
        if 'basket' in s or 'cart' in s or 'bag' in s:
            if 'view' in s  or 'go' in s:
                score += 1
        if score:
            if util.isDisplay(el):
                score += 2
            if el.tag_name == 'input':
                score += 3         
            if el.tag_name == 'button':
                score += 1                      
        return score
    return _proc(drv, check)
    
def checkout(drv):
    def check(el, s):
        score = 0
        if 'checkout' in s:
            score += 1
            if 'now' in s:
                score += 2
        if 'pay' in s:
            score += 1 
            if 'now'in s:
                score += 2
        if score:
            if util.isDisplay(el):
                score += 2        
            if el.tag_name == 'input':
                score += 3         
            if el.tag_name == 'button':
                score += 1                      
        return score
    return _proc(drv, check)    
    
def next(drv):
    def check(el, s):
        score = 0
        if 'continue' in s and 'shop' not in s:
            score += 1
            if 'guest' in s:
                score += 2
            if 'pay' in s:
                score += 1
            if 'checkout' in s:
                score += 2
            if 'ship' in s:
                score += 1      
        if score:
            if util.isDisplay(el):
                score += 2
            if el.tag_name == 'input':
                score += 3         
            if el.tag_name == 'button':
                score += 1                      
        return score
    return _proc(drv, check)     
    
def submitorder(drv):
    def check(el, s):
        score = 0        
        if 'pay' in s:
            score += 1 
            if 'now'in s:
                score += 2
        if 'submit' in s:
            score += 1 
            if 'order' in s:
                score += 2                
        if score:
            if util.isDisplay(el):
                score += 2        
            if el.tag_name == 'input':
                score += 3         
            if el.tag_name == 'button':
                score += 1                      
        return score
    return _proc(drv, check)     