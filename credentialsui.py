from PyQt5.QtWidgets import *

from bot.account_manager.credentials import sqliteprocessor
from baseui import *

class CredentialsListView(BasicGUIElement):
	def __init__(self, name):
		super().__init__(name)
		self.label = QLabel(name)
		self.credentials_list = QListWidget()
		for credentials in self.get_all().to_std_structure():
			self.add(credentials['email'])

	def get_all(self):
		return sqliteprocessor.process_credentials(CREDENTIALS_DB)

	def add(self, email):
		self.credentials_list.addItem(QListWidgetItem(email))

	def show(self, layout):
		layout.addWidget(self.label)
		layout.addWidget(self.credentials_list)

class AddCredentialsForm(SubmitForm):
	def __init__(self):
		super().__init__(QVBoxLayout(), TextField('Email Address'), \
			TextField('Password', True, self.process_credentials), \
			SubmitButton('Add Credentials', self.process_credentials))

	def add_credentials(self, email, password):
		sqliteprocessor.save_credentials(CREDENTIALS_DB, email, password)

	def process_credentials(self):
		email_field = self.get_element('Email Address')
		password_field = self.get_element('Password')

		email = str(email_field).strip()
		password = str(password_field).strip()
		if email and password:
			self.add_credentials(email, password)

		email_field.clear()
		password_field.clear()

class CredentialsUI(AddCredentialsForm):
	def __init__(self):
		super().__init__()

		all_creds = CredentialsListView('Emails Registered with Bot')
		self.elements[all_creds.name] = all_creds

		overall_layout = QHBoxLayout()
		overall_layout.addLayout(self.layout)
		overall_layout.addWidget(all_creds.credentials_list)
		self.layout = overall_layout

	def get_credentials_list_element(self):
		return self.elements['Emails Registered with Bot']

	def get_credentials_collection(self):
		return self.get_credentials_list_element().get_all()

	def add_credentials(self, email, password):
		super().add_credentials(email, password)
		self.get_credentials_list_element().add(email)
