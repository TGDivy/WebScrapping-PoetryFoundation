import pandas as pd

def joiner(total_pages, total_batches):
    file_names = [""]*total_batches*40
    for i in range(total_batches):
        #File name formating.
        j=0
        while(j<8000):
            file_names[i*40+int(j/200)] = "G:\\OneDrive - University of Edinburgh\\Poem Generation\\WebScrapping for Poems\\PoemData\\PoetryFoundationData"+str(i*total_pages+1)+"-"+str(total_pages*(i+1))+".txt"+ str(j) +"-"+str(j+200)+".csv"
            j=j+200
    return file_names

def main():
    file_names = joiner(400,5)
    list = []

    for name in file_names:
        try:
            list=list+[pd.read_csv(name)]
        except Exception as FileNotFoundError:
            print(".")
            pass
        except Exception as e:
            print(e)
    data = pd.concat(list)
    data = data.drop(columns="Unnamed: 0")
    data.to_csv("PoetryFoundationData.csv")
if __name__ == '__main__':
    main()
