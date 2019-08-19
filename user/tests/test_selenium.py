# from django.test import LiveServerTestCase
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys

# class AccountTestCase(LiveServerTestCase):

#     def setUp(self):
#         self.selenium = webdriver.safari
#         super(AccountTestCase, self).setUp()

#     def tearDown(self):
#         self.selenium.quit()
#         super(AccountTestCase, self).tearDown()

#     def test_register(self):
#         selenium = self.selenium
#         #Opening the link we want to test
#         selenium.get('http://localhost:8000/user/register/')
#         #find the form element
#         username = selenium.find_element_by_id('id_username')
#         email = selenium.find_element_by_id('id_email')
#         password1 = selenium.find_element_by_id('id_password1')
#         password2 = selenium.find_element_by_id('id_password2')

#         submit = selenium.find_element_by_name('submit')

#         #Fill the form with data
#         username.send_keys('unary')
#         email.send_keys('yusuf@qawba.com')
#         password1.send_keys('djangodjagno')
#         password2.send_keys('djangodjango')

#         #submitting the form
#         submit.send_keys(Keys.RETURN)

#         #check the returned result
#         assert 'Check your email' in selenium.page_source