from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from user.models import *
from django.urls import reverse
import time

class TestUser(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome('test_functional/chromedriver')

    def tearDwon(self):
        self.browser.close()

    def test_no_alert_is_displayed(self):
        self.browser.get(self.live_server_url())
        time.sleep(20)