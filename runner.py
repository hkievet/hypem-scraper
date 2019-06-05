from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pickle
import json

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
    driver.get(link)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, features="html.parser")
    time_machine_header = soup.select("#message")[0]
    t = time_machine_header.text
    date_text = t[t.index("(")+1:-2]

    tracks = soup.select('.haarp-section-track')
    song_data = []
    for i in range(5):
        track_soup = tracks[i]
        header = track_soup.select('.track_name')
        if not header:
            print(f"WARNING: missed a song: {link}")
            continue
        header = header[0]
        track_artist = ""
        s = header.select('.artist')
        if s and s[0] and s:
            track_artist = s[0].text
        track_name = ""
        s = header.select('.base-title')
        if s:
            track_name = s[0].text
        remix_link = ""
        s = header.select('.remix-link')
        if s:
            remix_link = s[0].text
        remix_count = 0
        s = header.select('.remix-count')
        if s:
            remix_count = s[0].text
        meta = track_soup.select('.meta')
        spotify_hyperlink = ""
        if meta:
            meta = meta[0]
            spotify_link = meta.find_all("a", text="Spotify")
            if spotify_link:
                spotify_hyperlink = spotify_link[0]['href']

        data = {
            'track_name': track_name,
            'track_artist': track_artist,
            'remix_link': remix_link,
            'remix_count': remix_count,
            'date_text': date_text,
            'spotify_link': spotify_hyperlink,
        }
        song_data.append(data)

    if song_data:
        save_songs(song_data)
        return True

    return False


def pickel_links(data):
    outfile = open(link_file, 'wb')
    pickle.dump(data, outfile)
    outfile.close()


def save_songs(all_song_data):
    with open('songs.txt', 'a+') as data_file:
        for song in all_song_data:
            data_file.write(json.dumps(song) + "\n")
            # data_file.write(
            # f"{song.get('track_name')}, {song['track_artist']}, {song['remix_link']}, {song['remix_count']}\n")


def process_links():
    infile = open(link_file, 'rb')
    data = pickle.load(infile)
    infile.close()
    with webdriver.Safari() as driver:
        driver.get("https://hypem.com")
        driver.find_element_by_link_text('Log in').click()
        driver.find_element_by_id('user_screen_name').send_keys('un')
        driver.find_element_by_id('user_password').send_keys('pw')
        driver.find_element_by_id('submitlogin').click()
        time.sleep(5)
        for link in data:
            if not link['scraped']:
                success = scrape_song_info(
                    driver, f"https://hypem.com{link['link']}")
                if success:
                    link['scraped'] = True
                    pickel_links(data)
                    print('successfully pickeled a link!')
                time.sleep(2)


def reset_links():
    infile = open(link_file, 'rb')
    data = pickle.load(infile)
    infile.close()
    for d in data:
        if d['link'] == '/popular/week:Oct-12-2015':
            d['scraped'] = True
            break
        else:
            d['scraped'] = True
    pickel_links(data)


def practice_scrape():
    process_links()
    # scrape_song_info(driver, 'https://hypem.com/popular')
    # driver.get("https://hypem.com/popular/lastweek")
    # soup = BeautifulSoup(driver.page_source, format="html.parser")


# reset_links()
# get_links()
practice_scrape()
