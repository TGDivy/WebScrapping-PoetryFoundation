import urllib.request
import bs4 as bs
import pandas as pd
import re
import numpy as np
from multiprocessing import Pool

# Reformats the string into readable text.
def pretty_text(text):
    final = (((text).replace(u'\xa0', u' ')).replace(u'\r ',u'\n'))
    return final

def parse(url): 
    #print(url) # Testing
    try:
        hdr = {'User-Agent':'Mozilla/5.0'}
        req = urllib.request.Request(url,headers=hdr)
        sauce = urllib.request.urlopen(req).read()
        soup = bs.BeautifulSoup(sauce,'html.parser') #Beautiful Soup object

        # Data Extraction from the url.
        poem = (pretty_text(soup.find_all('div', class_="o-poem")[0].text))

        title = soup.find_all('h1')[0].text

        poet = soup.find_all('a', href=re.compile('.*poets/.*'))[0].text

        tags = soup.find_all('a', href=re.compile('.*topics.*'))
        tags = [tag.text for tag in tags]
        tags = ",".join(tags)

        print(poet)
        #df_.iloc[i] = [title,poem,poet,tags]
        return(title,poem,poet,tags)

    except Exception as IndexError:
        return(Null,Null,Null,Null) 
    except Exception as e:
        print(e)
        return(Null,Null,Null,Null)

def load(total_pages, total_batches):
    file_names = [""]*total_batches
    for i in range(total_batches):
        #File name formating.
        file_names[i] = "PoetryFoundationUrls"+str(i*total_pages+1)+"-"+str(total_pages*(i+1))+".txt"
    return file_names

def main():
    #File name details.
    total_pages   = 10
    urls_per_page = 20
    total_batches = 5
    total_poems = total_pages*urls_per_page

    url_file_names = load(total_pages, total_batches)

    for file_name in url_file_names:

        print("START: "+file_name)

        urls = np.loadtxt(file_name, dtype="str")
        print(urls.size)
        urls = np.unique(urls) #Deleting the repeated url links.
        print(urls.size)

        # Multiprocessing the extractions.
        p = Pool(10)
        data = p.map(parse,urls) 
        p.terminate()

        print("DONE: "+file_name)
        dataF = pd.DataFrame(columns=["Title","Poem","Poet","Tags"], index=list(range(1,total_poems+1)))

        for row,rowNo in zip(data,list(range(total_poems))):
            print([row[0]])
            dataF.iloc[rowNo] = [row[0],row[1],row[2],row[3]]

        dataF.to_csv("PoetryFoundationData"+file_name[len("PoetryFoundationUrls"):]+".csv")

if __name__ == '__main__':
    main()
