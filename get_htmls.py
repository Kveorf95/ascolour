import time
import json
import os

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

product_urls = []

if __name__ == '__main__':

    driver = uc.Chrome()
    driver.maximize_window()

    with open('links.json', 'r') as f:
        product_urls = json.loads(f.read())

        for x in product_urls:
            for gender, products in x.items():
                if not os.path.exists(f'html/{gender}'):
                    os.mkdir(f'html/{gender}')
                for category, urls in products.items():
                    if not os.path.exists(f'html/{gender}/{category}'):
                        os.mkdir(f'html/{gender}/{category}')
                    for url in urls:
                        print(url)
                        driver.get(url)
                        time.sleep(2)

                        try:
                            driver.find_element(By.ID, 'region-check').find_element(By.CLASS_NAME, 'modal-close').click()
                        except:
                            pass

                        file_name = url.split('.au/')[1].split('/')[0]

                        with open(f'html/{gender}/{category}/{file_name}.0.html', 'w', encoding='utf-8') as file:
                            file.write(driver.page_source)
                        time.sleep(1)

                        try:
                            colours = driver.find_element(By.CLASS_NAME, 'swatch-container').find_elements(By.TAG_NAME,
                                                                                                           'label')
                            i = 1
                            for colour in colours[1:]:
                                colour.find_element(By.CLASS_NAME, 'form-option-variant--color').click()
                                time.sleep(2)
                                with open(f'html/{gender}/{category}/{file_name}.{i}.html', 'w',
                                          encoding='utf-8') as file:
                                    file.write(driver.page_source)
                                i += 1
                        except:
                            pass

    driver.quit()

