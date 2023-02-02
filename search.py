
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
browser_options = Options()
browser_options.add_argument('--headless') # Browserın headless (arkaplanda) çalışması için. Girilen sayfalar görülmek isterse bu kısım kaldırılabilir.


conn = sqlite3.connect('tire-social-media.db')  # Çekilen verileri kayıtlı tutmak için db oluşturur ve bağlanır, db ismi giriniz.
c = conn.cursor()

website_facebook = "facebook.com"
website_instagram = "instagram.com/p/"


def get_url(website, keywords, time_limit): #verilen website, anahtar kelime ve zaman kısıtlamasına göre aranacak
                                            #sayfanın url'ini oluşturur
    keyword = keywords.split(",")
    search_message=""
    for i in range(len(keyword)):
        if i==0:
            search_message+=f"{keyword[i]}"
        else :
            search_message+=f"+AROUND+{keyword[i]}"
    if time_limit==None or time_limit==0:
        time_limit_sc=""
    else :
        time_limit_sc=f'&as_qdr={time_limit}'

    URL = f'https://www.google.com/search?q=site:{website}+"{search_message}"{time_limit_sc}'
    
    return URL

def scrape_links(URL):
    driver = webdriver.Chrome(executable_path=PATH, options=browser_options)
    #driver = webdriver.Chrome(service=s, options=browser_options)

    # Eğer service has been deprecated, pass in executable path uyarısı alırsanız satır 47'yi yoruma alıp 46'yı yorumdan
    # çıkararak düzenleyebilirsiniz.

    # Eğer executable path has been deprecated, pass in service object uyarısı alırsanız satır 46'yı yoruma alıp 47'yi
    # yorumdan çıkararak düzenleyebilirsiniz.
    
    driver.get(URL)
    time.sleep(5) #Eğer sağlanan URL tarayıcıda açılıyorsa ama kodda URL response hatası veriyorsa burası arttırılabilir.
    page = driver.page_source
    soup = BeautifulSoup(page, "lxml")
    links = list()
    #try except bloğuyla gönderilerin bulunduğu iki class da alinacak.
    
    try:
        dummies = soup.find_all(class_="yuRUbf")
        for dummy in dummies:
            link = dummy.find('a', href=True)
            links.append(link['href'])
    except:
        print("bu class bulunmuyor")
    
    try:
        dummies = soup.find_all(class_="ct3b9e")
        for dummy in dummies:
            link = dummy.find('a', href=True)
            links.append(link['href'])
    except:
        print("bu class bulunmuyor")

    driver.close()
    return links

def create_table(name): #Eğer veritabanında henüz oluşturulmamışsa verilen isimle bir tablo açar
                        #Ben tablo isimleri olarak aranacak sosyal medyanın isimlerini tercih ettim (Facebook, Instagram)
    c.execute(f"""CREATE TABLE if not EXISTS {name}( Link text )""")
    conn.commit()
    
def check_insert_updates(name, links): #Yeni çekilen gönderilerin linklerini veritabanındakilerle karşılaştırarak yeni
                                       #paylaşım yapılıp yapılmadığına bakar, yapıldıysa bunları döner.
    updates = list()

    for link in links:
        c.execute(f"SELECT Link FROM {name} WHERE Link=?", (link,))
        if c.fetchone():
            pass
        else:
            updates.append(link)
    for i in range(len(updates)):
        c.execute(f"INSERT INTO {name} (Link) VALUES (?)",  (updates[i],))
        conn.commit()
    return updates
    
    

def islem(media_table, website, keywords, time_limit):
    URL = get_url(website, keywords, time_limit)
    links = scrape_links(URL)
    create_table(media_table)
    updates = check_insert_updates(media_table, links)
    
    return updates

def send_mail(name, updates): #Yeni paylaşım yapıldıysa bunları mail atar.
    db_user = ""  # Gönderici mail adresi eklenmeli.
    db_pass = ""      # Gönderici mail adresi parolası girilmeli veya başka şekilde çekilmeli
    db_recv = ""  # Alıcı mail adresi girilmeli.
    
    subject = f'{name} Gönderi Güncellemeleri' #Gönderilecek mailin konusu
    bodyList = list()
    for i in range(len(updates)):
        bodyList.append(f"{i+1}- {updates[i]} ")
    body = "\n\n".join(bodyList)
    em = EmailMessage()
    em['From'] = db_user
    em['To'] = db_recv
    em['Subject'] = subject
    em.set_content(body)
    
    context = ssl.create_default_context()
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465,
                          context=context) as smtp:  # SMTP sunucusu kullanılan sunucuya göre revize edilmelidir.
        smtp.login(db_user, db_pass)  # Bu ayarlama gmaile göre yapılmıştır
        smtp.sendmail(db_user, db_recv, em.as_string())


def main():
    
    keywords = "tire,belediye" # virgul koyarak beraber aratmak istediğiniz anahtar kelimeleri yazın
    time_limit = None  #=y1 olunca son 1 yıl, =d10 son 10 gun, =w5 son 5 hafta olan sonuclari gosteriyor, limit
                       #koymak istemezseniz bu degiskeni =None veya =0 yapabilirsiniz
    
    updates_facebook = islem("Facebook", website_facebook, keywords, time_limit)
    if len(updates_facebook)==0:
        pass
    else:
        send_mail("Facebook", updates_facebook)
    
    updates_instagram = islem("Instagram", website_instagram, keywords, time_limit)
    if len(updates_instagram)==0:
        pass
    else:
        send_mail("Instagram", updates_instagram)


if __name__ == "__main__":
    main()

