import random

class InvalidWordLengthBoundsError(Exception):
    def __init__(self):
        super().__init__('Please specify valid word length bounds.')

def get_random_word(min_word_len, max_word_len):
    '''
        @param min_word_len 
            - Minimum number of characters that must be in random word
            - Must be non-negative
        
        @param max_word_len 
            - Maximum number of characters that can be in random word
            - Must be non-negative

        @return 
            - A random word whose length is >= @min_word_len and <= @max_word_len characters.
            - If any of the inputs are invalid, then raise an InvalidWordLengthBoundsError.
    '''
    # Word length can be between min_word_len and max_word_len inclusive.
    if not min_word_len or not max_word_len or min_word_len < 0 or max_word_len < 0 or max_word_len < min_word_len:
        raise InvalidWordLengthBoundsError
    word_len = random.randint(min_word_len, max_word_len)
    return ''.join([chr(random.randint(0, 255)) for i in range(0, word_len)])

def get_n_random_words(n, word_len_bounds = (2, 10)):
    '''
        @param n
        (Required)
        Number of random words to generate

        @param word_len_bounds
        (Optional)
        Tuple containing the bounds for the word length of each randomly generated word;
        item 0 = minimum word length (2 by default), item 1 = maximum word length (10 by default)

        @return
            - A list with @n random words, where word_len_bounds[0] <= len(each word) <= word_len_bounds[1]
            - An InvalidWordLengthBoundsError if word_len_bounds is an invalid tuple (length < 2)
    '''
    if len(word_len_bounds) < 2 or n < 0:
        raise InvalidWordLengthBoundsError
    min_word_len = word_len_bounds[0]
    max_word_len = word_len_bounds[1]
    return [get_random_word(min_word_len, max_word_len) for i in range(0, n)]