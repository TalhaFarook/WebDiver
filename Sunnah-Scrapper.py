import pandas
from bs4 import BeautifulSoup
import requests
import re

links = ['/bukhari', '/muslim', '/nasai', '/abudawud', '/tirmidhi', '/ibnmajah']
total = [97, 56, 51, 43, 49, 37]

urls = []
for a, b in zip(links, total):
    for c in range(1, b+1):
        urls.append(f'https://sunnah.com/{a}/{c}')

collection, englishHadith, references, arabicHadith = [], [], [], []
for url in urls:
    print(url)
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
        
    htmlArabic = soup.find_all("div", class_="arabic_hadith_full arabic")

    for arabic in htmlArabic:
        arabicHadith.append(arabic.text)
        htmlCollection = soup.find("div", class_="crumbs").text
        collection.append(re.sub(r'Home » ', '', str(htmlCollection)))
    
    htmlHadiths = soup.find_all("div", class_="text_details")
    
    for hadith in htmlHadiths:
        englishHadith.append(hadith.text)
    
    htmlReferences = soup.find_all("tr")

    for reference in htmlReferences:
        if reference.find("a") is not None:
            references.append((reference.find("a").text))
            
persons, books = [], []
for col in collection:
    person, book = col.split(" » ")
    persons.append(person)
    books.append(book)
     
data = list(zip(books, persons, arabicHadith, englishHadith, references))
table = pandas.DataFrame(data, columns = ['Book Name', 'Collected By', 'Arabic', 'English', 'References'])
table = table.replace(to_replace= '\\r|\\n|\\t|Narrated|:|\u200f.\u200f|\u200f"\u200f|\n', value= '', regex=True)

urls = ['https://sunnah.com//nawawi40',
 'https://sunnah.com//qudsi40',
 'https://sunnah.com//shahwaliullah40']


collection, englishHadith, references, arabicHadith = [], [], [], []
for url in urls:
    print(url)
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
        
    htmlArabic = soup.find_all("div", class_="arabic_hadith_full arabic")

    for arabic in htmlArabic:
        arabicHadith.append(arabic.text)
        htmlCollection = soup.find("div", class_="crumbs").text
        collection.append(re.sub(r'Home » ', '', str(htmlCollection)))
    
    htmlHadiths = soup.find_all("div", class_="text_details")
    
    for hadith in htmlHadiths:
        englishHadith.append(hadith.text)
    
    htmlReferences = soup.find_all("tr")

    for reference in htmlReferences:
        if reference.find("a") is not None:
            references.append((reference.find("a").text))
            
persons, books = [], []
for col in collection:
    person, book = col.split(" » ")
    persons.append(person)
    books.append(book)
     
data = list(zip(books, books, arabicHadith, englishHadith, references))
table1 = pandas.DataFrame(data, columns = ['Book Name', 'Collected By', 'Arabic', 'English', 'References'])
table1 = table1.replace(to_replace= '\\r|\\n|\\t|Narrated|:|\u200f.\u200f|\u200f"\u200f|\n', value= '', regex=True)

b = []
for a in table1['Book Name']:
    b.append(re.sub(r"Forty Hadith of ", "", a))
    
table1['Collected By'] = b

links = ['/ahmad']
total = [7]

urls = []
for a, b in zip(links, total):
    for c in range(1, b+1):
        urls.append(f'https://sunnah.com/{a}/{c}')
        
collection, englishHadith, references, arabicHadith = [], [], [], []
for url in urls:
    print(url)
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
        
    htmlArabic = soup.find_all("div", class_="arabic_hadith_full arabic")

    for arabic in htmlArabic:
        arabicHadith.append(arabic.text)
        htmlCollection = soup.find("div", class_="crumbs").text
        collection.append(re.sub(r'Home » ', '', str(htmlCollection)))
    
    htmlHadiths = soup.find_all("div", class_="text_details")
    
    for hadith in htmlHadiths:
        englishHadith.append(hadith.text)
    
    htmlReferences = soup.find_all("tr")

    for reference in htmlReferences:
        if reference.find("a") is not None:
            references.append((reference.find("a").text))
            
persons, books = [], []
for col in collection:
    person, book = col.split(" » ")
    persons.append(person)
    books.append(book)
     
data = list(zip(books, persons, arabicHadith, englishHadith, references))
table3 = pandas.DataFrame(data, columns = ['Book Name', 'Collected By', 'Arabic', 'English', 'References'])
table3 = table3.replace(to_replace= '\\r|\\n|\\t|Narrated|:|\u200f.\u200f|\u200f"\u200f|\n', value= '', regex=True)

links = ['/riyadussalihin']
total = [19]

urls = []
for a, b in zip(links, total):
    for c in range(1, b+1):
        urls.append(f'https://sunnah.com/{a}/{c}')
        
collection, englishHadith, references, arabicHadith = [], [], [], []
for url in urls:
    print(url)
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
        
    htmlArabic = soup.find_all("div", class_="arabic_hadith_full arabic")

    for arabic in htmlArabic:
        arabicHadith.append(arabic.text)
        htmlCollection = soup.find("div", class_="crumbs").text
        collection.append(re.sub(r'Home » ', '', str(htmlCollection)))
    
    htmlHadiths = soup.find_all("div", class_="text_details")
    
    for hadith in htmlHadiths:
        englishHadith.append(hadith.text)
    
    htmlReferences = soup.find_all("tr")

    for reference in htmlReferences:
        if reference.find("a") is not None:
            references.append((reference.find("a").text))
            
