#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import dataBaseApi as dbAPI
import ParamsCalculator
import numpy as np

import random

class Dialog(QtGui.QDialog):
    def __init__(self, active_radio_btn, active_comboBoxIndex, parent=None):
        super(Dialog, self).__init__(parent)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.mood_button_group = QtGui.QButtonGroup()
        self.optimalParamLabel = QtGui.QLabel()

        # Just some button connected to `plot` method
        self.button = QtGui.QPushButton('Plot')
        self.button.clicked.connect(self.plot)

        self.graphType = active_radio_btn
        self.graphParamsType = active_comboBoxIndex

        self.data = dbAPI.getData('Select newCasesAdult, newCasesChild, newCasesHIVSIN, \
                newCasesAIDSAdult, newCasesAIDSChild, newCasesDeathAdult, newCasesDeathChild, newCasesDeathAllPeople, \
                allCasesHIVAdult, allCasesHIVChild, allCasesAIDSSIN, allCasesHIVAllPeople, \
                allCasesAIDSAdult, allCasesAIDSChild, allCasesAIDSAllPeople, \
                allCasesDeathAdult, allCasesDeathChild, allCasesDeathAllPeople, \
                allPeople, SINpercent, newCasesAllPeople, newCasesAIDSAllPeople from infection ', 22)

        # set the layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        button_layout = self.initRadioBtnGroup()
        layout.addLayout(button_layout)

        layout.addWidget(self.optimalParamLabel)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def initRadioBtnGroup(self):
        radioButtons = [QtGui.QRadioButton(u"Лінійна регресія"), QtGui.QRadioButton(u"Нелінійна регресія")]
        button_layout = QtGui.QVBoxLayout()

        for i in xrange(len(radioButtons)):
            button_layout.addWidget(radioButtons[i])
            self.mood_button_group.addButton(radioButtons[i], i)
        return button_layout

    def getPlotType(self):
        if (self.graphType == 0):
            self.plotData = {
                'x': np.arange(0,165, 1),
                'y':self.data[:, self.graphParamsType]
            }
        elif (self.graphType == 1):
            plot_type = self.mood_button_group.checkedId()
            self.plotData = ParamsCalculator.calcOptimalShiftParams(self.data, 10, self.graphParamsType, plot_type)
        elif (self.graphType == 4):
            self.plotData = ParamsCalculator.calculateModelParameters(self.data, 10,  self.graphParamsType)

    def plot(self):
        ''' plot some random stuff '''
        # random data
        # data = [random.random() for i in range(10)]

        # create an axis
        self.getPlotType()

        ax = self.figure.add_subplot(111)

        # discards the old graph
        ax.hold(True)

        print self.mood_button_group.checkedId()

        # plot data
        try:
            ax.plot(self.plotData['x'], self.plotData['y'], '.')
            ax.plot(self.plotData['x'], self.plotData['predict_y'], 'r')

            labelOptimalText = u"Оптимальне зміщення " + str(np.argmin(self.plotData['errors']) * 6) + u" місяців"
            self.optimalParamLabel.setText(labelOptimalText)
        except KeyError:
            print 'not found predict_key'

        # refresh canvas
        self.canvas.draw()
