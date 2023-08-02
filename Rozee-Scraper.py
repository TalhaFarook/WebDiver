from bs4 import BeautifulSoup
import pandas 

import warnings
warnings.filterwarnings("ignore")

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument("--headless")
from selenium.common.exceptions import WebDriverException

#International link
driver = webdriver.Chrome(options=chrome_options)

link = 'https://www.rozee.pk/international-jobs'
driver.get(link)  
html = driver.page_source

soup = BeautifulSoup(html, 'html.parser')

intUrls = []
jobs = soup.find_all('div', class_ = 'job internationalJobs')
for job in jobs:
    anchor = job.find('a')
    intUrls.append('https:' + anchor.get('href'))

while(1):
    check = 0
    options = soup.find_all('a')
    for option in options:
        if (option.text == 'Next'):
            check = 1
            link = 'https:' + option.get('href')
            driver.get(link)  
            html = driver.page_source

            soup = BeautifulSoup(html, 'html.parser')
            jobs = soup.find_all('div', class_ = 'job internationalJobs')
            for job in jobs:
                anchor = job.find('a')
                intUrls.append('https:' + anchor.get('href'))
    if check == 0:
        break

driver.quit()

# Local link
driver = webdriver.Chrome(options=chrome_options)

link = 'https://www.rozee.pk/jobs-by-industry'

driver.get(link)  
html = driver.page_source

soup = BeautifulSoup(html, 'html.parser')

temps = []
anchors = soup.find_all('a', class_ = 'text-muted nrs-14')
for anchor in anchors:
    link = anchor.get('href')
    if link is not None:
        temps.append('https:' + anchor.get('href'))
        
urls = []
for temp in temps:
    urls.append(temp)
    print(temp)
        
    driver.get(temp)  
    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')
    
    if soup.find('a', class_ = 'next') is not None and soup.find('a', class_ = 'next').text == 'Next':
        counter = 0
        while(1):
            counter += 20
            urls.append(temp + '/fpn/' + str(counter))
            link = temp + '/fpn/' + str(counter)
            print(link)
            
            driver.get(link)  
            html = driver.page_source

            soup = BeautifulSoup(html, 'html.parser')
            if len(soup.find_all('a', class_ = 'next')) == 2:
                continue
            else:
                break
        
driver.quit()

driver = webdriver.Chrome(options=chrome_options)

localUrls = []
for url in urls:
    driver.get(url)  
    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')

    jobs = soup.find_all('div', class_ = 'job')
    for job in jobs:
        anchor = job.find('a')
        if anchor is not None:
            print('https:' + anchor.get('href'))
            localUrls.append('https:' + anchor.get('href'))
        
driver.quit()

total = localUrls + intUrls
total = list(set(total))

driver = webdriver.Chrome(options=chrome_options)

