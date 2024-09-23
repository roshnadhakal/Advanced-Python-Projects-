## Supreme Court Case Scraping Automation
This project automates the daily extraction of case statuses and detailed information from the Supreme Court of Nepal's website using Selenium and BeautifulSoup.  
It stores the daily case status in a CSV file and detailed case information in JSON format. The project also schedules these tasks to run at specified times every day.

## Project Overview
This project scrapes data from the Supreme Court of Nepal's website. It has two primary functions:  

- Daily Case Status: Extracts and stores an overview of daily case statuses in a CSV file.  
- Case Details: Fetches detailed information on specific cases and saves them in JSON format.  
These tasks are scheduled to run at specified times every day using the schedule Python module.

## Technologies Used
- Python 3.12.4: Main programming language.   
- Selenium: For browser automation.  
- BeautifulSoup: To parse and extract HTML data.  
- Pandas: For data manipulation and CSV storage.  
- JSON: For saving detailed case information.  
- Schedule: To automate the daily task at specific times.  
- Chrome WebDriver: To interact with the website.

# Setup and Installation

**Requirements**

- Python 3.8 or higher
- Chrome WebDriver (download it from (https://chromedriver.chromium.org/) and ensure it's compatible with your Chrome browser version).

**Python Packages**

Install the required packages by running:  

```bash
pip install selenium beautifulsoup4 pandas schedule
```

**WebDriver Setup**  
Ensure that the chromedriver executable path is correctly set in the code. Update the following lines with your WebDriver path:    
```bash
service = Service(r'path_to_your_chromedriver')
```
**Run the project script:**
```bash
python your_script_name.py
```

## Features

**Daily Case Status Fetching:** 
- Scrapes daily case statuses from the Supreme Court website.  
- Stores the data in a CSV file (daily_case_status.csv).  
- If the CSV already exists, it updates the case count instead of duplicating data.
  
**Detailed Case Information:**

1. Fetches detailed case information like case registration, hearings, parties involved, and case status.  
2. Saves the detailed information in a JSON file (case_details.json) for specific case numbers.  
   
**Automated Scheduling:**

1. Uses the schedule library to run these tasks automatically at specified times every day.  
2. The tasks are run at 10:30 AM and 12:34 PM Nepal time.

## Usage

**Fetch Daily Case Status**  
The fetch_and_store_data() function scrapes the daily case status from the Supreme Court's website and stores it in a CSV file. It:    
- Extracts a table of daily case types and counts.    
- Updates the CSV file if it already exists or creates a new one otherwise.  
  
**Fetch Case Details**
The fetch_case_details(case_number) function extracts detailed information for a specific case. It:  
- Fetches case details like registration, hearings, involved parties, and case status.  
- Saves the data into a JSON file case_details.json with the case number as the key.

# Task Scheduling

Tasks are scheduled using the `schedule_tasks()` function. It:

- Automatically fetches and updates the daily case status at **10:30 AM** and **17:30 PM** every day.
- Fetches details for a list of specific case numbers at the same times.

To start scheduling, run the script, and the scraping will happen at the scheduled times:

```bash
python your_script_name.py
```
**File Structure:**  
daily_case_status.csv: Stores daily case statuses in a table format with Case Type and Count.   
case_details.json: Contains detailed case information, with the case number as the key.  

## Contributing
Feel free to fork the repository and submit pull requests to improve the code or add new features.   
