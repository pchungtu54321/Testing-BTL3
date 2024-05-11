import unittest
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

class TestCreateTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def get_element_wait(self, element_id, timeout=3):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.ID, element_id))
            )
        except TimeoutException:
            err = 'Element with id {} could not be found!'
            raise Exception(err.format(element_id))
    
    def first_step(self):
        self.driver.get('https://sso.hcmut.edu.vn/cas/login?service=https%3A%2F%2Flms.hcmut.edu.vn%2Flogin%2Findex.php%3FauthCAS%3DCAS')

        self.driver.find_element(By.NAME,"username").send_keys("010552")
        self.driver.find_element(By.NAME,"password").send_keys("010552")
        self.driver.find_element(By.NAME,"submit").click()
        time.sleep(2)

        # Go to link for create new quizz
        self.driver.get('https://lms.hcmut.edu.vn/course/modedit.php?add=quiz&type&course=48411&section=3&return=0&sr=0&beforemod=0')
        time.sleep(1)

        #Expand all
        self.driver.find_element(By.CLASS_NAME, 'collapseexpand').click()
        time.sleep(3)

    def test_1(self): 
        self.first_step()
        
        #Fill name
        self.driver.execute_script("arguments[0].setAttribute('value','test_1')", self.driver.find_element(By.ID, 'id_name'))
        time.sleep(1)

        #Save
        self.driver.find_element(By.ID,"id_submitbutton2").click()
        time.sleep(3)

        # Expected: Save success
        elements = self.driver.find_elements(By.CLASS_NAME,'activityname')
        for item in elements:
            if "test_1" in item.get_attribute("outerText"):
                assert item.is_displayed()
        
    def test_2(self): 
        self.first_step()

        #Fill name
        self.driver.execute_script("arguments[0].setAttribute('value','')", self.driver.find_element(By.ID, 'id_name'))
        time.sleep(1)

        #Save
        self.driver.find_element(By.ID,"id_submitbutton2").click()
        time.sleep(3)

        # Expected: error message
        error_message = self.driver.find_element(By.ID,'id_error_name').get_attribute("outerText")
        assert ("You must supply a value here" in error_message)

    def test_3(self): 
        self.first_step()
        
        #Fill name
        self.driver.execute_script("arguments[0].setAttribute('value','test_3')", self.driver.find_element(By.ID, 'id_name'))
        
        # Enable TimeOpen
        self.driver.find_element(By.ID, "id_timeopen_enabled").click()
        
        #Save
        self.driver.find_element(By.ID, "id_submitbutton2").click()
        time.sleep(3)

        # Expected: Save success
        elements = self.driver.find_elements(By.CLASS_NAME,'activityname')
        for item in elements:
            if "test_3" in item.get_attribute("outerText"):
                assert item.is_displayed()

    def test_4(self): 
        self.first_step()
        
        #Fill name
        self.driver.execute_script("arguments[0].setAttribute('value','test_4')", self.driver.find_element(By.ID, 'id_name'))
        
        #Enable TimeClose
        self.driver.find_element(By.ID, "id_timeclose_enabled").click()

        #Save
        self.driver.find_element(By.ID, "id_submitbutton2").click()
        time.sleep(3)

        # Expected: Save success
        elements = self.driver.find_elements(By.CLASS_NAME, 'activityname')
        for item in elements:
            if "test_4" in item.get_attribute("outerText"):
                assert item.is_displayed()

    def test_5(self): 
        self.first_step()

        #Fill name
        self.driver.execute_script("arguments[0].setAttribute('value','test_5')", self.driver.find_element(By.ID, 'id_name'))

        #Enable TimeLimit
        self.driver.find_element(By.ID, 'id_timelimit_enabled').click()
        
        #Save
        self.driver.find_element(By.ID,"id_submitbutton2").click()
        time.sleep(5)

        # Expected: Save success
        elements = self.driver.find_elements(By.CLASS_NAME, 'activityname')
        for item in elements:
            if "test_5" in item.get_attribute("outerText"):
                assert item.is_displayed()
    
    def test_6(self): 
        self.first_step()
        
        #Fill name
        self.driver.execute_script("arguments[0].setAttribute('value','test_6')", self.driver.find_element(By.ID, 'id_name'))

        #Make time range enable: Timeclose invalid
        self.driver.find_element(By.ID, 'id_timeopen_enabled').click()
        self.driver.find_element(By.ID, 'id_timeclose_enabled').click()
        self.driver.find_element(By.XPATH, '//*[@id="id_timeclose_year"]/option[text()="2000"]').click()

        #Save
        self.driver.find_element(By.ID,"id_submitbutton2").click()
        time.sleep(3)

        # Expected: error message
        error_message = self.driver.find_element(By.ID,'id_error_timeclose').get_attribute("outerText")
        assert ("Could not update the quiz. You have specified a close date before the open date." in error_message)

    def test_7(self): 
        self.first_step()

        #Fill name
        self.driver.execute_script("arguments[0].setAttribute('value','test_6')", self.driver.find_element(By.ID, 'id_name'))

        #Make time range enable: Timeopen invalid
        self.driver.find_element(By.ID, 'id_timeopen_enabled').click()
        self.driver.find_element(By.ID, 'id_timeclose_enabled').click()
        self.driver.find_element(By.XPATH, '//*[@id="id_timeopen_year"]/option[text()="2050"]').click()
        
        #Save
        self.driver.find_element(By.ID,"id_submitbutton2").click()
        time.sleep(3)

        # Expected: error message
        error_message = self.driver.find_element(By.ID,'id_error_timeclose').get_attribute("outerText") 
        assert ("Could not update the quiz. You have specified a close date before the open date." in error_message)
    
    def test_8(self): 
        self.first_step()

        #Fill name
        self.driver.execute_script("arguments[0].setAttribute('value','test_8')", self.driver.find_element(By.ID, 'id_name'))

        # Make timelimit invalid
        self.driver.find_element(By.ID, 'id_timelimit_enabled').click()
        self.driver.execute_script("arguments[0].setAttribute('value','-1')", self.driver.find_element(By.ID, 'id_timelimit_number'))

        #Save
        self.driver.find_element(By.ID,"id_submitbutton2").click()
        time.sleep(3)

        # Expected: error message
        assert (self.driver.find_element(By.ID,'id_error_timelimit').is_displayed())
        
    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()