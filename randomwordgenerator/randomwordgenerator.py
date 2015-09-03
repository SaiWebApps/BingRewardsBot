import primary
import backup

def generate_random_words(n = 1):
	'''
		@param n
			(Optional; default value = 1) Number of random words to generate;
			should be >= 0

		@return
			a list with n randomly generated strings, for n >= 0
	'''
	results = []
	try:
		# Primary generation method - Load dictionary from website, and select
		# n random words from that collection.
		results = primary.get_n_random_words(n)
	except:
		# If unable to read website, then generate n random strings.
		results = backup.get_n_random_words(n)
	return results if not results or len(results) > 1 else results[0]