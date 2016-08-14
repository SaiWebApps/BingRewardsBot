from PyQt5.QtWidgets import *

from bot.account_manager.credentials import sqliteprocessor

class BasicGUIElement:
	def __init__(self, name):
		self.name = name

	def show(self, layout):
		pass

class TextField(BasicGUIElement):
	def __init__(self, name, is_password_field = False, submit_on_enter = None):
		super().__init__(name)
		self.field_label = QLabel(name)
		self.field = QLineEdit()
		if is_password_field:
			self.field.setEchoMode(QLineEdit.Password)
		if submit_on_enter:
			self.field.returnPressed.connect(lambda: submit_on_enter())

	def show(self, layout):
		layout.addWidget(self.field_label)
		layout.addWidget(self.field)

	def clear(self):
		self.field.clear()

	def __str__(self):
		return self.field.text()

class SubmitButton(BasicGUIElement):
	def __init__(self, name, click_function):
		super().__init__(name)
		self.button = QPushButton(name)
		self.button.clicked.connect(lambda: click_function())

	def enable(self):
		self.button.setEnabled(True)

	def disable(self):
		self.button.setEnabled(False)

	def show(self, layout):
		layout.addWidget(self.button)

class ProgressBar(BasicGUIElement):
	def __init__(self, step_size):
		self.element = QProgressBar()
		self.current = 0
		self.step_size = step_size

	def increment(self):
		self.current += self.step_size
		self.element.setValue(self.current)

	def show(self, layout):
		layout.addWidget(self.element)

class SubmitForm:
	def __init__(self, layout, *args):
		self.layout = layout
		self.elements = {}
		for element in args:
			self.add_element(element)

	def get_element(self, name):
		return self.elements.get(name, None)

	def add_element(self, element):
		self.elements[element.name] = element
		element.show(self.layout)