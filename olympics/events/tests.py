from django.test import TestCase

# Create your tests here.
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Create your tests here.
class LoginFormTest(LiveServerTestCase):

  def testform(self):
    driver = webdriver.Chrome('C:/Users/Abhishek/Documents/ITLab/Exp10/chromedriver')
    #Choose your url to visit
    driver.get('http://127.0.0.1:8000/events/events')
    driver.find_element_by_link_text("Login").click()
    username = driver.find_element_by_id("id_username")
    password = driver.find_element_by_id("id_password")
    username.send_keys("abhishekc7")
    password.send_keys("password")
    driver.find_element_by_xpath('//input[@type="submit" and @value="Login" and @class="btn btn-primary"]').click()

    assert 'Logout' in driver.page_source


    #driver.find_elements_by_class_name('btn btn-primary').click()

    #driver.find_element_by_link_text("Login").click()
    #driver.find_element_by_value("login").click()
    #find the elements you need to submit form


class SearchTest(LiveServerTestCase):

  def testsearchevent(self):
    driver = webdriver.Chrome('C:/Users/Abhishek/Documents/ITLab/Exp10/chromedriver')

    driver.get('http://127.0.0.1:8000/events/events')
    searchbar = driver.find_element_by_name("search")
    searchbar.send_keys("Hockey")
    driver.find_element_by_xpath('//button[@type="submit"]').click()

    assert 'Hockey' in driver.page_source
    # assert 'Footabll' in driver.page_source


    # driver.find_element_by_name("submitsearch").click()


class CommentTest(LiveServerTestCase):

  def testcomment(self):
    driver = webdriver.Chrome('C:/Users/Abhishek/Documents/ITLab/Exp10/chromedriver')

    driver.get('http://127.0.0.1:8000/events/events')
    driver.find_element_by_link_text("Football").click()

    assert 'Football' in driver.page_source
    assert 'santagio' in driver.page_source
    assert 'Athlete List' in driver.page_source
    assert 'Comments' in driver.page_source

    driver.find_element_by_link_text("All events").click()
