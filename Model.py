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
import requests 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ModelClass:
    def __init__(self, edgedriver_path):
        service = Service(edgedriver_path)
        self.driver = webdriver.Edge(service=service)
        self.profile_data = {}
        self.screenshot_file = None
        self.screenshot_file_followers = None
        self.output_file = None
        self.username = ""
        self.followers = []
        self.followings = []

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

    def scrape_profile(self, username, ig_logged_in):
        self.username = username
        #get to insta profile 
        self.driver.get(f'https://www.instagram.com/{username}/')
        time.sleep(5)  
        
        try:
            time.sleep(5)  
            try:
                name_element = self.driver.find_element(By.TAG_NAME, 'h2')
                name = name_element.text if name_element else None
            except Exception:
                name = None
            try:
                bio = self.driver.find_element(By.XPATH, '//span[@class="_ap3a _aaco _aacu _aacx _aad7 _aade"]').text
            except Exception:
                bio = None

            try:
                ul = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'ul')))
                items = ul.find_elements(By.TAG_NAME, 'li')
                for li in items:
                    text = li.text
                    if 'posts' in text:
                        posts = int(text.split()[0].replace(',', ''))
                    elif 'followers' in text:
                        followers = int(text.split()[0].replace(',', ''))
                    elif 'following' in text:
                        following = int(text.split()[0].replace(',', ''))
            except Exception as e:
                print(f"Error in getting posts etc: {e}")
            
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

            # Click the followers link
            try:
                followers_link = WebDriverWait(self.driver, 500).until(
                    EC.presence_of_element_located((By.XPATH, f'//a[@href="/{username}/followers/"]'))
                )
                followers_link.click()
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "xyi19xy x1ccrb07 xtf3nb5 x1pc53ja x1lliihq x1iyjqo2 xs83m0k xz65tgg x1rife3k x1n2onr6")]'))
                )
            except Exception as e:
                print(f"Error clicking followers link: {e}")
                return
            
            try:
                followers_list = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "xyi19xy x1ccrb07 xtf3nb5 x1pc53ja x1lliihq x1iyjqo2 xs83m0k xz65tgg x1rife3k x1n2onr6")]'))
                )
                last_height = self.driver.execute_script("return arguments[0].scrollHeight", followers_list)

                while True:
                    self.driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", followers_list)
                    time.sleep(2)
                    new_height = self.driver.execute_script("return arguments[0].scrollHeight", followers_list)
                    if new_height == last_height:
                        break
                    last_height = new_height

                followers_elems = self.driver.find_elements(By.XPATH, '//span[@class="_ap3a _aaco _aacw _aacx _aad7 _aade"]')
                self.followers = [elem.text for elem in followers_elems]
            except Exception as e:
                print(f"Error scraping followers: {e}")

            try:
                close_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button._abl-'))
                )
                close_button.click()
                print("Close button clicked.")
            except Exception as e:
                print(f"Error clicking close button: {e}")


            # Click the following link
            try:
                following_link = WebDriverWait(self.driver, 500).until(
                    EC.presence_of_element_located((By.XPATH, f'//a[@href="/{username}/following/"]'))
                )
                following_link.click()
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "xyi19xy x1ccrb07 xtf3nb5 x1pc53ja x1lliihq x1iyjqo2 xs83m0k xz65tgg x1rife3k x1n2onr6")]'))
                )
            except Exception as e:
                print(f"Error clicking following link: {e}")
                return
            
            try:
                following_list = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "xyi19xy x1ccrb07 xtf3nb5 x1pc53ja x1lliihq x1iyjqo2 xs83m0k xz65tgg x1rife3k x1n2onr6")]'))
                )
                last_height = self.driver.execute_script("return arguments[0].scrollHeight", following_list)

                while True:
                    self.driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", following_list)
                    time.sleep(2)
                    new_height = self.driver.execute_script("return arguments[0].scrollHeight", following_list)
                    if new_height == last_height:
                        break
                    last_height = new_height

                following_elems = self.driver.find_elements(By.XPATH, '//span[@class="_ap3a _aaco _aacw _aacx _aad7 _aade"]')
                self.followings = [elem.text for elem in following_elems]
            except Exception as e:
                print(f"Error scraping following: {e}")

            try:
                close_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button._abl-'))
                )
                close_button.click()
                print("Close button clicked.")
            except Exception as e:
                print(f"Error clicking close button: {e}")


            self.output_file = os.path.join(screenshot_directory, f'{username}_profile.pdf')

            if posts != 0:
                try:
                    self.driver.execute_script("window.scrollTo(0,4000);")
                    time.sleep(10) 
                    images = self.driver.find_elements(By.TAG_NAME, 'img')
                    images = [image.get_attribute('src') for image in images]
                    folder_path = os.path.join(os.getcwd(), f"{username}_posts")
                    os.makedirs(folder_path, exist_ok=True)
                    for i, url in enumerate(images):
                        if url:
                            try:
                                img_data = requests.get(url).content
                                with open(os.path.join(folder_path, f'image_{i + 1}.jpg'), 'wb') as handler:
                                    handler.write(img_data)
                                print(f"Image {i + 1} saved.")
                            except Exception as e:
                                print(f"Error saving image {i + 1}: {e}")
                except:
                    pass

            return True
        except Exception as e:
            print(f"Error scraping profile: {e}")
            return False

    def save_to_pdf(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Social Media Profile Report', 0, 1, 'C')
        pdf.ln(10)

        if self.profile_data:
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, f"Profile: {self.profile_data.get('username')}", 0, 1, 'L')
            pdf.ln(10)

            pdf.set_font('Arial', '', 12)
            pdf.cell(0, 10, f"Name: {self.profile_data.get('name')}", 0, 1, 'L')
            pdf.cell(0, 10, f"Bio: {self.profile_data.get('bio')}", 0, 1, 'L')
            pdf.cell(0, 10, f"Posts: {self.profile_data.get('posts')}", 0, 1, 'L')
            pdf.cell(0, 10, f"Followers: {self.profile_data.get('followers')}", 0, 1, 'L')
            pdf.cell(0, 10, f"Following: {self.profile_data.get('following')}", 0, 1, 'L')
            pdf.ln(10)

            if self.followers:
                pdf.set_font('Arial', 'B', 12)
                pdf.cell(0, 10, "Followers List:", 0, 1, 'L')
                pdf.ln(10)
                pdf.set_font('Arial', '', 12)
                followers_list = "\n".join(self.followers)
                pdf.multi_cell(0, 10, followers_list)
                pdf.ln(10)

            if self.followings:
                pdf.set_font('Arial', 'B', 12)
                pdf.cell(0, 10, "Following List:", 0, 1, 'L')
                pdf.ln(10)
                pdf.set_font('Arial', '', 12)
                followings_list = "\n".join(self.followings)
                pdf.multi_cell(0, 10, followings_list)
                pdf.ln(10)

        if self.screenshot_file:
            pdf.image(self.screenshot_file, x=10, y=None, w=180)
            pdf.add_page()
        
        if self.screenshot_file_followers:
            pdf.image(self.screenshot_file_followers, x=10, y=None, w=180)
        
        pdf.output(self.output_file)
        print(f"PDF saved as {self.output_file}")
        return True

    def handle_not_now_popup(self):
        time.sleep(1)

        try:
            not_now_button = self.driver.find_element(By.XPATH, '//div[text()="Not now"]')
            not_now_button.click()
            time.sleep(2)
        except Exception as e:
            print(f"Not now button not found: {e}")

        try:
            not_now_button_2 = self.driver.find_element(By.XPATH, '//button[text()="Not Now"]')
            not_now_button_2.click()
            time.sleep(2)
        except Exception as e:
            print(f"Not now button 2 not found: {e}")

    def logout(self):
        try:
            self.driver.get(f'https://www.instagram.com/{self.username}/')
            time.sleep(3)
            profile_icon = self.driver.find_element(By.XPATH, '//span[@class="_2dbep qNELH"]')
            profile_icon.click()
            time.sleep(2)
            logout_button = self.driver.find_element(By.XPATH, '//button[text()="Log Out"]')
            logout_button.click()
            time.sleep(3)
            self.driver.quit()
            return True
        except Exception as e:
            print(f"Error logging out: {e}")
            return False
