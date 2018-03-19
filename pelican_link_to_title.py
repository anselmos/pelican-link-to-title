# -*- coding: utf-8 -*-
""" This is a main script for pelican_link_to_title """
from pelican import signals
from bs4 import BeautifulSoup
import urllib


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
    r = urllib.urlopen(url_page).read()
    soup = BeautifulSoup(r , "html.parser")
    return soup.find("title").string

def register():
    """ Registers Plugin """
    signals.article_generator_finalized.connect(link_to_title_plugin)
