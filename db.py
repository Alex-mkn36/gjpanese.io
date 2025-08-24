import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

import json
import requests
import urllib.request

level = int(input("level: "))
url = f"https://jlpt-vocab-api.vercel.app/api/words/random?level={level}"
response = requests.get(url)
if response.status_code == 200:
    response = urllib.request.urlopen(url)
    result = json.loads(response.read())
    print(result['word'])
else:
    None


x = result['word']


if __name__ == "__main__":

    # instantiate a Chrome browser
    driver = uc.Chrome(
        use_subprocess=False,
    )

    # visit the target URL
    driver.get("https://bot.sannysoft.com/")


    # Wait for the page to load
    time.sleep(1000)


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
    search_box.send_keys(f"Construct a japanese sentance using the word:{x}")
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


