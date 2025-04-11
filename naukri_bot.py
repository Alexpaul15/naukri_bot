from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import time
import random
import pandas as pd
from datetime import datetime
import os

class NaukriBot:
    def __init__(self):
        self.driver = None
        self.applied_jobs = set()
        self.max_applications = 1000
        self.current_applications = 0
        
        # User specified domains and locations
        self.job_domains = [
            "Marketing", "sales",
            "crm", "product", "manufacturing", "purchase", "distribution", 
            "product development"
        ]
        self.locations = ["Hyderabad", "Bengaluru", "Visakhapatnam"]
        
        # Default answers for application forms
        self.default_answers = {
            "notice_period": "Immediate",
            "current_ctc": "0",
            "expected_ctc": "4",
            "total_experience": "0",
            "current_location": "Hyderabad",
            "preferred_location": "Hyderabad, Bengaluru, Visakhapatnam",
            "reason_for_change": "Looking for better growth opportunities",
            "skills": "Team Management, Communication, Strategic Planning",
            "languages": "English, Hindi, Telugu",
            "willing_to_relocate": "Yes",
            "highest_qualification": "B.Tech",
            "current_company": "Fresher",
            "current_designation": "Fresher"
        }
        self.setup_driver()
        self.load_applied_jobs()

    def setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-notifications')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--disable-popup-blocking')
        
        # Add options to handle system lock
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-software-rasterizer')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_argument('--disable-session-crashed-bubble')
        chrome_options.add_argument('--disable-features=TranslateUI')
        chrome_options.add_argument('--disable-features=IsolateOrigins,site-per-process')
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.implicitly_wait(5)  # Reduced implicit wait
        self.driver.maximize_window()
        
        # Remove navigator.webdriver flag
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        # Set page load timeout
        self.driver.set_page_load_timeout(30)
        
        # Set script timeout
        self.driver.set_script_timeout(30)

    def load_applied_jobs(self):
        if os.path.exists('naukri_applied_jobs.csv'):
            df = pd.read_csv('naukri_applied_jobs.csv')
            self.applied_jobs = set(df['job_id'].tolist())

    def save_applied_job(self, job_id, job_title, company):
        df = pd.DataFrame({
            'job_id': [job_id],
            'job_title': [job_title],
            'company': [company],
            'applied_date': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
        })
        df.to_csv('naukri_applied_jobs.csv', mode='a', header=not os.path.exists('naukri_applied_jobs.csv'), index=False)
        self.applied_jobs.add(job_id)

    def run(self):
        # This method should be implemented to run the bot
        pass

    def wait_for_manual_login(self):
        print("\nPlease log in to Naukri.com within 60 seconds...")
        self.driver.get("https://www.naukri.com/nlogin/login")
        time.sleep(60)
        
        # Check if login was successful using multiple methods
        try:
            # Method 1: Check URL
            if "my.naukri.com" in self.driver.current_url:
                print("Successfully logged in!")
                return True
                
            # Method 2: Check for profile elements
            profile_selectors = [
                ".nI-gNb-drawer__bars",
                ".user-name",
                ".nI-gNb-menu__title",
                ".nI-gNb-profile__image",
                ".nI-gNb-profile__name",
                ".nI-gNb-profile__email",
                ".nI-gNb-profile__menu",
                ".nI-gNb-profile__menu-item"
            ]
            
            for selector in profile_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements and any(elem.is_displayed() for elem in elements): 
                        print("Successfully logged in!")
                        return True
                except:
                    continue
            
            # Method 3: Check for post-login elements
            post_login_selectors = [
                ".nI-gNb-menu__title",
                ".nI-gNb-menu__item",
                ".nI-gNb-menu__item--active",
                ".nI-gNb-menu__item--selected"
            ]
            
            for selector in post_login_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements and any(elem.is_displayed() for elem in elements):
                        print("Successfully logged in!")
                        return True
                except:
                    continue
            
            print("Login verification failed. Please make sure you're logged in.")
            return False
            
        except Exception as e:
            print(f"Error during login verification: {str(e)}")
            return False

    def search_jobs(self, keyword, location):
        try:
            print(f"Searching for {keyword} jobs in {location}...")
            
            # Format the URL properly
            keyword_formatted = keyword.lower().replace(' ', '-')
            location_formatted = location.lower()
            search_url = f"https://www.naukri.com/{keyword_formatted}-jobs-in-{location_formatted}"
            
            print(f"Navigating to: {search_url}")
            self.driver.get(search_url)
            time.sleep(5)  # Reduced wait time
            
            # First check if we're being redirected to login page
            if "login" in self.driver.current_url.lower():
                print("Redirected to login page. Please ensure you're logged in.")
                self.wait_for_manual_login()
                self.driver.get(search_url)
                time.sleep(5)
            
            # Multiple approaches to find job cards
            job_cards = []
            
            # Approach 1: Standard job card selectors
            job_selectors = [
                "article.jobTuple", 
                "div.jobTuple", 
                ".job-tuple",
                ".jobTupleHeader",
                "[data-job-id]",
                "div.tuple",
                ".job-container",
                ".job-card"
            ]
            
            for selector in job_selectors:
                try:
                    cards = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if cards and len(cards) > 0:
                        print(f"Found {len(cards)} jobs using selector: {selector}")
                        job_cards = cards
                        break
                except Exception as e:
                    print(f"Error with selector {selector}: {str(e)}")
            
            # Approach 2: Look for any elements that might be job listings
            if not job_cards:
                print("Trying alternative detection method...")
                try:
                    elements = self.driver.find_elements(By.TAG_NAME, "div")
                    potential_cards = []
                    
                    for elem in elements:
                        try:
                            if elem.is_displayed() and elem.text and len(elem.text) > 10:
                                text = elem.text.lower()
                                if ("years" in text and 
                                   (("experience" in text) or 
                                    ("salary" in text) or 
                                    ("apply" in text) or
                                    ("job" in text))):
                                    potential_cards.append(elem)
                        except:
                            continue
                    
                    if potential_cards:
                        print(f"Found {len(potential_cards)} potential job cards using text analysis")
                        job_cards = potential_cards
                except Exception as e:
                    print(f"Error in alternative detection: {str(e)}")
            
            if job_cards and len(job_cards) > 0:
                print(f"\nFound a total of {len(job_cards)} jobs for {keyword} in {location}")
                self.current_job_cards = job_cards
                return True
            else:
                print(f"No job cards found for {keyword} in {location}")
                return False
                
        except Exception as e:
            print(f"Error in search: {str(e)}")
            return False

if __name__ == "__main__":
    bot = NaukriBot()
    print("\nStarting Naukri.com Job Application Bot")
    print(f"Target: {bot.max_applications} applications")
    print("Domains:", ", ".join(bot.job_domains))
    print("Locations:", ", ".join(bot.locations))
    print("\nIMPORTANT: You will have 60 seconds to log in manually when the browser opens.")
    bot.run() 