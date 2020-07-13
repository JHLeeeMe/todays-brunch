import os
import sys
from github import Github
from brunch_scraper import get_title, get_body


def run(category: str):
    """Post github issue

    Keyword arguments:
        category: str -- brunch category
    Return:
        Unit
    """
    try:
        GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
        REPO_NAME = 'todays-brunch'
        CATEGORY = 'IT_트렌드'
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
    run(sys.argv[1])