dataAll = pandas.DataFrame(columns = ['Title', 'Description', 'Vacancies', 'Location', 'Min Education', 'Min Experience', 'Apply Before', 'URL'])
for url in total:   
    try:           
        driver.get(url)  
        print(url)
        html = driver.page_source

        soup = BeautifulSoup(html, 'html.parser')
        
        jobTitle = soup.find('h1', class_ = 'jtitle')
        
        if jobTitle is None:
            continue
            
        jobTitle = jobTitle.text.strip()
        
        jobDescription = []
        description = soup.find('div', class_ = 'jblk ul18')
        for line in description:
            jobDescription.append(line.text)
        
        jobDescription = ' '.join(jobDescription)
        jobDescription = ' '.join(jobDescription.split())
        
        titleJob = soup.find('div', 'jblk col-pl-0')
        jobDetails, titleCheck, locationCheck, educationCheck, experienceCheck, postingCheck = ['', '', '', '', ''], 0, 0, 0, 0, 0
        for detail, title in zip(titleJob.find_all('div', class_ = 'col-lg-7 col-md-7 col-sm-8 col-sm-6'), titleJob.find_all('b')):
            if title.text == 'Total Positions:':
                titleCheck = 1
                jobDetails[0] = ' '.join(detail.text.split())
            if title.text == 'Job Location:':
                locationCheck  = 1
                jobDetails[1] = ' '.join(detail.text.split())
            if title.text == 'Minimum Education:' or title.text == 'Education:':
                educationCheck = 1
                jobDetails[2] = ' '.join(detail.text.split())
            if title.text == 'Minimum Experience:' or title.text == 'Experience:' or title.text == 'Maximum Experience:':
                experienceCheck = 1
                jobDetails[3] = ' '.join(detail.text.split())
            if title.text == 'Posting Date:':
                postingCheck = 1
                jobDetails[4] = ' '.join(detail.text.split())
        if titleCheck == 0:
            jobDetails[0] = 'Null'
        if locationCheck == 0:
            jobDetails[1] = 'Null'
        if educationCheck == 0:
            jobDetails[2] = 'Null'
        if experienceCheck == 0:
            jobDetails[3] ='Null'
        if postingCheck == 0:
            jobDetails[4] = 'Null'

        jobDetails.append(url)     
        data = [[jobTitle, jobDescription, jobDetails[0], jobDetails[1], jobDetails[2], jobDetails[3], jobDetails[4], jobDetails[5]]]
        data = pandas.DataFrame(data, columns = ['Title', 'Description', 'Vacancies', 'Location', 'Min Education', 'Min Experience', 'Apply Before', 'URL'])
        dataAll = dataAll.append(data, ignore_index = True)
                    
    except WebDriverException as e:
        print(link, ": Page doesn't exist!")
        
driver.quit()

jobs1 = dataAll.copy()

driver = webdriver.Chrome(options=chrome_options)

dataAll = pandas.DataFrame(columns = ['Title', 'Description', 'Vacancies', 'Location', 'Min Education', 'Min Experience', 'Apply Before', 'URL'])
for url in total:   
    try:           
        driver.get(url)  
        
        if 'https://contour-software.rozee.pk/' in url:
            print(url)
            html = driver.page_source

            soup = BeautifulSoup(html, 'html.parser')

            jobTitle = soup.find('div', class_ = 'jtitle')

            if jobTitle is None:
                continue

            jobTitle = jobTitle.text.strip()

            jobDescription = []
            description = soup.find('div', class_ = 'jblk ul18')
            for line in description:
                jobDescription.append(line.text)

            jobDescription = ' '.join(jobDescription)
            jobDescription = ' '.join(jobDescription.split())

            titleJob = soup.find('div', 'jblk col-pl-0')
            jobDetails, titleCheck, locationCheck, educationCheck, experienceCheck, postingCheck = ['', '', '', '', ''], 0, 0, 0, 0, 0
            for detail, title in zip(titleJob.find_all('div', class_ = 'col-lg-7 col-md-7 col-sm-8 col-sm-6'), titleJob.find_all('b')):
                if title.text == 'Total Positions:':
                    titleCheck = 1
                    jobDetails[0] = ' '.join(detail.text.split())
                if title.text == 'Job Location:':
                    locationCheck  = 1
                    jobDetails[1] = ' '.join(detail.text.split())
                if title.text == 'Minimum Education:' or title.text == 'Education:':
                    educationCheck = 1
                    jobDetails[2] = ' '.join(detail.text.split())
                if title.text == 'Minimum Experience:' or title.text == 'Experience:' or title.text == 'Maximum Experience:':
                    experienceCheck = 1
                    jobDetails[3] = ' '.join(detail.text.split())
                if title.text == 'Posting Date:':
                    postingCheck = 1
                    jobDetails[4] = ' '.join(detail.text.split())
            if titleCheck == 0:
                jobDetails[0] = 'Null'
            if locationCheck == 0:
                jobDetails[1] = 'Null'
            if educationCheck == 0:
                jobDetails[2] = 'Null'
            if experienceCheck == 0:
                jobDetails[3] ='Null'
            if postingCheck == 0:
                jobDetails[4] = 'Null'

            jobDetails.append(url)     
            data = [[jobTitle, jobDescription, jobDetails[0], jobDetails[1], jobDetails[2], jobDetails[3], jobDetails[4], jobDetails[5]]]
            data = pandas.DataFrame(data, columns = ['Title', 'Description', 'Vacancies', 'Location', 'Min Education', 'Min Experience', 'Apply Before', 'URL'])
            dataAll = dataAll.append(data, ignore_index = True)

    except WebDriverException as e:
        print(link, ": Page doesn't exist!")
        
