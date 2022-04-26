import lyricsgenius as lg


file = open("lyrics.txt", "w")

genius = lg.Genius('Kazu51bV8gbOwO6RQpZA-ZQ-4iOWbGdiQADlWk6SRO6DGtoezXzRL6Qapzdpu-VJ', skip_non_songs=True, 
excluded_terms=["(Remix)", "(Live)"], remove_section_headers=True)

artists = ['Drake', 'Ed Sheeran', 'John Mayer', 'Kanye West','Eminem', 'Khalid', 'OneRepublic','Steve Aoki','Avicii']


def get_lyrics(arr, k):  # Write lyrics of k songs by each artist in arr
  c = 0  # Counter
  err = 0
  for name in arr:
    while True:
      try:
        songs = (genius.search_artist(name, max_songs=k, sort='popularity')).songs
        s = [song.lyrics for song in songs]
        file.write("\n \n   <|endoftext|>   \n \n".join(s))  # Deliminator
        c += 1
        print(f"Songs grabbed:{len(s)}")
        break
      except:
        err += 1
        print(err)
        pass
    # except:  #  Broad catch which will give us the name of artist and song that threw the exception
        # print(f"some exception at {name}: {c}")


get_lyrics(artists, 5)