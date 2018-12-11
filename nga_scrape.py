#!/usr/bin/env python3

import re
import argparse
import time
import logging
import urllib.parse as urlparse

from bs4 import BeautifulSoup

from nga_artists.artist import Artist
from nga_artists.database import ArtistDB
from nga_artists import html_request

NGA_ARTIST_INDEX_BASE_URL = 'https://web.archive.org/web/20121007172915/https://www.nga.gov/collection/'

# 1. This should be a program argument or configurable in some way.
# 2.Yeah, I guess that works. But is it really maintanable? What if I wanted to say:
# ./nga_scrape.py --db mydb.db
# What if the requirements for this tool increased in scope?
# Also, on a more practical level, what if you wanted to support the common:
# --help command line parameter that MOST if not all command line tools use?
# Implementing that would be difficult. Maybe use argparse?
# 3. Nice. Can you indent the parameters so that they are easier to read?
# 4. Why are these values in global scope?
# 5. Why does this code begin executing while it's being compiled?
# 6. This should be inside if __name__ == "__main__":


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Extract data into a sqlite3 database")
    parser.add_argument("--db-path", help="Provide the name of the database")

    args = parser.parse_args()

    log = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)

    artist_index_url = NGA_ARTIST_INDEX_BASE_URL + 'an.shtm'
    request_page = html_request.get_request(artist_index_url)

    soup = BeautifulSoup(request_page.text, 'html.parser')

    artist_initial_forms = soup.find_all('form', {'action': re.compile('an[A-Z]1\.htm')})

    artist_initial_links = []

    for form in artist_initial_forms:
        action_link = form.get('action')
        artist_initial_links.append(action_link)

    # Creating a database connection to a SQLite database
    log.info('Creating the Artist Database Table...')
    database = ArtistDB(args.db_path)

    for link in artist_initial_links:

        url = NGA_ARTIST_INDEX_BASE_URL + link
        request_page = html_request.get_request(url)
        soup = BeautifulSoup(request_page.text, 'html.parser')

        # Find the title that has information on the initial and total pages
        page_title = soup.find('title')
        title = soup.find("h3").text
        log.info(f"{title}...")

        initial_letter = title[-1]
        total_pages = int(page_title.text.strip().split()[-1])

        # Scrap each page
        for page_count in range(1, total_pages + 1):
            log.info(f"'{initial_letter}' Page {page_count} of {total_pages}...")
            page_url = NGA_ARTIST_INDEX_BASE_URL + f"an{initial_letter}{page_count}.htm"

            artists_page = html_request.get_request(page_url)
            new_soup = BeautifulSoup(artists_page.text, 'html.parser')

            last_links = new_soup.find(class_='AlphaNav')
            last_links.decompose()

            artist_name_list = new_soup.find(class_='BodyText')
            artist_name_list_items = artist_name_list.find_all('a')
            artist_description_list = artist_name_list.find_all('td')[1::2]

            for i in range(len(artist_name_list_items)):
                if len(artist_name_list_items[i].contents) != 0:

                    full_name = artist_name_list_items[i].contents[0]

                    # Ignore entry if the artist name is empty
                    if "," in full_name:
                        first_name = full_name.split(",")[1].strip()
                        last_name = full_name.split(",")[0].strip()
                    else:
                        first_name = full_name
                        last_name = ""

                    biography = artist_description_list[i].text
                    local_path = artist_name_list_items[i].get('href')
                    link = 'https://web.archive.org' + local_path

                    parsed = urlparse.urlparse(local_path)
                    artist_id = int(urlparse.parse_qs(parsed.query)['artistid'][0])

                    # Create an Artist object
                    artist = Artist(artist_id, first_name, last_name, biography, link)
                    print(artist)

                    database.add_entry(artist)

        time.sleep(5)

    log.info("Closing database connection to 'artist_names.db'...")
    database.close()
    log.info("Done Scraping.")
