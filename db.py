import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import regex
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

    grammar = 'から for because'
    word = result['word']

    # instantiate a Chrome browser
    driver = uc.Chrome(
        use_subprocess=False,
    )

    # visit the target URL
    driver.get("https://schoolhub.ai/prompt/chat-for-students")


    # Wait for the page to load
    time.sleep(4)


    # Accept cookies if the prompt appears (optional, depends on region)
    try:
        accept_button = driver.find_element(By.CLASS_NAME, "cm__btn")
        accept_button.click()
        time.sleep(1)
    except:
        pass  # If no cookie prompt, continue


    # Find the search box and enter "Copilot"
    time.sleep(2)
    search_box = driver.find_element(By.CSS_SELECTOR, 'textarea[aria-label="Talk to me!"]')
    search_box.send_keys(f"Construct one example Japanese sentence with no explanation using the word: {word}, with the Grammar point {grammar}, sentence complexity of N{level}. Format: Japanese sentence + example")
    search_box.send_keys(Keys.RETURN)  # Press Enter


    # Wait to see results
    time.sleep(3)


    # Get the full page source
    current_url= driver.current_url
    chat_response = driver.find_element(By.XPATH, f'//div[@class="gap-2"]/div[@class="space-y-2"]/p[contains(text(), "{word}") and not(contains(text(), "Japanese sentence"))]')

    # Break japanese text from english meaning/romaji
    japanese_text = ''.join(regex.findall(r'[\p{Script=Hiragana}\p{Script=Katakana}\p{Script=Han}ー。、！？]', chat_response.text))

    print(japanese_text)

    # Close the browser
    driver.quit()


