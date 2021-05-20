import sys
from PyQt5 import QtWidgets
from vksdApp import VKsdApp
from loginApp import LoginApp
from triggerDialog import TriggerDialog
import vk_api
import time

TRIGGERS_FILENAME = 'triggers.txt'
VK_LOGIN_DATA_FILENAME = 'vk_login_data.txt'

try:
	triggers = open(TRIGGERS_FILENAME, 'r').read()
except:
	triggers = ''

try:
	vk_login_data = open(VK_LOGIN_DATA_FILENAME, 'r').read().split('\n')[0].split(':')
except:
	vk_login_data = ['', '']

vk_login, vk_password = vk_login_data

def handle_captcha(captcha):
	url = captcha.get_url()
	text, ok = QtWidgets.QInputDialog.getText(self, 'CAPTCHA', 'Перейдите по ссылке и введите код капчи {}:'.format(url))
	if ok:
		captcha.try_again(text)
			
		
if __name__ == '__main__':
	vk = None
	def log_in_vk():
		login = login_window.vk_login.text()
		if login == '':
			login_window.outputText.setPlainText('empty login')
			return
		password = login_window.vk_password.text()
		if password == '':
			login_window.outputText.setPlainText('empty password')
			return
		sess = vk_api.VkApi(login, password, captcha_handler=handle_captcha)
		try:
			sess.auth()
			vk = sess.get_api()
			main_window.vk = vk
			main_window.show()
			login_window.close()
			open(VK_LOGIN_DATA_FILENAME, 'w').write('{}:{}'.format(login, password))
		except Exception as e:
			print(login, password)
			login_window.outputText.setPlainText(str(e))
			
	def edit_triggers():
		global triggers
		td = TriggerDialog(triggers)
		if td.exec():
			triggers = td.triggers.toPlainText()
			open(TRIGGERS_FILENAME, 'w').write(triggers)
			main_window.triggers = triggers
		
		
	app = QtWidgets.QApplication(sys.argv)
	login_window = LoginApp(vk_login, vk_password)
	login_window.about_button.clicked.connect(lambda: login_window.outputText.setPlainText(open('README.md', 'r').read()))
	login_window.login_button.clicked.connect(log_in_vk)
	
	main_window = VKsdApp(vk, triggers)
	main_window.edit_triggers_btn.clicked.connect(edit_triggers)
	login_window.show()
	app.exec_()
