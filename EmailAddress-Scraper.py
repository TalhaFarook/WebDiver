# + Ensure the script can locate and extract information from the "Impressum" page of each domain,
# + Handle different variations of email addresses (@, [ät], at, and so on...)
# + Can extract the Email Address from an Image. (Sometimes webmaster paste the Email as a JPEG or PNG, to prevent scraping)
# + This is an industry project, and these steps need to be performed on these URLs

from bs4 import BeautifulSoup
import pandas 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument("--headless")
from selenium.common.exceptions import WebDriverException
import re

import requests
from io import BytesIO
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\USER\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

urls = [
    "peersociallending.com",
    "kreditvergleich-kostenlos.net",
    "matblog.de", 
    "malta-tours.de",
    "wiseclerk.com",
    "urlaub-in-thailand.com",
    "findle.top",
    "niederrheinzeitung.de",
    "finanziell-umdenken.blogspot.com",
    "midbio.org",
    "klaudija.de",
    "pc-welt.wiki",
    "websitevalue.co.uk",
    "freizeitcafe.info",
    "ladenbau.de",
    "bierspot.de",
    "biboxs.com",
    "finance-it-blog.de",
    "guenstigerkreditvergleich.com",
    "cloudbiz.one",
    "frag-den-heimwerker.com",
    "fintech-intel.com",
    "selbst-schuld.com",
    "eltemkredit.com",
    "binoro.de",
    "siteurl.org",
    "frachiseportal.at",
    "finlord.cz",
    "vj-coach.de",
    "mountainstatescfc.org",
    "crowdstreet.de"
]

driver = webdriver.Chrome(options=chrome_options)

impressums = []
for url in urls:   
    try:
        link = 'https://' + url
        driver.get(link)  
        html = driver.page_source

        soup = BeautifulSoup(html, 'html.parser')

        anchors = soup.find_all('a')
        check = 0
        for anchor in anchors:
            if 'Impressum' in anchor.text:
                #Some websites have a proper link (https://...) to their impressum page and some have only a /page in href
                if '://' in anchor.get('href'):
                    impressums.append(anchor.get('href'))
                    check = 1
                    print(link, ": Impressum found!")
                    break
                else:
                    impressums.append(link + anchor.get('href'))
                    check = 1
                    print(link, ": Impressum found!")
                    break
        
        if (check == 0):
             print(link, ": Impressum doesn't exist!")
    #Some websites may give 404 error    
    except WebDriverException as e:
        print(link, ": Page doesn't exist!")

#Removing duplicates from the list        
impressums = list(set(impressums))

driver.quit()

pattern1 = r'\b\S+\[at\]\S+\b' #this pattern is for [a]
pattern2 = r'\b\S+@\S+\b' #this pattern is for @
pattern3 = r'\b\S+\s*@\s*\S+' #this pattern is for spaces in an email (abc @ .com)
pattern4 = r'[\w.-]+\(a\)[\w.-]+' #this pattern is for (a)

driver = webdriver.Chrome(options=chrome_options)

mails, impressumsList = [], []
for impressum in impressums:  
    print(impressum)
    driver.get(impressum) 
    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')
        
    html = soup.find_all('p')
    for h in html:
        if '[at]' in h.text:
            mails.append(re.findall(pattern1, h.text))
            impressumsList.append(impressum)
        if '[@]' in h.text:
            mails.append([h.text])
            impressumsList.append(impressum)
        elif '@' in h.text:
            if len(re.findall(pattern2, h.text)) > 0:
                mails.append(re.findall(pattern2, h.text))
                impressumsList.append(impressum)
                break
            else:
                mails.append(re.findall(pattern3, h.text))
            
    td_element = soup.find_all('td')
    for a in td_element:
        if '@' in a.text:
            mails.append(list(set(re.findall(pattern2, a.text))))
            impressumsList.append(impressum)
            break
            
    image = soup.find_all('img')
    for img in image:
        src = img.get('src')
        try:
            response = requests.get(src)
            image_data = response.content
            try:
                image = Image.open(BytesIO(image_data))
                text = pytesseract.image_to_string(image)
                if '@' in text or '(a)' in text:
                        if len(re.findall(pattern2, text)) > 0:
                            mails.append(re.findall(pattern2, text))
                            impressumsList.append(impressum)
                        else:
                            mails.append(re.findall(pattern4, text))
                            impressumsList.append(impressum)
                            break
            except Exception as e:
                continue
        except requests.exceptions.RequestException as e:
            continue

driver.quit()

temp = []
for emails in mails:
    for email in emails:
        temp.append(email)
        
cleanedMails = []
for email in temp:
    cleaned = email.replace(".comTel", ".com").replace(".deTel", ".de").replace("[@]", "@").replace("[at]", "@").replace(' ', '').replace("(a)", "@")
    cleanedMails.append(cleaned)

final = zip(impressumsList, cleanedMails)
emailDomains = pandas.DataFrame(final, columns = ['Domains', 'Emails'])

#Cleaning website addresses to only obtain domain names
emailDomains['Domains'] = emailDomains['Domains'].apply(lambda x: x.replace('https://www.', '').replace('http://www.', '').replace('https://', '').replace('http://', ''))
emailDomains['Domains'] = emailDomains['Domains'].apply(lambda x: x.replace('https://www.', '').split('.')[0])

emailDomains.to_csv('EmailAddress-Processed.csv', index=False)
