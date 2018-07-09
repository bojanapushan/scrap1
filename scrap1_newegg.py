# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 19:35:29 2018

@author: Shanmukha
"""

from urllib.request import urlopen as ur
from bs4 import BeautifulSoup as BS
my_url='https://www.newegg.com/global/in/Product/ProductList.aspx?Submit=ENE&DEPA=0&Order=BESTMATCH&Description=graphics+card&ignorear=0&N=-1&isNodeId=1'
#opening up connection and grabing the information
uclient=ur(my_url)
page_html=uclient.read()
uclient.close()
#html parsing
page_soup=BS(page_html,"html.parser")
#grab each product information
containers=page_soup.findAll("div",{"class":"item-container"})
filename="scrap1_newegg.csv"
f=open(filename,"w")
headers="brand,product_name,shipping\n"
f.write(headers)
for container in containers:
    brand=container.div.div.a.img['title']
    title_container=container.findAll("a",{"class":"item-title"})
    product_name=title_container[0].text
    shipping_container=container.findAll("li",{"class":"price-ship"})
    shipping=shipping_container[0].text.strip()
    print("brand: "+ brand)
    print("product_name: "+ product_name)
    print("shipping:"+ shipping)
    f.write(brand + "," +product_name.replace(",","|") + "," + shipping + "\n")
f.close()