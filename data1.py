import time
import traceback
from _csv import writer
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def getName(name):
    try:
        n = name.split(',')
        fs = n[0].split(' ')
        if len(n) == 1:
            suf = '-'
        else:
            suf = ','.join(n[1:])
        if len(fs) == 2:
            return fs[0],'-',fs[-1],suf
        elif len(fs) == 3:
            return fs[0],fs[1],fs[2],suf
        else:
            mn = ' '.join(fs[1:-1])
            return fs[0],mn,fs[-1],suf
    except:
        print(traceback.print_exc)

def getAddress(address):
    #     print(address)

    street, address_line2, city, state, zipcode = '-', '-', '-', '-', '-'

    if address == 'No Address Specified':
        return street, address_line2, city, state, zipcode
    else:
        address_parts = address.split(",")
        l = len(address_parts)
        if l == 1:
            street = address_parts[0]

        elif l == 2:
            street = address_parts[0]
            state = address_parts[1]

        else:

            street = address_parts[0].strip()

            city = address_parts[-3].strip()

            state = address_parts[-2].strip()

            zipcode = address_parts[-1].strip()
            if city != address_parts[1].strip() and state != address_parts[1].strip():
                address_line2 = address_parts[1].strip()

        return street, address_line2, city, state, zipcode

chrome_options = Options()

# Set up ChromeDriver service
webdriver_service = Service('chromedriver')  # Replace 'path/to/chromedriver' with the actual path to the ChromeDriver executable

# Set up ChromeDriver options
webdriver_options = webdriver.ChromeOptions()

driver = webdriver.Chrome(service=webdriver_service, options=webdriver_options)

f1 = open('sccds.csv', 'a')
writer_object = writer(f1)
writer_object.writerow(['Name','Practice Type','Company','address','Phone','Website'])


for i in range(1,140):
    driver.get(f"https://sccds.org/member-directory/page/{i}/?seed=481")

    # Find the username and password fields and enter the credentials
    name_field = driver.find_elements(By.XPATH, '/html/body/div/div/main/div/div/div/ul/li/div/a')
    for j in name_field:
        j.click()
        eccent_profile_name = driver.find_elements(By.ID, 'eccent_profile_name')
        practice_type_field = driver.find_elements(By.ID, 'practice_type_field')
        company_field = driver.find_elements(By.ID, 'company_field')
        address_field = driver.find_elements(By.ID, 'address_field')
        phone_field = driver.find_elements(By.ID, 'phone_field')
        website_field = driver.find_elements(By.ID, 'website_field')

        writer_object.writerow([eccent_profile_name[0].text,practice_type_field[0].text,company_field[0].text,address_field[0].text,phone_field[0].text,website_field[0].text])

        close = driver.find_elements(By.ID, 'eccent_close_win')
        close[0].click()
    print('pg',i)
f1.close()

df = pd.read_csv('./sccds.csv')
df = df[ df[ 'Name' ].str.contains( '@' )==False ]
df[['First Name', 'Middle Initial','Last Name','Suffix']] = df['Name'].apply(lambda name: pd.Series(getName(name)))
df[['Street Address', 'Address 2','City','State','ZIP']] = df['address'].apply(lambda address: pd.Series(getAddress(address)))
df1 = df[['First Name','Middle Initial','Last Name','Suffix','Practice Type','Company','Street Address','Address 2','City','State','ZIP','Phone','Website']]
df1.to_csv('extracted.csv')









