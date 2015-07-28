# -*- coding: utf-8 -*-
from multiprocessing.dummy import Pool as ThreadPool
from bs4 import BeautifulSoup
import urllib.request


#Construct the URLs List
urls = ['https://europa.eu/youth/evs_database_en?country=&town=&name=&pic=&eiref=&field_eyp_vp_accreditation_type=All&topic=&inclusion_topic=']#first url
pages = 228
for i in range(1,pages):#next urls
    urls.append('https://europa.eu/youth/evs_database_en?country=&town=&name=&pic=&eiref=&field_eyp_vp_accreditation_type=All&topic=&inclusion_topic=&page='+str(i))


#Write the first line in the csv
with open('fetched_data.csv',mode='w',encoding="utf-8") as f:
    firstLineValuesNames = "Name of the Organization|EVS/PIC No.|Field|City|County|Website"#csv delimiter="|"
    f.write(firstLineValuesNames + '\n')#write the first line



def getText(element):#In order to get the inner Text from the given element. Returns empty string if the element is None
    if element:
        return element.text
    return ''


# The main Function fetching the data from given URL
def getUrlData(url):

    print('fetching data for url: ' + url)
    req = urllib.request.Request(url)
    resp = urllib.request.urlopen(req)
    respData = resp.read()
    soup = BeautifulSoup(respData,from_encoding='utf-8')


    pagedata = []#init the returned list
    for o_list in soup.findAll('div', {'class' : 'o_list'}):
        org_name = getText(o_list.find('div', {'class': 'org_name'}))#get the organisation's name
        #print(org_name.encode('utf-8'))

        two_columns = o_list.find('div', {'class': 'two columns'})#get the EVS divs
        divElemList = []
        for divElement in two_columns.findAll('div'):#iter through the above divs
            elementText =  getText(divElement).encode('utf-8')
            if 'EVS accredited'.encode('utf-8') not in elementText:#we don't want the first div containing "EVS accredited". Only the next two containing the Number and the Status (in order)
                #print(elementText)
                divElemList.append(getText(divElement).replace("EVS no: ", "").replace("PIC no: ", "").replace(", ", "/"))
        evsPicField = '|'.join(divElemList)

        org_address = getText(o_list.find('div', {'class': 'org_address'}))#get the organisation's address (it will be "City,Country")

        org_address = org_address.replace(",","|")#replacing the "," with the defined csv delimiter="|"
        #print(org_address.encode('utf-8'))

        org_website_link = getText(o_list.find('div', {'class': 'org_website_link'}))#get the organisation's website url
        #print(org_website_link.encode('utf-8'))

        variablesList = [org_name,evsPicField,org_address,org_website_link]

        lineToWrite = '|'.join(variablesList)
        pagedata.append(lineToWrite.replace('| ', '|') + '\n')#Trim the excess spaces and add new line character in each line
    return pagedata



linesToWrite = []

###########
# Let's start Multithread Magic (we don't care about the order of fetched data)
###########

#make the Pool of workers
pool = ThreadPool(4)#Four threads are ok for url requests.

#open the urls in their own threads and return the results
results = pool.map(getUrlData, urls)

for result in results:#for each poll group extend the linesToWrite
    linesToWrite.extend(result)


#close the pool and wait for the work to finish
pool.close()
pool.join()


with open('fetched_data.csv', mode='a', encoding='utf-8') as f:#start writing data to csv delimiter="|"
    f.writelines(linesToWrite)