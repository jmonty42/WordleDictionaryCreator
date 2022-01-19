# WordleDictionaryCreator
I recently discovered [Wordle](https://www.powerlanguage.co.uk/wordle/) and instantly wanted to write something to help me solve the daily puzzle. This repo is the first half of my solution.

## Brief description of Wordle

![⬛⬛🟨⬛⬛
⬛🟩⬛⬛⬛
⬛🟩🟨🟨⬛
🟩🟩🟩🟩🟩](https://i.imgur.com/G4viCsI.png "Wordle Screenshot")

Wordle is a word-guessing game. You are given 6 chances to guess the word of the day. Each time you make a guess, the letters in the word you guessed are colored either green, yellow, or grey. Green means that letter appears in that location in the answer. Yellow means that letter appears in a different location in the answer. Grey indicates that letter is not in the answer (unless it is a duplicated letter that appears less frequently in the answer).

## My solution

My approach to generating good guesses falls into two parts:

1. Generate a dictionary of 5-letter words that makes finding words that fit the given clues fast.
2. For each guess, filter out words in the dictionary that no longer fit the constraints of the given clues.

This repo tackles the first part of my approach.

## Constructing the dictionary

The dictionary is a [Python dictionary type](https://docs.python.org/3/tutorial/datastructures.html#dictionaries), which is a key, value map. The keys are 5-letter English words. My source for these words is [dwyl/english-words](https://github.com/dwyl/english-words/blob/master/words_alpha.txt) on GitHub (not included). The value for each entry is another dictionary type where the keys are the unique letters in the word and the values are sets of positions where those letters appear in that word. Each word in the dictionary is also doubly-linked to its neighboring words in a given word frequency list (keyed with "prev" and "first"). My source for word frequency comes from [en.lexipedia.org](https://en.lexipedia.org/).

As an example, this is the dictionary entry for the word "books" from my data set:
```
'books':
    'b': {0},
    'o': {1,2},
    'k': {3},
    's': {4},
    'prev': 'rugby',
    'next': 'roman'
```

There is also one special entry in this dictionary under the key of "FIRST_WORD" that represents the beginning of the word frequency list.

After this dictionary is generated, it is pickled to disk so that it doesn't have to be generated every time the solver (the second part of my solution listed above) runs.

## Solver

For the second part of my solution, see my [WordleSolver](https://github.com/jmonty42/WordleSolver) repo.