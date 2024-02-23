# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 12:38:13 2023

@author: faiza

"""



from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import time
from selenium.common.exceptions import TimeoutException
import pandas as pd
import numpy as np
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException

# Initialize the Selenium WebDriver (you'll need to download the appropriate driver for your browser)
# Specify the path to the chromedriver executable
#chrome_driver_path = 'C:/Users/faiza/Downloads/chromedriver_win32/chromedriver.exe'

service = Service(executable_path='C:/Users/faiza/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe')
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
# Initialize the Chrome WebDriver with the options
#driver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)

# Define the URL of the web form
url = 'https://mnregaweb4.nic.in/netnrega/dynamic_phy_fin_detail.aspx?lflag=eng&fin_year=2023-2024&source=national&labels=labels&Digest=MZ7EPgZ8ZwgnIaImm+t7hA'

# Navigate to the web form
driver.get(url)

# Find and select the "State" dropdown
state_dropdown = Select(driver.find_element(By.NAME, 'ctl00$ContentPlaceHolder1$ddl_state'))

# Get the options from the "State" dropdown
state_options = state_dropdown.options
# Create an empty DataFrame to store the options
df_state_options = pd.DataFrame(columns=['Value', 'Text'])

# Loop through the options and store them in the DataFrame
for state_option in state_options:
    option_value = state_option.get_attribute('value')
    option_text = state_option.text
    df_state_options = df_state_options.append({'Value': option_value, 'Text': option_text}, ignore_index=True)

# Create an empty DataFrame to store district options
df_district_options = pd.DataFrame(columns=['State_Value', 'State_Text', 'District_Value', 'District_Text'])

# Loop through the state options in df_state_options
for index, row in df_state_options.iterrows():
    state_value = row['Value']
    state_text = row['Text']
    
    # Re-locate the "State" dropdown element
    state_dropdown = Select(driver.find_element(By.NAME, 'ctl00$ContentPlaceHolder1$ddl_state'))
    
    # Select the current state
    state_dropdown.select_by_value(state_value)
    
    # Wait briefly for the "District" dropdown to populate (customize the wait time if needed)
    time.sleep(5)
    # Find the "District" dropdown
    district_dropdown = Select(driver.find_element(By.NAME, 'ctl00$ContentPlaceHolder1$ddl_dist'))
    
    # Get the options from the "District" dropdown
    district_options = district_dropdown.options
    
    # Loop through the district options and store them in the DataFrame
    for district_option in district_options:
        district_value = district_option.get_attribute('value')
        district_text = district_option.text
        
        # Append the values to the DataFrame
        df_district_options = df_district_options.append({
            'State_Value': state_value,
            'State_Text': state_text,
            'District_Value': district_value,
            'District_Text': district_text
        }, ignore_index=True)

    
# Filter rows where District_Text is not equal to "select"
df = df_district_options[df_district_options['District_Text'] != 'Select']

# Export the filtered DataFrame to an Excel file
df.to_excel('D:/GIZ_WASCA/WASCA - 3/data_collected/state_district_options.xlsx', index=False)
    
df_district_options=df    


##load state distdic exce
df = pd.read_excel('D:/GIZ_WASCA/WASCA - 3/data_collected/state_district_options.xlsx')
#####  
##My lopp stopped in between at state 33 and district value 3332. so to start again I am removing values till there and restarting the loop
df_district_options= df[673:]

# Loop through each unique state value
# Get unique state values from df_district_options
unique_state_values = df_district_options['State_Value'].unique()

##
service = Service(executable_path='C:/Users/faiza/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe')
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
# Initialize the Chrome WebDriver with the options
#driver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)


# Define the URL of the web form
url = 'https://mnregaweb4.nic.in/netnrega/dynamic_phy_fin_detail.aspx?lflag=eng&fin_year=2023-2024&source=national&labels=labels&Digest=MZ7EPgZ8ZwgnIaImm+t7hA'

# Navigate to the web form
driver.get(url)




for state_value in unique_state_values:
    print(state_value)
    filtered_df = df_district_options[df_district_options['State_Value'] == state_value]

    # Re-locate the "State" dropdown element
    state_dropdown = Select(driver.find_element(By.NAME, 'ctl00$ContentPlaceHolder1$ddl_state'))
    state_dropdown.select_by_value(str(state_value))
    time.sleep(5)

    for index, row in filtered_df.iterrows():
        district_value = row['District_Value']
        print(district_value)

        # Select the current district
        try:
            district_option = driver.find_element(By.XPATH, f"//option[@value='{district_value}']")
            district_option.click()
            time.sleep(5)
            
            # Click the "Submit" button to generate the data
            submit_button = driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_Btnsubmit"]')
            submit_button.click()
            time.sleep(30)

            download_button = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_LinkButton1')
            download_button.click()
            time.sleep(30)

            # Re-locate the "District" dropdown after the page reloads
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'ctl00$ContentPlaceHolder1$ddl_dist')))
        
        except NoSuchElementException:
            print(f"District with value {district_value} not found. Moving to the next district.")
            url = 'https://mnregaweb4.nic.in/netnrega/dynamic_phy_fin_detail.aspx?lflag=eng&fin_year=2023-2024&source=national&labels=labels&Digest=MZ7EPgZ8ZwgnIaImm+t7hA'
            driver.get(url)
            state_dropdown = Select(driver.find_element(By.NAME, 'ctl00$ContentPlaceHolder1$ddl_state'))
            state_dropdown.select_by_value(str(state_value))
            continue
        
        except TimeoutException:
            print(f"Timeout exception occurred for district: {district_value}")
            url = 'https://mnregaweb4.nic.in/netnrega/dynamic_phy_fin_detail.aspx?lflag=eng&fin_year=2023-2024&source=national&labels=labels&Digest=MZ7EPgZ8ZwgnIaImm+t7hA'
            driver.get(url)
            state_dropdown = Select(driver.find_element(By.NAME, 'ctl00$ContentPlaceHolder1$ddl_state'))
            state_dropdown.select_by_value(str(state_value))
            continue
            
        except WebDriverException as e:
            if "request entity is too large" in str(e).lower():
                print(f"The page was not displayed because the request entity is too large for district: {district_value}.")
            else:
                print(f"A WebDriverException occurred: {e}")
            
            url = 'https://mnregaweb4.nic.in/netnrega/dynamic_phy_fin_detail.aspx?lflag=eng&fin_year=2023-2024&source=national&labels=labels&Digest=MZ7EPgZ8ZwgnIaImm+t7hA'
            driver.get(url)
            state_dropdown = Select(driver.find_element(By.NAME, 'ctl00$ContentPlaceHolder1$ddl_state'))
            state_dropdown.select_by_value(str(state_value))
            continue
            
        except Exception as e:
            print(f"Unexpected error occurred for district: {district_value}. Error: {e}")
            url = 'https://mnregaweb4.nic.in/netnrega/dynamic_phy_fin_detail.aspx?lflag=eng&fin_year=2023-2024&source=national&labels=labels&Digest=MZ7EPgZ8ZwgnIaImm+t7hA'
            driver.get(url)
            state_dropdown = Select(driver.find_element(By.NAME, 'ctl00$ContentPlaceHolder1$ddl_state'))
            state_dropdown.select_by_value(str(state_value))
            continue




##read the downlaoded data

file = "dynamic_phy_fin_detail - 2023-10-18T172749.276"

df = pd.read_html('C:/Users/faiza/Downloads/dynamic_phy_fin_detail - 2023-10-18T172749.276.xls')[0]
#column_names = ["S No.","Block", "Panchayat", 	"Work Category",	"Work Type/Proposed Status",	"Ongoing/Physical Completed Work Since Inception	Completed Work Since Inception","Complete Work in 2023-2024", 	"Complete Work in 2022-2023",	"Complete Work in 2021-2022", 	"Complete Work in 2020-2021", 	"Complete Work in 2019-2020", 	"Complete Work in 2018-2019", 	"Complete Work in 2017-2018",	"Complete Work in 2016-2017",	"Complete Work in 2015-2016",	"Completed Work in 2014-2015	", "Complete Work in 2013-2014", 	"Completed Work in 2012-2013"]

import os
import pandas as pd

# Specify the folder containing XLS files
folder_path = 'C:/Users/faiza/Downloads/'

# Initialize an empty DataFrame to store the combined data
combined_df = pd.DataFrame()

# Loop through files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.xls'):
        file_path = os.path.join(folder_path, filename)
        
        # Read the data from the current XLS file
        xls_df = pd.read_html(file_path)[0]
        
        # Append the data to the combined DataFrame
        combined_df = combined_df.append(xls_df, ignore_index=True)
        
        # Print the combined DataFrame
print(combined_df)

# Optionally, export the combined data to a single Excel file
combined_df.to_excel('combined_data.xlsx', index=False)



import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set the path to the ChromeDriver executable as an environment variable
os.environ['webdriver.chrome.driver'] = '/path/to/chromedriver'

# Initialize the Chrome WebDriver
driver = webdriver.Chrome()

# Define the URL of the web form
url = 'https://mnregaweb4.nic.in/netnrega/dynamic_phy_fin_detail.aspx?lflag=eng&fin_year=2023-2024&source=national&labels=labels&Digest=MZ7EPgZ8ZwgnIaImm+t7hA'

# Navigate to the web form
driver.get(url)

wait = WebDriverWait(driver, 10)


# Function to get options from a dropdown and return a DataFrame
def get_dropdown_options(dropdown_element):
    options = dropdown_element.options
    option_list = [{'Value': option.get_attribute('value'), 'Text': option.text} for option in options]
    return pd.DataFrame(option_list)


# Find and select the "State" dropdown
state_dropdown = Select(driver.find_element(By.NAME, 'ctl00$ContentPlaceHolder1$ddl_state'))
df_state_options = get_dropdown_options(state_dropdown)

# Create DataFrame to store state, district, block, and panchayat options
df_combined_options = pd.DataFrame(
    columns=['State_Value', 'State_Text', 'District_Value', 'District_Text', 'Block_Value', 'Block_Text',
             'Panchayat_Value', 'Panchayat_Text'])

# Loop through the state options and store district, block, and panchayat options
for _, state_row in df_state_options.iterrows():
    state_value = state_row['Value']
    state_text = state_row['Text']
    # Re-locate the "State" dropdown element
    state_dropdown = Select(driver.find_element(By.NAME, 'ctl00$ContentPlaceHolder1$ddl_state'))

    state_dropdown.select_by_value(state_value)
# Wait briefly for the "District" dropdown to populate (customize the wait time if needed)
    time.sleep(1)
    district_dropdown = Select(driver.find_element(By.NAME, 'ctl00$ContentPlaceHolder1$ddl_dist'))
    df_district = get_dropdown_options(district_dropdown)
    df_district['State_Value'] = state_value
    df_district['State_Text'] = state_text

    # Loop through district options to fetch block and panchayat options
    for _, district_row in df_district.iterrows():
        district_value = district_row['Value']
        district_text = district_row['Text']
        district_dropdown = Select(driver.find_element(By.NAME, 'ctl00$ContentPlaceHolder1$ddl_dist'))

        district_dropdown.select_by_value(district_value)
        time.sleep(1)

        block_dropdown = Select(driver.find_element(By.NAME, 'ctl00$ContentPlaceHolder1$ddl_blk'))
        df_block = get_dropdown_options(block_dropdown)
        df_block['State_Value'] = state_value
        df_block['State_Text'] = state_text
        df_block['District_Value'] = district_value
        df_block['District_Text'] = district_text

        # Loop through block options to fetch panchayat options
        for _, block_row in df_block.iterrows():
            block_value = block_row['Value']
            block_text = block_row['Text']
            block_dropdown = Select(driver.find_element(By.NAME, 'ctl00$ContentPlaceHolder1$ddl_blk'))

            block_dropdown.select_by_value(block_value)
            time.sleep(1)

            panchayat_dropdown = Select(driver.find_element(By.NAME, 'ctl00$ContentPlaceHolder1$ddl_pan'))
            df_panchayat = get_dropdown_options(panchayat_dropdown)
            df_panchayat['State_Value'] = state_value
            df_panchayat['State_Text'] = state_text
            df_panchayat['District_Value'] = district_value
            df_panchayat['District_Text'] = district_text
            df_panchayat['Block_Value'] = block_value
            df_panchayat['Block_Text'] = block_text

            # Concatenate panchayat options to the combined DataFrame
            df_combined_options = pd.concat([df_combined_options, df_panchayat])

# Save the merged DataFrame to a single Excel file
df_combined_options.to_excel('mgnrega_options_with_panchayat.xlsx', index=False)

# Close the WebDriver
driver.quit()


