# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib.request


urls = ['https://europa.eu/youth/evs_database_en?country=&town=&name=&pic=&eiref=&field_eyp_vp_accreditation_type=All&topic=&inclusion_topic=']#first url
pages = 228
for i in range(1,pages):#next urls
    urls.append('https://europa.eu/youth/evs_database_en?country=&town=&name=&pic=&eiref=&field_eyp_vp_accreditation_type=All&topic=&inclusion_topic=&page='+str(i))


for url in urls:
    print('fetching data for url: ' + url)
    req = urllib.request.Request(url)
    resp = urllib.request.urlopen(req)
    respData = resp.read()


    soup = BeautifulSoup(respData,from_encoding="utf-8")


    with open('fetched_data.txt',mode='a',encoding="utf-8") as f:
        f.write("\n\n" + "#"*10 + "\nData from URL: " + url + "#"*10)
        for o_list in soup.findAll('div', {'class' : 'o_list'}):
            for org_name in o_list.findAll('div', {'class': 'org_name'}):
                print(org_name.text.encode('utf-8'))
                f.write(org_name.text + ",")
            for org_address in o_list.findAll('div', {'class': 'org_address'}):
                print(org_address.text.encode('utf-8'))
                f.write(org_address.text + ",")
            for org_eiref in o_list.findAll('div', {'class': 'org_eiref'}):
                print(org_eiref.text.encode('utf-8'))
                f.write(org_eiref.text + ",")
            for org_website_link in o_list.findAll('div', {'class': 'org_website_link'}):
                print(org_website_link.text.encode('utf-8'))
                f.write(org_website_link.text + ",")
            f.write("\n")


    #data written from columns (all data)
    with open('fetched_data_col.txt',mode='a',encoding="utf-8") as f:
        f.write("\n\n" + "#"*10 + "\nData from URL: " + url + "#"*10)
        for o_list in soup.findAll('div', {'class' : 'o_list'}):
            for org_name in o_list.findAll('div', {'class': 'four columns'}):
                print(org_name.text.encode('utf-8'))
                f.write(org_name.text + " ||| ")
            for org_address in o_list.findAll('div', {'class': 'two columns'}):
                print(org_address.text.encode('utf-8'))
                f.write(org_address.text + " ||| ")
            f.write("\n")