# This project was made in partial fulfillment of the requirements for the course NSSECU2
# submitted by:
# ABANIEL, AARON C.
# BIACORA, LUIS GABRIEL S.
# BLASCO, GIAN RAPHAEL Q.
# EVANGELISTA, REGINALD ANDRE I.
# QUINONES, ANGELO Y.
# ROSALES, KEAN LOUIS R.
# Group 4 | S12
# Submitted to:
# ASCAN, ADRIAN GIOVANNI
# on 
# (deadline)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
import time
import pandas as pd
from fpdf import FPDF
import os

class ModelClass:
    def __init__(self, edgedriver_path):
        service = Service(edgedriver_path)
        self.driver = webdriver.Edge(service=service)
        self.profile_data = {}
        self.screenshot_file = None
        self.output_file = None
        self.username = ""

    def login_instagram(self, username, password):
        self.driver.get('https://www.instagram.com/accounts/login/')
        time.sleep(3)

        username_input = self.driver.find_element(By.NAME, 'username')
        password_input = self.driver.find_element(By.NAME, 'password')

        username_input.send_keys(username)
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)

        time.sleep(5)
        try:
            self.handle_not_now_popup()
            return True
        except Exception as e:
            print(f"Error during login: {e}")
            return False

    def scrape_profile(self, username):
        self.username = username
        self.driver.get(f'https://www.instagram.com/{username}/')
        time.sleep(5)  # Allow some time for the page to load

        try:
            # Wait for specific elements to be visible by sleeping
            time.sleep(3)  # Wait to ensure the profile page is fully loaded

            # Extract data, setting to None if the element is not found
            try:
                name = self.driver.find_element(By.XPATH, '//span[@class="x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye xvs91rp x1s688f x5n08af x10wh9bi x1wdrske x8viiok x18hxmgj"]').text
            except Exception:
                name = None

            try:
                bio = self.driver.find_element(By.XPATH, '//span[@class="_ap3a _aaco _aacu _aacx _aad7 _aade"]').text
            except Exception:
                bio = None

            try:
                posts = self.driver.find_element(By.XPATH, '//span[contains(@class, "xkhd6sd")]').text
            except Exception:
                posts = None

            try:
                followers = self.driver.find_element(By.XPATH, '//a[contains(@href, "/followers/")]/span').text
            except Exception:
                followers = None

            try:
                following = self.driver.find_element(By.XPATH, '//a[contains(@href, "/following/")]/span').text
            except Exception:
                following = None

            self.profile_data = {
                'username': username,
                'name': name,
                'bio': bio,
                'posts': posts,
                'followers': followers,
                'following': following,
            }

            screenshot_directory = 'Screenshots'
            os.makedirs(screenshot_directory, exist_ok=True)
            self.screenshot_file = os.path.join(screenshot_directory, f'{username}_profile.png')
            self.driver.get_screenshot_as_file(self.screenshot_file)
            print(f"Screenshot saved as {self.screenshot_file}")

            self.output_file = os.path.join(screenshot_directory, f'{username}_profile.pdf')

            return True
        except Exception as e:
            print(f"Error scraping profile: {e}")
            return False
        
    def save_to_pdf(self):
        try:
            if not self.profile_data or not self.screenshot_file or not self.output_file:
                print("Profile data, screenshot file, or output file is missing.")
                return False

            data = pd.DataFrame([self.profile_data])

            class PDF(FPDF):
                def header(self):
                    self.set_font('Arial', 'B', 12)
                    self.cell(0, 10, f'Social Media Profile Report', 0, 1, 'C')

                def chapter_title(self, title):
                    self.set_font('Arial', 'B', 12)
                    self.cell(0, 10, title, 0, 1, 'L')
                    self.ln(10)

                def chapter_body(self, body):
                    self.set_font('Arial', '', 12)
                    self.multi_cell(0, 10, body)
                    self.ln()

                def add_image(self, image_path):
                    self.image(image_path, x=10, y=None, w=180)

            pdf = PDF()
            pdf.add_page()

            for index, row in data.iterrows():
                pdf.chapter_title(f"Profile: {row['username']}")
                pdf.chapter_body(f"Name: {row['name']}\nBio: {row['bio']}\nPosts: {row['posts']}\nFollowers: {row['followers']}\nFollowing: {row['following']}\n")

            pdf.add_image(self.screenshot_file)
            pdf.output(self.output_file)
            print(f"PDF saved as {self.output_file}")

            return True
        except Exception as e:
            print(f"{e}")
            return False
           

    def handle_not_now_popup(self):
        time.sleep(1) 
        
        try:
            not_now_button = self.driver.find_element(By.XPATH, '//div[text()="Not now"]')
            not_now_button.click()
            print("Clicked 'Not now' button.")
            time.sleep(3)
            not_now_button = self.driver.find_element(By.XPATH, '//button[contains(@class, "_a9--") and contains(@class, "_ap36") and contains(@class, "_a9_1") and text()="Not Now"]')
            not_now_button.click()
            print("Clicked 'Not now' button.")
        except Exception as e:
            print(f"'Not now' button not found or already handled: {e}")

    def search_twitter(self, username):
        try:
            self.driver.get(f'https://twitter.com/{username}')
            time.sleep(5)  # Allow some time for the page to load

            # Check if the page loaded successfully
            if "This account doesn’t exist" in self.driver.page_source:
                print("Account does not exist.")
                return False

            # Optionally, take a screenshot of the profile
            screenshot_directory = 'Screenshots'
            os.makedirs(screenshot_directory, exist_ok=True)
            self.screenshot_file = os.path.join(screenshot_directory, f'{username}_twitter_profile.png')
            self.driver.get_screenshot_as_file(self.screenshot_file)
            print(f"Screenshot saved as {self.screenshot_file}")

            # Extract additional profile details if needed

            return True
        except Exception as e:
            print(f"Error searching Twitter: {e}")
            return False
        
    def close(self):
        self.driver.quit()
