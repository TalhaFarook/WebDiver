from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains

# Set up your own custom web driver with your local data in it (you are logged in to their linkedin account)
service = Service(executable_path = r"C:\Users\USER\Documents\ChromeDriver\chromedriver.exe")
option = Options()

chrome_options = webdriver.ChromeOptions()
option.add_experimental_option("debuggerAddress", "localhost:9222")
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options = chrome_options)

from bs4 import BeautifulSoup
import time

from collections import OrderedDict
import pandas
pandas.set_option('display.max_colwidth', None)
pandas.set_option('display.max_rows', None)

# URl encode the users search query to put in the url
import urllib.parse

def encodeURL(query):
    return urllib.parse.quote(query)

def linkedin(query, num):        
    # Preparing the URL for it
    url = 'https://www.linkedin.com/search/results/content/?keywords=' + encodeURL(query) + '&origin=GLOBAL_SEARCH_HEADER&searchId=0f2034f2-3f08-4731-8c95-5758c09fa55f&sid=kn'

    # Getting the web driver with custom options and establishing a connection with the prepared URL
    driver = webdriver.Chrome(service=service, options=option)
    try:
        driver.get(url)

        # Wait for the website to load initially
        time.sleep(5)

        temp1, temp2, flat, htmlNames = [], [], [], []
        # This range is set because a scrolling action will be taken by the chrome driver, as the posts load dynamically when you reach the end of the page. Decreasing it will result in fewer searches.
        while(1):
            # Deliberate sleep is added because the posts are loaded dynamically, so the script has to wait for the next set of posts to load when you reach the bottom.
            time.sleep(2)

            # Scrolling action performed here
            driver.execute_script("window.scrollBy(0, 500);")

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            # HTML of all the names are taken from the website
            temp1.append(soup.find_all('span', class_ = 'update-components-actor__title'))
            
            # HTML of all the text from the posts taken from the website
            temp2.append(soup.find_all('div', class_ = 'update-components-text relative feed-shared-update-v2__commentary'))

            # Flatten arrays ( Combine all the lists into one)
            flat1 = [row for rows in temp1 for row in rows]
            flat2 = [row for rows in temp2 for row in rows]

            # There are duplicates because the scroller option jumps when it reaches the end and the next set of posts is loaded. Removing the duplicates by OrderedDict, which makes sure that we retain the original order of posts/links
            htmlNames = list(OrderedDict.fromkeys(flat1))
            htmlPosts = list(OrderedDict.fromkeys(flat2))

            if len(htmlNames) >= num:  
                break

        # Creating a list of links extracted from the HTML
        nameList, counter = [], 0
        for row in htmlNames:
            try:
                if row.find('span', class_ = 'visually-hidden') is not None:
                    if counter < num:
                        counter += 1
                        nameList.append(row.find('span', class_ = 'visually-hidden').text.strip())
                    else:
                        break

            except Exception as e:
                print(f"An error occurred while user's name: {e}")
                
        # Creating a list of text extracted from the HTML
        textList, counter = [], 0
        for row in htmlPosts:
            try:
                if row.find('span', {'dir': 'ltr'}) is not None:
                    if counter < num:
                        counter += 1
                        textList.append(row.find('span', {'dir': 'ltr'}).text.strip())
                    else:
                        break

            except Exception as e:
                print(f"An error occurred while user's name: {e}")

        # Close the WebDriver
        driver.quit()

        # Create a DataFrame from the lists and save it into a CSV format
        output = pandas.DataFrame({'User Name': nameList, 'Post': textList})
        
        output.to_csv('LinkedIn-Unprocessed.csv', index=False)

    except Exception as e:
        print(f"An error occurred while running the script: {e}")

keyword = ''
maxSearch = 0

linkedin(keyword, maxSearch)
