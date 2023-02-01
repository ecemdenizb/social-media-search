from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import sqlite3
from email.message import EmailMessage
import ssl
import smtplib
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service

PATH = ""  # chromedriverın bilgisayarınızdaki yolu girilmelidir.
# chromedriver kurulu değilse: https://sites.google.com/chromium.org/driver/downloads

s = Service(PATH)


def main():
    keyword1 = "tire"
    keyword2 = "belediye"
    # URL = f"https://google.com/search?q={keyword}"
   # URL = f"https://www.google.com/search?q=site:www.instagram.com+{keyword1}"
    #URL_dummy=f"https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjruJm13PP8AhWKQPEDHXHBBsMQFnoECA8QAQ&url=https%3A%2F%2Fwww.instagram.com%2Fp%2F{keyword1}%2F"
   # URL=f'https://www.google.com/search?q=site=instagram.com+url=https://instagram.com/p/+"{keyword1}"'
    URL = f'https://www.google.com/search?q=site:https://instagram.com/p/+"{keyword1}+AROUND+{keyword2}"'
    driver = webdriver.Chrome(executable_path=PATH)
    driver.get(URL)
    
    time.sleep(30)
    driver.quit()
    #linkler = driver.find_elements(by=By.TAG_NAME, value="h3")

if __name__ == "__main__":
    main()

