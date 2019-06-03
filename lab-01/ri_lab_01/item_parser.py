# -*- coding: utf-8 -*-

import scrapy
from datetime import datetime

"""
  Parser for items of responses.
"""
class ItemParser():

  def parse_dcm_item(self, response):
    """
      Parses and return a DiarioDoCentroDoMundoItem from specified response.
    """
    return {
      'title' : self.__get_article_title(response),
      'sub_title' : self.__get_article_subtitle(response),
      'author' : self.__get_article_author(response),
      'date' : self.__get_article_publish_date(response),
      'section' : self.__get_article_section(response),
      'text' : self.__get_article_text(response),
      'url' : self.__get_article_url(response)
    }
    
  def __get_article_title(self, response):
    """
        Gets article's title.
    """
    return response.css('h1.entry-title::text').get()

  def __get_article_subtitle(self, response):
    """
        Gets article's subtitle.
    """
    return ""

  def __get_article_author(self, response):
    """
        Gets article's author.
    """
    author_separator = ". Por "
    article_title = self.__get_article_title(response)
    author = article_title.split(author_separator)[-1]
    return author if (author != article_title) else response.css('div.td-post-author-name a::text').get()

  def __get_article_publish_date(self, response):
    """
        Gets article's publish date.
    """
    index_timezone = 19
    non_formatted_str_date = response.css('time::attr(datetime)').get()
    non_formatted_str_date = non_formatted_str_date[:index_timezone]
    formatted_date = datetime.strptime(non_formatted_str_date, '%Y-%m-%dT%H:%M:%S')
    return formatted_date.strftime('%d/%m/%Y %H:%M:%S')

  def __get_article_section(self, response):
    """
        Gets article's section.
    """
    return ""

  def __get_article_text(self, response):
    """
        Gets article's text.
    """
    return "".join(response.css('article p::text').getall())

  def __get_article_url(self, response):
    """
        Gets article's page url.
    """
    return response.request.url