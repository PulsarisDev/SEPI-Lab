from selenium import webdriver
from selenium.webdriver.chrome.service import Service


if __name__ == "__main__":
    service = Service('msedgedriver')
    service.start()
    driver = webdriver.Remote(service.service_url)

    driver.get('http://localhost:8000/')

    assert 'Django' in driver.page_source

    driver.quit()