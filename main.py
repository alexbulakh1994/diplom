import BoxWidget
import sys
from PyQt4 import QtGui

class Window(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.setGeometry(50,50, 500, 300)
        self.setWindowTitle('HIV/AIDS infections')
        self.form_widget = BoxWidget.MainWidget(self)
        self.setCentralWidget(self.form_widget)

def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    GUI.show()
    sys.exit(app.exec_())

run()