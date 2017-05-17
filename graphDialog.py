#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from matplotlib import rc
import dataBaseApi as dbAPI
import ParamsCalculator
import numpy as np

import random

class Dialog(QtGui.QDialog):
    def __init__(self, active_radio_btn, active_comboBoxIndex, active_comboBox_Text, parent=None):
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
        self.graphParamText = active_comboBox_Text

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
                'y':self.data[:, self.graphParamsType],
                'xlabel': u"Місяці",
                'ylabel': self.graphParamText
            }
        elif (self.graphType == 1):
            plot_type = self.mood_button_group.checkedId()
            self.plotData = ParamsCalculator.calcOptimalShiftParams(self.data, 10, self.graphParamsType, plot_type)
            self.plotData['xlabel'] = u"% обстежених АРТ"
            self.plotData['ylabel'] = self.graphParamText
        elif (self.graphType == 3):
            plot_type = self.mood_button_group.checkedId()
            self.plotData = ParamsCalculator.calcOptimalShiftParams(self.data, 10, self.graphParamsType, plot_type)
            self.plotData['xlabel'] = u"Місяці"
            self.plotData['ylabel'] = self.graphParamText
        elif (self.graphType == 4):
            self.plotData = ParamsCalculator.calculateModelParameters(self.data, 10,  self.graphParamsType)
            self.plotData['xlabel'] = u"Місяці"
            self.plotData['ylabel'] = self.graphParamText

    def plot(self):
        self.getPlotType()

        font = {'family': 'Verdana', 'weight':'normal'}
        rc('font', **font)
        ax = self.figure.add_subplot(111)

        # discards the old graph
        ax.hold(True)

        if self.graphType == 3:
            self.stepPlot(ax)
        else:
            try:
                plt.xlabel(self.plotData['xlabel'])
                plt.ylabel(self.plotData['ylabel'])
                ax.plot(self.plotData['x'], self.plotData['y'], '.')
                ax.plot(self.plotData['x'], self.plotData['predict_y'], 'r')

                labelOptimalText = u"Оптимальне зміщення " + str(self.plotData['errors'] * 6) + u" місяців"
                self.optimalParamLabel.setText(labelOptimalText)

            except KeyError:
                print 'not found predict_key'

        self.canvas.draw()

    def stepPlot(self, ax):
        try:
            plt.xlabel(self.plotData['xlabel'])
            plt.ylabel(self.plotData['ylabel'])

            data = self.ecomonicValues()
            ax.step(data['x'], data['y'])

        except KeyError:
            print 'not found predict_key'

    def ecomonicValues(self):
        shiftY_Data = self.plotData['y'][self.plotData['optimal_shift']:]
        shiftX_Data = self.plotData['x'][self.plotData['optimal_shift']:]
        ecomonicValues = shiftY_Data[1:] - shiftY_Data[:-1] / (shiftX_Data[1:] - shiftX_Data[:-1])

        correctLen = len(ecomonicValues) - len(ecomonicValues) % 6
        return {
            'y': np.mean(ecomonicValues[:correctLen].reshape(-1, 6), axis=1),
            'x': np.arange(0, correctLen, 6)
        }

