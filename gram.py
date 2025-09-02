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

####generate_sentence function####
def generate_sentence(level, grammar):
    level = level
    if level == None:
        japanese_text = "Error1: No level selected"
        return japanese_text
    
    url = f"https://jlpt-vocab-api.vercel.app/api/words/random?level={level}"
    response = requests.get(url)
    if response.status_code == 200:
        result = response.json()
    else:
        japanese_text = "Error1: Unable to fetch word"
        return japanese_text

    grammar = grammar
    if grammar == None:
        japanese_text = "Error1: No grammar selected"
        return japanese_text
    
    word = result['word']

    # instantiate a Chrome browser
    driver = uc.Chrome(
        use_subprocess=False, headless=True
    )

    # visit the target URL
    driver.get("https://schoolhub.ai/prompt/chat-for-students")


    # Wait for the page to load
    try:
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "text-lg")))
    except:
        driver.quit()
        japanese_text = "Error1: Unable to fetch word"
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
        japanese_text = "Error1: Unable to locate input box"
        return japanese_text
    
    time.sleep(5)

    # Get the full page source
    try:
        chat_response = wait.until(EC.presence_of_element_located((By.XPATH, f'//p[contains(., "{word}") and not(contains(., "Japanese sentence"))]')))
        chat_response = driver.find_element(By.XPATH, f'//p[contains(., "{word}") and not(contains(., "Japanese sentence"))]')
    except:
        driver.quit()
        japanese_text = "Error1: Unable to fetch response"
        return japanese_text
    
    # Break japanese text from english meaning/romaji
    japanese_text = ''.join(regex.findall(r'[\p{Script=Hiragana}\p{Script=Katakana}\p{Script=Han}ー。、！？]', chat_response.text))

    # Close the browser
    driver.quit()
    return japanese_text

####check function#####
def check(answer, grammar):

    answer = answer
    grammar = grammar
    # instantiate a Chrome browser
    driver = uc.Chrome(
        use_subprocess=False, headless=True
    )

    # visit the target URL
    driver.get("https://schoolhub.ai/prompt/chat-for-students")


    wait = WebDriverWait(driver, 15)

    # Wait for the page to load
    try:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "text-lg")))
    except:
        driver.quit()
        answer = "Error2: Unable to fetch word"
        return answer


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
        search_box.send_keys(f"Check the following Japanese sentence if it uses the correct grammar structure of {grammar} and makes sense '{answer}'. Then provide an explanation and a correct example if applicable.  Answer in the following format: Grammar structure for {grammar} = True/False + Makes sense = True/False + Explanation + correct example")
        
        time.sleep(1)

        # Press Enter
        try: 
            if search_box.is_displayed() and search_box.is_enabled():
                search_box.send_keys(Keys.RETURN)
        except:
            driver.quit()
            answer = "Error2: Input box not interactable"
            return answer  
    except:
        driver.quit()
        answer = "Error2: Unable to locate input box"
        return answer

    time.sleep(5)

    # Get the full page source
    try:
        chat_marking = wait.until(EC.presence_of_element_located((By.XPATH, f'//p[contains(., "{grammar}") and not(contains(., "Check the following Japanese sentence"))]')))
        chat_marking = driver.find_element(By.XPATH, f'//p[contains(., "{grammar}") and not(contains(., "Check the following Japanese sentence"))]')
    except:
        driver.quit()
        answer = "Error2: Unable to fetch response"
        return answer
    
    answer = chat_marking.text

    # Close the browser
    driver.quit()

    return answer
