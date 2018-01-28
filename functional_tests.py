from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_add_url_item_and_add_to_watchlist(self):
        # Julie user has heard about a cool new online watchlist app. She goes
        # to check out its homepage
        self.browser.get('http://localhost:8000')

        # She notices the page title and header mention watchman
        self.assertIn('Watchlist', self.browser.title)

if __name__ == '__main__':
    unittest.main(warnings='ignore')
