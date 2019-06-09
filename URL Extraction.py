#import urllib.request #This won't be used as the tables are dynamically loaded.
import bs4 as bs
import re
import numpy as np #Using this to efficiently create the output file.

# For simulating the table on the webpage which is dynamically loaded.
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from multiprocessing import Pool
import time

total_pages     = 10
links_per_page  = 20

def UrlExtract(batch_number):
    #Setting up the browser
    path = r"C:\\Users\\divyb\\OneDrive\\Desktop\\chromedriver.exe" #Path for my Chrome driver.
    driver = webdriver.Chrome(executable_path = path) # Setting up the browser with selenium.



    page_start = batch_number*total_pages + 1 # Knowing which page this iteration will start from.

    urls = np.array(["s"*(192)]*total_pages*links_per_page) # it seems, no url link is longer than 192 charachters, and each page contains 20 links
    for i in range(0,total_pages):
        print(i+page_start) # For testing purposes only.

        # The site below, has all its content on different webpages, this makes it easier.
        site = "https://www.poetryfoundation.org/poems/browse#page="+str(i+page_start)+"&sort_by=recently_added"
        driver.implicitly_wait(45)
        time.sleep(1)
        driver.get(site) # Opening the website.
        html_source = driver.page_source # Getting the html formate file of the webpage after it has been loaded by the browser.

        #Creating beautiful soup object to parse the links.
        soup = bs.BeautifulSoup(html_source, features="html.parser")

        count = 0 #We only want a certain number of useful url links.

        for aHref in soup.find_all("a",href=re.compile('.*/poems/[0-9]+/.*')): #All the useful poem links have a format /poems/29393/[name]
            urls[((i)*links_per_page)+count] = (aHref.get("href"))
            if(count==(links_per_page-1)): # 0 indexing.
                break
            count+=1

    np.savetxt("PoetryFoundationUrls"+str(page_start)+"-"+str(page_start+total_pages-1)+".txt", urls, fmt="%s")

def main():
    # Total pages the poetry foundation has, 2200
    #Dividing the task in batches so that its faster with multiprocessing.
    # That is 11 batches of size 200 per page are required to get all the poem urls

    total_pages    = 10 # Total number of pages we want to extract in a single file, each page consists of 20 poem links.
    links_per_page = 20 # After inspecting the webpage element.
    total_batches  = 5 # Number of times we want to do the operation.
    start_batch_from = 0 # Because sometimes, I run the program for a small number of batches first.
    batch_iterable = list(range(start_batch_from,total_batches+start_batch_from))

    #multiprocessing with pool.
    print("start")
    p = Pool(processes = 3)
    p.map(UrlExtract,batch_iterable)
    p.terminate()
    print("end")


if __name__ == '__main__':
    main()
