# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib.request


urls = ['https://europa.eu/youth/evs_database_en?country=&town=&name=&pic=&eiref=&field_eyp_vp_accreditation_type=All&topic=&inclusion_topic=']#first url
pages = 228
for i in range(1,pages):#next urls
    urls.append('https://europa.eu/youth/evs_database_en?country=&town=&name=&pic=&eiref=&field_eyp_vp_accreditation_type=All&topic=&inclusion_topic=&page='+str(i))


with open('fetched_data.csv',mode='w',encoding="utf-8") as f:#write the first line in the csv
    firstLineValuesNames = "Name of the Organization|EVS/PIC No.|Field|City|County|Website"#csv delimiter="|"
    f.write(firstLineValuesNames + '\n')#write the first line


for url in urls:
    print('fetching data for url: ' + url)
    req = urllib.request.Request(url)
    resp = urllib.request.urlopen(req)
    respData = resp.read()
    soup = BeautifulSoup(respData,from_encoding="utf-8")


    with open('fetched_data.csv',mode='a',encoding="utf-8") as f:#start writing data to csv delimiter="|"
        for o_list in soup.findAll('div', {'class' : 'o_list'}):
            for org_name in o_list.findAll('div', {'class': 'org_name'}):#get the organisation's name
                #print(org_name.text.encode('utf-8'))
                f.write(org_name.text + "|")
            for two_columns in o_list.findAll('div', {'class': 'two columns'}):#get the EVS divs
                for divElement in two_columns.findAll('div'):#iter through the above divs
                    elementText =  divElement.text.encode('utf-8')
                    if 'EVS accredited'.encode('utf-8') not in elementText:#we don't want the first div containing "EVS accredited". Only the next two containing the Number and the Status (in order)
                        #print(elementText)
                        f.write(divElement.text.replace("EVS no: ","").replace("PIC no: ","").replace(", ","/") + "|")
            for org_address in o_list.findAll('div', {'class': 'org_address'}):#get the organisation's address (it will be "City,Country")
                #print(org_address.text.encode('utf-8'))
                f.write(org_address.text.replace(",","|") + "|")#replacing the "," with the defined csv delimiter="|"
            for org_eiref in o_list.findAll('div', {'class': 'org_eiref'}):#get the organisation's EIRef
                #print(org_eiref.text.encode('utf-8'))
                f.write(org_eiref.text + "|")
            for org_website_link in o_list.findAll('div', {'class': 'org_website_link'}):#get the organisation's website url
                #print(org_website_link.text.encode('utf-8'))
                f.write(org_website_link.text)
            f.write("\n")