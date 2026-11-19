#!/usr/bin/python3
"""Recursively counts keywords in the hot post titles of a subreddit."""
import json
from urllib.error import HTTPError
from urllib.request import HTTPRedirectHandler, Request, build_opener


class NoRedirect(HTTPRedirectHandler):
    """Do not follow redirects."""
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def count_words(subreddit, word_list, after=None, counts=None):
    """Prints a sorted count of keywords found in hot post titles."""
    if counts is None:
        counts = {}
    if not isinstance(subreddit, str) or not subreddit or not word_list:
        return
    words = [w.lower() for w in word_list]
    url = "https://www.reddit.com/r/{}/hot.json?limit=100".format(subreddit)
    if after:
        url += "&after={}".format(after)
    req = Request(url, headers={"User-Agent": "alu-api:v1.0"})
    data = None
    try:
        with build_opener(NoRedirect).open(req, timeout=10) as res:
            data = json.loads(res.read().decode("utf-8"))["data"]
        children = data["children"]
    except (HTTPError, Exception):
        children = None
    if children is not None:
        for child in children:
            for token in child["data"]["title"].lower().split():
                if token in words:
                    counts[token] = counts.get(token, 0) + 1
        after = data.get("after")
        if after:
            return count_words(subreddit, word_list, after, counts)
    if not counts:
        return
    totals = {}
    for word, number in counts.items():
        totals[word] = number * words.count(word)
    for word, number in sorted(totals.items(), key=lambda x: (-x[1], x[0])):
        print("{}: {}".format(word, number))
