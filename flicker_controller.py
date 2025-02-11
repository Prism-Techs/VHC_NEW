from PyQt5 import QtCore, QtGui, QtWidgets
import threading
import time
from globalvar import globaladc
from flicker_demo import Ui_Form
import sys

class PeriodicThread(threading.Thread):
    def __init__(self, interval, callback):
        super().__init__()
        self.interval = interval
        self.callback = callback
        self.stopped = threading.Event()
        self.paused = threading.Event()
        self.isStarted = False

    def run(self):
        self.isStarted = True
        while not self.stopped.is_set():
            if not self.paused.is_set():
                self.callback()
                time.sleep(self.interval)

    def stop(self):
        self.stopped.set()
        self.paused.set()

    def pause(self):
        self.paused.set()

    def resume(self):
        self.paused.clear()

    def kill(self):
        self.stopped.set()

class FlickerController(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        # Initialize variables
        self.defaultDepth = 7
        self.maxDepth = 15
        self.currentDepth = 0
        self.flickerInterval = globaladc.get_flicker_delay()
        self.flickerOn = False
        self.flicker_bool = True
        self.threadCreated = False
        
        # Connect signals
        self.ui.upButton.clicked.connect(self.upButtonClicked)
        self.ui.upButton_2.clicked.connect(self.downButtonClicked)
        self.ui.pushButton_3.clicked.connect(self.toggleFlicker)
        self.ui.pushButton_2.clicked.connect(self.goHome)
        
        # Connect navigation buttons
        self.ui.pushButton_4.clicked.connect(lambda: self.navigateTo('FlickerScreen'))
        self.ui.pushButton_5.clicked.connect(lambda: self.navigateTo('CffFovea'))
        self.ui.pushButton_6.clicked.connect(lambda: self.navigateTo('BrkFovea'))
        self.ui.pushButton_7.clicked.connect(lambda: self.navigateTo('CffParaFovea'))
        self.ui.pushButton_8.clicked.connect(lambda: self.navigateTo('BrkParaFovea'))
        self.ui.pushButton_9.clicked.connect(lambda: self.navigateTo('TestResult'))
        
        # Initial UI setup
        self.ui.numberLabel.setText(str(self.currentDepth))
        self.updateButtonStates()
        
        # Prepare hardware
        globaladc.flicker_Prepair()

    def upButtonClicked(self):
        if self.currentDepth < self.maxDepth:
            self.currentDepth += 1
            self.ui.numberLabel.setText(str(self.currentDepth))
            globaladc.buzzer_1()

    def downButtonClicked(self):
        if self.currentDepth > 0:
            self.currentDepth -= 1
            self.ui.numberLabel.setText(str(self.currentDepth))
            globaladc.buzzer_1()

    def toggleFlicker(self):
        if not self.threadCreated:
            self.worker_flik = PeriodicThread(self.flickerInterval, self.periodic_event)
            self.threadCreated = True

        globaladc.buzzer_1()
        self.flickerOn = not self.flickerOn
        
        if self.flickerOn:
            self.ui.pushButton_3.setText("Flicker on")
            self.currentDepth = self.defaultDepth
            self.ui.numberLabel.setText(str(self.currentDepth))
            self.ui.upButton.setEnabled(True)
            self.ui.upButton_2.setEnabled(True)
            if not self.worker_flik.isStarted:
                self.worker_flik.start()
            else:
                self.worker_flik.resume()
        else:
            self.ui.pushButton_3.setText("Flicker off")
            self.currentDepth = 0
            self.ui.numberLabel.setText(str(self.currentDepth))
            self.ui.upButton.setEnabled(False)
            self.ui.upButton_2.setEnabled(False)
            if self.threadCreated:
                self.worker_flik.pause()

    def periodic_event(self):
        if self.flicker_bool:
            globaladc.fliker(self.currentDepth)  # Hardware control
            self.flicker_bool = False
        else:
            globaladc.fliker(0)  # Reset hardware state
            self.flicker_bool = True

    def updateButtonStates(self):
        enabled = self.flickerOn
        self.ui.upButton.setEnabled(enabled)
        self.ui.upButton_2.setEnabled(enabled)

    def goHome(self):
        if self.threadCreated:
            self.worker_flik.stop()
            self.worker_flik.kill()
            self.threadCreated = False
        self.hide()
        # if 'MainScreen' in pageDisctonary:
        #     pageDisctonary['MainScreen'].show()

    def navigateTo(self, page):
        if self.threadCreated:
            self.worker_flik.stop()
            self.worker_flik.kill()
            self.threadCreated = False
        self.hide()
        # if page in pageDisctonary:
        #     pageDisctonary[page].show()

    def show(self):
        super().show()
        globaladc.flicker_Prepair()
        self.currentDepth = 0
        self.flickerOn = False
        self.ui.upButton.setEnabled(False)
        self.ui.upButton_2.setEnabled(False)
        self.ui.pushButton_3.setText("Flicker off")

    def hide(self):
        if self.threadCreated:
            self.worker_flik.stop()
            self.worker_flik.kill()
            self.threadCreated = False
        super().hide()

    def closeEvent(self, event):
        if self.threadCreated:
            self.worker_flik.stop()
            self.worker_flik.kill()
        event.accept()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = FlickerController()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
