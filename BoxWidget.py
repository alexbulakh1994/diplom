#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import  graphDialog
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class MainWidget(QtGui.QWidget):

    def __init__(self, parent):
        super(MainWidget, self).__init__(parent)

        self.cb = QtGui.QComboBox()
        self.mood_button_group = QtGui.QButtonGroup()
        self.editor = QtGui.QHBoxLayout()
        self.initMainWidget()
        self.radio_button_clicked()

    def initMainWidget(self):
        mainWidget = QtGui.QVBoxLayout()
        button_layout = self.initRadioBtnGroup()

        vbox = QtGui.QVBoxLayout()
        graphBtn = QtGui.QPushButton(u'Детальніше')
        graphBtn.clicked.connect(self.showgraph)
        vbox.addWidget(graphBtn)

        mainWidget.addLayout(button_layout)
        mainWidget.addLayout(self.editor)
        mainWidget.addStretch()
        mainWidget.addLayout(vbox)

        self.setLayout(mainWidget)

    def initRadioBtnGroup(self):
        radioButtons = [QtGui.QRadioButton(u"Статистичні графіки"), QtGui.QRadioButton(u"Зміщення профілактики"),
                        QtGui.QRadioButton(u"Додавання даних до Бд"), QtGui.QRadioButton(u"Економічні характеристики"),
                        QtGui.QRadioButton(u"Параметри моделі")]

        radioButtons[0].setChecked(True)
        button_layout = QtGui.QVBoxLayout()

        for i in xrange(len(radioButtons)):
            button_layout.addWidget(radioButtons[i])
            self.mood_button_group.addButton(radioButtons[i], i)
            self.connect(radioButtons[i], SIGNAL("clicked()"), self.radio_button_clicked)
        return button_layout

    def showgraph(self):
        active_radioBtn_index = self.mood_button_group.checkedId()
        active_comboBox_index = self.cb.currentIndex()
        active_comboBox_Text = self.cb.currentText()
        dialog = graphDialog.Dialog(active_radioBtn_index, active_comboBox_index, active_comboBox_Text)
        dialog.exec_()

    def radio_button_clicked(self):
        id = self.mood_button_group.checkedId()

        if id == 0:
            self.statisticPlotWidget()
        elif id == 1:
            self.findBestShift()
        elif id == 2:
            self.tableView()
        elif id == 3:
            self.economicMeaning()
        elif id == 4:
            self.findBestShift()

    def clearLayout(self):
        while self.editor.count():
            child = self.editor.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def statisticPlotWidget(self):
        self.clearLayout()

        label = QtGui.QLabel(u"Вибір типу статистики:", self)
        self.cb = QtGui.QComboBox()

        self.cb.addItems([u"Статистика нових випадків ВІЛ-інфекції серед дорослих",
                     u"Статистика нових випадків ВІЛ-інфекції серед дітей",
                     u"Статистика нових випадків ВІЛ-інфекції серед СІН",
                     u"Статистика нових випадків СНІД серед дорослих",
                     u"Статистика нових випадків СНІД серед дітей",
                     u"Статистика нових випадків СНІД серед СІН",
                     u"Статистика смертності від ВІЛ/СНІД серед дорослих",
                     u"Статистика смертності від ВІЛ/СНІД серед дітей",
                     u"Статистика смертності від ВІЛ/СНІД серед СІН"
                    ])
        self.cb.resize(self.cb.sizeHint())

        self.editor.addWidget(label)
        self.editor.addWidget(self.cb)
        self.editor.setAlignment(QtCore.Qt.AlignLeft)

    def findBestShift(self):
        self.clearLayout()

        label = QtGui.QLabel(u"Параметри:", self)
        self.cb = QtGui.QComboBox()
        self.cb.addItems([u"Швидкість передачі ВІЛ-інфекції серед дітей",
                     u"Швидкість передачі ВІЛ-інфекції серед дорослих",
                     u"Швидкість передачі ВІЛ-інфекції серед СІН осіб",
                     u"Швидкість переходу зі стану ВІЛ-інфікований до стану СНІД серед дітей",
                     u"Швидкість переходу зі стану ВІЛ-інфікований до стану СНІД серед дорослих",
                     u"Швидкість переходу зі стану ВІЛ-інфікований до стану СНІД серед СІН",
                     u"Смертність серед СНІД інфікованих дітей",
                     u"Смертність серед СНІД інфікованих дорослих",
                     u"Смертність серед СНІД інфікованих СІН",
                     u"Швидікість притоку населення в України"])
        self.cb.resize(self.cb.sizeHint())

        self.editor.addWidget(label)
        self.editor.addWidget(self.cb)
        self.editor.setAlignment(QtCore.Qt.AlignLeft)

    def economicMeaning(self):
        self.clearLayout()

        label = QtGui.QLabel(u"Параметри:", self)
        self.cb = QtGui.QComboBox()
        self.cb.addItems([u"Швидкість передачі ВІЛ-інфекції серед дітей",
                          u"Швидкість передачі ВІЛ-інфекції серед дорослих",
                          u"Швидкість передачі ВІЛ-інфекції серед СІН осіб",
                          u"Швидкість переходу зі стану ВІЛ-інфікований до стану СНІД серед дітей",
                          u"Швидкість переходу зі стану ВІЛ-інфікований до стану СНІД серед дорослих",
                          u"Швидкість переходу зі стану ВІЛ-інфікований до стану СНІД серед СІН",
                          u"Смертність серед СНІД інфікованих дітей",
                          u"Смертність серед СНІД інфікованих дорослих",
                          u"Смертність серед СНІД інфікованих СІН",
                          u"Швидікість притоку населення в України"])
        self.cb.resize(self.cb.sizeHint())

        self.editor.addWidget(label)
        self.editor.addWidget(self.cb)
        self.editor.setAlignment(QtCore.Qt.AlignLeft)

    def tableView(self):
        self.clearLayout()
        table = QtGui.QTableWidget()

        # initiate table
        table.setWindowTitle("QTableWidget Example @pythonspot.com")
        table.setRowCount(100)
        table.setColumnCount(10)


        self.editor.addWidget(table)
        self.editor.setAlignment(QtCore.Qt.AlignLeft)
        table.show()