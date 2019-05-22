from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pickle

link_file = "links2scrape"

def get_links():
    with webdriver.Safari() as driver:
        driver.get("https://hypem.com")
        driver.find_element_by_link_text('Log in').click()
        driver.find_element_by_id('user_screen_name').send_keys('un')
        driver.find_element_by_id('user_password').send_keys('pw')
        driver.find_element_by_id('defaultform').submit()
        time.sleep(5)
        driver.get('https://hypem.com/popular/lastweek')
        soup = BeautifulSoup(driver.page_source, features="html.parser")
        flux_capacitor: BeautifulSoup = soup.find(id="flux-capacitor")
        months = flux_capacitor.select('.full')
        links = []
        for m in months:
            links = links + [a['href'] for a in m.select('a')]
        links = [{"link": l, "scraped": False} for l in links]
        outfile = open(link_file, 'wb')
        pickle.dump(links, outfile)
        outfile.close()

def scrape_song_info(driver, link):
    return


def process_links():
    infile = open(link_file, 'rb')
    data = pickle.load(infile)
    infile.close()
    with webdriver.Safari() as driver:
        driver.get("https://hypem.com")
        driver.find_element_by_link_text('Log in').click()
        driver.find_element_by_id('user_screen_name').send_keys('un')
        driver.find_element_by_id('user_password').send_keys('pw')
        driver.find_element_by_id('defaultform').submit()
        time.sleep(5)
        for link in data:
            if not link.scraped:
                scrape_song_info(driver, link['link'])

def practice_scrape():
    with webdriver.Safari() as driver:
        driver.get("https://hypem.com/popular/lastweek")
        soup = BeautifulSoup(driver.page_source, format="html.parser")


practice_scrape():

