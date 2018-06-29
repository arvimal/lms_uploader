#!/usr/bin/env python3

__author__ = "Vimal A R"
__email__ = "vimal@redhat.com"

import configparser
import logging
import os
import sys
import re

import pathlib2

HOME = os.getenv('HOME')
LMS_HOME = HOME + "/.config/lms_uploader/"
CONFIG = LMS_HOME + "lms_uploader.conf"
HISTORY = LMS_HOME + "history"
LOG_FILE = LMS_HOME + "messages"

# We expect the `chromedriver` file to be in the same dir as `lms_uploader.py`
CHROME_DRIVER = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), "chromedriver")
LMS_URL = "<ADD URL HERE"

#
lms_logger = logging.getLogger(__name__)
lms_logger.setLevel(logging.INFO)

handler = logging.FileHandler(LOG_FILE)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
lms_logger.addHandler(handler)


def check_config():
    """
    Check/Create the LMS_UPLOADER configuration
    """

    if all([pathlib2.Path(CONFIG).exists(), CHROME_DRIVER, LOG_FILE]):
        # logging.basicConfig(filename=LOG_FILE, level=logging.INFO)
        lms_logger.info("-" * 20)
        lms_logger.info("lms_uploader starting up, running initial checks.")
        lms_logger.info("{} exists.".format(pathlib2.Path(CONFIG)))
        lms_logger.info("{} exists.".format(pathlib2.Path(CHROME_DRIVER)))

        # Checking the contents of CONFIG

        #
        logging.info("Returning control to lms_uploader")
        print("\n{:>40}".format("-LMS UPLOADER-"))
        pass

    else:
        print("\n{:>40}".format("-LMS UPLOADER-"))
        print("\n- Initial configuration:")

        # CREATE LMS_UPLOADER HOME, CONFIG, HISTORY, LOG_FILE
        pathlib2.Path(LMS_HOME).mkdir()
        pathlib2.Path(CONFIG).touch(exist_ok=True)
        pathlib2.Path(HISTORY).touch(exist_ok=True)
        pathlib2.Path(LOG_FILE).touch(exist_ok=True)

        # LET'S LOG SINCE LOG_FILE IS UP
        logging.basicConfig(filename=LOG_FILE, level=logging.INFO)
        logging.info("lms_uploader initial run")
        logging.info("Generating configuration files.")

        # WRITE THE CONF FILE
        conf_parser = configparser.ConfigParser()
        conf_parser.add_section("global")
        conf_vars = {
            "LMS_HOME": LMS_HOME,
            "CONFIG": CONFIG,
            "HISTORY": HISTORY,
            "LOG_FILE": LOG_FILE,
            "CHROME_DRIVER": CHROME_DRIVER
        }

        for k, v in conf_vars.items():
            conf_parser.set("global", k, v)

        with open(CONFIG, "w") as config_file:
            conf_parser.write(config_file)

        logging.info("{} creation complete.".format(CONFIG))
        logging.info("Returning control to lms_uploader")
        print("\n{:>40}".format("-LMS UPLOADER-"))


def course_init():
    """
    Create the SCORM template

    We expect the SCORM package to be
    located in the current working directory.
    """

    print("1. Gathering Course info - \n")

    # Gathering course information

    # 1. Error hits
    info_errors = 0

    # 2. Collecting Course name and Course code
    course_name = input("{:<25}".format("Course full name                : "))
    course_code = input("{:<25}".format("Course code [eg: cee-AB-123]    : "))
    # 2.1. course regex
    course_regex = re.compile("^([ce]){3}-([a-z]{2})-(\d{3})$", re.I)

    if course_regex.search(course_code):
        course_info_file = course_code + ".txt"
        scorm_package = course_code + ".zip"

    else:
        course_info_file = "CEE_COURSE.txt"
        print("\n Invalid entry for Course code, should be in the form `cee-<AB>-<123>`")
        print(" Manually set the `Course code` in {}".format(course_info_file))
        # Settings values due to user input error
        course_code = "<FILL MISSING INFO>"
        scorm_package = course_code + ".zip"
        # Not considering the `course_info_file` var set properly,
        # we still have two vars not set, hence two errors.
        info_errors += 2


    # 3. Collecting Course category, either `Technical` or `Soft skills`
    course_category_dict = {
        "1": "Technical",
        "2": "Professional Development and Individual Leadership"
    }
    print("{:<20}".format("\n2. Course category -\n"))
    print(" * Technical   [1]")
    print(" * Soft skills [2]")
    course_category = input("\n{:<25}".format("Enter category number  :"))
    if course_category not in course_category_dict.keys():
        print("\n Invalid entry for Course Category, should either be 1 or 2.")
        print(" Manually set the `Course Category` in {}".format(course_info_file))
        course_category = "<FILL MISSING INFO>"
        info_errors += 1
    else:
        course_category = course_category_dict[course_category]

    # 4. Collecting Course visibility, either `All` or `Enrolled`
    course_visibility_dict = {
        "1": "All",
        "2": "Enrolled Users"
    }
    print("{:<20}".format("\n3. Course visibility -\n"))
    print(" * All         [1]")
    print(" * Enrolled    [2]")
    course_visibility = input("\n{:<25}".format("Enter course visibility: "))
    if course_visibility not in course_visibility_dict.keys():
        print("\n Invalid entry for Course visibility, should be either 1 or 2.")
        print(" Manually set the `Course visibility` in {}".format(course_info_file))
        course_visibility = "<FILL MISSING INFO>"
        info_errors += 1
    else:
        course_visibility = course_visibility_dict[course_visibility]

    # 5. Collecting Associate name
    print("{:<20}".format("\n4. Associate information -"))
    associate_name = input("\n{:<20}".format(" * Associate name      : "))
    associate_email = input("{:<20}".format(" * Email address       : "))

    # 6. Rolling up the captured information
    pathlib2.Path(course_info_file).touch(exist_ok=True)
    course_parser = configparser.ConfigParser()
    course_parser.add_section("Course information")
    course_vars = {
        "course_name": course_name,
        "course_code": course_code,
        "scorm_package": scorm_package,
        "course_category": course_category,
        "course_visibility": course_visibility,
        "associate_name": associate_name,
        "associate_email": associate_email,
        "course_description": '""" """'
    }

    for k, v in course_vars.items():
        course_parser.set("Course information", k, v)
        # print(k, v)

    with open(course_info_file, "w") as cif:
        course_parser.write(cif)

    # 7. Status update to the end user
    print("\n- IMPORTANT -")
    print("\n 1. Course information captured in {}.\n".format(course_info_file))
    print(" 2. Fill the `Course Description` section in {}.\n".format(course_info_file))

    if info_errors != 0:
        print(" 3. Errors present in {}: {}\n".format(course_info_file, info_errors))
        print("\nExecute `lms_uploader push` once the errors are fixed.\n")
    else:
        print("\nExecute `lms_uploader push` once the description is added.\n")
    sys.exit(0)

