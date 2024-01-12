#from scraper import Scraper
from course import Course
from scraper import Scraper
from phone import Phone

import os
from dotenv import load_dotenv 

# TODO: Play around with using queries instead of webscraping

if __name__ == "__main__":
    load_dotenv()

    scraper = Scraper(os.getenv("PROXY"))
    phone = Phone(os.getenv('MY_NUMBER'), os.getenv('TWILIO_NUMBER'), os.getenv('ACC_SID'), os.getenv('auth_token'))
    scraper.addCourses(Course("oscar.gatech", term_in="202402", crn_in="27768"))
    scraper.start(phone)
