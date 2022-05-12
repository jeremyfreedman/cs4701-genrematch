import os
import pickle
import utils.songlyrics as sl
import sklearn as sk
from sklearn import tree
import sys
import collections

def parse_input(lyr):
    x=lyr.find('\n')
    song2 = sl._clean(lyrics[x+1:])
    new_song = ''
    for i in range(len(song2)):
        char = song2[i]
        if char == '\n':
            new_song += ' '
        elif char == '(' or char == ')':
            new_song += ''
        else:
            new_song += char
    new_song = new_song.encode('ascii','ignore').decode()
    song2 = new_song.split(' ')
    song2 = song2[:len(song2)-1]
    wordfreq = []
    x = dict(collections.Counter(song2))
    wordfreq.append(x)

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')

    models = [("Decision Tree Classifier", "model_dtc.pkl")]
    print("\n\n\n\n\nWelcome to GenreMatch!\nBy Jeremy Freedman, Reza Madhavan, and Kunal Sheth\n")
    print("Available models:")
    for i in range(len(models)):
        print(f"[{i+1}] {models[i][0]}")
    print("Please pick a model (specify the number): ", end="")
    mdl = int(input())-1
    print(f"You chose {models[mdl][0]}")
    with open(models[mdl][1], 'rb') as f:
        clf = pickle.load(f)
    print(f"Input song lyrics for genre prediction:")
    lyrics = input()
    print(clf.predict(parse_input(lyrics)))
