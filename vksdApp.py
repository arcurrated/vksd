import time
from PyQt5 import QtWidgets

import pyqtdesigns.vksd_design as design

class VKsdApp(QtWidgets.QMainWindow, design.Ui_vk_scout_desktop):
	def __init__(self, vk, triggers=''):
		super().__init__()
		self.setupUi(self)
		self.get_city_btn.clicked.connect(self.get_city)
		self.get_new_page_btn.clicked.connect(self.get_new_page)
		self.get_page_by_bdate_btn.clicked.connect(self.get_page_by_bdate)
		self.from_link_btn.clicked.connect(self.set_vk_id_by_link)
		self.list_groups_btn.clicked.connect(self.check_groups)
		self.find_triggers_btn.clicked.connect(self.find_triggers)
		self.add_link_btn.clicked.connect(self.add_link)
		self.remove_link_btn.clicked.connect(self.remove_selected_list_item)
		self.reset_list_btn.clicked.connect(self.listWidget.clear)
		self.find_by_friends_btn.clicked.connect(self.frintersect)
		self.vk = vk
		self.triggers = triggers
		
	def set_vk_id_by_link(self):
		text, ok = QtWidgets.QInputDialog.getText(self, 'VK ID by link', 'Ведите ссылку на страницу ВК:')
		if ok:
			if 'vk.com' not in text:
				self.output('link is not valid')
				return
			try:
				users_data = self.vk.users.get(user_ids=text.split('vk.com/')[-1])
			except Exception as e:
				self.output(str(e))
				return
			if len(users_data) == 0:
				self.output('page is not existing')
				return
			try:
				self.vk_id_input.setText(str(users_data[0]['id']))
			except Exception as e:
				self.output(str(e))
			
	
	def get_city(self):
		#city by vk_id
		self.progressBar.setValue(0)
		vk_id = self.vk_id_input.text()
		if vk_id == '':
			self.output('no VK ID')
			return
		try:
			vk_id = int(vk_id)
		except:
			self.output('VK ID not valid')
			return
		
		try:
			friends = self.vk.friends.get(user_id=vk_id, fields='city')
		except Exception as e:
			self.output('ERR: {}'.format(e))
			return
		
		totals = []
		for i, friend in enumerate(friends['items']):
			self.progressBar.setValue(i/len(friends['items'])*100)
			if 'city' in friend:
				city = friend['city']['title']
				for total in totals:
					if total['title'] == city:
						total['count'] += 1
						break
				else:
					totals.append({'title': city, 'count': 1})
		
		totals_sorted = []
		for city in totals:
			for i, city_sorted in enumerate(totals_sorted):
				if city['count'] > city_sorted['count']:
					totals_sorted.insert(i, city)
					break
			else:
				totals_sorted.append(city)
		
		text = ''
		for city in totals_sorted[:5]:
			text += '{1} - {0}\n'.format(city['title'], city['count'])
		self.progressBar.setValue(100)
		self.output(text)
		
	def get_new_page(self):
		#user with such friends
		self.progressBar.setValue(0)
		vk_id = self.vk_id_input.text()
		if vk_id == '':
			self.output('no VK ID')
			return
		try:
			vk_id = int(vk_id)
		except:
			self.output('VK ID not valid')
			return
			
		try:
			friends = self.vk.friends.get(user_id=vk_id, fields='is_closed')
		except Exception as e:
			self.output('ERR: {}'.format(e))
			return
		
		first_friends = friends['items']
		first_friends_ids = [f['id'] for f in first_friends]
		
		second_friends = []

		for j, friend in enumerate(first_friends):
			self.progressBar.setValue(j/len(first_friends)*50)
			
			if 'deactivated' in friend or 'is_closed' in friend and friend['is_closed']:
				continue
			time.sleep(0.5)
			try:
				friend_friends = self.vk.friends.get(user_id=friend['id'], fields='first_name')
			except Exception as e:
				self.output_append('ERR: {}'.format(e))
				continue
			
			for friend_friend in friend_friends['items']:
				for i, second_friend in enumerate(second_friends):
					if second_friend['id'] == friend_friend['id']:
						second_friends[i]['count'] += 1
						break
				else:
					friend_friend['count'] = 1
					second_friends.append(friend_friend)
			
		sorted_second_friends = []
		for j,sec_friend in enumerate(second_friends):
			self.progressBar.setValue(j/len(second_friends)*50+50)
			for i, sorted_sec_fr in enumerate(sorted_second_friends):
				if sec_friend['count'] > sorted_sec_fr['count']:
					sorted_second_friends.insert(i, sec_friend)
					break
			else:
				sorted_second_friends.append(sec_friend)
		
		text = ''
		for fr in sorted_second_friends[:6]:
			if fr['id'] == vk_id:
				continue
			text += '{} - {} {} vk.com/id{}\n'.format(fr['count'], fr['first_name'], fr['last_name'], fr['id'])
		self.output(text)
		self.progressBar.setValue(100)
		
		
	def get_page_by_bdate(self):
		#user in friends with bdate
		self.progressBar.setValue(0)
		vk_id = self.vk_id_input.text()
		if vk_id == '':
			self.output('no VK ID')
			return
		try:
			vk_id = int(vk_id)
		except:
			self.output('VK ID not valid')
			return
			
		try: 
			bdate = self.bdate_input.text()
			bdate_day, bdate_month = bdate.split('.')
			bdate_day = int(bdate_day)
			bdate_month = int(bdate_month)
		except:
			self.output('BDATE NOT VALID')
			return
			
		try:
			friends = self.vk.friends.get(user_id=vk_id, fields='bdate')
		except Exception as e:
			self.output('ERR: {}'.format(e))
			return
		
		text = ''
		for i, friend in enumerate(friends['items']):
			self.progressBar.setValue(i/len(friends['items'])*100)
			if 'bdate' in friend:
				if friend['bdate'].split('.')[:2] == [str(bdate_day), str(bdate_month)]:
					text += '{} {} {} {}\n'.format(friend['first_name'], friend['last_name'], friend['bdate'], 'vk.com/id{}'.format(friend['id']))
		self.output(text)
		self.progressBar.setValue(100)
		
	def check_groups(self):
		vk_id = self.vk_id_input.text()
		self.progressBar.setValue(0)
		if vk_id == '':
			self.output('no VK ID')
			return
		try:
			vk_id = int(vk_id)
		except:
			self.output('VK ID not valid')
			return
			
		try:
			groups = self.vk.groups.get(user_id=vk_id, extended=1, count=1000)
		except Exception as e:
			self.output(str(e))
			return
		
		text = ''
		for group in groups['items']:
			text += '{}   vk.com/public{}\n'.format(group['name'], group['id'])
		self.output(text)
		self.progressBar.setValue(100)
		
	def find_triggers(self):
		if self.triggers == '':
			return
		vk_id = self.vk_id_input.text()
		self.progressBar.setValue(0)
		if vk_id == '':
			self.output('no VK ID')
			return
		try:
			vk_id = int(vk_id)
		except:
			self.output('VK ID not valid')
			return
			
		try:
			user_data = self.vk.users.get(user_id=vk_id, fields='about, status')
		except Exception as e:
			self.output(str(e))
			return
		if len(user_data) == 0:
			self.output('no user with this vk id')
			return
		text = ''
		user_data = user_data[0]
		if self._find_triggers(user_data, 'status'):
			text += 'Cтатус пользователя: {}\n'.format(user_data['status'])
		if self._find_triggers(user_data, 'about'):
			text += 'О себе пользователя: {}\n'.format(user_data['about'])
			
		try: 
			friends = self.vk.friends.get(user_id=vk_id, fields='status,about')
		except Exception as e:
			self.output(str(e))
			return
		for i, friend in enumerate(friends['items']):
			self.progressBar.setValue(i/len(friends['items'])*50)
			if self._find_triggers(friend, 'status'):
				text += 'vk.com/id{} статус: {}\n'.format(friend['id'], friend['status'])
			if self._find_triggers(friend, 'about'):
				text += 'vk.com/id{} о себе: {}\n'.format(friend['id'], friend['about'])
		
		try:
			groups = self.vk.groups.get(user_id=vk_id, extended=1, fields='status', count=1000)
		except Exception as e:
			self.output(str(e))
			return
			
		for i, group in enumerate(groups['items']):
			self.progressBar.setValue(i/len(groups['items'])*50+50)
			if self._find_triggers(group, 'name'):
				text += 'vk.com/public{} название: {}\n'.format(group['id'], group['name'])
			if self._find_triggers(group, 'status'):
				 text += 'vk.com/public{} статус: {}\n'.format(group['id'], group['status'])
			
		self.progressBar.setValue(100)
		self.output(text)
		
	def _find_triggers(self, obj, field):
		if field in obj:
			for trigger in self.triggers.split(','):
				if trigger.strip().lower() in obj[field].lower():
					return True
		return False

	def add_link(self):
		text, ok = QtWidgets.QInputDialog.getText(self, 'VK ID by link', 'Ведите ссылку на страницу ВК:')
		if ok:
			if 'vk.com' not in text:
				self.output('link is not valid')
				return
			try:
				users_data = self.vk.users.get(user_ids=text.split('vk.com/')[-1])
			except Exception as e:
				self.output(str(e))
				return
			if len(users_data) == 0:
				self.output('page is not existing')
				return
			try:
				if 'deactivated' in users_data[0] or users_data[0]['is_closed']:
					self.output('Списки друзей недоступны')
					return

				vk_id = users_data[0]['id']
				for i in range(self.listWidget.count()):
						if self.listWidget.item(i).text().split(' ')[-1] == str(vk_id):
							break
				else:
					self.listWidget.addItem("{} {} {}".format(users_data[0]['first_name'], users_data[0]['last_name'], vk_id))
			except Exception as e:
				self.output(str(e))

	def remove_selected_list_item(self):
		curr = self.listWidget.currentItem()
		if curr != None:
				for i in range(self.listWidget.count()):
					if self.listWidget.item(i) == curr:
						self.listWidget.takeItem(i)
						break
		else:
			self.output('для удаления выберите профиль в списке')

	def frintersect(self):
			self.progressBar.setValue(0)
			count = self.listWidget.count()
			if count == 0:
				self.output('no vk ids')
				return

			vk_ids = []
			for i in range(count):
				vk_ids.append(int(self.listWidget.item(i).text().split(' ')[-1]))

			friends = []
			merged_friends = []
			for i, vk_id in enumerate(vk_ids):
				self.progressBar.setValue(i/len(vk_ids)*99)
				try:
					friends = self.vk.friends.get(user_id=vk_id, fields='first_name')
				except Exception as e:
					self.output('ERR: {}'.format(e))
					return
				
				friends = friends['items']
				friends_ids = [f['id'] for f in friends]
				if vk_id == vk_ids[0]:
					merged_friends = friends_ids
				merged_friends = set(merged_friends)&set(friends_ids)

			text = ''
			for fr_id in merged_friends:
				for friend in friends:
					if fr_id == friend['id']:
						text += '{} {} vk.com/id{}\n'.format(friend['first_name'], friend['last_name'], friend['id'])
			self.output(text)
			self.progressBar.setValue(100)
		
		
	def output(self, data):
		self.outputField.setPlainText(data)
