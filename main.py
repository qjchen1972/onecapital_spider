from bs4 import BeautifulSoup
import numpy as np
import requests
from selenium.webdriver.common.by import By
import time
import logging
import re
import argparse
from browse import Browser
import btn
import ipt
import util

logger = logging.getLogger(__name__)

info = {'email': 'lmp13cdmhc@temporary-mail.net',
         'country': 'United States',
         'name': 'Kimberly J Stack',
         'firstname': 'Kimberly',
         'lastname': 'Stack',
         'address': '567 Cambridge Place',    
         'zipcode': '92236',
         'city': 'COACHELLA',             
         'state': 'California',
         'phone': '410-545-7170',
         }

card2 = {'cardnumber': '5563014443756068', 
         'nameoncard': 'Kimberly J Stack',
         'expiration': '07/2028',
         'securitycode': '321',
         }
         
card1 = {'cardnumber': '5563012185122747', 
         'nameoncard': 'Kimberly J Stack',
         'expiration': '02/2026',
         'securitycode': '776',}

'''     
msg = 'Thank you for your orderWe are currently processing your order and will send you a confirmation email shortly.Your order number is 468617351.(function(){/*  Copyright The Closure Library Authors. SPDX-License-Identifier: Apache-2.0 */ var aa="function"==typeof Object.create?Object.create:function(a){function b(){}b.prototype=a;return new b},m;if("function"==typeof Object.setPrototypeOf)m=Object.setPrototypeOf;else{var n;a:{var ba={a:!0},p={};try{p.__proto__=ba;n=p.a;break a}catch(a){}n=!1}m=n?function(a,b){a.__proto__=b;if(a.__proto__!==b)throw new TypeError(a+" is not extensible");return a}:null}var q=m,r=this||self;function t(a){var b;a:{if(b=r.navigator)if(b=b.userAgent)break a;b=""}return-1!=b.indexOf(a)};var u={},v=null;var ca="undefined"!==typeof Uint8Array,da=!(t("Trident")||t("MSIE"))&&"function"===typeof r.btoa;var w="function"===typeof Symbol&&"symbol"===typeof Symbol()?Symbol():void 0;function x(a){var b;w?b=a[w]:b=a.i;return null==b?0:b}function z(a,b){w?a[w]=b:void 0!==a.i?a.i=b:Object.defineProperties(a,{i:{value:b,configurable:!0,writable:!0,enumerable:!1}})};var A={};'      
pattern = re.compile(r'order\s*number\s+is.{0,1}\s*\d+', re.I)
res = re.search(pattern, msg)
if res: 
    print(res.group(0))
exit()
'''
       
def createAll():
    drv = Browser()
    drv.open_scroll('https://capitaloneshopping.com/s/all')
    
    xpath = '//div[contains(@class, "all-stores-list")]//a'
    els = drv.get_elements(By.XPATH, xpath)
    sites = dict()
    for i, el in enumerate(els):        
        href = el.get_attribute('href')
        ans = href.split('/')
        name = el.get_attribute('textContent')
        if name:   
            sites[name] = ans[4]
            print(i, name, ans[4]) 
            
    np.save('allurl.npy', sites)    
    ans = np.load('allurl.npy', allow_pickle=True)
    
def proc_good(drv, timeout):

    util.clickSelect(drv)
    rds = util.getRadios(drv)
    
    num = 0
    util.rndRadio(drv, rds, rand=False)        
    while num < 3:
        util.wait(1)
        done = btn.addcart(drv)
        if done: break
        num += 1
        util.rndRadio(drv, rds, rand=True)
    #print('addcart', done, num)   
    if not done: return False
    util.wait(timeout)
    if ipt.isAddressPage(drv): return True
    
    done = btn.viewcart(drv) 
    #print('viewcart', done)    
    if done:
        util.wait(timeout)
        if ipt.isAddressPage(drv): return True
           
    done =  btn.checkout(drv)
    #print('checkout', done) 
    if done:
        util.wait(timeout)
        if ipt.isAddressPage(drv): return True
        
    num = 0        
    while num < 2:       
        done =  btn.next(drv)
        #print('next', num, done) 
        if done:
            util.wait(timeout)
            if ipt.isAddressPage(drv): return True            
        num += 1
    return False        
    

