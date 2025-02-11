from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
import time
from globalvar import globaladc,pageDisctonary


class FlickerThread(QThread):
    trigger = pyqtSignal()

    def __init__(self, interval):
        super().__init__()
        self.interval = interval
        self.isRunning = False
        self.isStarted = False

    def run(self):
        self.isRunning = True
        self.isStarted = True
        while self.isRunning:
            self.trigger.emit()
            time.sleep(self.interval)

    def stop(self):
        self.isRunning = False

    def kill(self):
        self.stop()
        self.wait()
        self.isStarted = False

    def resume(self):
        if not self.isRunning:
            self.isRunning = True
            if not self.isStarted:
                self.start()

class Ui_FlickerDemo(object):
    def setupUi(self, Form):
        self.Form = Form
        Form.setObjectName("Form")
        Form.resize(1024, 600)
        Form.setStyleSheet("background-color:#000000;")

        # Initialize variables
        self.flicker_bool = True
        self.threadCreated = False
        self.depth_value = 7
        self.max_depth = 15
        self.interval = globaladc.get_flicker_delay()

        # Header Frame
        self.frame_4 = QtWidgets.QFrame(Form)
        self.frame_4.setGeometry(QtCore.QRect(0, 0, 1024, 40))
        self.frame_4.setStyleSheet("background-color:#1f2836;")
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)

        # Header Title
        self.title_label = QtWidgets.QLabel(self.frame_4)
        self.title_label.setGeometry(QtCore.QRect(60, 0, 281, 41))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(16)
        font.setBold(True)
        self.title_label.setFont(font)
        self.title_label.setStyleSheet("color:white;")
        self.title_label.setText("Vekaria Healthcare")

        # Main Content Frame
        self.main_frame = QtWidgets.QFrame(Form)
        self.main_frame.setGeometry(QtCore.QRect(280, 100, 711, 441))
        self.main_frame.setStyleSheet("""
            QFrame {
                background-color:#1f2836;
                border-radius:30px;
            }
        """)

        # Depth Control Frame
        self.depth_frame = QtWidgets.QFrame(self.main_frame)
        self.depth_frame.setGeometry(QtCore.QRect(50, 120, 191, 221))

        # Depth Label
        self.depth_label = QtWidgets.QLabel(self.main_frame)
        self.depth_label.setGeometry(QtCore.QRect(100, 40, 131, 61))
        font = QtGui.QFont()
        font.setFamily("Helvetica Rounded")
        font.setPointSize(18)
        font.setBold(True)
        self.depth_label.setFont(font)
        self.depth_label.setStyleSheet("color:white;")
        self.depth_label.setText("Depth")

        # Up Button
        self.upButton = QtWidgets.QPushButton(self.depth_frame)
        self.upButton.setGeometry(QtCore.QRect(70, 10, 60, 60))
        self.upButton.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                border: 1px solid white;
                border-radius: 30px;
                font-size: 40px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #177bad;
            }
        """)
        self.upButton.setText("+")
        self.upButton.setEnabled(False)

        # Depth Display
        self.numberLabel = QtWidgets.QLabel(self.depth_frame)
        self.numberLabel.setGeometry(QtCore.QRect(60, 86, 80, 60))
        font = QtGui.QFont()
        font.setFamily("Helvetica Rounded")
        font.setPointSize(28)
        font.setBold(True)
        self.numberLabel.setFont(font)
        self.numberLabel.setStyleSheet("""
            background-color: black;
            color: white;
            padding: 5px;
            border:2px solid white;
            border-radius: 5px;
        """)
        self.numberLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.numberLabel.setText(str(self.depth_value))

        # Down Button
        self.downButton = QtWidgets.QPushButton(self.depth_frame)
        self.downButton.setGeometry(QtCore.QRect(70, 160, 60, 60))
        self.downButton.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                border: 1px solid white;
                border-radius: 30px;
                font-size: 50px;
            }
            QPushButton:hover {
                background-color: #177bad;
            }
        """)
        self.downButton.setText("-")
        self.downButton.setEnabled(False)

        # Flicker Control Button
        self.flickerButton = QtWidgets.QPushButton(self.main_frame)
        self.flickerButton.setGeometry(QtCore.QRect(350, 90, 240, 51))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(16)
        font.setBold(True)
        self.flickerButton.setFont(font)
        self.flickerButton.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                border: none;
                border-radius: 15px;
                padding: 10px;
                border:2px solid white;
            }
        """)
        self.flickerButton.setText("Flicker On")

        # Navigation Buttons
        self.homeButton = QtWidgets.QPushButton(self.main_frame)
        self.homeButton.setGeometry(QtCore.QRect(490, 350, 160, 51))
        self.homeButton.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                border: none;
                border-radius: 15px;
                padding: 10px;
                border:2px solid white;
            }
        """)
        self.homeButton.setText("HOME")

        self.exitButton = QtWidgets.QPushButton(self.main_frame)
        self.exitButton.setGeometry(QtCore.QRect(300, 350, 160, 51))
        self.exitButton.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                border: none;
                border-radius: 15px;
                padding: 10px;
                border:2px solid white;
            }
        """)
        self.exitButton.setText("EXIT")

        # Connect signals
        self.upButton.clicked.connect(self.up_button_clicked)
        self.downButton.clicked.connect(self.down_button_clicked)
        self.flickerButton.clicked.connect(self.toggle_flicker)
        self.homeButton.clicked.connect(self.on_home)
        self.exitButton.clicked.connect(self.on_exit)

    def up_button_clicked(self):
        if self.depth_value < self.max_depth:
            self.depth_value += 1
            self.numberLabel.setText(str(self.depth_value))
        globaladc.buzzer_1()

    def down_button_clicked(self):
        if self.depth_value > 0:
            self.depth_value -= 1
            self.numberLabel.setText(str(self.depth_value))
        globaladc.buzzer_1()

    def toggle_flicker(self):
        globaladc.buzzer_1()

        if not self.threadCreated:
            self.worker_flik = FlickerThread(self.interval)
            self.worker_flik.trigger.connect(self.periodic_event)
            self.threadCreated = True

        if self.flickerButton.text() == "Flicker On":
            self.flickerButton.setText("Flicker Off")
            self.upButton.setEnabled(True)
            self.downButton.setEnabled(True)
            self.depth_value = 7
            self.numberLabel.setText(str(self.depth_value))
            if not self.worker_flik.isStarted:
                self.worker_flik.start()
            else:
                self.worker_flik.resume()
        else:
            self.flickerButton.setText("Flicker On")
            self.depth_value = 0
            self.numberLabel.setText(str(self.depth_value))
            self.upButton.setEnabled(False)
            self.downButton.setEnabled(False)
            if self.threadCreated:
                self.worker_flik.stop()

    def periodic_event(self):
        if self.flicker_bool:
            globaladc.fliker(self.depth_value)
            self.flicker_bool = False
        else:
            globaladc.fliker(0)
            self.flicker_bool = True

    def show(self):
        globaladc.flicker_Prepair()
        self.Form.show()
        self.depth_value = 0
        self.numberLabel.setText(str(self.depth_value))
        self.upButton.setEnabled(False)
        self.downButton.setEnabled(False)
        self.flickerButton.setText("Flicker On")

    def hide(self):
        if self.threadCreated:
            self.worker_flik.stop()
            self.worker_flik.kill()
            self.threadCreated = False
        self.Form.hide()

    def on_home(self):
        self.hide()
        if 'MainScreen' in pageDisctonary and pageDisctonary['MainScreen']:
            pageDisctonary['MainScreen'].show()

    def on_exit(self):
        self.hide()
        if 'MainScreen' in pageDisctonary and pageDisctonary['MainScreen']:
            pageDisctonary['MainScreen'].show()

class FlickerDemo(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_FlickerDemo()
        self.ui.setupUi(self)

    def show(self):
        self.ui.show()

    def hide(self):
        self.ui.hide()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = FlickerDemo()
    window.show()
    sys.exit(app.exec_())