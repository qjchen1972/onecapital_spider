# -*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common import exceptions as ex
from bs4 import BeautifulSoup
import numpy as np
import requests
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
#import undetected_chromedriver as uc
#from selenium_stealth import stealth
import os
import time


class Browser:

    original_window = None
    def __init__(self, headless=False, delay=20):
        
        #os.system(r'start chrome --remote-debugging-port=9527')
        
        options = webdriver.ChromeOptions()
        #options.add_experimental_option("debuggerAddress", "127.0.0.1:9527")
        
        #DesiredCapabilities.CHROME["pageLoadStrategy"] = "none" 
        
        #options.add_experimental_option('detach', True)  
        options.add_argument('--start-maximized')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging']) 
        options.add_argument("--log_level= 3")
        
        #options.add_argument("--incognito")
        #options.add_argument("--disable-blink-features=AutomationControlled")
        
        prefs = {'profile.managed_default_content_settings.images': 2}
        options.add_experimental_option('prefs',prefs)

        if headless:
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
        
        self.driver = webdriver.Chrome(
                                service=Service(ChromeDriverManager().install()), 
                                options=options)
        #self.driver = uc.Chrome()
        # Selenium Stealth settings
        '''
        stealth(self.driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,)
        '''        
        #self.driver.implicitly_wait(delay)
        
    def max_window(self):
        self.driver.maximize_window()
    
    def get_element_wait(self, by, value, secs=5):   
        try:
            element = WebDriverWait(self.driver, secs, 1).until(\
                 EC.presence_of_element_located((by, value)))
            return element     
        except Exception as e:
            return None
    
    def get_element(self, by, value):
        try:
            el = self.driver.find_element(by, value) 
            return el            
        except Exception as e:
            return None
        
    def get_elements(self, by, value):
        try:
            els = self.driver.find_elements(by, value)        
        except Exception as e:
            els = []        
        return els
        
    def click(self, el):
        try:
            el.click()
            return True
        except Exception as e:
            return False
    
    def scorll_click(self, el):
        try:
            self.driver.execute_script("arguments[0].scrollIntoView();", el)        
            el.click()
            return True
        except Exception as e:
            return False            
    
    def scroll_element(self, el):
        try:
            self.driver.execute_script("arguments[0].scrollIntoView();", el) 
            return True            
        except Exception as e:
            return False
    
    def scroll(self, value):
        try:            
            driver.execute_script("window.scrollBy(0, %d)" %(value))            
        except Exception as e:
            pass    
        
    def scroll_bottom(self):
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        except Exception as e:
            pass
            
    def scroll_top(self):
        try:
            driver.execute_script("window.scrollTo(0, 0)")
        except Exception as e:
            pass
            
    def js_click(self, el):
        try:
            self.driver.execute_script("arguments[0].click();",el);
            return True
        except Exception as e:
            #print(e)
            return False        
    
    def link_click(self, el):
        try:
            url = el.get_attribute("href");
            self.driver.get(url)
            return True
        except Exception as e:
            #print(e)
            return False        
    
    def submit(self, el):
        try:
            el.submit()
            return True
        except Exception as e:
            return False      
            
    def key_click(self, el):
        try:
            el.send_keys(Keys.ENTER);
            return True
        except Exception as e:
            #print(e)
            return False 
    
    def right_click(self,el): 
        try:
            ActionChains(self.driver).context_click(el).perform()
            return True
        except Exception as e:
            #print(e)
            return False            
            
    def move_to_element(self, el):
        try:
            ActionChains(self.driver).move_to_element(el).perform()
            return True
        except Exception as e:
            #print(e)
            return False            
            
    def double_click(self, el):
        try:
            ActionChains(self.driver).double_click(el).perform()
            return True
        except Exception as e:
            #print(e)
            return False            
    
    
    def get_attribute(self, el, attribute):
        try:
            return el.get_attribute(attribute)   
        except Exception as e:
            return None        
    def get_allAttr(self, el):
        try:
            attr = self.driver.execute_script('var items = {}; for (index = 0;\
                            index < arguments[0].attributes.length; ++index) {\
                            items[arguments[0].attributes[index].name] =\
                            arguments[0].attributes[index].value };\
                            return items;', el)
            return  attr               
        except Exception as e:
            return None                                      
    
    def get_text(self, el):
        try:    
            return el.text
        except Exception as e:
            return None             
        
    def get_title(self):
        return self.driver.title

    def get_url(self):
        return self.driver.current_url

    def open(self, url):
        try:
            self.driver.get(url) 
            return True 
        except Exception as e:
            return False        
            
    def open_scroll(self, url, num=10):
        try:
            self.driver.get(url)
            for i in range(num):
                self.driver.execute_script(
                   "window.scrollTo(0, document.body.scrollHeight/10*%s);" % i)
                time.sleep(0.5)
            return True    
            #time.sleep(5)        
            #ActionChains(self.driver).scroll_by_amount(0, 30000).perform()
        except Exception as e:
            return False    
        
    def accept_alert(self):
        try:
            self.driver.switch_to.alert.accept()       
        except Exception as e:
            pass     
        

    def dismiss_alert(self):
        try:
            self.driver.switch_to.alert.dismiss()       
        except Exception as e:
            pass
        

    def switch_to_frame(self, el):
        try:
            self.driver.switch_to.frame(el)
        except Exception as e:
            pass
                
    def switch_to_frame_out(self):
        self.driver.switch_to.default_content()        
    
    def send_value(self, el, text):
        try:
            el.send_keys(text) 
            return True            
        except Exception as e:
            print(e)
            return False            
            
    def send_value_x(self, el, text):
        try:
            for s in  text:
                el.send_keys(s)  
            return True                
        except Exception as e:
            print(e)
            return False     
    
    def clear(self, el):
        #el.clear()
        try:
            el.send_keys(Keys.CONTROL,"a")
            el.send_keys(Keys.DELETE)
            return True            
        except Exception as e:
            return False
        
    def quit(self):
        self.driver.quit()
    
    def close(self):
        self.driver.close()
        
    def handle(self):
        return self.driver.current_window_handle
    
    def handles(self):
        return self.driver.window_handles
        
    def pagesrc(self):        
        return self.driver.page_source          