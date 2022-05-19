# GenreMatch
## Jeremy Freedman, Reza Madhavan, Kunal Sheth

To run:
1. Build model and dataset by running thru all cells of `filtered.ipynb`
2. Run `python3 .` in the project root directory

Source files:
- `__main__.py`: entrypoint for GenreMatch frontend
- `main.ipynb`: notebook for feature extraction and model generation
- `utils/songlyrics.py`: songlyrics.com lyric scraper and data cleaner
- `utils/grab_lyrics.py`: simple script automating `songlyrics` module use
- `data/*`: lyrics CSV for training, words for frontend TF-IDF computations
- `model_*.pkl`: pickled (serialized) decision tree, KNN, and naive bayes 
classifiers
- `README.md`: this file
