# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'trigger_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtdesigns.trigger_dialog_design as design

class TriggerDialog(QtWidgets.QDialog, design.Ui_triggerDialog):
	def __init__(self, triggers=''):
		super().__init__()
		self.setupUi(self)
		self.triggers.setPlainText(triggers)