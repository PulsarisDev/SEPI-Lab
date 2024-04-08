import unittest
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.service = Service('msedgedriver')
        self.service.start()
        self.driver = webdriver.Remote(self.service.service_url)
        return super().setUp()
    
    def tearDown(self) -> None:
        self.driver.quit()
        return super().tearDown()
    
    def test_1(self) -> None:
        self.driver.get('http://localhost:8000/')

        self.assertIn('To-Do', self.driver.title)
        header_text = self.driver.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('To-Do', header_text)

        input_box = self.driver.find_element(By.ID, 'id_new_item')
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            'Enter a to-do item'
            )
        
        input_box.send_keys('Buy flowers')

        input_box.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.driver.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertIn('Buy flowers', [row.text for row in rows])

        self.fail('Finish the test!')


if __name__ == "__main__":
    unittest.main()