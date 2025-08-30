import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import regex
import json
import requests
import urllib.request


def generate_sentence(level, grammar):
    level = level
    if level == None:
        japanese_text = "Error: No level selected"
        return japanese_text
    
    url = f"https://jlpt-vocab-api.vercel.app/api/words/random?level={level}"
    response = requests.get(url)
    if response.status_code == 200:
        response = urllib.request.urlopen(url)
        result = json.loads(response.read())
    else:
        japanese_text = "Error: Unable to fetch word"
        return japanese_text

    grammar = grammar
    if grammar == None:
        japanese_text = "Error: No grammar selected"
        return japanese_text
    
    word = result['word']

    # instantiate a Chrome browser
    driver = uc.Chrome(
        use_subprocess=False,
    )

    # visit the target URL
    driver.get("https://schoolhub.ai/prompt/chat-for-students")


    # Wait for the page to load
    try:
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "text-xl")))
    except:
        driver.quit()
        japanese_text = "Error: Unable to fetch word"
        return japanese_text


    # Accept cookies if the prompt appears (optional, depends on region)
    try:
        accept_button = driver.find_element(By.CLASS_NAME, "cm__btn")
        accept_button.click()
        time.sleep(1)
    except:
        pass  # If no cookie prompt, continue

    # Find the search box and enter "Copilot"
    try:
        search_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'textarea[aria-label="Talk to me!"]')))
        search_box = driver.find_element(By.CSS_SELECTOR, 'textarea[aria-label="Talk to me!"]')
        search_box.send_keys(f"Construct one example Japanese sentence with no explanation using the word: {word}, with the Grammar point {grammar}, sentence complexity of N{level}. Format: Japanese sentence + example")
        search_box.send_keys(Keys.RETURN)  # Press Enter
    except:
        driver.quit()
        japanese_text = "Error: Unable to locate input box"
        return japanese_text

    # Wait to see results
    time.sleep(10)


    # Get the full page source
    try:
        chat_response = wait.until(EC.presence_of_element_located((By.XPATH, f'//div[@class="gap-2"]/div[@class="space-y-2"]/p[contains(text(), "{word}") and not(contains(text(), "Japanese sentence"))]')))
        chat_response = driver.find_element(By.XPATH, f'//div[@class="gap-2"]/div[@class="space-y-2"]/p[contains(text(), "{word}") and not(contains(text(), "Japanese sentence"))]')
    except:
        driver.quit()
        japanese_text = "Error: Unable to fetch response"
        return japanese_text
    
    # Break japanese text from english meaning/romaji
    japanese_text = ''.join(regex.findall(r'[\p{Script=Hiragana}\p{Script=Katakana}\p{Script=Han}ー。、！？]', chat_response.text))

    # Close the browser
    driver.quit()
    return japanese_text