persons, books = [], []
for col in collection:
    person, book = col.split(" » ")
    persons.append(person)
    books.append(book)
     
data = list(zip(books, persons, arabicHadith, englishHadith, references))
table4 = pandas.DataFrame(data, columns = ['Book Name', 'Collected By', 'Arabic', 'English', 'References'])
table4 = table4.replace(to_replace= '\\r|\\n|\\t|Narrated|:|\u200f.\u200f|\u200f"\u200f|\n', value= '', regex=True)

links = ['/mishkat']
total = [24]

urls = []
for a, b in zip(links, total):
    for c in range(1, b+1):
        urls.append(f'https://sunnah.com/{a}/{c}')
        
collection, englishHadith, references, arabicHadith = [], [], [], []
for url in urls:
    print(url)
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
        
    htmlArabic = soup.find_all("div", class_="arabic_hadith_full arabic")

    for arabic in htmlArabic:
        arabicHadith.append(arabic.text)
        htmlCollection = soup.find("div", class_="crumbs").text
        collection.append(re.sub(r'Home » ', '', str(htmlCollection)))
    
    htmlHadiths = soup.find_all("div", class_="text_details")
    
    for hadith in htmlHadiths:
        englishHadith.append(hadith.text)
    
    htmlReferences = soup.find_all("tr")

    for reference in htmlReferences:
        if reference.find("a") is not None:
            references.append((reference.find("a").text))
            
persons, books = [], []
for col in collection:
    person, book = col.split(" » ")
    persons.append(person)
    books.append(book)
     
data = list(zip(books, persons, arabicHadith, englishHadith, references))
table5 = pandas.DataFrame(data, columns = ['Book Name', 'Collected By', 'Arabic', 'English', 'References'])
table5 = table5.replace(to_replace= '\\r|\\n|\\t|Narrated|:|\u200f.\u200f|\u200f"\u200f|\n', value= '', regex=True)

links = ['/shamail']
total = [56]

urls = []
for a, b in zip(links, total):
    for c in range(1, b+1):
        urls.append(f'https://sunnah.com/{a}/{c}')

collection, englishHadith, references, arabicHadith = [], [], [], []
for url in urls:
    print(url)
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
        
    htmlArabic = soup.find_all("div", class_="arabic_hadith_full arabic")

    for arabic in htmlArabic:
        arabicHadith.append(arabic.text)
        htmlCollection = soup.find("div", class_="crumbs").text
        collection.append(re.sub(r'Home » ', '', str(htmlCollection)))
    
    htmlHadiths = soup.find_all("div", class_="text_details")
    
    for hadith in htmlHadiths:
        englishHadith.append(hadith.text)
    
    htmlReferences = soup.find_all("tr")

    for reference in htmlReferences:
        if reference.find("a") is not None:
            references.append((reference.find("a").text))
            
persons, books = [], []
for col in collection:
    person, book = col.split(" » ")
    persons.append(person)
    books.append(book)
     
data = list(zip(books, persons, arabicHadith, englishHadith, references))
table7 = pandas.DataFrame(data, columns = ['Book Name', 'Collected By', 'Arabic', 'English', 'References'])
table7 = table7.replace(to_replace= '\\r|\\n|\\t|Narrated|:|\u200f.\u200f|\u200f"\u200f|\n', value= '', regex=True)


urls = ['https://sunnah.com/hisn']

collection, englishHadith, books, persons, references, arabicHadith = [], [], [], [], [], []
for url in urls:
    print(url)
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
        
    htmlArabic = soup.find_all("div", class_="arabic_hadith_full arabic")

    for arabic in htmlArabic:
        arabicHadith.append(arabic.text)
        htmlCollection = soup.find("div", class_="crumbs").text
        collection.append(re.sub(r'Home » ', '', str(htmlCollection)))
        
        books.append('Fortress of the Muslim (Hisn al-Muslim)')
        persons.append('Sa`id b. `Ali b. Wahf al-Qahtani')
    
    htmlHadiths = soup.find_all("div", class_="text_details")
    
    for hadith in htmlHadiths:
        englishHadith.append(hadith.text)
    
    htmlReferences = soup.find_all("tr")

    for reference in htmlReferences:
        if reference.find("a") is not None:
            references.append((reference.find("a").text))

data = list(zip(books, persons, arabicHadith, englishHadith, references))
table9 = pandas.DataFrame(data, columns = ['Book Name', 'Collected By', 'Arabic', 'English', 'References'])
table9 = table9.replace(to_replace= '\\r|\\n|\\t|Narrated|:|\u200f.\u200f|\u200f"\u200f|\n', value= '', regex=True)

combined_df = pandas.concat([table, table1, table3, table4, table5, table7, table9])
combined_df = combined_df.reset_index(drop=True)
combined_df = combined_df.replace(to_replace= '[U+200F]\\"[U+200F]', value= '', regex=True)

new_column_order = ['Arabic', 'English', 'Book Name', 'Collected By', 'References']  
df_rearranged = combined_df[new_column_order] 

df_rearranged.to_csv("Sunnah-Processed.csv", index=False)