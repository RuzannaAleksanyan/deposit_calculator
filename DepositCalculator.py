from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
from selenium.webdriver.chrome.options import Options

# Function for format checking
def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%d/%m/%Y")
        return True
    except ValueError:
        return False

# Function to check that start_date does not exceed the current date
def is_valid_start_date(start_date_str):
    try:
        start_date = datetime.strptime(start_date_str, "%d/%m/%Y")
        today = datetime.today()
        return start_date >= today
    except ValueError:
        return False

# Function to check if end_date is after start_date
def is_valid_end_date(start_date_str, end_date_str):
    try:
        start_date = datetime.strptime(start_date_str, "%d/%m/%Y")
        end_date = datetime.strptime(end_date_str, "%d/%m/%Y")
        return end_date > start_date
    except ValueError:
        return False

# Data entry from a computer user
while True:
    amount = input("Please enter the deposit amount: ")

    try:
        amount = float(amount)
    except ValueError:
        print("The amount must be a number. Please try again.")
        continue

    while True:
        start_date = input("Please enter the start date of the deposit (day/month/year): ")
        if not is_valid_date(start_date):
            print("The start date is in the wrong format. Please enter it in the format: day/month/year.")
        elif not is_valid_start_date(start_date):
            print("The start date must be on or after the current day. Please try again.")
        else:
            break

    while True:
        end_date = input("Please enter the end date of the deposit (day/month/year): ")
        if not is_valid_date(end_date):
            print("The end date is in the wrong format. Please enter it in the format: day/month/year.")
        elif not is_valid_end_date(start_date, end_date):
            print("The end date must be after the start date. Please try again.")
        else:
            break

    break

# Activating headless mode
chrome_options = Options()
chrome_options.add_argument("--headless") 
chrome_options.add_argument("--disable-gpu")  
chrome_options.add_argument("--window-size=1920x1080")

# Loading WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://www.acba.am/en/calculators/deposit-calculator/deposit-calculator-classic")

# Wait for the page to load and the website's "amount" field to become visible (30 seconds)
WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.NAME, "depositSum")))

try:
    amount_input = driver.find_element(By.CSS_SELECTOR, "input[name='depositSum']")
except Exception as e:
    print(f"Error finding on the website: {e}")
    driver.quit()
    exit()

amount_input.clear()
amount_input.send_keys(amount) 

try:
    start_input = driver.find_element(By.CSS_SELECTOR, "input[id='depositStartDay']")
    start_input.send_keys(start_date) 
except Exception as e:
    print(f"Error: start_input field not found: {e}")
    driver.quit()
    exit()

try:
    end_input = driver.find_element(By.NAME, "depositEndDay")
    end_input.send_keys(end_date)  
except Exception as e:
    print(f"Error: end_input field not found: {e}")
    driver.quit()
    exit()

calculate_button = driver.find_element(By.XPATH, "//input[@type='submit' and @value='Calculate']")
calculate_button.click()

try:
    time.sleep(3)  
    income_field = driver.find_element(By.NAME, "depositTotal")
    income = income_field.get_attribute("value") 
    print("Estimated income: ", income)
except Exception as e:
    print(f"Error: Income field not found or empty: {e}")

# Close browser
driver.quit()
