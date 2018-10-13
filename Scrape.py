import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
import selenium
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re
import unicodedata

driver= webdriver.Chrome()
# driver.set_page_load_timeout(10)
driver.get("https://www.vogue.com/fashion-shows/spring-2019-menswear")
time.sleep(2)
    
try:
    searchclick=driver.find_element_by_class_name("show-finder--button show-finder--button__season")
    searchclick.click()
    time.sleep(2)
    print("try part executed")
    driver.quit()
except :
    searchclick=driver.find_element_by_xpath("//*[@id='main']/div[2]/div/div/div/button[2]/span[1]")
    searchclick.click()
    time.sleep(2)
    print("exception part executed")
    element_list = driver.find_element_by_xpath("//ul[@class='show-finder--list']")
    content = element_list.text
    driver.quit()
    print("program completed")
   
item_list = content.split("\n")
pattern = re.compile('[^\d].*(2017|2018|2019).*')  #Prints links that only contain the year '2017,'2018', & '2019'
newlist = list(filter(pattern.match, item_list))

item_list_new=[]
for i in newlist:
    a = i.replace(" ","-")
    item_list_new.append(a)
	
dict_item_list_new = {"shows":item_list_new}
df_item_list_new = pd.DataFrame(dict_item_list_new)
df_item_list_new.to_excel("E:/vogue_shows.xlsx")
    
def scraping(url):
    html = urlopen(url)
    bsObj = BeautifulSoup(html.read(),"lxml")
    links = []
    list_of_shows = bsObj.find("div",class_="season-module--tab-container season-module--tab-container__latest").findAll('a')
    for i in list_of_shows:
        links.append(i.text)    
    return links

show_from_excel = pd.read_excel("E:/vogue_shows_shows.xlsx",sheet_name = "Sheet1")

dict_for_shows = {}
count = 0
for i in show_from_excel["shows"]:
    url_changed =  "https://www.vogue.com/fashion-shows/" + i.lower()
    
    a = scraping(url_changed)
    dict_for_shows[i.lower()] = a
    count +=1
    print(count) 
   
df_dict_for_Shows = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in dict_for_shows.items() ]))
df_dict_for_Shows.to_excel("E:/final_vogue.xlsx")
