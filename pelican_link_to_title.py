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
    import redis
    redconn = redis.Redis(host='localhost', port=6379, db=0)
    found = redconn.get(url_page)
    if not found:
        r = urllib.urlopen(url_page).read()
        soup = BeautifulSoup(r , "html.parser")
        title = soup.find("title").string
        redconn.set(url_page, title)
        return title
    else:
        return found


def content_object_init(instance):
    if instance._content is not None:
        content = instance._content
        soup = BeautifulSoup(content, "html5lib")

        for ctbl in soup.find_all('ahref'):
            url_page = ctbl.contents[0]
            if url_page:
                if "http://" in url_page or "https://" in url_page:
                    ctbl.name = "a"
            try:
                ctbl.string = read_page(url_page)
            except:
                pass
            ctbl.attrs = {"href": url_page}
        instance._content = soup.decode()
            # If beautiful soup appended html tags.
        if instance._content.startswith('<html>'):
            instance._content = instance._content[12:-14]

def register():
    """ Registers Plugin """
    signals.content_object_init.connect(content_object_init)
    # signals.article_generator_finalized.connect(link_to_title_plugin)
