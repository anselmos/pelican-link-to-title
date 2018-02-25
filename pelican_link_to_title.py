# -*- coding: utf-8 -*-
""" This is a main script for pelican_link_to_title """
from pelican import signals
from bs4 import BeautifulSoup
import urllib


def link_to_title_plugin(generator):
    "Link_to_Title plugin "
    article_ptags = {}
    for article in generator.articles:
        soup = BeautifulSoup(article._content, 'html.parser')
        p_tags = soup.find_all('ahref')
        for tag in p_tags:
            url_page = tag.string
            if url_page:
                if "http://" in url_page or "https://" in url_page:
                    tag.name = "a"
                    tag.string = read_page(url_page)
                    tag.attrs = {"href": url_page}
        article._content = str(soup).decode("utf-8")

def read_page(page):
    r = urllib.urlopen(page).read()
    soup = BeautifulSoup(r , "html.parser")
    return soup.find("title").string

def register():
    """ Registers Plugin """
    signals.article_generator_finalized.connect(link_to_title_plugin)