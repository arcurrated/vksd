from PyQt5 import QtWidgets
import pyqtdesigns.login_design as design

class LoginApp(QtWidgets.QMainWindow, design.Ui_LoginWindow):
	def __init__(self, login='', password=''):
		super().__init__()
		self.setupUi(self)
		self.vk_login.setText(login)
		self.vk_password.setText(password)
