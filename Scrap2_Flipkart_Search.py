
# coding: utf-8

# In[20]:


from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
import datetime


# In[12]:


baseurl="https://www.flipkart.com/search?&sort=price_desc&q="
search_key = input("Enter Search Word:")
start_url = "{0}{1}".format(baseurl,search_key)

r  = requests.get(start_url)
data = r.text
soup = BeautifulSoup(data)

nav_pages=soup.findAll("nav",{"class":"_1ypTlJ"})

items = []
page_nums = []
for link in nav_pages[0].find_all('a'):
    if link.text.isdigit():
        page_nums.append(link.text)

for page_num in page_nums:
    time.sleep(10)  #to avoid bot feeling
    url = "{0}&page={1}".format(start_url,page_num)
    r1  = requests.get(url)
    data1 = r1.text
    soup1 = BeautifulSoup(data1)

    objs=soup1.findAll("div",{"class":"_3O0U0u"})
    for obj in objs:
        name = None
        rating = None
        price = None
        
        name=obj.findAll("div",{"class":"_3wU53n"})
        if name:
            name = name[0].text
        else:
            name = None
        rating=obj.findAll("div",{"class":"hGSR34 _2beYZw"})
        if rating:
            rating = rating[0].text
            rating = rating.split()[0]
            rating = float(rating)
        else:
            rating = None
        price=obj.findAll("div",{"class":"_1vC4OE _2rQ-NK"})
        if price:
            price = price[0].text
            price = ''.join(e for e in price if e.isdigit())
            price = float(price)
        else:
            price = None
			

        items.append([name,rating,price,int(page_num)])


# In[14]:


labels = ['name','rating','price','page_num']
df = pd.DataFrame(items, columns=labels)


# In[21]:


cdate = datetime.datetime.now().strftime("%Y%m%d%H%M")
out_file_name = "Flipkart_{}_{}.csv".format(search_key,cdate)
df.to_csv(out_file_name,index=False)

