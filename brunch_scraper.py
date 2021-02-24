import time
from typing import List
from pytz import timezone
from datetime import datetime

import bs4
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


Tag = bs4.element.Tag


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
    for e in get_tags(category):
        publish_time = e.find('span', {'class': 'publish_time'}).text

        if not is_today(publish_time):
            break

        href = 'https://brunch.co.kr' + e['href']
        author = 'by ' + e.find_all('span', {'class': 'name_txt'})[-1].text
        title = e.find('strong').text
        content = e.find('span', {'class': 'article_content'}).text + ' ...'

        issue_body += '<h1>' + title + '</h1>' \
            '<a href="' + href + '">' + href + '</a><br><br>' + \
            content + \
            '<h3><p align="right">' + author + '</h3></p><br><br><br>'

    return issue_body


def get_tags(category: str) -> List[Tag]:
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

    url = 'https://brunch.co.kr/keyword/' + category + '?q=g'
    driver.get(url)
    elem = driver.find_element_by_tag_name('body')
    for i in range(5):
        elem.send_keys(Keys.END)
        time.sleep(1)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    a_tags = soup.body.find_all('a', {'class': 'link_post'})

    driver.quit()

    return a_tags


def is_today(publish_time: str) -> bool:
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
