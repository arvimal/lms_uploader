LMS UPLOADER
=============

# 1. Introduction

The `lms_uploader` utility intend to automate the SCORM upload process to the LMS as easy as possible.

Since the backend of LMS (`totara`) has limited features over its API, this utility tries to use a different approach to solve the problem.

# 2. Installation

## 2.1. Installing in a Virtual Environment

In order to get the latest packages, which in many cases won't be always possible in your particular OS, we will install the requirements in a Virtual Environment.

This is not a virtual machine, but a Python virtual environment. Simply follow the steps below.

* Create a virtual environment

```bash
# python3.6 -m venv lms_uploader

# cd lms_uploader

# source lms_uploader/bin/activate
```

* Install python bindings for Selenium.

```bash
# pip install selenium --user
```

NOTE: `lms_uploader` ships with the driver for Chrome. For more details on the Chrome driver, refer:

* Getting started: `https://sites.google.com/a/chromium.org/chromedriver/getting-started`
* Chrome driver packages: `https://chromedriver.storage.googleapis.com/index.html?path=2.40/`.
* x86_64 driver for Linux: `https://chromedriver.storage.googleapis.com/2.40/chromedriver_linux64.zip`

# 3. How to execute `lms_uploader`?

`lms_uploader` supports two switches, for now.

1. `init` - Creates the template for the course, and asks the user for inputs (Course code, Course name, other stuff..)

2. `push` - Uses the information in the template to push/upload the SCORM file to LMS.