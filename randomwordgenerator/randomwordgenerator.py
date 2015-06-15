import primary
import backup

def generate_random_words(n = 1):
	results = []
	try:
		results = primary.get_n_random_words(n)
	except:
		results = secondary.get_n_random_words()
	return results if not results or len(results) > 1 else results[0]