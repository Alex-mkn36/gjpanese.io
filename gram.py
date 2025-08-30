import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import regex
import json
import requests
import urllib.request

def load_example(level, grammmar):
    driver = None
    try:
        url = f"https://jlpt-vocab-api.vercel.app/api/words/random?level={level}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            result = response.json()
            word = result['word']
        else:
            print("Error:", response.status_code)
            return "Error: JLPT API failed"

        grammar = grammmar
        print(grammar)
        print(level)

        # instantiate a Chrome browser
        driver = uc.Chrome(use_subprocess=False)
        driver.set_page_load_timeout(20)

        # visit the target URL
        driver.get("https://schoolhub.ai/prompt/chat-for-students")
        print("loaded")

        # Wait for the page to load
        time.sleep(4)

        # Accept cookies if the prompt appears (optional, depends on region)
        try:
            accept_button = driver.find_element(By.CLASS_NAME, "cm__btn")
            accept_button.click()
            time.sleep(1)
        except Exception as e:
            print("No cookie prompt or error:", e)

        # Find the search box and enter the prompt
        time.sleep(2)
        search_box = driver.find_element(By.CSS_SELECTOR, 'textarea[aria-label="Talk to me!"]')
        search_box.send_keys(
            f"Construct one example Japanese sentence with no explanation using the word: {word}, with the Grammar point {grammar}, sentence complexity of N{level}. Format: Japanese sentence + example"
        )
        search_box.send_keys(Keys.RETURN)
        print("after enter")

        # Wait to see results
        time.sleep(5)

        # Locate the chat response containing the specific word
        chat_response = driver.find_element(
            By.XPATH,
            f'//div[@class="gap-2"]/div[@class="space-y-2"]/p[contains(text(), "{word}") and not(contains(text(), "Japanese sentence"))]'
        )

        # Break japanese text from english meaning/romaji
        japanese_text = ''.join(
            regex.findall(r'[\p{{Script=Hiragana}}\p{{Script=Katakana}}\p{{Script=Han}}ー。、！？]', chat_response.text)
        )
        print("japanese text: " + japanese_text)

        return japanese_text if japanese_text else "No Japanese text found."
    except Exception as e:
        print("Exception in load_example:", e)
        return f"Error generating example: {e}"
    finally:
        if driver:
            try:
                driver.quit()
            except Exception:
                pass


