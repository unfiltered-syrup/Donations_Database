try:
    from fake_useragent import UserAgent
    import requests
    from bs4 import BeautifulSoup
    import urllib.request
    import urllib.request, json 
    import os
    from xml.dom.minidom import parse
    import pandas as pd
    from selenium import webdriver
    import time
    import random
except ImportError:
    print('You are missing a package, refer to list of requirements and install or update those packages')


saved_years = []

def get_xml(ein): #TODO check for cases with multiple links
    wait_time = random.uniform(1,5) #inserting random wait time to avoid getting blocked
    c=0
    xml_990s = soup.find_all('a', class_="action xml") #fetch all links
    for link in xml_990s: #iterate through links
        year = str(link.parent.select("h4:nth-of-type(2)")[0].text) #select year
        if year not in saved_years:
            c += 1
            urls = "https://projects.propublica.org"+link['href'] #get url of xml file
            ua_str = UserAgent().chrome
            r = requests.get(urls,allow_redirects=True,headers={"User-Agent": ua_str} ) #fetch xml and save
            with open(name+'/xml_data/'+name+year+'.xml', 'wb') as f:
                f.write(r.content)
                print('fetched', name, year, 'xml data')
                time.sleep(wait_time)
                wait_time = random.uniform(1,7)
                saved_years.append(year)

def get_pdf_link(ein):
    wait_time = random.uniform(0,5)
    pdf_990s = soup.find_all('a', class_="action")
    for link in pdf_990s:
        if("990" in link.text):
            get_pdf(link)
            time.sleep(wait_time)
            wait_time = random.uniform(1,7) #inserting random wait time


def get_pdf(link):
    year = str(link.parent.select("h4:nth-of-type(2)")[0].text)
    if year not in saved_years:
        urls = "https://projects.propublica.org"+link['href']
        driver.get(urls)
        pdf_soup = BeautifulSoup(driver.page_source, 'html.parser')
        pdf_download_section = pdf_soup.find_all('a')
        for links in pdf_download_section:
            if("Download" in links.text ):
                pdf_to_download = "https://projects.propublica.org"+links['href']
                ua_str = UserAgent().chrome
                r = requests.get(pdf_to_download,allow_redirects=True,headers={"User-Agent": ua_str, 'referer': "https://www.google.com/"})
                with open(name+'/pdf_data/'+name+year+'.pdf', 'wb') as f:
                    f.write(r.content)
                    print('fetched', name, year, 'pdf data')
                    saved_years.append(year)

def get_name(soup):
    t = soup.find_all('h1')
    return t[1].text



ein = input("ENTER EIN: ")
end_point = "https://projects.propublica.org/nonprofits/organizations/"
full_url = end_point+ein
resp = requests.get(full_url)
soup = BeautifulSoup(resp.text, 'html.parser')
name = str(get_name(soup)).replace(" ", "_")
driver = webdriver.Chrome()
directory = os.getcwd()
folder_path = directory + '/'+name
if not os.path.exists(folder_path):
    print('Creating direcotry for', name)
    os.makedirs(folder_path+'/xml_data')
    os.makedirs(folder_path+'/pdf_data')
    get_xml(ein)
    get_pdf_link(ein)
else:
    print('Directory already exists')


