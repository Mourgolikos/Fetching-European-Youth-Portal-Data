# -*- coding: utf-8 -*-
__author__ = 'Paschaleris Triantafyllos'
from multiprocessing.dummy import Pool as ThreadPool
from bs4 import BeautifulSoup
import urllib.request
from collections import OrderedDict


#Construct the URLs List
urls = ['https://europa.eu/youth/evs_database_en?country=&town=&name=&pic=&eiref=&field_eyp_vp_accreditation_type=All&topic=&inclusion_topic=']#first url
pages = 228
for i in range(1,pages):#next urls
    urls.append('https://europa.eu/youth/evs_database_en?country=&town=&name=&pic=&eiref=&field_eyp_vp_accreditation_type=All&topic=&inclusion_topic=&page='+str(i))


#Write the first line in the csv
with open('fetched_data.csv',mode='w',encoding="utf-8") as f:
    firstLineValuesNames = "Name|Address|Postal Code|City|Country|EVS accreditation type|Website|Email|Phone|Fax|EVS No.|PIC No.|Organisation topics"#csv delimiter="|"
    f.write(firstLineValuesNames + '\n')#write the first line




def getText(element):#In order to get the inner Text from the given element. Returns empty string if the element is None
    if element:
        return element.text
    return ''


def trimWhiteSpacesBeforeAfterDelimiter(stringg,delimiter):
    return stringg.replace(' ' + delimiter, '|').replace(delimiter + ' ', '|')



def getFullowedUrlData(furl,dataDict_passed):
    print('fetching data for followed url: ' + furl)
    req = urllib.request.Request(furl)
    resp = urllib.request.urlopen(req)
    respData = resp.read()
    soup = BeautifulSoup(respData,from_encoding='utf-8')


    dataDict = dataDict_passed#some renaming matching to the parent function's Dictionary naming

    topics = soup.find('div', {'class' : 'topics'})
    block1 = topics.find('div', {'class' : 'block1'})

    if block1:#checking if NoneType
        block1circle = block1.find('ul', {'class' : 'circle'})
        if block1circle:#checking if NoneType
            dataDict['Organisation topics']  = ' & '.join([elem.text for elem in block1circle.findAll('li')])#reading the data about Organisation's Type and Field (this order)



    block2 = topics.find('div', {'class' : 'block2'})

    for row,divElem in enumerate(block2.findAll('p')):#reading the data about Organisation's Type and Field (this order)
        if "Web" in getText(divElem):
            dataDict['Website'] = getText(divElem).replace('Web: ', '')
        elif "Email" in getText(divElem):
            dataDict['Email'] = getText(divElem).replace('Email: ', '')
        elif "Phone" in getText(divElem):
            dataDict['Phone'] = getText(divElem).replace('Phone: ', '')
        elif "Fax" in getText(divElem):
            dataDict['Fax'] = getText(divElem).replace('Fax: ', '')
        elif row == 0:
            dataDict['Name'] = getText(divElem)
        elif row == 1:
            dataDict['Address'] = getText(divElem)
        elif row == 2:
            dataDict['Postal Code'] = getText(divElem)
        elif row == 3:
            splitted = getText(divElem).split(',')#they are separated by ',' e.g.: "City, Country"
            if len(splitted)>1:#sometimes City is not provided!
                dataDict['City'] = splitted[0]
                dataDict['Country'] = splitted[1]
            else:
                dataDict['Country'] = splitted[0]

    return dataDict



# The main Function fetching the data from given URL
def getUrlData(url):

    #Setup the dictionary that will hold the data
    dataDict = OrderedDict()#...because the order is important
    dataDict['Name']                    = ''#completed in followed url
    dataDict['Address']                 = ''#completed in followed url
    dataDict['Postal Code']             = ''#completed in followed url
    dataDict['City']                    = ''#completed in followed url
    dataDict['Country']                 = ''#completed in followed url
    dataDict['EVS accreditation type']  = ''
    dataDict['Website']                 = ''#completed in followed url
    dataDict['Email']                   = ''#completed in followed url
    dataDict['Phone']                   = ''#completed in followed url
    dataDict['Fax']                     = ''#completed in followed url
    dataDict['EVS No.']                 = ''
    dataDict['PIC No.']                 = ''
    dataDict['Organisation topics']     = ''#completed in followed url


    print('fetching data for url: ' + url)
    req = urllib.request.Request(url)
    resp = urllib.request.urlopen(req)
    respData = resp.read()
    soup = BeautifulSoup(respData,from_encoding='utf-8')


    pagedata = []#init the returned list that will hold the Dictionary for the


    for o_list in soup.findAll('div', {'class' : 'o_list'}):

        org_name = o_list.find('div', {'class': 'org_name'})#get the organisation's name
        urlToFollow = r'https://europa.eu' + org_name.find('a')['href']#get the href attribute

        # the following line will rewrite the dataDict with the data from the followe url
        dataDict = getFullowedUrlData(furl=urlToFollow, dataDict_passed=dataDict)

        # now fetch the remaining data values from the original parent-page
        two_columns = o_list.find('div', {'class': 'two columns'})#get the EVS divs
        for divElement in two_columns.findAll('div'):#iter through the above divs
            elementText =  getText(divElement)
            if 'EVS no:' in elementText:
                dataDict['EVS No.'] = elementText
            elif 'PIC no:' in elementText:
                dataDict['PIC No.'] = elementText
            elif 'EVS accredited' not in elementText:
                dataDict['EVS accreditation type'] = elementText.replace(", ", "/")


        lineToWrite = '|'.join(list(dataDict.values()))

        pagedata.append(trimWhiteSpacesBeforeAfterDelimiter(stringg=lineToWrite, delimiter='|') + '\n')#Trim the excess spaces and add new line character in each line
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