from googlenewsdecoder import new_decoderv1

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import xml.etree.ElementTree as ET
import csv
from selenium.webdriver.chrome.options import Options
from selenium import webdriver


# TODO: generic publication class to inherit from
class BBCPublication:
    def __init__(self, title, google_news_link, publish_date):
        self.title = title
        self.google_news_link = google_news_link
        self.publish_date = publish_date

        self.news_link = ""

        self.headline = ""
        self.article = ""

        self.decode()
        self.parse()

    def decode(self):
        try:
            decoded_url = new_decoderv1(self.google_news_link)
            if decoded_url.get("status"):
                self.news_link = decoded_url["decoded_url"]
            else:
                print("Error:", decoded_url["message"])
        except Exception as e:
            print(f"Error occurred: {e}")

    def parse(self):
        try:
            # Send a request to the URL
            response = requests.get(self.news_link)
            response.raise_for_status()  # Raise an error for bad status codes

            # Parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            # Extract the headline
            self.headline = soup.find('h1').get_text()  # maybe class_='sc-518485e5-0 bWszMR'
            # Extract all article text for "news/articles"
            # Doesn't work for "sport", "weather", "news/videos"
            article_divs = soup.find_all('div', class_='sc-18fde0d6-0 dlWCEZ')
            self.article = " ".join(div.get_text() for div in article_divs)

            # TODO: get author <script type="application/ld+json"> has
            #  "author": [{"@type": "Person", "name": "Kathryn Armstrong"}] in the dictionary
        except Exception as e:
            return {'Error': str(e)}

    def print(self):
        print(f"Title: {self.title}")
        print(f"  Google Link: {self.google_news_link}")
        print(f"  Publish Date (GMT): {self.publish_date}")
        print(f"  News Link: {self.news_link}")
        print(f"  Headline: {self.headline}")
        print(f"  Article: {self.article}")


# Searches can be tested at https://news.google.com/home?hl=en-US&gl=US&ceid=US:en
class NewsQuery:
    def __init__(self, news_site, start_date, end_date):
        self.news_site = news_site
        self.start_date = start_date
        self.end_date = end_date

        news_site_query = "site%3A" + news_site
        start_date_query = "after%3A" + start_date
        end_date_query = "before%3A" + end_date
        self.query = news_site_query + "%20" + start_date_query + "%20" + end_date_query

        self.query_url = "https://news.google.com/rss/search?q=" + self.query + "&hl=en-US&gl=US&ceid=US:en"


def get_publications():
    # Construct the Google News query to generate the rss feed.
    news_site = "bbc.com"  # reuters.com doesn't allow scraping
    start_date = "2024-12-23"
    end_date = "2024-12-24"
    news_query = NewsQuery(news_site, start_date, end_date)
    print("Query URL: {query_url}".format(query_url=news_query.query_url))

    # Execute the search to get the rss feed.
    response = requests.get(news_query.query_url)
    rss_content = response.text
    # print(rss_content)

    # Parse the XML element tree
    root = ET.fromstring(response.text)
    items = root.findall(".//item")

    # Extract each publication from the xml
    publications = []
    for i, item in enumerate(items, start=1):
        title = item.find("title").text
        google_news_link = item.find("link").text
        publish_date = item.find("pubDate").text

        if news_site == "bbc.com":
            publication = BBCPublication(title, google_news_link, publish_date)
        else:
            print("Only BBC supported for now")
            exit(0)

        publication.print()
        publications.append(publication)

    # Write publications to the CSV file
    csv_file = "publications"+start_date+"to"+end_date+"by"+news_site+".csv"

    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(["Headline", "Publish Date", "Article"])
        # Write each publication's data
        for publication in publications:
            writer.writerow([
                publication.headline,
                publication.publish_date,
                publication.news_link,
                publication.article
            ])

    # TODO: Convert to Pandas DataFrame and Clean
    # df = pd.DataFrame(entries)
    # Convert 'pubDate' to datetime for filtering (if it exists)
    # if "pubDate" in df.columns:
        # df["pubDate"] = pd.to_datetime(df["pubDate"], errors="coerce")
    # Filter and process the data (e.g., clean or query it)
    # filtered_df = df.dropna(subset=["title", "pubDate"])  # Drop rows with missing values
    # filtered_df = filtered_df.sort_values(by="pubDate")  # Sort by publication date


if __name__ == '__main__':
    get_publications()
