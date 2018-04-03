# -*- coding: utf-8 -*-
""" This is a main script for pelican_link_to_title """
from pelican import signals
from bs4 import BeautifulSoup
import requests


def link_to_title_plugin(generator):
    "Link_to_Title plugin "
    article_ahreftag= {}
    for article in generator.articles:
        soup = BeautifulSoup(article._content, 'html.parser')
        ahref_tag = soup.find_all('ahref')
        if ahref_tag:
            article_ahreftag[article] = (ahref_tag, soup)

    for article, (p_tags, soup) in article_ahreftag.items():
        for tag in p_tags:
            url_page = tag.string
            if url_page:
                if "http://" in url_page or "https://" in url_page:
                    tag.name = "a"
                    tag.string = read_page(url_page)
                    tag.attrs = {"href": url_page}
            else:
                continue
        article._content = str(soup).decode("utf-8")

def read_page(url_page):
    import redis
    redconn = redis.Redis(host='localhost', port=6379, db=0)
    found = redconn.get(url_page)
    if not found:
        header_response = requests.head(url_page)
        if "text/html" in header_response.headers["content-type"]:
            html = requests.get(url_page).text
            soup = BeautifulSoup(html , "html.parser")
            title = soup.find("title").string
            redconn.set(url_page, title)
            return title
        else:
            return get_non_html_page_title(url_page, header_response)
    else:
        return found

def get_non_html_page_title(url_page, header_response):
    file_str = url_page.split("/")[-1]
    file_ext = file_str.split(".")
    url_domain = url_page.split("//")[1].split("/")[0]
    if len(file_ext) > 1:
        # file with extension in url.
        return "Url to {} file: {} on domain: {}".format(file_ext[-1], file_str, url_domain)
    else:
        # no file with extension in url
        return "Url to: {}".format(url_page)

def register():
    """ Registers Plugin """
    signals.article_generator_finalized.connect(link_to_title_plugin)
