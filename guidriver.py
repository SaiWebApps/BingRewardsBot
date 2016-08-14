from argparse import ArgumentParser
import sys

from PyQt5.QtWidgets import *
from bingrewardsbotui import BingRewardsBotWidget

def main():
	parser = ArgumentParser('Accumulate daily Bing Rewards desktop and mobile points.')
	parser.add_argument('-f', '--filename', required = True, \
		help = 'Name of the SQLite database file (*.db) with the target Bing Rewards ' + \
			   'accounts\' credentials; if the provided filename does not exist, then ' + \
               'it shall be created.')

	app = QApplication(sys.argv)
	bing_bot_widget = BingRewardsBotWidget(parser.parse_args().filename)
	bing_bot_widget.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()