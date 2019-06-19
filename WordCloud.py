import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import numpy as np
from PIL import Image
import pandas as pd
import random

def file():
    DataSet = pd.read_csv("G:\\OneDrive - University of Edinburgh\\Poem Generation\\WebScrapping-PoetryFoundation\\PoetryFoundationData.csv")
    tags = DataSet["Tags"]
    tags = tags.dropna()
    string =""
    #print(tags)
    for i in tags:
        string = string+i
    return string

def grey_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(0, 0%%, %d%%)" % random.randint(60, 100)

def create_word_cloud(string):
   maskArray = np.array(Image.open("bookmask.png"))
   cloud = WordCloud(background_color = "black", mask=maskArray,width=1280,height=720,scale=2, max_words = 200, stopwords = set(STOPWORDS), color_func=grey_color_func)
   cloud.generate(string)
   cloud.to_file("wordCloud.png")
   pass

def main():
    string = file()
    create_word_cloud(string)

if __name__ == '__main__':
    main()
