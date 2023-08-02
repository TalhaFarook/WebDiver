from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains

# Set up your own custom web driver with your local data in it (you are logged in to their facebook account)
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

def facebook(query, num):
    # Preparing the URL for it and encoding the user query to match the URL
    url = 'https://www.facebook.com/search/posts/?q=' + encodeURL(query) + '&filters=eyJyZWNlbnRfcG9zdHM6MCI6IntcIm5hbWVcIjpcInJlY2VudF9wb3N0c1wiLFwiYXJnc1wiOlwiXCJ9In0%3D'

    # Getting the web driver with custom options and establishing a connection with the prepared URL
    driver = webdriver.Chrome(service=service, options=option)
    try:
        driver.get(url)

        # Wait for the website to load initially
        time.sleep(3)

        temp, flat, htmlLinks = [], [], []
        # This range is set because a scrolling action will be taken by the chrome driver, as the posts load dynamically when you reach the end of the page. Decreasing it will result in fewer searches.
        for _ in range(1, num):
            try:
                # Deliberate sleep is added because the posts are loaded dynamically, so the script has to wait for the next set of posts to load when you reach the bottom.
                time.sleep(1)

                hover = driver.find_elements(By.CSS_SELECTOR, ".x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x1heor9g.xt0b8zv.xo1l8bm")

                # Using action chains to create a hover effect because the URL of a Facebook post is hidden unless you hover over the timestamp.
                actions = ActionChains(driver)

                for element in hover:
                    try:
                        actions.move_to_element(element).perform()
                    except Exception as e:
                        continue
            except Exception as e:
                print(f"An error occurred while performing hover action: {e}")

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            # HTML of all the links are taken from the website
            temp.append(soup.find_all('a', class_='x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g xt0b8zv xo1l8bm'))

            # Flatten the list
            flat = [row for rows in temp for row in rows]

            # There are duplicates because the scroller option jumps when it reaches the end and the next set of posts is loaded. Removing the duplicates by OrderedDict, which makes sure that we retain the original order of posts/links
            htmlLinks = list(OrderedDict.fromkeys(flat))

            total = sum(len(row) for row in htmlLinks)

            if total >= num*2: #Taking extra posts just in case some error occurs
                break

            # Scrolling action performed here
            current = driver.execute_script("return window.pageYOffset;")
            driver.execute_script(f"window.scrollBy({current}+1000, {current}+2000);")

        # Creating a list of links extracted from the HTML
        links, counter = [], 0
        for link in htmlLinks:
            try:
                if 'facebook' in link['href']:
                    if counter < num:
                        if link['href'] not in links:
                            counter += 1
                            links.append(link['href'])
                    else:
                        break
                        
            except Exception as e:
                print(f"An error occurred while processing link: {e}")

        # Close the WebDriver
        driver.quit()

        # Extact data from each facebook page retrieved
        driver = webdriver.Chrome(service=service, options=option)

        nameList, urlList = [], []
        for link in links:
            try:
                driver.get(link)

                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')

                nameHTML = soup.find('a', class_='x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xzsf02u x1s688f')
                if nameHTML is not None:
                    nameList.append(nameHTML.text.strip())
                else:
                    # There are some facebook pages with the span tag, meaning their names can't be clicked. It may be due to their account being deleted, removed etc
                    nameHTML = soup.find('span', class_='x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xzsf02u x1s688f')
                    if nameHTML is not None:
                        nameList.append(nameHTML.text.strip())
                    else:
                        nameHTML = soup.find('div', class_='x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xzsf02u x1s688f')
                        if nameHTML is not None:
                            nameList.append(nameHTML.text.strip())
                        else:
                            nameList.append('')

                urlList.append(driver.current_url)

            except Exception as e:
                print(f"An error occurred while processing link: {e}")

        # Close the WebDriver
        driver.quit()

        # Create a DataFrame from the lists and save it in a CSV format
        output = pandas.DataFrame({'User Name': nameList, 'Post URL': urlList})
        
        output.to_csv('Facebook-Unprocessed.csv', index=False)

    except Exception as e:
        print(f"An error occurred while running the script: {e}")

keyword = ''
maxSearch = 0

facebook(keyword, maxSearch)
