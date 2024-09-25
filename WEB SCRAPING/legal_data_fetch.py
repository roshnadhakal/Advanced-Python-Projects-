import requests
from bs4 import BeautifulSoup
import time
import schedule
import warnings
import json
import os
import pandas as pd
from nepali.datetime import nepalidate, parser

# Suppress the unverified HTTPS request warnings
warnings.filterwarnings("ignore", message="Unverified HTTPS request")


"""-----------------------------------FETCH CASE DETAILS FROM CASE NUMBERS-----------------------------------------------"""

# Define the URL of the form
url = 'https://supremecourt.gov.np/lic/sys.php?d=reports&f=case_details'

# List of case numbers to submit
case_numbers = [
    '080-CR-0096', '080-CR-0126', '080-CR-0199', '080-CR-0187', '080-CR-0190',
    '080-CR-0202', '080-CR-0212', '081-CR-0001', '081-CR-0002'
]  # Adding the case numbers here

# Create a session to persist parameters across requests
session = requests.Session()

# Loop through each case number and submit it
def fetch_case_details():
    all_data = {}
    # Print at the beginning
    print("Redirected to case details page for case numbers")
    # Print at the beginning
    print("saving data....")
    for case_number in case_numbers:
        # Prepare the payload for the POST request
        payload = {
            'regno': case_number,    # The case number input
            'mode': 'show',          # Mode set to show
            'list': 'list'           # List parameter (if applicable)
        }

        # Send a POST request to submit the form (simulating the button click)
        response = session.post(url, data=payload, verify='False')
        response.encoding = 'utf-8'

        # Check if the submission was successful
        if response.ok:
            # Parse the response content
            soup = BeautifulSoup(response.text, 'html.parser')

            # Check if the page contains the records found message
            records_found = soup.find(string=lambda text: text and "Total" in text and "Records Found" in text)
            if records_found:
                # Find the table with case details
                table = soup.find('div', class_='table-wrap')

                if table:
                    # Find all rows in the table
                    rows = table.find_all('tr')

                    # Check if there are at least two rows (header and one data row)
                    if len(rows) > 1:
                        # Find the link in the second row
                        link = rows[1].find('a')

                        if link:
                            # Construct the URL for the detailed case view
                            detail_url = link['href']
                            detail_url = f'https://supremecourt.gov.np/lic/{detail_url}'  # Ensure it's a complete URL

                            # Follow the link to the detailed case page
                            detail_response = session.get(detail_url, verify=False)
                            detail_response.encoding = 'utf-8'

                            # Check if the redirected page was successful
                            if detail_response.ok:

                                # Parse the detailed case page content
                                detailed_soup = BeautifulSoup(detail_response.text, 'html.parser')

                                # Extract case details from the detailed page
                                details = {}

                                # Extracting case details (replace 'table-hover' with actual class or id if different)
                               
                                case_table = detailed_soup.find('table', {'class': 'table-hover'})
                                rows = case_table.find_all('tr')
                                details['मुद्दाको विवरण'] = {}  
                                for row in rows:
                                    cols = row.find_all('td')
                                    for i in range(0, len(cols), 2):
                                        if cols[i].get('class') is not None and 'caption' in cols[i].get('class', []):
                                            key = cols[i].text.strip().replace(":", "")
                                            value = cols[i + 1].text.strip() if i + 1 < len(cols) else ""
                                            details['मुद्दाको विवरण'][key] = value


                                # Extracting लगाब details
                                lagab_table = detailed_soup.find('table', {'class': 'table-bordered'})
                                details['लगाब मुद्दाहरुको विवरण'] = []
                                if lagab_table:
                                    lagab_rows = lagab_table.find_all('tr')
                                    if len(lagab_rows) <= 1:
                                        details['लगाब मुद्दाहरुको विवरण'].append({
                                            'दर्ता नँ': '  ',
                                            'दर्ता मिती': '  ',
                                            'मुद्दा': '  ',
                                            'वादीहरु': '  ',
                                            'प्रतिवादीहरु ': '  ',
                                        })
                                    else:
                                        for row in lagab_rows[1:]:
                                            cols = row.find_all('td')
                                            lagab_details = {
                                                'दर्ता नँ': cols[0].text.strip(),
                                                'दर्ता मिती': cols[1].text.strip(),
                                                'मुद्दा': cols[2].text.strip(),
                                                'वादीहरु': cols[3].text.strip(),
                                                'प्रतिवादीहरु': cols[4].text.strip(),
                                            }
                                            details['लगाब मुद्दाहरुको विवरण'].append(lagab_details)

                            # Extracting तारेख विवरण
                            tarekh_table = detailed_soup.find_all('table', {'class': 'table-bordered'})[1]
                            details['तारेख विवरण'] = []
                            if tarekh_table:
                                tarekh_rows = tarekh_table.find_all('tr')
                                if len(tarekh_rows)<=1:
                                    details['तारेख विवरण'].append({
                                        'तारेख मिती': ' ',
                                        'विवरण': ' ',
                                        'तारेखको किसिम': ' ',
                                        '   ': ' ',
                                        })
                                else:
                                    for row in tarekh_rows[1:]:
                                        cols = row.find_all('td')
                                        details['तारेख विवरण'].append({
                                            'तारेख मिती': cols[0].text.strip(),
                                            'विवरण': cols[1].text.strip(),
                                            'तारेखको किसिम': cols[2].text.strip(),
                                            '   ': cols[3].text.strip()
                                        })

                            # Extracting मुद्दाको स्थितीको विवरण
                            sthiti_table = detailed_soup.find_all('table', {'class': 'table-bordered'})[2]
                            details['मुद्दाको स्थितीको बिस्तृत विवरण'] = []
                            if sthiti_table:
                                sthiti_rows = sthiti_table.find_all('tr')
                                if len(sthiti_rows) <= 1:
                                    details['मुद्दाको स्थितीको बिस्तृत विवरण'].append({
                                        'मिती': '  ',
                                        'विवरण': '  ',
                                        'स्थिती': '  ',
                                    })
                                else:
                                    for row in sthiti_rows[1:]:
                                        cols = row.find_all('td')
                                        details['मुद्दाको स्थितीको बिस्तृत विवरण'].append({
                                            'मिती': cols[0].text.strip(),
                                            'विवरण': cols[1].text.strip(),
                                            'स्थिती': cols[2].text.strip(),
                                        })

                            # Extracting पेशी को विवरण
                            peshi_table = detailed_soup.find_all('table', {'class': 'table-bordered'})[3]
                            details['पेशी को विवरण'] = []
                            if peshi_table:
                                peshi_rows = peshi_table.find_all('tr')
                                if len(peshi_rows)<=1:
                                    details['पेशी को विवरण'].append({
                                        'सुनवाइ मिती': ' ',
                                        'न्यायाधीशहरू': ' ',
                                        'मुद्दाको स्थिती': ' ',
                                        'आदेश /फैसलाको किसिम': ' ',
                                        })
                                else:
                                    for row in peshi_rows[1:]:
                                        cols = row.find_all('td')
                                        details['पेशी को विवरण'].append({
                                            'सुनवाइ मिती': cols[0].text.strip(),
                                            'न्यायाधीशहरू': cols[1].text.strip(),
                                            'मुद्दाको स्थिती': cols[2].text.strip(),
                                            'आदेश /फैसलाको किसिम': cols[3].text.strip(),
                                        })


                                # Save the extracted details
                                all_data[case_number] = details

    # Save the data to a JSON file
    filename = 'case_details.json'
    if os.path.exists(filename):
        # Read existing data
        with open(filename, 'r', encoding='utf-8') as file:
            existing_data = json.load(file)
        # Update the existing data with new data
        existing_data.update(all_data)
    else:
        # If the file doesn't exist, create a new one with all_data
        existing_data = all_data

    # Save the updated data back to the JSON file
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(existing_data, file, ensure_ascii=False, indent=4)

    # Print the final message after all data is saved
    print("Data saved successfully.")


