import requests
from bs4 import BeautifulSoup
import time
import random
import urllib3
from course import Course
from phone import Phone

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# TODO Clean Up / Add more exception handling

class Scraper():

    def __init__(self, proxy: str = None):
        self.__courses = []

        if proxy:
            self.__proxy = {"http": proxy}
        else:
            self.__proxy = None
    
    def addCourses(self, *courses : Course):
        for course in courses:
            if self.__hasValidURL(course):
                self.__courses.append(course)

    def __hasValidURL(self, course: Course) -> bool:
        try:
            self.__getNumSeats(course)
            return True
        except IndexError:
            print(f"Could not find index value that is associated with the course. Try checking if you entered course info correctly. CRN: {course.crn}")
        except requests.exceptions.InvalidURL:
            print(f"Invalid URL, make sure your university portal uses the same scheme as described. If not, change the base URL of the course. CRN: {course.crn}")
        except requests.exceptions.ConnectionError:
            print(f"Connection Timeout")
        return False

    def __getPageContents(self, course: Course) -> str:
        if self.__proxy:
            return requests.get(course.url, proxies=self.__proxy, verify=False).content
        return requests.get(course.url).content
    
    def __getNumSeats(self, course: Course) -> int:
        soup = BeautifulSoup(self.__getPageContents(course), 'html.parser')
        portalTable = soup.findAll('table')[3]
        numSeatsOpen = portalTable.findAll('td')[4].getText()

        return int(numSeatsOpen)

    def __hasOpenSeat(self, course: Course) -> bool:
        seatsAvailable = self.__getNumSeats(course)
        return seatsAvailable > 0
    
    def __scrapeAllCourses(self, phone: Phone) -> None:
        for course in self.__courses:
            if self.__hasOpenSeat(course):
                print(f"FOUND A SEAT CRN:{course.crn}")
                if phone:
                    phone.sendSMS(f"CRN: {course.crn} has Open Spot")
                self.__courses.remove(course)

            time.sleep(random.uniform(30, 60)) 
        time.sleep(random.uniform(90, 300))

    def start(self, phone: Phone = None) -> None:
        print("Starting...")
        if phone:
            phone.sendSMS("Starting...")
        while self.__courses:
            self.__scrapeAllCourses(phone)
        print("Done")
        if phone:
            phone.sendSMS("No courses left")