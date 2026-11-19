#!/usr/bin/python3
"""Prints the titles of the first 10 hot posts of a subreddit."""
import json
from urllib.error import HTTPError
from urllib.request import HTTPRedirectHandler, Request, build_opener


class NoRedirect(HTTPRedirectHandler):
    """Do not follow redirects."""
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def top_ten(subreddit):
    """Prints the first 10 hot post titles, None if invalid."""
    if not isinstance(subreddit, str) or not subreddit:
        print(None)
        return
    url = "https://www.reddit.com/r/{}/hot.json?limit=10".format(subreddit)
    req = Request(url, headers={"User-Agent": "alu-api:v1.0"})
    try:
        with build_opener(NoRedirect).open(req, timeout=10) as res:
            data = json.loads(res.read().decode("utf-8"))
        posts = data["data"]["children"]
    except (HTTPError, Exception):
        print(None)
        return
    for post in posts[:10]:
        print(post["data"]["title"])