driver.quit()

jobs2 = dataAll.copy()

contour = []
for url in total:
    if 'https://www.rozee.pk/contour' in url:
        contour.append(url)

driver = webdriver.Chrome(options=chrome_options)

count = 0
dataAll = pandas.DataFrame(columns = ['Title', 'Description', 'Vacancies', 'Location', 'Min Education', 'Min Experience', 'Apply Before', 'URL'])
for url in contour:   
    try:     
        count += 1
        driver.get(url) 
    
        print(url)
        html = driver.page_source

        soup = BeautifulSoup(html, 'html.parser')

        jobTitle = ''
        titles = soup.find_all('div', class_ = 'h3')
        for title in titles:
            if title.find('b') is not None:
                jobTitle = title.find('b').text

        jobDescription = []
        description = soup.find('div', class_ = 'defLnSpce defJdDet')
        for line in description:
            jobDescription.append(line.text)

        jobDescription = ' '.join(jobDescription)
        jobDescription = ' '.join(jobDescription.split())

        titleJob = soup.find_all('div', 'col-md-9')

        jobDetails, titleCheck, locationCheck, educationCheck, experienceCheck, postingCheck = ['', '', '', '', ''], 0, 0, 0, 0, 0
        for single in titleJob:
            for detail, title in zip(single.find_all('div', class_ = 'col-lg-6 col-md-6 col-sm-6'), single.find_all('div', class_ = 'col-lg-4 col-md-6 col-sm-4')):
                if title.text.strip() == 'Total Position':
                    titleCheck = 1
                    jobDetails[0] = ' '.join(detail.text.split())
                if title.text.strip() == 'Job Location':
                    locationCheck  = 1
                    jobDetails[1] = ' '.join(detail.text.split())
                if title.text.strip() == 'Minimum Education' or title.text == 'Education':
                    educationCheck = 1
                    jobDetails[2] = ' '.join(detail.text.split())
                if title.text.strip() == 'Apply By':
                    if ',' not in title.text.strip():
                        
                        experienceCheck = 1
                        jobDetails[3] = ' '.join(detail.text.split())
                    else:
                        if title.text.strip() == 'Posted On':
                            postingCheck = 1
                            jobDetails[4] = ' '.join(detail.text.split())
            if titleCheck == 0:
                jobDetails[0] = 'Null'
            if locationCheck == 0:
                jobDetails[1] = 'Null'
            if educationCheck == 0:
                jobDetails[2] = 'Null'
            if experienceCheck == 0:
                jobDetails[3] ='Null'
            if postingCheck == 0:
                jobDetails[4] = 'Null'

        jobDetails.append(url)     
        data = [[jobTitle, jobDescription, jobDetails[0], jobDetails[1], jobDetails[2], jobDetails[3], jobDetails[4], jobDetails[5]]]
        data = pandas.DataFrame(data, columns = ['Title', 'Description', 'Vacancies', 'Location', 'Min Education', 'Min Experience', 'Apply Before', 'URL'])
        dataAll = dataAll.append(data, ignore_index = True)
        
    except WebDriverException as e:
        print(url, ": Page doesn't exist!")
        
driver.quit()

driver = webdriver.Chrome(options=chrome_options)

jobs3 = dataAll[~dataAll['Min Experience'].str.contains(',')]
jobs3.reset_index(drop=True, inplace=True)

combined_df = pandas.concat([jobs1, jobs2, jobs3], ignore_index=True)

combined_df.to_csv('Rozee-Unprocessed.csv')
