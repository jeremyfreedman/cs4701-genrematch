"""
GenreMatch entrypoint for frontend
"""

import ast
import math
import os
import pickle
import utils.songlyrics as sl
import numpy as np

# populate with (<model name>, <pickle filename>)
models = [("Decision Tree Classifier", "model_dtc.pkl"), ("Gaussian Naive Bayes", "model_nb.pkl"), ("K-Nearest Neighbors", "model_knn.pkl")]

def parse_input(lyr):
    song = sl._clean(lyr)
    song = song.encode("ascii", "ignore").decode()
    return list(filter(lambda x: x != "", song.split(" ")))


def run():
    print("Available models:")
    for i in range(len(models)):
        print(f"[{i+1}] {models[i][0]}")
    print("> Please pick a model (specify the number): ", end="")
    mdl = int(input()) - 1
    print(f"> You chose {models[mdl][0]}")
    with open(models[mdl][1], "rb") as f:
        clf = pickle.load(f)
    with open("data/words.txt") as f:
        word_appearance_cnt = f.readlines()
    word_appearance_cnt = ast.literal_eval(word_appearance_cnt[0])
    song_cnt = word_appearance_cnt["SONG_CNT"]
    del word_appearance_cnt["SONG_CNT"]
    words = word_appearance_cnt.keys()
    word_dict = {n: 0 for n in words}
    print(
        f"> Input song lyrics for genre prediction:\n>> Press CTRL+D or 3 newlines to end input!"
    )
    lyrics_arr = []
    try:  # run until CTRL+D pressed
        while True:
            lyrics_arr.append(input())
            if lyrics_arr[-3:] == ["", "", ""]:
                break
    except EOFError:
        pass
    lyrics = "\n".join(lyrics_arr)
    lyrics_parsed = parse_input(lyrics)
    for w in lyrics_parsed:
        if w in word_dict.keys():
            word_dict[w] += 1
    uniq_wordict = {}
    for w in words:  # tf-idf
        uniq_wordict[w] = word_dict[w] * math.log(song_cnt / word_appearance_cnt[w])
    print(
        f"> This sounds like \033[1m{clf.predict(np.array(list(uniq_wordict.values()) + [len(set(lyrics_parsed))]).reshape(1,-1))[0]}\033[0m!"
    )
    return (word_dict, uniq_wordict, len(set(lyrics_parsed)))


if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")

    print(
        "\n\n\n\n\nWelcome to GenreMatch!\nBy Jeremy Freedman, Reza Madhavan, and Kunal Sheth\n"
    )
    word_dict, uniq_wordict, cnt = run()
    while True:
        print("\n> What next?")
        print("[A]nother song\n[S]ee the data\n[E]xit\n> ", end="")
        cmd = input()
        if cmd.upper() == "A":
            word_dict, uniq_wordict, cnt = run()
        if cmd.upper() == "S":
            print(f"| Your song had \033[1m{cnt}\033[0m unique words.")
            print(f"| The top 10 signatures were:")
            print(
                f"|- {list(map(lambda x: x[0], sorted(uniq_wordict.items(), key=lambda x: x[1], reverse=True)[:10]))}"
            )
            print(f"| Their respective weights were:")
            print(
                f"|- {list(map(lambda x: round(x[1], 2), sorted(uniq_wordict.items(), key=lambda x: x[1], reverse=True)[:10]))}"
            )
        if cmd.upper() == "E" or cmd.upper() == "Q":
            print("Goodbye! :-)")
            exit(0)
