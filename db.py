from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


x = input("Type something you want to say to copilot ")


# Path to your ChromeDriver
chrome_driver_path = "chromedriver.exe"  # Replace with your actual path


# Set up the driver
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)


# Open Google homepage
driver.get("https://copilot.microsoft.com")


# Wait for the page to load
time.sleep(4)


# Accept cookies if the prompt appears (optional, depends on region)
try:
    accept_button = driver.find_element(By.XPATH, "//button[contains(text(),'Accept all')]")
    accept_button.click()
    time.sleep(1)
except:
    pass  # If no cookie prompt, continue


# Find the search box and enter "Copilot"
time.sleep(2)
search_box = driver.find_element(By.ID, "userInput")
search_box.send_keys(f"Is the japanese phrase written correctly? Answer in Yes and No: {x}")
search_box.send_keys(Keys.RETURN)  # Press Enter


# Wait to see results
time.sleep(10)


# Get the full page source
current_url= driver.current_url
chat_response = driver.find_element(By.CSS_SELECTOR, "p")


# Print part of the HTML
print("Current URL:", current_url)
print("Chat says:", chat_response.text)


# Close the browser
driver.quit()
