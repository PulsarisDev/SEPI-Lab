from django.test import LiveServerTestCase
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(LiveServerTestCase):
    def setUp(self) -> None:
        self.service = Service('msedgedriver')
        self.service.start()
        self.driver = webdriver.Remote(self.service.service_url)
        return super().setUp()
    
    def tearDown(self) -> None:
        self.driver.quit()
        return super().tearDown()
    
    def check_for_row_in_list_table(self, row_text: str):
        table = self.driver.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self) -> None:
        self.driver.get(self.live_server_url)

        self.assertIn('To-Do', self.driver.title)
        header_text = self.driver.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('To-Do', header_text)

        input_box = self.driver.find_element(By.ID, 'id_new_item')
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            'Enter a to-do item'
            )
        
        input_box = self.driver.find_element(By.ID, 'id_new_item')
        input_box.send_keys('Buy flowers')
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)

        input_box = self.driver.find_element(By.ID, 'id_new_item')
        input_box.send_keys('Give a gift to Lisi')
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)

        self.check_for_row_in_list_table('1: Buy flowers')
        self.check_for_row_in_list_table('2: Give a gift to Lisi')
        
        self.fail('Finish the test!')
