
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import re as re
import time
import pandas as pd



# Get Webdriver path, username and password
PATH = input("Enter the Webdriver path: ")
USERNAME = input("Enter the username: ")
PASSWORD = input("Enter the password: ")
print(PATH)
print(USERNAME)
print(PASSWORD)

# Use driver to open the link
driver = webdriver.Chrome(PATH)
driver.get("https://www.linkedin.com/uas/login")
time.sleep(3)


# Use login credentials to login
email=driver.find_element_by_id("username")
email.send_keys(USERNAME)
password=driver.find_element_by_id("password")
password.send_keys(PASSWORD)
time.sleep(3)
password.send_keys(Keys.RETURN)


post_links = []
post_texts = []
post_names = []


def Scrape_func(a,b,c):
    name = a[28:-1]
    page = a
    time.sleep(10)

    driver.get(page + 'detail/recent-activity/shares/')  
    start=time.time()
    lastHeight = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        newHeight = driver.execute_script("return document.body.scrollHeight")
        if newHeight == lastHeight:
            break
        lastHeight = newHeight
        end=time.time()
        if round(end-start)>20:
            break

    company_page = driver.page_source   

    linkedin_soup = bs(company_page.encode("utf-8"), "html")
    linkedin_soup.prettify()
    containers = linkedin_soup.findAll("div",{"class":"occludable-update ember-view"})
    print("Fetching data from account: "+ name)
    iterations = 0
    nos = int(input("Enter number of posts: "))
    for container in containers:

        try:
            text_box = container.find("div",{"class":"feed-shared-update-v2__description-wrapper ember-view"})
            text = text_box.find("span",{"dir":"ltr"})
            b.append(text.text.strip())
            c.append(name)
            iterations += 1
            print(iterations)
            
            if(iterations==nos):
                break

        except:
            pass    



n = int(input("Enter the number of entries: "))
for i in range(n):
    post_links.append(input("Enter the link: "))
for j in range(n):
    Scrape_func(post_links[j],post_texts,post_names)

        
driver.quit()


data = {
    "Name": post_names,
    "Content": post_texts,
}

df = pd.DataFrame(data)
df.to_csv("test1.csv", encoding='utf-8', index=False) #for csv

writer = pd.ExcelWriter("test1.xlsx", engine='xlsxwriter') #for xlsx
df.to_excel(writer, index =False)
writer.save()

