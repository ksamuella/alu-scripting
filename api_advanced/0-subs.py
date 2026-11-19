#!/usr/bin/python3
"""Queries the Reddit API and returns the number of subscribers."""
import json
from urllib.error import HTTPError
from urllib.request import HTTPRedirectHandler, Request, build_opener


class NoRedirect(HTTPRedirectHandler):
    """Do not follow redirects."""
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def number_of_subscribers(subreddit):
    """Returns total subscribers of a subreddit, 0 if invalid."""
    if not isinstance(subreddit, str) or not subreddit:
        return 0
    url = "https://www.reddit.com/r/{}/about.json".format(subreddit)
    req = Request(url, headers={"User-Agent": "alu-api:v1.0"})
    try:
        with build_opener(NoRedirect).open(req, timeout=10) as res:
            data = json.loads(res.read().decode("utf-8"))
        return data["data"]["subscribers"]
    except (HTTPError, Exception):
        return 0
