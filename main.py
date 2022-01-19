import pickle

DEFAULT_WORD_SOURCE_FILENAME = "words.txt"
DEFAULT_WORD_FREQUENCY_FILENAME = "word_frequencies.txt"
DEFAULT_DICTIONARY_OUTPUT_FILENAME = "dictionary.pickle"


def main():
    """Constructs a linked hash map (referred to as the dictionary). The keys are the words from the input word list.
    The value for each key is a character position map. The key is a unique letter in the word and the value is a set
    of indices where that letter appears in the word.

    example: "books":
        'b' -> {0}
        'o' -> {1,2}
        'k' -> {3}
        's' -> {4}

    Each word (starting with the word saved in the dictionary under the key "FIRST_WORD") links to its neighbors in the
    word frequency list with the keys in its character count map of "prev" and "next". So for the example of "books"
    above, the value of dictionary["books"] would end up being:

    'b' -> {0}
    'o' -> {1,2}
    'k' -> {3}
    's' -> {4}
    'prev' -> "rugby"
    'next' -> "roman"

    The result is pickled to disk at the specified file name.
    """
    dictionary = {}
    with open(DEFAULT_WORD_SOURCE_FILENAME, 'r') as source_file:
        source_lines = source_file.readlines()
    # construct the dictionary from the input file
    for line in source_lines:
        word = line.strip()
        # only add words with 5 letters
        if len(word) == 5:
            # positions map: letter -> {positions}
            char_count = {}
            for index in range(len(word)):
                if word[index] not in char_count:
                    char_count[word[index]] = set()
                char_count[word[index]].add(index)
            dictionary[word] = char_count
            # used for sorting by most common word
            dictionary[word]["prev"] = ''
            dictionary[word]["next"] = ''
    with open(DEFAULT_WORD_FREQUENCY_FILENAME, 'r') as frequencies_file:
        freq_lines = frequencies_file.readlines()
    prev_word = ''
    first_word = ''
    # find the most commonly used words according to the frequency file
    # frequency file is sorted by most common word first
    for line in freq_lines:
        # format is: word # # #...
        # (only care about the word)
        split_line = line.split()
        if len(split_line) > 0:
            word = split_line[0]
            if word in dictionary:
                if first_word == '':
                    first_word = word
                else:
                    dictionary[prev_word]["next"] = word
                    dictionary[word]["prev"] = prev_word
                prev_word = word
    # not every word in the dictionary is in the frequency file, so loop through the dictionary and add any unlinked
    # words in the order they're found
    for word in list(dictionary):
        if dictionary[word]["prev"] == '' and dictionary[word]["next"] == '':
            dictionary[prev_word]["next"] = word
            dictionary[word]["prev"] = prev_word
            prev_word = word
    dictionary["FIRST_WORD"] = first_word

    print(len(dictionary))
    with open(DEFAULT_DICTIONARY_OUTPUT_FILENAME, 'wb') as output:
        pickle.dump(dictionary, output, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    main()
