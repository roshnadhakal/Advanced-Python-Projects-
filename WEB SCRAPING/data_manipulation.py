import datetime
from nepali.datetime import nepalidate  # Correct import
import json
import re

# Function to convert English digits to Nepali digits
def convert_to_nepali_digits(date_str):
    english_to_nepali_digits = {
        '0': '०', '1': '१', '2': '२', '3': '३', '4': '४', 
        '5': '५', '6': '६', '7': '७', '8': '८', '9': '९'
    }
    return ''.join(english_to_nepali_digits.get(char, char) for char in date_str)

# Function to convert the Nepali date from the format (२०८०।०४।१९) to NepaliDate (२०८०-०४-१९)
def convert_nepali_date(nepali_date_str):
    # Check if the date string is empty or not valid
    if nepali_date_str.strip() == "":
        return nepali_date_str

    try:
        # Split the date by '।' and convert it into NepaliDate object
        date_parts = list(map(int, re.split('।', nepali_date_str)))
        nepali_date = nepalidate(date_parts[0], date_parts[1], date_parts[2])
        
        # Format the date into yyyy-mm-dd format and convert it to Nepali digits
        formatted_date = nepali_date.strftime('%Y-%m-%d')
        return convert_to_nepali_digits(formatted_date)
    except Exception as e:
        print(f"Error converting date {nepali_date_str}: {e}")
        return nepali_date_str  # Return original if conversion fails
    
# Function to clean up strings by removing \r\n and excessive spaces
def clean_string(value):
    if isinstance(value, str):
        # Remove \r\n and replace multiple spaces with a single space
        return re.sub(r'\s+', ' ', value).strip()
    return value

# Recursive function to clean all strings in the JSON structure and remove empty key-value pairs
def clean_json_strings(data):
    if isinstance(data, dict):
        cleaned_data = {}
        for key, value in data.items():
            # Clean the key and value, and skip if key is empty
            clean_key = clean_string(key)
            if clean_key == "":
                continue  # Skip if the key is empty
            if isinstance(value, (dict, list)):
                cleaned_data[clean_key] = clean_json_strings(value)
            else:
                cleaned_data[clean_key] = clean_string(value)
        return cleaned_data
    elif isinstance(data, list):
        return [clean_json_strings(item) for item in data]
    else:
        return data

# Define a recursive function to update all the dates in the JSON structure
def update_dates_in_json(data):
    if isinstance(data, dict):
        for key, value in data.items():
            # Check if the value is a date field we need to update
            if key in ['दर्ता मिती', 'रुजु मिती', 'तारेख मिती', 'सुनवाइ मिती', 'मिती']:
                data[key] = convert_nepali_date(value)
            elif isinstance(value, (dict, list)):
                update_dates_in_json(value)
    elif isinstance(data, list):
        for item in data:
            update_dates_in_json(item)

# Load the JSON file containing case details
filename = 'case_details.json'
with open(filename, 'r', encoding='utf-8') as file:
    case_data = json.load(file)

# Clean all the strings in the case data and remove empty key-value pairs
cleaned_case_data = clean_json_strings(case_data)

# Update all the dates in the cleaned case data
update_dates_in_json(cleaned_case_data)

# Save the updated and cleaned case data back to the JSON file
with open(filename, 'w', encoding='utf-8') as file:
    json.dump(cleaned_case_data, file, ensure_ascii=False, indent=4)

print("Dates updated and unwanted key-value pairs removed successfully.")
