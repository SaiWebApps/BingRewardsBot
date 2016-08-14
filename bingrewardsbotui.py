import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, pyqtSignal

from bot.botconfig import PhantomJSBotConfig
from bot.manager import BingRewardsBotManager
from baseui import ProgressBar, SubmitButton
from credentialsui import CredentialsUI

class BotProgressMonitor(QThread):
	update_progress = pyqtSignal(int)

	def __init__(self, bot_mgr):
		super().__init__()
		self.bot_mgr = bot_mgr

	def run(self):
		last_observed_progress = 0
		while last_observed_progress < 100:
			current_progress = self.bot_mgr.get_percent_completed()
			if last_observed_progress != current_progress:
				self.update_progress.emit(current_progress)
				last_observed_progress = current_progress

class BingRewardsBotWidget(QWidget):
	def __init__(self, db_filename):
		super().__init__()
		self.init_ui(db_filename)

	def update_progress_bar(self, value):
		self.progress_bar.setValue(value)
		if value == 100:
			self.run_bot_button.enable()
			self.progress_bar.deleteLater()

	def run_bot(self):
		# Add progress bar to the layout.
		self.progress_bar = QProgressBar()
		self.layout.addWidget(self.progress_bar)

		# Run BingRewardsBotManager.
		creds = self.credentials_ui.get_credentials_collection()
		mgr = BingRewardsBotManager(PhantomJSBotConfig(30), creds, PhantomJSBotConfig(20), creds)
		mgr.run()

		# Monitor the BingRewardsBotManager's progress, and update the progress bar accordingly.
		self.progress_monitor = BotProgressMonitor(mgr)
		self.progress_monitor.update_progress.connect(self.update_progress_bar)
		self.progress_monitor.start()

		self.run_bot_button.disable()

	def init_ui(self, db_filename):
		self.setWindowTitle('Bing Rewards Bot')
		
		self.layout = QVBoxLayout()
		self.credentials_ui = CredentialsUI(db_filename)
		self.layout.addLayout(self.credentials_ui.layout)

		self.run_bot_button = SubmitButton('Run Bing Rewards Bot', self.run_bot)
		self.run_bot_button.show(self.layout)

		self.setLayout(self.layout)