# Web Scraping Challenge

## Overview

This project addresses a web scraping challenge focused on extracting data from the blog posts of the website [https://rategain.com/blog](https://rategain.com/blog). The goal is to collect information such as the title, date, image URL, and likes count from each blog post.

## Implementation

The program uses the `concurrent.futures` module in Python to concurrently execute tasks, optimizing efficiency, especially for I/O-bound operations like web scraping. The `ThreadPoolExecutor` is employed to extract all the pages of the blogging website, creating a list of URLs to be processed.

With multiple crawlers, the script proceeds to scrape each URL using the `requests` library, establishing a persistent session and adding headers to emulate legitimate browser requests. Upon successful requests, the HTML content is parsed using BeautifulSoup, a Python library that simplifies data extraction from HTML and XML files.

For each blog post within the div tag with the class 'wrap,' relevant information such as title, date, image URL, and likes is extracted using their respective classes and tags. If the image URL is not found, a "Not found" statement is inserted. A dictionary is then created to store all the details.

## Data Storage

After iterating through all the URLs, the collected information is saved in a .csv file. If a file with the specified filename already exists, a new file is created to save the data. The .csv file includes columns for title, date, image URL, and likes count.

## Usage

To use this script:

1. Ensure Python is installed on your system.
2. Install the required libraries: `requests`, `beautifulsoup4`.
3. Execute the script in a Python environment.

```bash
python web_scraping_challenge.py
