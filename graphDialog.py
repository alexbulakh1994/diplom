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

        self.getPlotType()

        # set the layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def getPlotType(self):
        if (self.graphType == 0):
            self.plotData = {
                'x': np.arange(0,165, 1),
                'y':self.data[:, self.graphParamsType]
            }
        elif (self.graphType == 1):
            self.plotData = ParamsCalculator.calculateOptimalShift(self.data, 10, self.graphParamsType)
        elif (self.graphType == 4):
            self.plotData = ParamsCalculator.calculateModelParameters(self.data, 10,  self.graphParamsType)

    def plot(self):
        ''' plot some random stuff '''
        # random data
        # data = [random.random() for i in range(10)]

        # create an axis
        ax = self.figure.add_subplot(111)

        # discards the old graph
        ax.hold(False)

        # plot data
        ax.plot(self.plotData['x'], self.plotData['y'], '.', self.plotData['x'], self.plotData['predict_y'], 'r')

        # refresh canvas
        self.canvas.draw()
