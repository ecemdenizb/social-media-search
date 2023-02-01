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
    keyword = "tire"
    # URL = f"https://google.com/search?q={keyword}"
    URL = f"https://www.google.com/search?q=site%3Ahttps%3A%2%2Fwww.instagram.com%2Fp%2F+**{keyword}**"
    
    driver = webdriver.Chrome(executable_path=PATH)
    
    driver.get(URL)
    time.sleep(30)


if __name__ == "__main__":
    main()

