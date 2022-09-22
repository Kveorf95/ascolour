import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time
import json

url_links = []
product_links = []

if __name__ == '__main__':

    driver = uc.Chrome()
    driver.maximize_window()

    with open('urls.json', 'r') as f:
        url_links = json.loads(f.read())

        for value in url_links:
            driver.get(value)
            time.sleep(1)
            driver.execute_script("window.scrollTo(0, 3000)")
            time.sleep(1)
            aa = driver.find_elements(By.CLASS_NAME, "category-page")
            for a in aa:
                a = a.find_element(By.CLASS_NAME, "js-first-time").get_attribute('href')
                product_links.append(a)

            print(len(product_links))
        print(len(product_links))

    with open("product_urls.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(product_links, ensure_ascii=False, indent=4))
    driver.quit()


