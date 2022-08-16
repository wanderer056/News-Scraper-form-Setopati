from bs4 import BeautifulSoup
import requests
import time
import pandas as pd

pagesToGet=9
upperupperframe=[]
cat_link_list= ["political","social","market","entertainment","khelkud","view","International"]

filename="finalscrapednews.csv"
f=open(filename,"a",encoding="utf-8")
headers="Headline, Link, Date, Author,Thumbnail \n"
f.write(headers)
for cat_link in cat_link_list:
    upperframe=[]
    for page in range(1,pagesToGet+1):
        print("processing page : ", page)
        
        url = "https://en.setopati.com/{}?page=".format(cat_link)+str(page)
        print(url)

        response = requests.get(url)

        html_text = response.text

        time.sleep(2)

        soup = BeautifulSoup(html_text, 'html.parser')
        frame=[]

        news_list_vast = soup.find_all('div', class_='news-cat-list') #list containing all the class from news-cat-list which is like    parent of our required class for seperating the news

        news_list=[]  #for storing individual newss block filtered from above

        for news_block in news_list_vast:
            news_list.extend(news_block.find_all("div",attrs={"class":["col-md-4","col-md-6"]})) #merging the tag containing col-md-4 and col-md-6 creating single list that can be iterated 

        #Extracting specific details to csv file
        for news in news_list:
            Headline= news.find("span",class_="main-title").text
            Link = news.a['href']
            Date= news.find("span",class_="time-stamp").text
            Author=news.find("span",class_="author-left").text
            Thumbnail=news.img.get('src')

            frame.append((Headline,Link,Date,Author,Thumbnail))
            f.write(Headline.replace(",","^")+","+Link+","+Date.replace(",","^")+","+Author.replace(",","^")+","+Thumbnail+"\n")

        upperframe.extend(frame)
    upperupperframe.extend(upperframe)

f.close()

#For visualizing data with panda only
data=pd.DataFrame(upperupperframe, columns=['Headline','Link','Date','Author','Thumbnail'])
data.head()