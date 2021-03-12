"""Brunch Scraper

Functions:
    get_title(category: str) -> str
    get_body(category: str) -> str

    _get_tags(category: str) -> List[Tag]
    _is_today(publish_time: str) -> bool

"""
import time
from typing import List
from urllib import parse
from pytz import timezone
from datetime import datetime

import bs4
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


Tag = bs4.element.Tag
URL_BASE = 'https://brunch.co.kr'


def get_title(category: str) -> str:
    """Create issue title.

    Args:
        category: str
            brunch category

    Returns:
        issue_title: str

    """
    issue_title = "[" + category + "] Today's brunch - " + \
        datetime.now(tz=timezone('Asia/Seoul')).strftime('%Y.%m.%d')

    return issue_title


def get_body(category: str) -> str:
    """Create issue body.

    include url, author, brunch title, content

    Args:
        category: str
            brunch category

    Returns:
        issue_body: str

    """
    issue_body = ''
    for e in _get_tags(category):
        publish_time = e.find('span', {'class': 'publish_time'}).text

        if not _is_today(publish_time):
            break

        href = URL_BASE + e['href']
        author = 'by ' + e.find_all('span', {'class': 'name_txt'})[-1].text
        title = e.find('strong').text
        content = e.find('span', {'class': 'article_content'}).text + ' ...'

        issue_body += '<h1>' + title + '</h1>' \
            '<a href="' + href + '">' + href + '</a><br><br>' + \
            content + \
            '<h3><p align="right">' + author + '</h3></p><br><br><br>'

    return issue_body


def _get_tags(category: str) -> List[Tag]:
    """Get 'a' tags

    scrolling & get page_source

    Args:
        category: str
            brunch category

    Returns:
        a_tags: bs4.element.ResultSet

    """
    # headless option
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')

    # chromedriver는 Github Actions에서 설치하게 했기때문에 경로가 이러하다.
    driver = webdriver.Chrome('chromedriver', options=options)
    driver.implicitly_wait(5)

    driver.get(URL_BASE)

    elems = driver.find_elements_by_class_name(
        'keyword_item.brunch_keyword_item'
        )
    for elem in elems:
        href_attr = elem.get_attribute('href')
        href_attr = href_attr.replace(URL_BASE + '/keyword/', '') \
                             .replace('?q=g', '')
        if href_attr == parse.quote(category):
            target = elem
            target.click()
            break

    driver.close()  # 첫번째 탭 닫기
    last_tab = driver.window_handles[-1]
    driver.switch_to.window(window_name=last_tab)

    elem = driver.find_element_by_tag_name('body')
    for i in range(5):
        elem.send_keys(Keys.END)
        time.sleep(1)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    a_tags = soup.body.find_all('a', {'class': 'link_post'})

    driver.quit()

    return a_tags


def _is_today(publish_time: str) -> bool:
    """Check today

    Args:
        publish_time: str
            publish time

    Returns:
        : bool

    """
    # 'n시간전' or 'n분전'
    if len(publish_time) < 6:
        return True

    today = datetime.now(tz=timezone('Asia/Seoul')).strftime('%d')
    pub = datetime.strptime(publish_time, '%b %d. %Y').strftime('%d')

    return today == pub
