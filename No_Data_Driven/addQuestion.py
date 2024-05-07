import unittest
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

class TestAddQuestion(unittest.TestCase):
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
        self.driver.get('https://lms.hcmut.edu.vn/question/bank/editquestion/question.php?courseid=48411&sesskey=MORn49Z0Oy&qtype=truefalse&returnurl=%2Fquestion%2Fedit.php%3Fcourseid%3D48411%26deleteall%3D1&courseid=48411&category=63872')
        time.sleep(1)
    
    def test_1(self):
        self.first_step()
        
        #Fill name
        self.driver.execute_script("arguments[0].setAttribute('value','test_1')", self.driver.find_element(By.ID, 'id_name'))
        time.sleep(1)

        #Save
        self.driver.find_element(By.ID,"id_updatebutton").click()
        time.sleep(3)

        # Expected: error message
        error_message = self.driver.find_element(By.ID,'id_error_questiontext').get_attribute("outerText")
        assert ("You must supply a value here" in error_message)

    def test_2(self):
        self.first_step()
        
        #Fill description
        frame = self.driver.find_element(By.ID, "id_questiontext_ifr")  # Locate the iframe element
        self.driver.switch_to.frame(frame)
        body = self.driver.find_element(By.TAG_NAME, "body")
        body.clear()
        # Fill text into the body element
        body.send_keys("test_2")

        self.driver.switch_to.default_content()

        #Save
        self.driver.find_element(By.ID,"id_updatebutton").click()
        time.sleep(3)

        # Expected: error message
        error_message = self.driver.find_element(By.ID,'id_error_name').get_attribute("outerText")
        assert ("You must supply a value here" in error_message)

    def test_3(self):
        self.first_step()
        
        #Remove mark
        self.driver.execute_script("arguments[0].setAttribute('value','')", self.driver.find_element(By.ID, 'id_defaultmark'))
        time.sleep(1)

        # Expected: error message
        error_message = self.driver.find_element(By.ID,'id_error_defaultmark').get_attribute("outerText")
        assert ("You must supply a value here" in error_message)

    def test_4(self):
        self.first_step()
        
        #Fill name
        self.driver.execute_script("arguments[0].setAttribute('value','test_4')", self.driver.find_element(By.ID, 'id_name'))
        time.sleep(1)

        #Fill description
        frame = self.driver.find_element(By.ID, "id_questiontext_ifr")  # Locate the iframe element
        self.driver.switch_to.frame(frame)
        body = self.driver.find_element(By.TAG_NAME, "body")
        body.clear()
        # Fill text into the body element
        body.send_keys("test_4")

        self.driver.switch_to.default_content()

        #Save
        self.driver.find_element(By.ID,"id_updatebutton").click()
        time.sleep(3)

        # Expected: Save success -> Change to edit mode
        title = self.driver.find_element(By.TAG_NAME,"h2").text
        assert ("Editing" in title)

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()