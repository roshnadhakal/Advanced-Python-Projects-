from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup  # Parse HTML content easily
import pandas as pd  # for data manipulation and storage in CSV
import os  # to interact with the operating system (file management)
import json
from datetime import datetime, timedelta
import schedule  # Schedule tasks at a specified time
import time
from selenium.webdriver.chrome.options import Options


# Function to fetch daily case status and store in CSV

def fetch_and_store_data():
    print("Fetching daily case status...")  # Print message indicating fetching has started
    url = 'https://supremecourt.gov.np/web/eng/index'
    service = Service(r'F:\Work\PYTHON\chromedriver-win64\chromedriver.exe')
    driver = webdriver.Chrome(service=service)  # Create a new Chrome browser instance

    try:
        driver.get(url)
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        table = soup.find('table', {'width': '100%'})  # Find the specific table on the page
        if table is None:
            print("Could not find the table on the webpage.")
            return

        rows = table.find_all('tr')
        data = {}
        for row in rows:
            cols = row.find_all(['th', 'td'])
            cols = [col.text.strip() for col in cols]
            if len(cols) == 2:  # If the row has two columns, treat it as valid data
                data[cols[0]] = {
                    'Count': int(cols[1])
                }

        df = pd.DataFrame(data).T   # Convert the data dictionary into a pandas DataFrame
        df.reset_index(inplace=True)
        df.columns = ['Case Type', 'Count']
        csv_file = 'daily_case_status.csv'

        if not os.path.exists(csv_file):
            df.to_csv(csv_file, mode='w', header=True, index=False)
            print("Created new CSV file.")
        else:
            existing_df = pd.read_csv(csv_file)
            # Update or append data to the existing DataFrame
            for case_type in df['Case Type']:
                if case_type in existing_df['Case Type'].values:
                    existing_df.loc[existing_df['Case Type'] == case_type, ['Count']] = df.loc[df['Case Type'] == case_type, ['Count']].values
                else:
                    existing_df = existing_df.append(df[df['Case Type'] == case_type], ignore_index=True)

            existing_df.to_csv(csv_file, mode='w', header=True, index=False)
            print("CSV file updated.")
    finally:
        driver.quit()
    print("Daily case status fetching completed.")  # Print message after fetching is completed




# Function to fetch detailed case information based on a case number

