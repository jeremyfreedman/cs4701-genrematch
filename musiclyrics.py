# MIT License

# Copyright (c) 2022 Jeremy Freedman

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from bs4 import BeautifulSoup
from collections import defaultdict
import requests
import json

agent = "Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) \
        Gecko/20100101 Firefox/24.0"
headers = {"User-Agent": agent}
base = "https://www.songlyrics.com/"


def lyrics(artist, path):
    """
    `artist` argument should be artist name (spaces OK, ideally dashes)
    `path` argument should be songlyrics track path (eg. /blinding-lights-lyrics)
    Returns: lyric text from songlyrics.com of requested song
    """
    url = base + artist.replace(" ", "-") + path
    request = requests.get(url, headers=headers)
    soup = BeautifulSoup(request.content, "html.parser")
    return soup.find("p", {"id": "songLyricsDiv"}).text


def words(lyrics):
    """
    `lyrics`: a string containing song lyrics (presumably separated by spaces
    and newlines)
    """
    return set(lyrics.split())


def lines(lyrics):
    """
    `lyrics`: a string containing song lyrics (presumably separated by spaces
    and newlines)
    """
    return set(lyrics.split("\n"))


def words_popularity(lyrics):
    """
    `lyrics`: a string containing song lyrics (presumably separated by spaces
    and newlines)
    """
    d = defaultdict(lambda: 0)
    for word in lyrics.split():
        d[word] += 1
    return dict(d)
