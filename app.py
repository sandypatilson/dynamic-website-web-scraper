import requests
from bs4 import BeautifulSoup
import pandas as pd


baseurl = 'https://www.thewhiskyexchange.com/'

#headers = {
   # 'User-Agent':'Mozilla'
#}

r = requests.get('https://www.thewhiskyexchange.com/c/35/japanese-whisky')
soup = BeautifulSoup(r.content, 'lxml')

productlist = soup.find_all('li', class_='product-grid__item')

productlinks = []

for item in productlist:
    for link in item.find_all('a', href = True):
        productlinks.append(baseurl + link['href'])
        

whiskylist = []
for link in productlinks:
    r = requests.get(link) #headers = headers)
    soup = BeautifulSoup(r.content, 'lxml')
    name = soup.find('h1', class_ = 'product-main__name').text.strip()
    price = soup.find('p', class_ = 'product-action__price').text.strip()
    try:
        rating = soup.find('div', class_= 'review-overview').text.strip()
    except:
        rating = 'no rating'

    whisky = {
        'name': name,
        'rating':rating,
        'price': price
        }
    whiskylist.append(whisky)
    print("Saving ", whisky['name'])

df = pd.DataFrame(whiskylist)
print(df.head())
df.to_excel("E:/Projects/scrapped excel sheet/sample.xlsx")