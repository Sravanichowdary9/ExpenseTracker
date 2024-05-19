# Testing the regular flow of the application

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import unittest

class BucksBunnyTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--ignore-certificate-errors")
        
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        cls.driver.get("http://127.0.0.1:9000")  

    def test_click_lets_go_button(self):
        driver = self.driver
        button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Let\'s Go!')]"))
        )
        button.click()

        # Add sleep to slow down the execution
        time.sleep(3)

        WebDriverWait(driver, 10).until(EC.url_contains("signup"))

        expected_url = "http://127.0.0.1:9000/signup"  
        self.assertEqual(driver.current_url, expected_url)

        self.assertTrue(driver.find_element(By.XPATH, "//h2[text()='CREATE AN ACCOUNT']").is_displayed())

    def test_fill_signup_form(self):
        driver = self.driver
        driver.get("http://127.0.0.1:9000/signup")  

        driver.find_element(By.XPATH, "//*[@id='firstName']").send_keys("Eric")
        driver.find_element(By.XPATH, "//*[@id='middleName']").send_keys("M")
        driver.find_element(By.XPATH, "//*[@id='lastName']").send_keys("Edwards")
        driver.find_element(By.XPATH, "//*[@id='username']").send_keys("ericedwards")
        driver.find_element(By.XPATH, "//*[@id='email']").send_keys("ericedwards@example.com")
        driver.find_element(By.XPATH, "//*[@id='dob']").send_keys("01-01-1990")
        driver.find_element(By.XPATH, "//*[@id='mobile']").send_keys("1234567890")
        driver.find_element(By.XPATH, "//*[@id='password']").send_keys("password123")
        driver.find_element(By.XPATH, "//*[@id='confirmPassword']").send_keys("password123")
        driver.find_element(By.XPATH, "//*[@id='city']").send_keys("New York")

        time.sleep(3)

        driver.find_element(By.XPATH, "//button[text()='Sign Up']").click()

        time.sleep(3)

    def test_login_after_signup(self):
        driver = self.driver
        driver.get("http://127.0.0.1:9000/login")  

        driver.find_element(By.XPATH, "//*[@id='username']").send_keys("ericedwards")
        driver.find_element(By.XPATH, "//*[@id='password']").send_keys("password123")

        time.sleep(3)

        driver.find_element(By.XPATH, "//button[text()='Log in']").click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h2[text()='Expense Dashboard']"))
        )

    @classmethod
    def tearDownClass(cls):
        time.sleep(10)
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
