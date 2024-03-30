from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import unittest


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
        self.fail("Finished the test!")


if __name__ == "__main__":
    unittest.main()