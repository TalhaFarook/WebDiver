#!/usr/bin/env python
# coding: utf-8

# In[46]:


import pandas
from bs4 import BeautifulSoup

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
# chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)

counter, urlList = 0, []
while True:
    try:
        driver.get("https://www.zameen.com/")
        
        # Wait for the dropdown button to be clickable and click it
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="body-wrapper"]/header/div[6]/div/div[2]/div[2]/div[1]/div[1]/div/div'))).click()

        dropdown = driver.find_element(By.CLASS_NAME, 'ede17658')
        # Get all the buttons from the dropdown (cities)
        buttons = dropdown.find_elements(By.TAG_NAME, 'button')

        # Click the button depending upon the counter, which makes sure that only the first unclicked button is pressed.
        buttons[counter].click()

        # Now the city has been selected, click the Find button to search for that particular city.
        driver.find_element(By.XPATH, '//*[@id="body-wrapper"]/header/div[6]/div/div[2]/div[2]/div[1]/a').click()

        # Add the current URL to the list
        urlList.append(driver.current_url)

        # Increment the counter for the next iteration
        counter += 1
        
        # Add a break condition, so when all the buttons (cities) have been clicked and their url has been copied, so break this loop and move to the next step.
        if counter >= len(buttons):
            break
        
    except Exception as e:
        continue # The reason I didn't print the error because the clicks get interrupted a lot and the output will look messy. The script scrapes every city, don't worry!

# Close the webdriver after processing all the buttons
driver.quit()

driver = webdriver.Chrome(options=chrome_options) 

links = []
for url in urlList:
    counter = 1
    
    while(1):
        try:      
            # Replace the iteration number from the link (https://www.zameen.com/Homes/Islamabad-3-1.html, the 1 is replace by 2, 3, 4...)
            if counter == 6:
                break
            
            new = url.split('.html')[0][:-1] + str(counter) + '.html'
            driver.get(new)
            
            counter += 1

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            
            # Check if this text doesn't appear, which shows us that we have reached the end of the property for that city.
            if soup.find('span', class_ = '_5264eceb') is not None:
                if soup.find('span', class_ = '_5264eceb').text.strip() == 'Sorry, there are no active properties matching your criteria.':
                    break
                
            # There are multiple links on the website, but we are only taking the ones with '/Property' in them which points towards a particular property
            anchors = soup.find_all('a', class_ = '_7ac32433', href=lambda href: href and '/Property/' in href)
            for link in anchors:
                # Preparing the link for the url, as it is missing the protocol and domain name.
                links.append(f"https://www.zameen.com{link['href']}")

        except Exception as e:
            print("Error:", str(e)) # Ignore the error message, just one link timed out because the response didn't come in time
            
driver.quit()

driver = webdriver.Chrome(options=chrome_options)
data = []
for link in links:
    try:
        driver.get(link)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        title = soup.find('h1', class_ = '_64bb5b3b')
        if title is not None:
            title = title.text.strip()
        else:
            title = ''

        details = soup.find('ul', {'aria-label': 'Property details'})

        types, price, location, baths, area, beds, amenities = '', '', '', '', '', '', ''
        
        for detail in details.find_all('li'):
            if detail.find('span', {'aria-label': 'Type'}) is not None:
                types = detail.find('span', {'aria-label': 'Type'}).text.strip()

            elif detail.find('span', {'aria-label': 'Price'}) is not None:
                price = detail.find('span', {'aria-label': 'Price'}).text.strip()

            elif detail.find('span', {'aria-label': 'Location'}) is not None:
                location = detail.find('span', {'aria-label': 'Location'}).text.strip()

            elif detail.find('span', {'aria-label': 'Baths'}) is not None:
                baths = detail.find('span', {'aria-label': 'Baths'}).text.strip()

            elif detail.find('span', {'aria-label': 'Area'}) is not None:
                area = detail.find('span', {'aria-label': 'Area'}).text.strip()

            elif detail.find('span', {'aria-label': 'Beds'}) is not None:
                beds = detail.find('span', {'aria-label': 'Beds'}).text.strip()
                
        url = driver.current_url

        amenities = ''
        allAmenities = soup.find_all('ul', class_ = '_6e283b70')
        for categoryAmenities in allAmenities:
            if categoryAmenities is not None:
                amenitiesList = categoryAmenities.find_all('span', class_ = '_17984a2c')
                if amenitiesList is not None:
                    for amenity in amenitiesList:
                        amenities += (f"{amenity.text.strip()}; ")

        data.append([title, types, price, location, baths, area, beds, amenities, url])

    except Exception as e:
        continue
            
driver.quit()

output = pandas.DataFrame(data, columns = ['Title', 'Type', 'Price', 'Location', 'Baths', 'Area', 'Beds', 'Amenities', 'Link'])

# Checking for null and duplicate values

output = output[output['Price'] != '']
output = output[output['Type'] != '']
output = output[output['Link'] != '']
output = output[output['Beds'] != '-']
output = output[output['Baths'] != '-']
output.reset_index(drop = True, inplace = True)

print(output.duplicated().sum(), "duplicates found!")
if output.duplicated().sum():
    output = Mainoutput.drop_duplicates().reset_index(drop = True)
    print("Duplicate values dropped!")
    print(output.duplicated().sum(), "duplicates left!")
    
output.to_csv('Zameen-Processed.csv', index = False)