def inputInfo(drv):    
    if not ipt.email(drv, info['email']):
        return False
    ipt.country(drv, info['country'])
    ipt.state(drv, info['state'])
    ipt.fullname(drv, info['name'])
    ipt.firstname(drv, info['firstname'])
    ipt.lastname(drv, info['lastname'])
    ipt.address(drv, info['address'])
    ipt.zipcode(drv, info['zipcode'])
    ipt.phone(drv, info['phone'])
    ipt.city(drv, info['city'])    
    return True

def inputCard(drv, card):
    if not ipt.cardnumber(drv, card['cardnumber'], do=True):
        return False
    ipt.nameoncard(drv, card['nameoncard'], do=True)
    ipt.cv2(drv, card['securitycode'], do=True)
    el = ipt.expiration(drv, card['expiration'], do=True)
    if el is None:
        exp = card1['expiration'].split('/')
        ipt.month(drv, exp[0], do=True)  
        ipt.year(drv, exp[1][2:], do=True)
    return True  

def proc_info(drv, timeout):
    
    done = btn.enteraddress(drv)
    #print('enteraddress', done)    
    if done: 
        util.wait(1)
    
    if not inputInfo(drv): 
        return False
        
    num = 0    
    while num <= 2:       
        el = ipt.cardnumber(drv, do=False)
        if el: break
        done = btn.next(drv)    
        #print('next', num, done)
        if done:
            util.wait(timeout)
        num += 1
        
    if el is None: return False    
    if not inputCard(drv, card1): 
        return False
        
    util.clickRadio(drv)    
    util.wait(1)    
    done = btn.submitorder(drv)
    if not done: return False
    util.wait(timeout)
    msg = util.getMsg(drv)
    if msg:
        #print('resp', msg)    
        if not inputCard(drv, card2): 
            return False        
        util.clickRadio(drv)    
        util.wait(1)
        done = btn.submitorder(drv)
        if not done:
            return False
        util.wait(timeout)
        msg = util.getAns(drv)
        
    else:
        msg = util.getAns(drv)
    
    if not msg: return False    
    #print('ans:', msg[:20])   
    pattern = re.compile(r'order\s*number\s+is.{0,1}\s*\d+', re.I)
    res = re.search(pattern, msg)
    if res: 
        print(res.group(0))
    return res

def allurl():
    uls = np.load('allurl.npy', allow_pickle=True).item()
    drv = Browser(headless=False)
    pattern = re.compile(r'^[b-z].*', re.I)
    for name, url in uls.items():
        
        if not re.match(pattern, name) : continue    
        if url[:4] != 'http':
            url = 'https://' + url
        print(name, url)          
        href = util.getGoodsUrl(drv, url)
        print(href)
        if href is None: continue
        drv.open(href)
        util.wait()
        if not proc_good(drv):
            print('proc  good error')
            #time.sleep(10000) 
            continue
        if not proc_info(drv):
            print('proc  info error') 
            #time.sleep(10000)             
        else:
            print('%s is OK!' % url)    

if __name__ == '__main__':     
     
    #createAll()
    #allurl()
    exit()
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', type=int, default=15, metavar='timeout', help='input timeout (default: 15)')
    args = parser.parse_args() 
    timeout = args.t
    uls = ['https://armani-beauty.ca',  'https://tommyjohn.com',
          'https://us.myprotein.com/', 'https://www.skincarerx.com/',
          'https://www.dermstore.com/', 'https://www.skinstore.com/',
          'https://us.no7beauty.com/', 'https://www.omorovicza.com/',
          'https://baabuk.com',]
          
    old = time.time()
    drv = Browser(headless=False)
        
    for url in uls:
        print('start %s' % url)
        href = util.getGoodsUrl(drv, url)
        #print(href)
        if href is None:
            print('%s is No Find Goods' % url)                          
            continue
        drv.open(href)
        util.wait(timeout)
        if not proc_good(drv, timeout):
            #print('proc  good error')
            print('%s is No OK!' % url) 
            continue
        if not proc_info(drv, timeout):
            #print('proc  info error')
            print('%s is No OK!' % url)             
        else:
            print('%s is OK!' % url)       
                
    print(time.time() - old)
        
    