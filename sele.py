import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize the WebDriver
driver = webdriver.Chrome()

# Open the IMDb URL
driver.get('https://www.imdb.com/search/title/?genres=romance')

scroll_offset = 1000  # Adjust scroll offset value

page_no = 5
i=1

try:
    while i <= page_no:
        # Wait for the "See more" button to become visible
        see_more_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "ipc-see-more__text"))
        )

        # Scroll to the "See more" button
        driver.execute_script(f"arguments[0].scrollIntoView(); window.scrollBy(0, - {scroll_offset});", see_more_button)

        # Wait for the button to be clickable
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "ipc-see-more__text")))

        # Click on the "See more" button
        driver.execute_script("arguments[0].click();", see_more_button)

        # Wait for the page to load
        time.sleep(5)
        i+=1

except Exception as e:
    print(e)
finally:
    # Quit the WebDriver session
    driver.quit()
    pass
