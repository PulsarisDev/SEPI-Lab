from django.test import LiveServerTestCase
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):
    def setUp(self) -> None:
        self.service = Service('msedgedriver')
        self.service.start()
        self.driver = webdriver.Remote(self.service.service_url)
        return super().setUp()
    
    def tearDown(self) -> None:
        self.driver.quit()
        return super().tearDown()
    
    def wait_for_row_in_list_table(self, row_text: str):
        start_time = time.time()
        while True:
            try:
                table = self.driver.find_element(By.ID, 'id_list_table')
                rows = table.find_elements(By.TAG_NAME, 'tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except(AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

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

        input_box = self.driver.find_element(By.ID, 'id_new_item')
        input_box.send_keys('Give a gift to Lisi')
        input_box.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: Buy flowers')
        self.wait_for_row_in_list_table('2: Give a gift to Lisi')
        
    def test_multiple_users_can_start_lists_at_different_urls(self):
        self.driver.get(self.live_server_url)
        input_box = self.driver.find_element(By.ID, 'id_new_item')
        input_box.send_keys('Buy flowers')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy flowers')

        zhangsan_list_url = self.driver.current_url
        self.assertRegex(zhangsan_list_url, '/lists/.+')

        self.driver.quit()
        self.driver = webdriver.Remote(self.service.service_url)
        self.driver.get(self.live_server_url)

        page_text = self.driver.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Buy flowers', page_text)
        self.assertNotIn('Give a gift to Lisi', page_text)

        input_box = self.driver.find_element(By.ID, 'id_new_item')
        input_box.send_keys('Buy milk')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        wangwu_list_url = self.driver.current_url
        self.assertRegex(wangwu_list_url, '/lists/.+')

        self.assertNotEqual(wangwu_list_url, zhangsan_list_url)

        page_text = self.driver.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Buy flowers', page_text)
        self.assertIn('Buy milk', page_text)
