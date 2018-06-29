#!/usr/bin/env python3

__author__ = "Vimal A R"
__email__ = "vimal@redhat.com"

import argparse
import os
import sys
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from lms_init import check_config, course_init
from lms_verify import read_template, verify_template

chrome_options = Options()
chrome_options.add_argument("--disable-infobars")


CHROME_DRIVER = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), "chromedriver")
LMS_URL = "ADD URL HERE"


class LMS_UPLOADER:
    """
    A utility to upload SCORM files to LMS,
    and create a consumable course.
    """

    def __init__(self, action=None):
        """
        Branch here
        """

        try:
            if action[1] == "init":
                check_config()
                course_init()
            elif action[1] == "push":
                self.initiate_browser()
            elif action[1] == None:
                check_config()
                print("\n`lms_uploader` expects either `init` or `push` as arguments.\n")
                sys.exit(-1)
        except IndexError:
            print("\n`lms_uploader` expects either `init` or `push` as arguments.\n")
            sys.exit(-1)


    def initiate_browser(self):
        # print("PATH: {}".format(os.path.realpath(__file__)))

        os.environ["webdriver.chrome.driver"] = CHROME_DRIVER
        browser = webdriver.Chrome(CHROME_DRIVER, chrome_options=chrome_options)
        browser.maximize_window()
        browser.get(LMS_URL)
        browser.implicitly_wait(20)

        # Sleep and wait for a login
        time.sleep(20)

        # `CREATE COURSE` XPath
        create_course_xpath = browser.find_element(By.XPATH, "//input[@value='Create Course']")
        create_course_xpath.click()

        # time.sleep(10)

        course_fname_xpath = browser.find_element(By.ID, "id_fullname")
        course_fname_xpath.send_keys("Red Hat Test Course")
        course_sname_xpath = browser.find_element(By.ID, "id_shortname")
        course_sname_xpath.send_keys("cee-an-110")
        course_summary_xpath = browser.find_element(By.ID, "id_summary_editoreditable")
        course_summary_xpath.send_keys("Testing Course Summary")

        course_fmt_expand_xpath = browser.find_element(By.ID, "id_courseformathdr")
        course_fmt_expand_xpath.click()

        #course_topicfmt_xpath = browser.find_element(By.ID, "id_format")




        time.sleep(20)

        # XPath of `Course Full Name`: //input[@id='id_fullname']
        # XPath of `Course Code`: //input[@id='id_shortname']
        # XPath of `Course description`: l-page']//div[@id='id_summary_editoreditable']
