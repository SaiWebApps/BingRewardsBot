import random

def get_random_word(min_word_len = 2, max_word_len = 10):
	'''
		@param min_word_len 
			- Minimum number of characters that must be in random word
			- Must be non-negative
		@param max_word_len 
			- Maximum number of characters that can be in random word
			- Must be non-negative
		@return 
			- a random word that at least @min_word_len and at most @max_word_len
			characters.
			- None if @min_word_len and/or @max_word_len are negative OR if
			@min_word_len > @max_word_len
	'''
	# Word length can be between min_word_len and max_word_len inclusive.
	if min_word_len < 0 or max_word_len < 0 or max_word_len < min_word_len:
		return None
	word_len = random.randrange(min_word_len, max_word_len + 1)
	return ''.join([chr(random.randint(0, 255)) for i in range(0, word_len)]).decode('utf-8')

def get_n_random_words(n):
	'''
		@return
			- a list with the results of running get_random_word above @n times
			- None if n is negative
	'''
	return [get_random_word() for i in range(0, n)] if n >= 0 else None