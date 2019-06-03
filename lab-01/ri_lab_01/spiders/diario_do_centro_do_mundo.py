# -*- coding: utf-8 -*-
import scrapy
import json
from ri_lab_01.item_parser import ItemParser

class DiarioDoCentroDoMundoSpider(scrapy.Spider):
  name = 'diario_do_centro_do_mundo'
  allowed_domains = ['diariodocentrodomundo.com.br']
  start_urls = []
  visited_urls = []

  def __init__(self, *a, **kw):
    super(DiarioDoCentroDoMundoSpider, self).__init__(*a, **kw)
    with open('seeds/diario_do_centro_do_mundo.json') as json_file:
         data = json.load(json_file)
    self.start_urls = list(data.values())
  
  def already_visited(self, url):
    """
      Indicates if the specified url has already been visited.
    """
    return url in self.visited_urls

  def parse(self, response):
    """
      Parses page from specified response.
    """
    if (self.__is_section_page(response.url)):
      # Follow articles from section page
      for article_link in self.__get_articles_links(response):
        yield scrapy.Request(article_link, callback=self.parse)
    else:
      # Crawl current page
      item_parser = ItemParser()
      crawled_item = item_parser.parse_dcm_item(response)
      yield crawled_item

      # Follow next page
      next_page = self.__get_next_page(response)
      yield scrapy.Request(next_page, callback=self.parse)

      # Follow related pages
      for related_page in self.__get_related_pages(response):
        yield scrapy.Request(related_page, callback=self.parse)
    
    self.__finish_parse_and_save_file(response)
  
  def __finish_parse_and_save_file(self, response):
    """
      Finishes parse and saves HTML page.
    """
    self.visited_urls.append(response.url)
    page = response.url.split("/")[-2]
    filename = 'pages/dcm-%s.html' % page
    with open(filename, 'wb') as f:
      f.write(response.body)
    self.log('Saved file %s' % filename)
  
  def __is_section_page(self, url):
    """
      Indicates if the page from specified url is a section page
      (e.g., Política, Mídia, Cultura, etc.) not an article page.
    """
    return url in self.start_urls
  
  def __get_articles_links(self, response):
    """
      Considering that response is a section page, returns the
      links of articles listed in that section.
    """
    return response.css('h3.entry-title.td-module-title a::attr(href)').getall()
  
  def __get_next_page(self, response):
    """
      Returns the link from next page.
    """
    index_next_page = 1
    return response.css('.td-post-next-prev-content a::attr(href)')[index_next_page].get()

  def __get_related_pages(self, response):
    """
      Returns the links from related pages.
    """
    return response.css('.td-related-span4 .item-details a::attr(href)').getall()