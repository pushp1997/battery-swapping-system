import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("use-fake-ui-for-media-stream")
options.binary_location = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
driver_path = "/Users/pushp/battery-swapping-system/chromedriver"

# Creating driver for simulation
driver = webdriver.Chrome(options=options, executable_path=driver_path)
driver.maximize_window()
driver.implicitly_wait(2)
driver.get("http://localhost:8000/kiosk/")

# Creating driver for rack status
driver1 = webdriver.Chrome(options=options, executable_path=driver_path)
driver1.maximize_window()
driver1.implicitly_wait(2)
driver1.get("http://localhost:8000/rack/")
time.sleep(1)

###########################
#  Test Registration Flow
###########################

# Open registration page
registrationButton = driver.find_element(by=By.ID, value="registerButton")
registrationButton.click()
time.sleep(0.5)

# Fill The Registration form
registration_form = driver.find_element(by=By.ID, value="registrationFrm")
input_email = driver.find_element(by=By.NAME, value="email")
input_email.send_keys("john.doe@gmail.com")
time.sleep(0.5)
input_name = driver.find_element(by=By.NAME, value="name")
input_name.send_keys("John Doe")
time.sleep(0.5)
input_deposit_count = driver.find_element(by=By.NAME, value="deposit-count")
input_deposit_count.send_keys("4")
time.sleep(0.5)
input_license = driver.find_element(by=By.NAME, value="license")
input_license.send_keys("YGJ34HGJ63K")
time.sleep(0.5)
input_phone = driver.find_element(by=By.NAME, value="phone")
input_phone.send_keys("0895890390")
time.sleep(0.5)
input_pin = driver.find_element(by=By.NAME, value="pin")
input_pin.send_keys("1234")
time.sleep(0.5)
input_confirm_pin = driver.find_element(by=By.NAME, value="confirm-pin")
input_confirm_pin.send_keys("1234")
time.sleep(0.8)
registration_form.submit()
time.sleep(0.5)

# Fill The User Deposit form
user_deposit_form = driver.find_element(by=By.ID, value="user_deposit_form")
time.sleep(0.5)
input_card_number = driver.find_element(by=By.NAME, value="card_number")
input_card_number.send_keys("7545786992343223")
time.sleep(0.5)
input_name_on_card = driver.find_element(by=By.NAME, value="name_on_card")
input_name_on_card.send_keys("John Doe")
time.sleep(0.5)
input_cvv = driver.find_element(by=By.NAME, value="cvv")
input_cvv.send_keys("734")
time.sleep(0.5)
input_expiry = driver.find_element(by=By.NAME, value="expiry")
input_expiry.send_keys("12/28")
time.sleep(0.5)
user_deposit_form.submit()
time.sleep(3)

# Going to back to Main Menu
registration_success_form = driver.find_element(by=By.ID, value="registration_success_form")
registration_success_form.submit()

###########################
#  Test Login Flow
###########################

# Open QR Scan Page
loginButton = driver.find_element(by=By.ID, value="loginButton")
loginButton.click()
time.sleep(10)
input_enter_pin = driver.find_element(by=By.ID, value="enter-pin")
input_enter_pin.send_keys("1234")
login_pin_form = driver.find_element(by=By.ID, value="login_pin_form")
login_pin_form.submit()
time.sleep(1.5)

###########################
# Balance Recharge Flow
###########################

# Open the recharge page
recharge_button = driver.find_element(by=By.ID, value="recharge_button")
recharge_button.click()
time.sleep(1.5)

# Fill The Recharge form
user_recharge_payment_form = driver.find_element(by=By.ID, value="user_recharge_payment_form")
input_recharge_amount = driver.find_element(by=By.NAME, value="recharge_amount")
input_recharge_amount.send_keys("3000")
time.sleep(0.5)
input_card_number = driver.find_element(by=By.NAME, value="card_number")
input_card_number.send_keys("7545786992343223")
time.sleep(0.5)
input_name_on_card = driver.find_element(by=By.NAME, value="name_on_card")
input_name_on_card.send_keys("John Doe")
time.sleep(0.5)
input_cvv = driver.find_element(by=By.NAME, value="cvv")
input_cvv.send_keys("734")
time.sleep(0.5)
input_expiry = driver.find_element(by=By.NAME, value="expiry")
input_expiry.send_keys("12/28")
time.sleep(0.5)
user_recharge_payment_form.submit()
time.sleep(1.5)

##################################
# Request Battery Flow (Success)
##################################

# Open Request Battery Page
request_battery_button = driver.find_element(by=By.ID, value="request_battery_button")
request_battery_button.click()
time.sleep(0.5)

# Fill Request Battery Form
request_battery_form = driver.find_element(by=By.ID, value="request_battery_form")
input_batteries_withdrawal = driver.find_element(by=By.NAME, value="batteries_withdrawal")
input_batteries_withdrawal.send_keys("3")
time.sleep(0.5)
request_battery_form.submit()
time.sleep(5)

# Going back to dashboard from user battery
user_dashboard_button = driver.find_element(by=By.ID, value="user_dashboard_button")
user_dashboard_button.click()
time.sleep(1.5)

##################################
# Submit Battery Flow (Success)
##################################

# Open Submit Battery Page
submit_battery_button = driver.find_element(by=By.ID, value="submit_battery_button")
submit_battery_button.click()
time.sleep(0.5)

# Fill Submit Battery Form
submit_battery_form = driver.find_element(by=By.ID, value="submit_battery_form")
input_batteries_submission = driver.find_element(by=By.NAME, value="batteries_submission")
input_batteries_submission.send_keys("2")
time.sleep(0.5)
submit_battery_form.submit()
time.sleep(5)

# After Successfull Withdrawal, going back to dashboard
battery_submission_success_form = driver.find_element(
    by=By.ID, value="battery_submission_success_form"
)
battery_submission_success_form.submit()
time.sleep(5)

time.sleep(1)
driver.quit()
driver1.quit()
