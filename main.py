"""main

1. scrape today's brunch using brunch_scraper module
2. post on github issue

Functions:
    _run(category: str = 'IT_트렌드')

"""

import os
import sys

from github import Github

from brunch_scraper import get_title, get_body


def _run(category: str = 'IT_트렌드'):
    """Post github issue

    Args:
        category: str = 'IT_트렌드'
            brunch category

    """
    try:
        GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
        REPO_NAME = 'todays-brunch'
        CATEGORY = category
        issue_title = get_title(CATEGORY)
        issue_body = get_body(CATEGORY)

        if issue_body == '':
            print('There is no updated brunch.')
            sys.exit()

        repo = Github(GITHUB_TOKEN).get_user().get_repo(REPO_NAME)
        res = repo.create_issue(title=issue_title, body=issue_body)
        print('Success!')
        print(res)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        for i in range(1, len(sys.argv)):
            _run(sys.argv[i])
    else:
        _run()
