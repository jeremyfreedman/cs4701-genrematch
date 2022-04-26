# MIT License

# Copyright (c) 2017 Adam Horrigan with modifications by Jeremy Freedman, 2022

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
import requests
import json

agent = "Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) \
        Gecko/20100101 Firefox/24.0"
headers = {"User-Agent": agent}
base = "https://www.azlyrics.com/"


def artists(letter):
    if letter.isalpha() and len(letter) == 1:
        letter = letter.lower()
        url = base + letter + ".html"
        req = requests.get(url, headers=headers)
        soup = BeautifulSoup(req.content, "html.parser")
        data = []

        for div in soup.find_all("div", {"class": "container main-page"}):
            links = div.findAll("a")
            for a in links:
                data.append(a.text.strip())
        return json.dumps(data)
    else:
        raise Exception("Unexpected Input")


def songs_filter(songs):
    return list(
        set(
            filter(
                lambda s: s.lower().count("remix") == 0
                and s.lower().count("demo") == 0,
                songs,
            )
        )
    )


def songs(artist):
    artist = artist.lower().replace(" ", "")
    first_char = artist[0]
    if first_char.isnumeric():
        first_char = "19"
    url = base + first_char + "/" + artist + ".html"
    req = requests.get(url, headers=headers)

    res = []

    soup = BeautifulSoup(req.content, "html.parser")

    all_albums = soup.find("div", id="listAlbum")
    first_album = all_albums.find("div", class_="album")
    for tag in first_album.find_next_siblings(["a", "div"]):
        if tag.name == "div":
            songs = tag.find_next("div", class_="listalbum-item")
            if songs is not None:
                for d in songs:
                    res.append(d.text)
    return songs_filter(res)


def lyrics(artist, song):
    artist = artist.lower().replace(" ", "")
    song = song.lower().replace(" ", "")
    url = base + "lyrics/" + artist + "/" + song + ".html"

    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.content, "html.parser")
    l = soup.find_all("div", attrs={"class": None, "id": None})
    if not l:
        return {"Error": "Unable to find " + song + " by " + artist}
    elif l:
        l = [x.getText() for x in l]
        return l
