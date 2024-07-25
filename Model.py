from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd
from fpdf import FPDF
from selenium.webdriver.edge.service import Service 

class ModelClass:
    def __init__(self, edgedriver_path):
        service = Service(edgedriver_path)
        self.driver = webdriver.Edge(service=service)

    def login_instagram(self, username, password):
        self.driver.get('https://www.instagram.com/accounts/login/')
        time.sleep(3)

        username_input = self.driver.find_element(By.NAME, 'username')
        password_input = self.driver.find_element(By.NAME, 'password')

        username_input.send_keys(username)
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)
        
        time.sleep(5)
        self.handle_not_now_popup()
        try:
            self.driver.find_element(By.XPATH, '//span[@aria-label="Profile"]')
            return True
        except:
            return False

    def scrape_profile(self, username):
        self.driver.get(f'https://www.instagram.com/{username}/')
        time.sleep(3)

        try:
            profile_data = {
            'username': username,
            'name': self.driver.find_element(By.XPATH, '//h1').text,
            'bio': self.driver.find_element(By.XPATH, '//div[@class="-vDIg"]/span').text,
            'posts': self.driver.find_element(By.XPATH, '//li[1]/span/span').text,
            'followers': self.driver.find_element(By.XPATH, '//li[2]/a/span').get_attribute('title'),
            'following': self.driver.find_element(By.XPATH, '//li[3]/a/span').text,
            }

            screenshot_directory = '/Screenshots/'
            screenshot_filename = f'{screenshot_directory}{username}_profile.png'
            self.driver.get_screenshot_as_file(screenshot_filename)
            print(f"Screenshot saved as {screenshot_filename}")

            return profile_data
        except:
            return None
        

    def search_facebook_profile(self, name):
        self.driver.get('https://www.facebook.com/')
        time.sleep(3)
        
        search_box = self.driver.find_element(By.XPATH, '//input[@aria-label="Search Facebook"]')
        search_box.send_keys(name)
        search_box.send_keys(Keys.RETURN)
        
        time.sleep(3)
        
        profiles = self.driver.find_elements(By.XPATH, '//div[@role="article"]//a[@role="link"]')
        if profiles:
            profiles[0].click()
            time.sleep(3)
            return self.scrape_facebook_profile()
        return None

    def scrape_facebook_profile(self):
        profile_data = {
            'name': self.driver.find_element(By.XPATH, '//h1').text,
            'bio': self.driver.find_element(By.XPATH, '//div[@data-testid="profile_intro_card_bio"]').text if self.driver.find_elements(By.XPATH, '//div[@data-testid="profile_intro_card_bio"]') else '',
            'friends': self.driver.find_element(By.XPATH, '//div[@data-testid="profile_intro_card_friends"]').text if self.driver.find_elements(By.XPATH, '//div[@data-testid="profile_intro_card_friends"]') else ''
        }
        return profile_data

    def save_to_pdf(self, profile_data, screenshot_file, output_file):
        data = pd.DataFrame([profile_data])

        class PDF(FPDF):
            def header(self):
                self.set_font('Arial', 'B', 12)
                self.cell(0, 10, 'Social Media Profile Report', 0, 1, 'C')

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

        pdf.add_image(screenshot_file)

        pdf.output(output_file)

        
    def logout(self, platform='instagram'):
        if platform == 'instagram':
            time.sleep(3)
            profile_button = self.driver.find_element(By.XPATH, '//span[@aria-label="Profile"]')
            profile_button.click()

            time.sleep(2)
            profile_menu = self.driver.find_element(By.XPATH, '//div[@role="menu"]')
            logout_button = profile_menu.find_element(By.XPATH, '//div[text()="Log Out"]')

            logout_button.click()

            time.sleep(2)
            try:
                confirm_button = self.driver.find_element(By.XPATH, '//button[text()="Log Out"]')
                confirm_button.click()
            except:
                pass  

            time.sleep(3)
            return True
        
    def handle_not_now_popup(self):
        time.sleep(5) 
        
        try:
            not_now_button = self.driver.find_element(By.XPATH, '//div[text()="Not now"]')
            not_now_button.click()
            print("Clicked 'Not now' button.")
        except:
            print("'Not now' button not found or already handled.")

    def close(self):
        self.driver.quit()
