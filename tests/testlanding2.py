import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
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

    def test_click_login_link(self):
        driver = self.driver

        login_link = driver.find_element(By.XPATH, "//a[text()='Login']")
        

        login_link.click()


        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h2[text()='ALREADY A MEMBER?']"))
        )

    def test_login(self):
        driver = self.driver
        driver.get("http://127.0.0.1:9000/login")  

        driver.find_element(By.XPATH, "//*[@id='username']").send_keys("ericedwards")
        driver.find_element(By.XPATH, "//*[@id='password']").send_keys("password123")

        driver.find_element(By.XPATH, "//button[text()='Log in']").click()

        welcome_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Welcome')]"))
        )
        self.assertTrue(welcome_message.is_displayed())

    @classmethod
    def tearDownClass(cls):
        time.sleep(10)
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
