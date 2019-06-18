import urllib.request
import bs4 as bs
import pandas as pd
import re
import numpy as np
from multiprocessing import Pool
import time
import sys
# For simulating the table on the webpage which is dynamically loaded.
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Reformats the string into readable text.
def pretty_text(text):
    final = (((text).replace(u'\xa0', u' ')).replace(u'\r ',u'\n'))
    return final

def parse(url):
    #print(".")
    sys.stdout.write("+") # Testing
    sys.stdout.flush()
    try:
        hdr = {'User-Agent':'Mozilla/5.0'}
        req = urllib.request.Request(url,headers=hdr)
        sauce = urllib.request.urlopen(req, timeout=10).read()
        soup = bs.BeautifulSoup(sauce,'html.parser') #Beautiful Soup object

        # Data Extraction from the url.
        poem = (pretty_text(soup.find_all('div', class_="o-poem")[0].text))

        title = soup.find_all('h1')[0].text

        poet = soup.find_all('a', href=re.compile('.*poets/.*'))[0].text

        tags = soup.find_all('a', href=re.compile('.*topics.*'))
        tags = [tag.text for tag in tags]
        tags = ",".join(tags)

        #print(poet)
        #sys.stdout.write('.')
        #sys.stdout.flush()
        #df_.iloc[i] = [title,poem,poet,tags]
        return(title,poem,poet,tags)

    except Exception as IndexError:
        return(None,None,None,None)
    except Exception as e:
        print(e)
        return(None,None,None,None)

def load(total_pages, total_batches):
    file_names = [""]*total_batches
    for i in range(4,total_batches+4):
        #File name formating.
        file_names[i-4] = "PoetryFoundationUrls"+str(i*total_pages+1)+"-"+str(total_pages*(i+1))+".txt"
    return file_names

def main():
    #File name details.
    total_pages   = 400
    urls_per_page = 20
    total_batches = 1
    total_poems = total_pages*urls_per_page

    url_file_names = load(total_pages, total_batches)
    print(url_file_names)
    for file_name in url_file_names:

        print("START: "+file_name)

        urls = np.loadtxt(file_name, dtype="str")
        print(urls.size)
        urls = np.unique(urls) #Deleting the repeated url links.
        print(urls.size)

        # Multiprocessing the extractions.
        i=0
        while(i<urls.size):
            timenow = time.time()
            p = Pool()
            data = 0
            if(i+200<urls.size):
                data = p.map(parse,urls[i:i+200])
            else:
                data = p.map(parse,urls[i:urls.size])
            print()
            print("Should terminate now, took",time.time()-timenow)
            p.terminate()
            p.join()

            print("DONE: "+file_name + str(i) +"-"+str(i+200))
            dataF = pd.DataFrame(columns=["Title","Poem","Poet","Tags"], index=list(range(1,200+1)))

            for row,rowNo in zip(data,list(range(total_poems))):
                dataF.iloc[rowNo] = [row[0],row[1],row[2],row[3]]
            dataF = dataF.dropna()
            dataF.to_csv("G:\\OneDrive - University of Edinburgh\\Poem Generation\\WebScrapping for Poems\\PoemData\\PoetryFoundationData"+file_name[len("PoetryFoundationUrls"):]+ str(i) +"-"+str(i+200)+".csv")
            i=i+200



if __name__ == '__main__':
    main()
