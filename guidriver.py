import sys

from PyQt5.QtWidgets import *
from bingrewardsbotui import BingRewardsBotWidget

def main():
	app = QApplication(sys.argv)
	bing_bot_widget = BingRewardsBotWidget()
	bing_bot_widget.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()