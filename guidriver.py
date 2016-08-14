from argparse import ArgumentParser

from ui.bingrewardsbotui import BingRewardsBotApp

def main():
	parser = ArgumentParser('Accumulate daily Bing Rewards desktop and mobile points.')
	parser.add_argument('-f', '--db_filename', required = True, \
		help = 'Name of the SQLite database file (*.db) with the target Bing Rewards ' + \
			   'accounts\' credentials; if the provided filename does not exist, then ' + \
               'it shall be created.')

	app = BingRewardsBotApp()
	app.run(parser.parse_args().db_filename)

if __name__ == '__main__':
	main()