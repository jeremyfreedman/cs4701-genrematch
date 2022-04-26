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
import string
import json

agent = "Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) \
        Gecko/20100101 Firefox/24.0"
headers = {"User-Agent": agent}
base = "https://www.songlyrics.com/"


def _clean(lyrics):
    """
    `lyrics`: a string containing song lyrics (presumably separated by spaces
    and newlines)
    Returns: provided lyrics shifted to lowercase with punctuation and CRLF
    removed
    """
    return (
        lyrics.translate(str.maketrans("", "", string.punctuation))
        .lower()
        .replace("\r", "")
    )


def artist(artist=None, cnt=None, url=None):
    """
    `artist` argument should be artist name (spaces or dashes separation OK)
    `url`, if provided, will ignore artist and path and query URL directly
    Returns: JSON-style dict containing genre and song URLs
    This function grabs every song under the artist's profile, so there will
    be lots of "duplicates" (live recordings, remasters, etc). Specify an
    album with `album()` below to get more concise results.
    Genre may be None if SongLyrics doesn't report one.
    """
    if url is None:
        url = base + artist.replace(" ", "-").lower() + "-lyrics"
    ret = {}
    request = requests.get(url, headers=headers)
    soup = BeautifulSoup(request.content, "html.parser")
    genre = soup.find("div", class_="pagetitle")
    if genre is not None and genre.p is not None:
        genre = genre.p.a.text
    tags = soup.find("table", class_="tracklist").find_all(href=True)
    ret["artist"] = artist
    ret["genre"] = genre
    ret["tracks"] = [a["href"] for a in tags]
    if cnt is not None:
        ret["tracks"] = ret["tracks"][:cnt]
    return ret


def album(artist=None, album=None, url=None):
    """
    `artist` argument should be artist name (spaces or dashes separation OK)
    `album` argument should be album name (spaces or dashes separation OK)
    `url`, if provided, will ignore artist and path and query URL directly
    Returns: set of songlyrics.com track URLs from requested album
    """
    if url is None:
        url = base + artist.replace(" ", "-").lower() + "/" + album.replace(" ", "-")
    request = requests.get(url, headers=headers)
    soup = BeautifulSoup(request.content, "html.parser")
    tags = soup.find("table", class_="tracklist").find_all(href=True)
    return {a["href"] for a in tags}


def lyrics(artist=None, title=None, url=None):
    """
    `artist` argument should be artist name (spaces or dashes separation OK)
    `title` argument should be track title (spaces or dashes separation OK)
    `url`, if provided, will ignore artist and title and query URL directly
    Returns: lyric text from songlyrics.com of requested song
    """
    if url is None:
        url = (
            base
            + artist.replace(" ", "-").lower()
            + "/"
            + title.replace(" ", "-").lower()
            + "-lyrics"
        )
    request = requests.get(url, headers=headers)
    soup = BeautifulSoup(request.content, "html.parser")
    return soup.find("p", {"id": "songLyricsDiv"}).text


def words(lyrics, stopwords):
    """
    `lyrics`: a string containing song lyrics (presumably separated by spaces
    and newlines)
    `stopwords`: a list of stopwords to skip
    Returns: original lyrics cleaned (see `_clean()`), split by space/newline,
    moved into a set (such that each word occurs only once)
    """
    return list(filter(lambda word:\
                       word not in stopwords, set(_clean(lyrics).split())))


def lines(lyrics):
    """
    `lyrics`: a string containing song lyrics (presumably separated by spaces
    and newlines)
    Returns: unique, cleaned lines from provided lyrics
    """
    return set(_clean(lyrics).split("\n"))


def words_freq(lyrics, stopwords):
    """
    `lyrics`: a string containing song lyrics (presumably separated by spaces
    and newlines)
    `stopwords`: a list of stopwords to skip
    Returns: a dictionary mapping the frequency of each word's occurrence in
    the cleaned lyrics
    """
    d = defaultdict(lambda: 0)
    for word in _clean(lyrics).split():
        if word not in stopwords:
            d[word] += 1
    return dict(d)