def fetch_case_details(case_number):
    print(f"Fetching details for case number {case_number}...")  # Print message indicating case fetching has started
    service = Service(r'F:\Work\PYTHON\chromedriver-win64\chromedriver.exe')
    driver = webdriver.Chrome(service=service)

    try:
        driver.get('https://supremecourt.gov.np/lic/sys.php?d=reports&f=case_details')
        wait = WebDriverWait(driver, 10)

        # Locate and input the case number
        case_number_input = wait.until(EC.presence_of_element_located((By.ID, 'regno')))
        case_number_input.send_keys(case_number)

        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' and @class='btn btn-primary']")))
        submit_button.click()

         # Click on the link for detailed case information
        wait.until(EC.presence_of_element_located((By.XPATH, "//td/a[contains(text(), 'मुद्दाको बिस्तृत विवरण')]"))).click()
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'rblock')))

        # Fetching data from the detailed information section
        details = {}

        # Extracting case details
        case_table = driver.find_element(By.CLASS_NAME, 'table-hover')
        rows = case_table.find_elements(By.TAG_NAME, 'tr')

        details['मुद्दाको विवरण'] = {}

        # Loop through rows and extract the data
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, 'td')
            for i in range(0, len(cols), 2):
                if 'caption' in cols[i].get_attribute('class'):
                    key = cols[i].text.strip().replace(":", "")
                    value = cols[i + 1].text.strip() if i + 1 < len(cols) else ""
                    details['मुद्दाको विवरण'][key] = value 


        # Extracting लगाब details
        lagab_table = driver.find_element(By.CLASS_NAME, 'table-bordered')
        lagab_rows = lagab_table.find_elements(By.TAG_NAME, 'tr')

        details['लगाब मुद्दाहरुको विवरण'] = []

        if len(lagab_rows) <= 1:
            details['लगाब मुद्दाहरुको विवरण'].append({
                'दर्ता नँ': '  ',
                'दर्ता मिती': '  ',
                'मुद्दा': '  ',
                'वादीहरु': '  ',
                'प्रतिवादीहरु': '  ',
                'हालको स्थिती': '  ',
            })
        else:
            for row in lagab_rows[1:]: # Loop through rows to extract each entry
                cols = row.find_elements(By.TAG_NAME, 'td')
                entry = {
                    'दर्ता नँ': cols[0].text.strip() if len(cols) > 0 else '',
                    'दर्ता मिती': cols[1].text.strip() if len(cols) > 1 else '',
                    'मुद्दा': cols[2].text.strip() if len(cols) > 2 else '',
                    'वादीहरु': cols[3].text.strip() if len(cols) > 3 else '',
                    'प्रतिवादीहरु': cols[4].text.strip() if len(cols) > 4 else '',
                    'हालको स्थिती': cols[5].text.strip() if len(cols) > 5 else '',
                }
                details['लगाब मुद्दाहरुको विवरण'].append(entry)


        # Extracting तारेख details
        tarekh_table = driver.find_elements(By.CLASS_NAME, 'table-bordered')[1]
        tarekh_rows = tarekh_table.find_elements(By.TAG_NAME, 'tr')

        details['तारेख विवरण'] = []
        for row in tarekh_rows[1:]:
            cols = row.find_elements(By.TAG_NAME, 'td')
            details['तारेख विवरण'].append({
                'तारेख मिती': cols[0].text.strip(),
                'विवरण': cols[1].text.strip(),
                'तारेखको किसिम': cols[2].text.strip(),
                '   ': cols[3].text.strip()
            })


        # Extracting मुद्दाको स्थितीको विवरण
        sthiti_table = driver.find_elements(By.CLASS_NAME, 'table-bordered')[2]
        sthiti_rows = sthiti_table.find_elements(By.TAG_NAME, 'tr')

        details['मुद्दाको स्थितीको बिस्तृत विवरण'] = []
        if len(sthiti_rows) <= 1:
            details['मुद्दाको स्थितीको बिस्तृत विवरण'].append({
                'मिती': '  ',
                'विवरण': '  ',
                'स्थिती': '  ',
            })
        else:
            for row in sthiti_rows[1:]:
                cols = row.find_elements(By.TAG_NAME, 'td')
                details['मुद्दाको स्थितीको बिस्तृत विवरण'].append({
                    'मिती': cols[0].text.strip(),
                    'विवरण': cols[1].text.strip(),
                    'स्थिती': cols[2].text.strip(),
                })

        # Extracting पेशी को विवरण
        peshi_table = driver.find_elements(By.CLASS_NAME, 'table-bordered')[3]
        peshi_rows = peshi_table.find_elements(By.TAG_NAME, 'tr')

        details['पेशी को विवरण'] = []
        for row in peshi_rows[1:]:
            cols = row.find_elements(By.TAG_NAME, 'td')
            details['पेशी को विवरण'].append({
                'सुनवाइ मिती': cols[0].text.strip(),
                'न्यायाधीशहरू': cols[1].text.strip(),
                'मुद्दाको स्थिती': cols[2].text.strip(),
                'आदेश /फैसलाको किसिम': cols[3].text.strip(),
            })


        # Save the data to a JSON file and update/append if necessary
        filename = 'case_details.json'

        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as file:
                all_data = json.load(file)
        else:
            all_data = {}

        all_data[case_number] = details

        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(all_data, file, ensure_ascii=False, indent=4)

        print("Data saved successfully.")  # Print message after saving data
    finally:
        driver.quit()
    

# Function to schedule daily data extraction at a specific time
def schedule_tasks():
    case_numbers = [
        '080-CR-0096', '080-CR-0126', '080-CR-0199', '080-CR-0187', '080-CR-0190',
        '080-CR-0202', '080-CR-0212', '081-CR-0001', '081-CR-0002'
    ]

    # Schedule daily case status at 10:30 AM and 5:30 PM Nepal time
    schedule.every().day.at("10:30").do(fetch_and_store_data)
    schedule.every().day.at("17:30").do(fetch_and_store_data)


    # Schedule case number details at 10:30 AM and 5:30 PM Nepal time
    for case_number in case_numbers:
        schedule.every().day.at("10:30").do(fetch_case_details, case_number)
        schedule.every().day.at("17:30").do(fetch_case_details, case_number)

    print("Scraping scheduled for  at 10:30 AM and 5:30 PM.")

    while True:
        schedule.run_pending()
        time.sleep(1)

# Start the scheduling
if __name__ == "__main__":
    schedule_tasks()