"""-----------------------------------FETCH AND STORE DAILY CASE STATUS-----------------------------------------------"""
# Function to fetch daily case status and store in CSV
def fetch_and_store_data():
    print("Fetching daily case status...")
    url = 'https://supremecourt.gov.np/web/eng/index'

    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        table = soup.find('table', {'width': '100%'})
        if table is None:
            print("Could not find the table on the webpage.")
            return

        rows = table.find_all('tr')
        data = {}
        for row in rows:
            cols = row.find_all(['th', 'td'])
            cols = [col.text.strip() for col in cols]
            if len(cols) == 2:
                data[cols[0]] = {'Count': int(cols[1])}

        df = pd.DataFrame(data).T
        df.reset_index(inplace=True)
        df.columns = ['Case Type', 'Count']
        csv_file = 'daily_case_status.csv'

        if not os.path.exists(csv_file):
            df.to_csv(csv_file, mode='w', header=True, index=False)
            print("Created new CSV file.")
        else:
            existing_df = pd.read_csv(csv_file)
            for case_type in df['Case Type']:
                if case_type in existing_df['Case Type'].values:
                    existing_df.loc[existing_df['Case Type'] == case_type, ['Count']] = df.loc[df['Case Type'] == case_type, ['Count']].values
                else:
                    existing_df = existing_df.append(df[df['Case Type'] == case_type], ignore_index=True)

            existing_df.to_csv(csv_file, mode='w', header=True, index=False)
            print("CSV file updated.")
    except requests.RequestException as e:
        print(f"An error occurred while fetching data: {e}")

    print("Daily case status fetching completed.")


# Function to schedule daily data extraction at a specific time
def schedule_tasks():
    try:
        # Schedule daily case status at 10:30 AM and 5:30 PM Nepal time
        schedule.every().day.at("12:12").do(fetch_and_store_data)
        schedule.every().day.at("17:30").do(fetch_and_store_data)

        # Schedule case number details at 10:30 AM and 5:30 PM Nepal time
        schedule.every().day.at("12:12").do(fetch_case_details)
        schedule.every().day.at("17:30").do(fetch_case_details)

        print("Scraping scheduled for 10:30 AM and 5:30 PM.")

        while True:
            schedule.run_pending()
            time.sleep(1)

    except KeyboardInterrupt:
        print("Scheduling stopped by user.")
    finally:
        session.close()

# Start the scheduling
if __name__ == "__main__":
    schedule_tasks()
