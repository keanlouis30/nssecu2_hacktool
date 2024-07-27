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





#Model


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
from difflib import SequenceMatcher
from reportlab.lib.utils import ImageReader
import io
from PIL import Image as PILImage
import io
import tempfile
import re


class ModelClass:
    def __init__(self, edgedriver_path):
        service = Service(edgedriver_path)
        self.driver = webdriver.Edge(service=service)
        self.profile_data = {}
        self.image_data = []  
        self.screenshot_data = None  
        self.username = ""
        self.followers = []
        self.followings = []
        self.profiles = []
        self.date_joined = ""


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
            name_element = self.driver.find_element(By.XPATH, '//span[contains(@class, "x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye xvs91rp x1s688f x5n08af x10wh9bi x1wdrske x8viiok x18hxmgj")]')
            name = name_element.text
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

        name_element.click()

        try:
            date_joined_element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,"//span[text()='Date joined']" )))
            date_joined = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//span[text()='Date joined']/following-sibling::span[1]"))
                ).text
        except:
            date_joined = None

        self.profile_data = {
            'username': username,
            'name': name,
            'bio': bio,
            'posts': posts,
            'followers': followers,
            'following': following,
            'date_joined': date_joined
        }

        try:
            close_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[text()='Close']"))
            )
            self.screenshot_data = io.BytesIO(self.driver.get_screenshot_as_png())
            date_joined_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[text()='Date joined']"))
            )
            close_button.click()
            print("Button clicked successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")

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
                print("scroll down page")
                self.driver.execute_script("window.scrollTo(0,4000);")
                time.sleep(10) 
                print("getting images")
                images = self.driver.find_elements(By.CSS_SELECTOR, "div._aagv img") 
                for image in images:
                    url = image.get_attribute('src')
                    alt = image.get_attribute('alt')
                    if url:
                        try:
                            response = requests.get(url)
                            img = PILImage.open(io.BytesIO(response.content))
                            print("storing image + caption")
                            self.image_data.append({'image': img, 'caption': alt})
                        except Exception as e:
                            print(f"Error processing image: {e}")
            except Exception as e:
                print(f"Error extracting images: {e}")
        print("scrape done")
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

            try:
                for key, value in self.profile_data.items():
                    elements.append(Paragraph(f"<b>{key.capitalize()}:</b> {value}", style_normal))
                    elements.append(Spacer(1, 12))
            except Exception as e:
                print(f"Error saving profile data: {e}")

        temp_file_paths = []

        try:
            if self.screenshot_data:
                try:
                    print("Attempting to add screenshot to PDF")
                    img_reader = ImageReader(io.BytesIO(self.screenshot_data.getvalue()))
                    img = Image(img_reader, width=6*inch, height=6*inch)
                    elements.append(img)
                    print("Screenshot added to PDF elements")
                except Exception as e:
                    print(f"Error adding screenshot to PDF: {e}")

            if self.followers:
                try:
                    elements.append(Paragraph("<b>Followers:</b>", styles['Heading2']))
                    elements.append(Spacer(1, 0.2 * inch))
                    followers_list = "<br/>".join(self.followers)
                    elements.append(Paragraph(followers_list, style_normal))
                    elements.append(Spacer(1, 12))
                except Exception as e:
                    print(f"Error saving followers list: {e}")

            if self.followings:
                try:
                    elements.append(Paragraph("<b>Following:</b>", styles['Heading2']))
                    elements.append(Spacer(1, 0.2 * inch))
                    followings_list = "<br/>".join(self.followings)
                    elements.append(Paragraph(followings_list, style_normal))
                    elements.append(Spacer(1, 12))
                except Exception as e:
                    print(f"Error saving following list: {e}")

            if self.image_data:
                try:
                    elements.append(Paragraph("<b>Images and Captions:</b>", styles['Heading2']))
                    elements.append(Spacer(1, 0.2 * inch))
                    for data in self.image_data:
                        img_data = data['image']
                        caption = data['caption']

                        if isinstance(img_data, PILImage.Image):
                            img_bytes = io.BytesIO()
                            img_data.save(img_bytes, format='JPEG')
                            img_data = img_bytes.getvalue()

                        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
                            img = PILImage.open(io.BytesIO(img_data))
                            img.save(temp_file, format='JPEG')
                            temp_file_path = temp_file.name
                            temp_file_paths.append(temp_file_path)
                        elements.append(Image(temp_file_path, width=6*inch, height=6*inch))
                        elements.append(Spacer(1, 12))
                        elements.append(Paragraph(f"<b>Caption:</b> {caption}", style_normal))
                        elements.append(Spacer(1, 12))
                except Exception as e:
                    print(f"Error saving posts + caption: {e}")

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
  
    def scrape_twitter(self, username):
        self.driver.get(f'https://twitter.com/{username}')
        time.sleep(5)

        try:
            name = self.driver.find_element(By.XPATH, '//div[@data-testid="UserName"]').text
            self.add_profile_data({
                'platform': 'Twitter',
                'username': username,
                'name': name
            })
            return True
        except Exception as e:
            print(f"Error scraping Twitter: {e}")

    def scrape_youtube(self, username):
        self.driver.get(f'https://www.youtube.com/{username}')
        time.sleep(5)

        try:
            name = self.driver.find_element(By.XPATH, '//yt-formatted-string[@id="text"]').text
            self.add_profile_data({
                'platform': 'YouTube',
                'username': username,
                'name': name
            })
            return True
        except Exception as e:
            print(f"Error scraping YouTube: {e}")




    def find_matches(self, target_username):
        matches = []

        for profile in self.profiles:
            name_similarity = self.string_similarity(target_username, profile['name'])

          
            threshold = 0.5
            if name_similarity > threshold:
                matches.append({
                    'platform': profile['platform'],
                    'username': profile['username'],
                    'name_similarity': name_similarity
                })

        return matches
    
    def add_profile_data(self, profile_data):
        self.profiles.append(profile_data)

    def string_similarity(self, a, b):
        return SequenceMatcher(None, a, b).ratio()
    
    def scrape_google(self, username):
        try:
            social_media_sites = ["twitter.com", "youtube.com", "facebook.com"]
            search_results = []

            for site in social_media_sites:
                search_query = f"{username} site:{site}"
                self.driver.get(f'https://www.google.com/search?q={search_query}')
                time.sleep(5)

                
                page_source = self.driver.page_source
                urls = re.findall(r'(https?://[^\s"]+)', page_source)

            for url in urls:
                if site in url:
                    if site != "facebook.com" :
                        username = "@" + username
                    search_results.append(url)

           
            results_file = 'social_media_search_results.txt'
            with open(results_file, 'w') as file:
                for result in search_results:
                    file.write(f"{result}\n")

            return search_results

        except Exception as e:
            print(f"Error searching Google: {e}")
            return None
        

        return False

