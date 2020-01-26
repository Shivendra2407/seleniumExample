#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup

#url = "http://www.python.org"
url = "http://www.collegedunia.com"
response = requests.get(url)
# parse html
page = str(BeautifulSoup(response.content,features="html.parser"))


def getURL(page):
    """

    :param page: html of web page (here: Python home page) 
    :return: urls in that page 
    """

    start_link = page.find("a href")
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1: end_quote]
    return url, end_quote


def get_text_length(page_url):
    try:
        response = requests.get(page_url)
        html = response.content
        soup = BeautifulSoup(html,features="html.parser")
        text = soup.get_text()
        print(page_url," has text size ",len(text))
    except Exception as e:
        print("Exception-> "+str(e))


if __name__ == '__main__':
    url_list = []

    while True:
        url, n = getURL(page)
        page = page[n:]
        if url:
            url_list.append(url)
        else:
            break
