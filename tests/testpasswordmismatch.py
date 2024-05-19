import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import unittest

class MismatchedPasswordsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--ignore-certificate-errors")
        
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        cls.driver.get("http://127.0.0.1:9000/signup")  

    def test_mismatched_passwords(self):
        driver = self.driver

        driver.find_element(By.XPATH, "/html/body/div/form/div[4]/div[1]/div/input").send_keys("password123")
        driver.find_element(By.XPATH, "/html/body/div/form/div[4]/div[2]/div/input").send_keys("password456")  # Different confirm password


        mismatch_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//p[contains(text(), 'Passwords do not match')]"))
        )
        self.assertTrue(mismatch_message.is_displayed(), "Mismatched password message not displayed")

    @classmethod
    def tearDownClass(cls):
        time.sleep(10)
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
