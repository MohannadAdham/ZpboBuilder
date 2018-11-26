# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'zpbo_builder_dialog_base.ui'
#
# Created: Wed May 02 11:47:57 2018
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_ZpboBuilderDialogBase(object):
    def setupUi(self, ZpboBuilderDialogBase):
        ZpboBuilderDialogBase.setObjectName(_fromUtf8("ZpboBuilderDialogBase"))
        ZpboBuilderDialogBase.resize(400, 496)
        self.button_box = QtGui.QDialogButtonBox(ZpboBuilderDialogBase)
        self.button_box.setGeometry(QtCore.QRect(40, 420, 341, 32))
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.button_box.setObjectName(_fromUtf8("button_box"))
        self.combo_zpbo = QtGui.QComboBox(ZpboBuilderDialogBase)
        self.combo_zpbo.setGeometry(QtCore.QRect(100, 60, 281, 21))
        self.combo_zpbo.setObjectName(_fromUtf8("combo_zpbo"))
        self.combo_zsro = QtGui.QComboBox(ZpboBuilderDialogBase)
        self.combo_zsro.setGeometry(QtCore.QRect(100, 110, 281, 22))
        self.combo_zsro.setObjectName(_fromUtf8("combo_zsro"))
        self.combo_t_noeud = QtGui.QComboBox(ZpboBuilderDialogBase)
        self.combo_t_noeud.setGeometry(QtCore.QRect(100, 160, 281, 22))
        self.combo_t_noeud.setObjectName(_fromUtf8("combo_t_noeud"))
        self.density_spinbox = QtGui.QDoubleSpinBox(ZpboBuilderDialogBase)
        self.density_spinbox.setGeometry(QtCore.QRect(100, 210, 161, 22))
        self.density_spinbox.setObjectName(_fromUtf8("density_spinbox"))
        self.label = QtGui.QLabel(ZpboBuilderDialogBase)
        self.label.setGeometry(QtCore.QRect(20, 60, 46, 13))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.label_5 = QtGui.QLabel(ZpboBuilderDialogBase)
        self.label_5.setGeometry(QtCore.QRect(20, 110, 46, 13))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_6 = QtGui.QLabel(ZpboBuilderDialogBase)
        self.label_6.setGeometry(QtCore.QRect(20, 160, 61, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.label_7 = QtGui.QLabel(ZpboBuilderDialogBase)
        self.label_7.setGeometry(QtCore.QRect(20, 210, 51, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.temp_path_btn = QtGui.QPushButton(ZpboBuilderDialogBase)
        self.temp_path_btn.setGeometry(QtCore.QRect(310, 280, 75, 23))
        self.temp_path_btn.setObjectName(_fromUtf8("temp_path_btn"))
        self.temp_path_line = QtGui.QLineEdit(ZpboBuilderDialogBase)
        self.temp_path_line.setGeometry(QtCore.QRect(100, 280, 191, 21))
        self.temp_path_line.setObjectName(_fromUtf8("temp_path_line"))
        self.result_path_line = QtGui.QLineEdit(ZpboBuilderDialogBase)
        self.result_path_line.setGeometry(QtCore.QRect(100, 330, 191, 21))
        self.result_path_line.setObjectName(_fromUtf8("result_path_line"))
        self.result_path_btn = QtGui.QPushButton(ZpboBuilderDialogBase)
        self.result_path_btn.setGeometry(QtCore.QRect(310, 330, 75, 23))
        self.result_path_btn.setObjectName(_fromUtf8("result_path_btn"))
        self.label_8 = QtGui.QLabel(ZpboBuilderDialogBase)
        self.label_8.setGeometry(QtCore.QRect(10, 280, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.label_9 = QtGui.QLabel(ZpboBuilderDialogBase)
        self.label_9.setGeometry(QtCore.QRect(10, 330, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName(_fromUtf8("label_9"))

        self.retranslateUi(ZpboBuilderDialogBase)
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL(_fromUtf8("accepted()")), ZpboBuilderDialogBase.accept)
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL(_fromUtf8("rejected()")), ZpboBuilderDialogBase.reject)
        QtCore.QMetaObject.connectSlotsByName(ZpboBuilderDialogBase)

    def retranslateUi(self, ZpboBuilderDialogBase):
        ZpboBuilderDialogBase.setWindowTitle(_translate("ZpboBuilderDialogBase", "Zpbo Builder", None))
        self.label.setText(_translate("ZpboBuilderDialogBase", "zpbo", None))
        self.label_5.setText(_translate("ZpboBuilderDialogBase", "zsro", None))
        self.label_6.setText(_translate("ZpboBuilderDialogBase", "t_noeud", None))
        self.label_7.setText(_translate("ZpboBuilderDialogBase", "Densité", None))
        self.temp_path_btn.setText(_translate("ZpboBuilderDialogBase", "Parcourire", None))
        self.result_path_btn.setText(_translate("ZpboBuilderDialogBase", "Parcourire", None))
        self.label_8.setText(_translate("ZpboBuilderDialogBase", "Temp folder", None))
        self.label_9.setText(_translate("ZpboBuilderDialogBase", "Result folder", None))

