import songlyrics as sl
import pandas as pd

pop = ['One Direction', 'Ariana Grande', 'Justin Bieber', 'Miley Cyrus', 'Justin Timberlake', 'Katy Perry', 'Black Eyed Peas', 'Demi Lovato', 'Meghan Trainor', 'Kesha', 
       'Lady Gaga', 'Shawn Mendes', 'Sam Smith', 'Camilla Cabello', 'Chainsmokers', 'Jason Derulo', 'Calvin Harris', 'Pink', '5 Seconds of Summer', 'The Weeknd', 
       'Harry Styles', 'Jennifer Lopez', 'Charlie Puth', 'Michael Jackson', 'Prince']
rap_hiphop = ['Fetty Wap', 'Migos', '21 Savage', '88GLAM', 'Roddy Rich', 'Lil Baby', 'Eminem', 'Snoop Dogg', 'Drake','Kanye West', 'Travis Scott', 'Dr Dre','Lil Wayne' ,
       '50 Cent' ,'Jay-Z', 'Kendrick Lamar' ,'J Cole' ,'Nas' ,'Kid Cudi' ,'Cardi B', 'Nicki Minaj', 'A$AP Rocky' ,'Pop Smoke', 'Meek Mill', 'Young Thug']
country = ['Tim McGraw', 'Blake Shelton', 'George Strait', 'Garth Brooks', 'Luke Bryan', 'Luke Combs', 'Kenny Chesney', 'Keith Urban', 'Johnny Cash', 'Carrie Underwood', 
           'Brad Paisley', 'Merie Haggard', 'Jason Aldean', 'Dierks Bentley', 'Alan Jackson', 'Chris Stapleton', 'Kenny Rogers', 'Toby Keith', 'Darius Rucker', 'George Jones', 
           'Willie Nelson', 'Miranda Lambert', 'Chris Young', 'Randy Travis', 'Thomas Rhett']
soul_rb = ['Stevie Wonder', 'Ray Charles', 'John Legend', 'Ne-Yo', 'Alicia Keys', 'Mariah Carey', 'Miguel', 'Bob Marley', 'Giveon', 'Otis Redding', 'Aretha Franklin', 
               'Marvin Gaye', 'Al Green', 'Sam Cooke', 'Sza', 'Teddy Pendergrass', 'Commodores', 'Leon Bridges']
alternative = ['Nirvana', 'The Script', 'OneRepublic', 'Imagine Dragons', 'Coldplay', 'U2', 'Train', 'Weezer', 'Fall Out Boy', 'Paramore', 'Maroon 5', 'Arctic Monkeys', 
               'Snow Patrol', 'Walk The Moon', 'Radiohead', 'Green Day', 'Cage The Elephant', 'The Strokes', 'The All-American Rejects', 'The Chemical Brothers', 
               'Blink-182', 'Incubus', 'Simple Plan']
rock = ['Queen', 'Led Zeppelin', 'Rolling Stones', 'ACDC', 'Guns N Roses', 'Red Hot Chili Peppers', 'The Eagles', 'Fleetwood Mac', 'The Doors', 'Pink Smith', 
        'Aerosmith', 'Stevie Nicks', 'Journey', 'The Police', 'The Kings', 'The Who', 'Van Halen', 'Bob Dylan', 'The Beatles', 'Linkin Park', 'Nickelback', 'Tame Impala', 
        'Foo Fighters', 'Bon Jovi', 'Leonard Cohen']
metal = ['Metallica', 'Black Sabbath', 'Judas Preist', 'Slayer', 'Death', 'Tool', 'Korn', 'Dream Theater', 'Slipknot', 'Pantera', 'Iron Maiden', 'Avenged Sevenfold', 
         'Alice in Chains', 'Anthrax', 'Rage Against the Machine', 'Mastodon', 'Five Finger Death Punch', 'Rammstein', 'System of a Down', 'Machine Head', 
         'Mercyful Fate', 'Manowar', 'Nightwish', 'Deep Purple', 'Def Leppard']

genre_artists = {'pop':pop, 'rap_hiphop':rap_hiphop, 'country':country, 'soul_rb':soul_rb, 'alternative':alternative, 'rock':rock, 'metal':metal}

df = pd.DataFrame(columns = ['Artist','Genre','Lyrics'])

print(f"[grab_lyrics] begin scrape")
print(f"[grab_lyrics] total artists: {sum([len(a) for a in genre_artists.values()])}")

for genre in genre_artists:
    print(f"[Genre] beginning {genre}")
    for artist in genre_artists[genre]:
        print(f"[Artist] beginning {artist}")
        songs = sl.artist(artist=artist, cnt=25)['tracks']
        lyrics = ""
        for song in songs:
            print(f"[Song] scraping {song}")
            try:
                lyrics += (sl.lyrics(url=song) + '\n')
            except:
                print(f"\t[Song] error encountered! Skipping")
                pass
        df = df.append({'Artist':artist, 'Genre':genre, 'Lyrics':lyrics}, ignore_index=True)
        print(f"[Artist] concluding {artist}")
    print(f"[Genre] concluding {genre}")


df.to_csv('all_sl.csv')
        
