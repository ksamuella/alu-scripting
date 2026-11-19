#!/usr/bin/python3
"""Recursively returns the titles of all hot posts of a subreddit."""
import json
from urllib.error import HTTPError
from urllib.request import HTTPRedirectHandler, Request, build_opener


class NoRedirect(HTTPRedirectHandler):
    """Do not follow redirects."""
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def recurse(subreddit, hot_list=None, after=None):
    """Returns a list of all hot post titles, None if invalid."""
    if hot_list is None:
        hot_list = []
    if not isinstance(subreddit, str) or not subreddit:
        return None
    url = "https://www.reddit.com/r/{}/hot.json?limit=100".format(subreddit)
    if after:
        url += "&after={}".format(after)
    req = Request(url, headers={"User-Agent": "alu-api:v1.0"})
    try:
        with build_opener(NoRedirect).open(req, timeout=10) as res:
            data = json.loads(res.read().decode("utf-8"))["data"]
        children = data["children"]
    except (HTTPError, Exception):
        return hot_list if hot_list else None
    for child in children:
        hot_list.append(child["data"]["title"])
    after = data.get("after")
    if after:
        return recurse(subreddit, hot_list, after)
    return hot_list if hot_list else None
