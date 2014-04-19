#!/usr/bin/env python

import unittest
from os import system
from time import sleep

from nose.tools import nottest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


# We don't want nose to pick this class up when running from runtests.bash
#   hence the @nottest decorator
@nottest
class TestLivesPool(unittest.TestCase):
    """Monolithic TestCase for front-end testing

    To extend this TestCase, add a step_* method
        with a test. Add this method at appropriate
        index in self.steps
    """

    def setUp(self):
        # Start the server
        system("supervisord > /dev/null 2>&1")
        system("supervisorctl start cutthroat-0")

        self.driver = webdriver.Firefox()
        # An implicit wait is to tell WebDriver to poll the DOM for a
        # certain amount of time when trying to find an element or elements
        # if they are not immediately available. The default setting is
        # 0. Once set, the implicit wait is set for the life of the
        # WebDriver object instance.
        self.driver.implicitly_wait(10)

    def test_steps(self):
        """Monolithic test method/step runner"""
        for step in self.steps:
            try:
                step()
                print("{} succeeded.".format(step.__name__))
            except Exception as e:
                self.fail("{} failed ({}: {})".format(step.__name__, type(e), e))

    @property
    def steps(self):
        """Return steps to run in order"""
        return [
            self.step_test_signin,
            self.step_test_joinaroom,
            self.step_test_createaroom,
            self.step_test_roomlobby,
            self.step_test_game
        ]

    def step_test_signin(self):
        """Test signin.html"""
        self.driver.get("http://127.0.0.1:9700")
        self.driver.find_element_by_name("username").send_keys("test")
        self.driver.find_element_by_name("password").send_keys("test")
        self.driver.find_element_by_id("signinButton").click()
        sleep(3)  # Wait for the joinaroom page to load
        # Test that login was successful
        assert "join a room" in self.driver.title.lower()

    def step_test_joinaroom(self):
        pass  # TODO

    def step_test_createaroom(self):
        pass  # TODO

    def step_test_roomlobby(self):
        pass  # TODO

    def step_test_game(self):
        pass  # TODO

    def tearDown(self):
        self.driver.close()
        system("supervisorctl stop all")


if __name__ == "__main__":
    unittest.main()
