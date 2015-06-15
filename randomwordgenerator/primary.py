import random
import requests

_URL = 'http://svnweb.freebsd.org/csrg/share/dict/words?view=co'

##### BEGIN Word Filtering Auxiliary Functions (Helpers) #####

def _does_word_begin_with_prefix(word, prefix):
	'''
		@return 
			- true if @word begins with @prefix, false otherwise
			- true if @suffix is None
	'''
	return word.startswith(prefix) if prefix else True

def _does_word_end_with_suffix(word, suffix):
	'''
		@return 
			- true if @word ends with @suffix, false otherwise
			- true if @suffix is None
	'''
	return word.endswith(suffix) if suffix else True

def _does_word_contain_substring(word, substr):
	'''
		@return 
			- true if @word contains @substr, false otherwise
			- true if @substr is None
	'''
	return substr in word if substr else True

def _does_word_meet_all_conditions(word, prefix, suffix, substr):
	'''
		@return 
			- true if @word starts with @prefix, @word ends with @suffix, and
			@word contains @substr, false otherwise
			- true if @prefix, @suffix, and @substr are all None (unspecified)
	'''
	return _does_word_begin_with_prefix(word, prefix) and \
			_does_word_end_with_suffix(word, suffix) and \
			_does_word_contain_substring(word, substr)

##### END Word Filtering Auxiliary Functions (Helpers) #####

##### BEGIN Random Word Retrieval + Generation Functions #####

def get_words(prefix, suffix, substr):
	'''
		@return a list of unique words from _URL that meet the specified criteria
	'''
	all_words = requests.get(_URL, stream = True)
	return [word.decode('utf-8') for word in all_words.iter_lines() if _does_word_meet_all_conditions(word, prefix, suffix, substr)]

def _get_random_word(pool):
	'''
		@param pool - a list/pool of words
		@return a randomly-selected word from @pool
	'''
	word = random.choice(pool)
	pool.remove(word)
	return word

def get_n_random_words(num_random_words, prefix = None, suffix = None, substr = None):
	'''
		@param prefix
			- A character or phrase that all target words must start with
		@param suffix
			- A character or phrase that all target words must end with
		@param substr
			- A character or phrase that all target words must contain
		@param num_random_words
			- The number of random words to generate
			- Must be nonnegative
		@return 
			- a list of @num_random_words unique words from _URL that 
			meet the specified criteria
			- all words meeting the specified criteria if @num_random_words 
			exceeds the number of matching words
			- None if @num_random_words is < 0, [] if @num_random_words is 0
	'''
	if num_random_words < 0:
		return None

	filtered_words = get_words(prefix, suffix, substr)
	if num_random_words >= len(filtered_words):
		return filtered_words
	# Select @num_random_words words randomly from the list of words that match
	# the specified criteria (a.k.a, @filtered_words).
	return [_get_random_word(filtered_words) for i in range(0, num_random_words)]

##### END Random Word Retrieval + Generation Functions #####
