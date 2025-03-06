from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
import ctypes

# Ֆունկցիա ֆորմատի ստուգման համար
def is_valid_date(date_str):
    try:
        # Ստուգում ենք ամսաթվի ձևաչափը՝ օր/ամիս/տարի
        datetime.strptime(date_str, "%d/%m/%Y")
        return True
    except ValueError:
        return False

# Ֆունկցիա ստուգելու համար, որ start_date-ը չի անցնում ներկայիս ամսաթվից
def is_valid_start_date(start_date_str):
    try:
        start_date = datetime.strptime(start_date_str, "%d/%m/%Y")
        today = datetime.today()
        return start_date >= today
    except ValueError:
        return False

# Ֆունկցիա ստուգելու համար, որ end_date-ն լինի start_date-ից հետո
def is_valid_end_date(start_date_str, end_date_str):
    try:
        start_date = datetime.strptime(start_date_str, "%d/%m/%Y")
        end_date = datetime.strptime(end_date_str, "%d/%m/%Y")
        return end_date > start_date
    except ValueError:
        return False

# Համակարգչի օգտագործողից տվյալների մուտքագրում
while True:
    amount = input("Խնդրում ենք մուտքագրել ավանդի գումարը: ")

    # Ստուգում, որ գումարը պետք է լինի թվեր
    try:
        amount = float(amount)
    except ValueError:
        print("Գումարը պետք է լինի թվով։ Խնդրում ենք փորձել նորից.")
        continue

    # Ստուգել start_date-ի մուտքը
    while True:
        start_date = input("Խնդրում ենք մուտքագրել ավանդի սկիզբը (օր/ամիս/տարի): ")
        if not is_valid_date(start_date):
            print("Սկիզբ ամսաթվը սխալ ֆորմատով է: Խնդրում ենք մուտքագրել ըստ ձևաչափի՝ օր/ամիս/տարի (օր/ամիս/տարի)")
        elif not is_valid_start_date(start_date):
            print("Սկիզբ ամսաթվը պետք է լինի ներկա օրվա կամ դրանից հետո: Խնդրում ենք փորձել նորից.")
        else:
            break

    # Ստուգել end_date-ի մուտքը
    while True:
        end_date = input("Խնդրում ենք մուտքագրել ավանդի վերջը (օր/ամիս/տարի): ")
        if not is_valid_date(end_date):
            print("Վերջ ամսաթվը սխալ ֆորմատով է: Խնդրում ենք մուտքագրել ըստ ձևաչափի՝ օր/ամիս/տարի (օր/ամիս/տարի)")
        elif not is_valid_end_date(start_date, end_date):
            print("Վերջ ամսաթվը պետք է լինի սկիզբ ամսաթվից հետո: Խնդրում ենք փորձել նորից.")
        else:
            break

    # Եթե բոլոր ստուգումները անցան, դուրս ենք գալիս հիմնական while-loop-ից
    break

# Բեռնում ենք WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get("https://www.acba.am/en/calculators/deposit-calculator/deposit-calculator-classic")

# Սպասել, որ էջը բեռնվի և կայքի "amount" դաշտը տեսանելի դառնա (30 վայրկյան)
WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.NAME, "depositSum")))

# Գումարի մուտքագրում
try:
    amount_input = driver.find_element(By.CSS_SELECTOR, "input[name='depositSum']")
except Exception as e:
    print(f"Սխալ կայքում գտնելու ժամանակ: {e}")
    driver.quit()
    exit()

amount_input.clear()  # Մաքրում ենք դաշտը
amount_input.send_keys(amount)  # Մուտքագրում ենք ավանդի գումարը

# Սկիզբը և վերջը մուտքագրելը
try:
    start_input = driver.find_element(By.CSS_SELECTOR, "input[name='depositStartDay']")
    start_input.clear()  # Մաքրում ենք դաշտը
    start_input.send_keys(start_date)  # Մուտքագրում ենք սկիզբ ամսաթվը
except Exception as e:
    print(f"Սխալ՝ չի գտնվել start_input դաշտը: {e}")
    driver.quit()
    exit()

# try:
#     end_input = driver.find_element(By.NAME, "depositEndDay")
#     end_input.clear()  # Մաքրում ենք դաշտը
#     end_input.send_keys(end_date)  # Մուտքագրում ենք վերջ ամսաթվը
# except Exception as e:
#     print(f"Սխալ՝ չի գտնվել end_input դաշտը: {e}")
#     driver.quit()
#     exit()


# # Սեղմել Calculate կոճակը
# calculate_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Calculate')]")
# calculate_button.click()

# # Մատուցել եկամուտը
# time.sleep(3)  # Թույլ տալ բեռնվել վեբ-էլեմենտին
# income_field = driver.find_element(By.ID, "resultIncome")  # Income դաշտը
# income = income_field.text  # Եկամուտը կարդալ

# # Արդյունքը MessageBox-ի միջոցով ցուցադրել
# # ctypes.windll.user32.MessageBoxW(0, f"Եկամուտը. {income}", "Հաշվարկված եկամուտ", 1)
# # Արդյունքը ցուցադրել console-ում
# print(f"Եկամուտը: {income}")

# # Բրաուզերը փակել
# driver.quit()
