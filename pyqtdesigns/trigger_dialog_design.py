# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'trigger_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_triggerDialog(object):
    def setupUi(self, triggerDialog):
        triggerDialog.setObjectName("triggerDialog")
        triggerDialog.resize(480, 480)
        self.verticalLayout = QtWidgets.QVBoxLayout(triggerDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(triggerDialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.triggers = QtWidgets.QPlainTextEdit(triggerDialog)
        self.triggers.setObjectName("triggers")
        self.verticalLayout.addWidget(self.triggers)
        self.buttonBox = QtWidgets.QDialogButtonBox(triggerDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(triggerDialog)
        self.buttonBox.accepted.connect(triggerDialog.accept)
        self.buttonBox.rejected.connect(triggerDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(triggerDialog)

    def retranslateUi(self, triggerDialog):
        _translate = QtCore.QCoreApplication.translate
        triggerDialog.setWindowTitle(_translate("triggerDialog", "Редактирование триггеров"))
        self.label.setText(_translate("triggerDialog", "Редактирование триггеров, все изменения сохранятся"))
