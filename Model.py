from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
import time
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
import os
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image as PILImage
import io
import tempfile

class ModelClass:
    def __init__(self, edgedriver_path):
        service = Service(edgedriver_path)
        self.driver = webdriver.Edge(service=service)
        self.profile_data = {}
        self.image_data = []  # List to store images as byte arrays
        self.screenshot_data = None  # Byte array for screenshot
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
        self.driver.get(f'https://www.instagram.com/{username}/')
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

        # Capture screenshot as byte array
        self.screenshot_data = io.BytesIO(self.driver.get_screenshot_as_png())

        # Click the followers link
        try:
            followers_link = WebDriverWait(self.driver, 500).until(
                EC.presence_of_element_located((By.XPATH, f'//a[@href="/{username}/followers/"]'))
            )
            followers_link.click()
            WebDriverWait(self.driver, 500).until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "xyi19xy x1ccrb07 xtf3nb5 x1pc53ja x1lliihq x1iyjqo2 xs83m0k xz65tgg x1rife3k x1n2onr6")]'))
            )
        except Exception as e:
            print(f"Error clicking followers link: {e}")
            return
        
        try:
            followers_list = WebDriverWait(self.driver, 500).until(
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

        time.sleep(3)
        try:
            close_button = WebDriverWait(self.driver, 500).until(
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
            WebDriverWait(self.driver, 500).until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "xyi19xy x1ccrb07 xtf3nb5 x1pc53ja x1lliihq x1iyjqo2 xs83m0k xz65tgg x1rife3k x1n2onr6")]'))
            )
        except Exception as e:
            print(f"Error clicking following link: {e}")
            return
        
        try:
            following_list = WebDriverWait(self.driver, 500).until(
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

        time.sleep(3)
        try:
            close_button = WebDriverWait(self.driver, 500).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button._abl-'))
            )
            close_button.click()
            print("Close button clicked.")
        except Exception as e:
            print(f"Error clicking close button: {e}")

        if posts != 0:
            try:
                self.driver.execute_script("window.scrollTo(0,4000);")
                time.sleep(10) 
                images = self.driver.find_elements(By.CSS_SELECTOR, "div._aagv img") 
                image_urls = [image.get_attribute('src') for image in images]

                for url in image_urls:
                    if url:
                        try:
                            img_data = requests.get(url).content
                            self.image_data.append(img_data)  # Store image as byte array
                            print(f"Image added to array.")
                        except Exception as e:
                            print(f"Error adding image: {e}")
            except Exception as e:
                print(f"Error scraping profile: {e}")
                return False

        return True

    def save_to_pdf(self):
        doc = SimpleDocTemplate(f"{self.profile_data.get('username')}_report.pdf", pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        style_normal = styles["Normal"]
        style_heading = styles["Heading1"]

        elements.append(Paragraph("Social Media Profile Report", style_heading))
        elements.append(Spacer(1, 0.2 * inch))

        if self.profile_data:
            elements.append(Paragraph(f"Profile: {self.profile_data.get('username')}", style_heading))
            elements.append(Spacer(1, 0.2 * inch))

            elements.append(Paragraph(f"Name: {self.profile_data.get('name')}", style_normal))
            elements.append(Paragraph(f"Bio: {self.profile_data.get('bio')}", style_normal))
            elements.append(Paragraph(f"Posts: {self.profile_data.get('posts')}", style_normal))
            elements.append(Paragraph(f"Followers: {self.profile_data.get('followers')}", style_normal))
            elements.append(Paragraph(f"Following: {self.profile_data.get('following')}", style_normal))
            elements.append(Spacer(1, 0.2 * inch))

            if self.followers:
                elements.append(Paragraph("Followers List:", style_heading))
                elements.append(Spacer(1, 0.2 * inch))
                followers_list = "<br/>".join(self.followers)
                elements.append(Paragraph(followers_list, style_normal))
                elements.append(Spacer(1, 0.2 * inch))

            if self.followings:
                elements.append(Paragraph("Following List:", style_heading))
                elements.append(Spacer(1, 0.2 * inch))
                followings_list = "<br/>".join(self.followings)
                elements.append(Paragraph(followings_list, style_normal))
                elements.append(Spacer(1, 0.2 * inch))

        temp_file_paths = []

        try:
            if self.screenshot_data:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
                    temp_file.write(self.screenshot_data.getvalue())
                    temp_file_path = temp_file.name
                    temp_file_paths.append(temp_file_path)
                elements.append(Image(temp_file_path, width=6*inch, height=4*inch))

            for img_data in self.image_data:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
                    img = PILImage.open(io.BytesIO(img_data))
                    img = img.convert('RGB')
                    img.save(temp_file, format='JPEG')
                    temp_file_path = temp_file.name
                    temp_file_paths.append(temp_file_path)
                elements.append(Image(temp_file_path, width=3*inch, height=3*inch))

            doc.build(elements)
        finally:
            for temp_file_path in temp_file_paths:
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)

        print(f"PDF saved as {self.profile_data.get('username')}_report.pdf")
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
