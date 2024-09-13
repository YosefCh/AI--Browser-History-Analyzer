import datetime
import os
import browser_history as bh
import pandas as pd
from dateutil import parser
import pytz
import re
import time


# get start time to use for calculating duration of program
start = datetime.datetime.now()
print('')

print("""The warnings stating that certain browsers are not installed or supported can be ignored. 
The program will still run successfully.""")
print()


# allow the user to see the above line by waiting  a few seconds before the warning messages obscure it.
for _ in range(4):  
        time.sleep(1)
        print("", end="", flush=True)
 
with open('browser_history_file_path.txt', 'r') as file:
    browser_history_path = file.read()       


                   

# Function to clean up ambiguous Unicode characters and keep only alphanumeric characters
def clean_alphanumeric(text):
    
    # remove leading or trailing whitespace
    text = text.strip()
    
    # This uses the re.sub function from the re (regular expression) module to replace one or more whitespace 
    # characters (\s+) with a hyphen (-). One of the columns needed to be cleaned up to remove whitespace characters
    text = re.sub(r'\s+', '-', text)
    
    # This uses re.sub again to remove any character that is not an uppercase letter (A-Z), lowercase letter (a-z), 
    # digit (0-9), or hyphen (-). The ^ inside the square brackets negates the character class.
    text = re.sub(r'[^a-zA-Z0-9-]', '', text)
    return text


# Function to export browser history
def export_browser_history():
    """
    Export browser history to a CSV file.
    
    This function retrieves the browser history using the browser_history library,
    converts it to a DataFrame, and saves it to a CSV file at the specified path.
    """
    
    history = bh.get_history()
    df_browser_history = pd.DataFrame(history.histories, columns=['Date', 'URL', 'browser'])
    df_browser_history['browser'] = df_browser_history['browser'].apply(clean_alphanumeric)
    df_browser_history.to_csv(browser_history_path, index=False)

# Function to adjust and round a timestamp to the nearest second
def adjust_and_round_timestamp(timestamp):
    timestamp = parser.parse(timestamp)
    local_tz = pytz.timezone('US/Eastern')
    local_time = timestamp.astimezone(local_tz)
    rounded_time = local_time.replace(microsecond=0)
    formatted_time = rounded_time.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_time


# Delete old borwser history file if it exists
if os.path.exists(browser_history_path):
    os.remove(browser_history_path)
    print('Old browser history file deleted.')
    
print()

# call the function to export the browser history
export_browser_history()
print()
print('New browser history file created.')
print()

        
# Read the browser history CSV file into a DataFrame
df_history = pd.read_csv(browser_history_path)

print('Processing.....')

        
# Adjust and round the 'Date' column for each row
for i in df_history.index:
    df_history.at[i, 'Date'] = adjust_and_round_timestamp(df_history.at[i, 'Date'])

       
# Overwrite the original CSV file with the filtered DataFrame
df_history.to_csv(browser_history_path, index=False)


end_time = datetime.datetime.now()
print()
print("Program Complete")
print("Duration: ", end="")
print(end_time - start)
print('')
