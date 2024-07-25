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
        """Log in to Instagram."""
        self.driver.get('https://www.instagram.com/accounts/login/')
        time.sleep(3)

        username_input = self.driver.find_element(By.NAME, 'username')
        password_input = self.driver.find_element(By.NAME, 'password')

        username_input.send_keys(username)
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)
        
        time.sleep(5)

    def scrape_profile(self, username):
        """Scrape Instagram profile data."""
        self.driver.get(f'https://www.instagram.com/{username}/')
        time.sleep(3)

        profile_data = {
            'username': username,
            'name': self.driver.find_element(By.XPATH, '//h1').text,
            'bio': self.driver.find_element(By.XPATH, '//div[@class="-vDIg"]/span').text,
            'posts': self.driver.find_element(By.XPATH, '//li[1]/span/span').text,
            'followers': self.driver.find_element(By.XPATH, '//li[2]/a/span').get_attribute('title'),
            'following': self.driver.find_element(By.XPATH, '//li[3]/a/span').text,
        }
        return profile_data

    def save_to_pdf(self, profile_data, output_file):
        """Save profile data to a PDF report."""
        data = pd.DataFrame([profile_data])

        class PDF(FPDF):
            def header(self):
                self.set_font('Arial', 'B', 12)
                self.cell(0, 10, 'Instagram Profile Report', 0, 1, 'C')

            def chapter_title(self, title):
                self.set_font('Arial', 'B', 12)
                self.cell(0, 10, title, 0, 1, 'L')
                self.ln(10)

            def chapter_body(self, body):
                self.set_font('Arial', '', 12)
                self.multi_cell(0, 10, body)
                self.ln()

        pdf = PDF()
        pdf.add_page()

        for index, row in data.iterrows():
            pdf.chapter_title(f"Profile: {row['username']}")
            pdf.chapter_body(f"Name: {row['name']}\nBio: {row['bio']}\nPosts: {row['posts']}\nFollowers: {row['followers']}\nFollowing: {row['following']}\n")

        pdf.output(output_file)

    def close(self):
        """Close the WebDriver."""
        self.driver.quit()
