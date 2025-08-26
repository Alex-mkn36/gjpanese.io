import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

import json
import requests
import urllib.request


if __name__ == "__main__":

    level = 5
    url = f"https://jlpt-vocab-api.vercel.app/api/words/random?level={level}"
    response = requests.get(url)
    if response.status_code == 200:
        response = urllib.request.urlopen(url)
        result = json.loads(response.read())
        print(result['word'])
    else:
        None


    x = result['word']

    # instantiate a Chrome browser
    driver = uc.Chrome(
        use_subprocess=False,
    )

    # visit the target URL
    driver.get("https://schoolhub.ai/prompt/chat-for-students")


    # Wait for the page to load
    time.sleep(16)


    # Accept cookies if the prompt appears (optional, depends on region)
    try:
        accept_button = driver.find_element(By.CLASS_NAME, "flex w-full rounded-md border border-input bg-background px-3 py-2 ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 mb-2 h-8 max-h-48 min-h-8 border-none text-base")
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


