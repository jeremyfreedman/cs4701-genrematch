"""
GenreMatch entrypoint for frontend
"""

import ast
import os
import pickle
import utils.songlyrics as sl
import numpy as np

def parse_input(lyr):
    x=lyr.find('\n')
    song = sl._clean(lyrics[x+1:])
    song = song.encode('ascii','ignore').decode()
    return list(filter(lambda x: x != '', song.split(' ')))

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
    with open("data/words.txt") as f:
        words = f.readlines()
    words = ast.literal_eval(words[0])
    word_dict = {n : 0 for n in words}
    print(f"Input song lyrics for genre prediction:")
    lyrics = input()
    for w in parse_input(lyrics):
        if w in word_dict.keys():
            word_dict[w] += 1
    print(clf.predict(np.array(list(word_dict.values()) + [0]).reshape(1,-1))[0])
