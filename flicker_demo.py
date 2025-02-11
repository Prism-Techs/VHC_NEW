from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal, Qt
import time
from globalvar import pageDisctonary, globaladc

# Constants
DEFAULT_DEPTH = 7
MAX_DEPTH = 15
INTERVAL = globaladc.get_flicker_delay()
TEXT_FLICKER_OFF = "Flicker is Off Press to Change"
TEXT_FLICKER_ON = "Flicker is On Press to Change"

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
            if not self.isRunning:
                break
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
        Form.setObjectName("FlickerDemo")
        Form.resize(1024, 600)
        Form.setStyleSheet("background-color:#000000;")
        
        # Initialize variables
        self.flicker_bool = True
        self.threadCreated = False
        self.depth_value = DEFAULT_DEPTH
        self._prepared = False
        
        # Setup UI components
        self.setupHeader(Form)
        self.setupMainContent(Form)
        self.setupSideMenu(Form)
        self.setupControls()
        
        # Initialize LED state
        try:
            globaladc.all_led_off()
            globaladc.blue_led_on()
        except Exception as e:
            print(f"Error initializing LED: {str(e)}")

    def setupHeader(self, Form):
        # Top header frame
        self.header_frame = QtWidgets.QFrame(Form)
        self.header_frame.setGeometry(QtCore.QRect(0, 0, 1024, 40))
        self.header_frame.setStyleSheet("background-color:#1f2836;")
        
        # Company name label
        self.company_label = QtWidgets.QLabel(self.header_frame)
        self.company_label.setGeometry(QtCore.QRect(60, 0, 900, 41))
        font = QtGui.QFont("Helvetica Neue", 16)
        font.setBold(True)
        self.company_label.setFont(font)
        self.company_label.setStyleSheet("color:white;")
        self.company_label.setText("Macular Densitometer                                                          Flicker Demo")
        
        # Version label
        self.version_label = QtWidgets.QLabel(self.header_frame)
        self.version_label.setGeometry(QtCore.QRect(930, 0, 71, 41))
        self.version_label.setStyleSheet("color:white;")
        self.version_label.setText("V1.0")

    def setupMainContent(self, Form):
        # Main content frame
        self.content_frame = QtWidgets.QFrame(Form)
        self.content_frame.setGeometry(QtCore.QRect(280, 100, 711, 441))
        self.content_frame.setStyleSheet("""
            QFrame {
                background-color:#1f2836;
                border-radius:30px;
            }
        """)
        
        # Depth label
        self.depth_label = QtWidgets.QLabel(self.content_frame)
        self.depth_label.setGeometry(QtCore.QRect(100, 40, 131, 61))
        font = QtGui.QFont("Helvetica Rounded", 18)
        font.setBold(True)
        self.depth_label.setFont(font)
        self.depth_label.setStyleSheet("color:white;")
        self.depth_label.setText("Depth")
        self.depth_label.setAlignment(Qt.AlignCenter)
        
        # Control buttons frame
        self.control_frame = QtWidgets.QFrame(self.content_frame)
        self.control_frame.setGeometry(QtCore.QRect(50, 120, 191, 221))
        
        # Up button
        self.upButton = QtWidgets.QPushButton(self.control_frame)
        self.upButton.setGeometry(QtCore.QRect(70, 10, 60, 60))
        self.upButton.setStyleSheet("""
            QPushButton {
                background-color: #f56c87;
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
        
        # Depth display
        self.numberLabel = QtWidgets.QLabel(self.control_frame)
        self.numberLabel.setGeometry(QtCore.QRect(60, 86, 80, 60))
        font = QtGui.QFont("Helvetica Rounded", 28)
        font.setBold(True)
        self.numberLabel.setFont(font)
        self.numberLabel.setStyleSheet("""
            background-color: black;
            color: white;
            padding: 5px;
            border: 2px solid white;
            border-radius: 5px;
        """)
        self.numberLabel.setAlignment(Qt.AlignCenter)
        self.numberLabel.setText(str(self.depth_value))
        
        # Down button
        self.downButton = QtWidgets.QPushButton(self.control_frame)
        self.downButton.setGeometry(QtCore.QRect(70, 160, 60, 60))
        self.downButton.setStyleSheet("""
            QPushButton {
                background-color: #f56c87;
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
        
        # Flicker button
        self.flickerButton = QtWidgets.QPushButton(self.content_frame)
        self.flickerButton.setGeometry(QtCore.QRect(300, 150, 350, 51))
        font = QtGui.QFont("Arial", 20)
        self.flickerButton.setFont(font)
        self.flickerButton.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                border: 2px solid white;
            }
        """)
        self.flickerButton.setText(TEXT_FLICKER_OFF)
        
        # Navigation buttons
        self.exitButton = QtWidgets.QPushButton(self.content_frame)
        self.exitButton.setGeometry(QtCore.QRect(300, 350, 160, 51))
        self.homeButton = QtWidgets.QPushButton(self.content_frame)
        self.homeButton.setGeometry(QtCore.QRect(490, 350, 160, 51))
        
        button_style = """
            QPushButton {
                background-color: black;
                color: white;
                border: 2px solid white;
                border-radius: 15px;
                padding: 10px;
            }
        """
        
        for button in [self.exitButton, self.homeButton]:
            button.setStyleSheet(button_style)
            font = QtGui.QFont("Helvetica Rounded", 16)
            font.setBold(True)
            button.setFont(font)
        
        self.exitButton.setText("EXIT")
        self.homeButton.setText("HOME")

    def setupSideMenu(self, Form):
        buttons = [
            ("Flicker Demo", 150, True),
            ("CFF Fovea", 210, False),
            ("BRK Fovea", 270, False),
            ("CFF Para-Fovea", 330, False),
            ("BRK Para-Fovea", 390, False),
            ("Test Result", 450, False)
        ]
        
        for text, y, is_active in buttons:
            btn = QtWidgets.QPushButton(Form)
            btn.setGeometry(QtCore.QRect(10, y, 240, 40))
            style = f"""
                QPushButton {{
                    background-color: {'white' if is_active else 'black'};
                    color: {'black' if is_active else 'white'};
                    border: 2px solid white;
                }}
            """
            btn.setStyleSheet(style)
            font = QtGui.QFont("Arial", 20)
            btn.setFont(font)
            btn.setText(text)

    def setupControls(self):
        self.upButton.clicked.connect(self.up_button_clicked)
        self.downButton.clicked.connect(self.down_button_clicked)
        self.flickerButton.clicked.connect(self.toggle_flicker)
        self.homeButton.clicked.connect(self.on_home)
        self.exitButton.clicked.connect(self.on_exit)
        
        # Initialize button states
        self.upButton.setEnabled(False)
        self.downButton.setEnabled(False)

    def up_button_clicked(self):
        try:
            if self.depth_value < MAX_DEPTH:
                self.depth_value += 1
                self.numberLabel.setText(str(self.depth_value))
            globaladc.buzzer_1()
        except Exception as e:
            print(f"Error in up_button_clicked: {str(e)}")

    def down_button_clicked(self):
        try:
            if self.depth_value > 0:
                self.depth_value -= 1
                self.numberLabel.setText(str(self.depth_value))
            globaladc.buzzer_1()
        except Exception as e:
            print(f"Error in down_button_clicked: {str(e)}")

    def toggle_flicker(self):
        try:
            globaladc.buzzer_1()
            
            if not self.threadCreated:
                self.worker_flik = FlickerThread(INTERVAL)
                self.worker_flik.trigger.connect(self.periodic_event)
                self.threadCreated = True
            
            if self.flickerButton.text() == TEXT_FLICKER_OFF:
                self.flickerButton.setText(TEXT_FLICKER_ON)
                self.upButton.setEnabled(True)
                self.downButton.setEnabled(True)
                self.upButton.setStyleSheet(self.upButton.styleSheet().replace("#f56c87", "#a0f291"))
                self.downButton.setStyleSheet(self.downButton.styleSheet().replace("#f56c87", "#a0f291"))
                self.depth_value = DEFAULT_DEPTH
                self.numberLabel.setText(str(self.depth_value))
                if not self.worker_flik.isStarted:
                    self.worker_flik.start()
                else:
                    self.worker_flik.resume()
            else:
                self.flickerButton.setText(TEXT_FLICKER_OFF)
                self.depth_value = 0
                self.numberLabel.setText(str(self.depth_value))
                self.upButton.setEnabled(False)
                self.downButton.setEnabled(False)
                self.upButton.setStyleSheet(self.upButton.styleSheet().replace("#a0f291", "#f56c87"))
                self.downButton.setStyleSheet(self.downButton.styleSheet().replace("#a0f291", "#f56c87"))
                if self.threadCreated:
                    self.worker_flik.stop()
        except Exception as e:
            print(f"Error in toggle_flicker: {str(e)}")

    def periodic_event(self):
        try:
            if self.flicker_bool:
                globaladc.fliker(self.depth_value)
                self.flicker_bool = False
            else:
                globaladc.fliker(0)
                self.flicker_bool = True
        except Exception as e:
            print(f"Error in periodic_event: {str(e)}")

    def showEvent(self, event):
        try:
            if not self._prepared:
                globaladc.flicker_Prepair()
                globaladc.all_led_off()
                globaladc.blue_led_on()
                self._prepared = True
                
            # Reset UI state
            self.depth_value = 0
            self.numberLabel.setText(str(self.depth_value))
            self.upButton.setEnabled(False)
            self.downButton.setEnabled(False)
            self.flickerButton.setText(TEXT_FLICKER_OFF)
        except Exception as e:
            print(f"Error in showEvent: {str(e)}")
        super().showEvent(event)

    def hideEvent(self, event):
        try:
            if self.threadCreated:
                self.worker_flik.stop()
                self.worker_flik.kill()
                self.threadCreated = False
            self._prepared = False
            globaladc.all_led_off()
        except Exception as e:
            print(f"Error in hideEvent: {str(e)}")
        super().hideEvent(event)

    def on_home(self):
        self.hide()
        if 'MainScreen' in pageDisctonary:
            pageDisctonary['MainScreen'].show()

    def on_exit(self):
        self.hide()
        if 'MainScreen' in pageDisctonary:
            pageDisctonary['MainScreen'].show()

class FlickerDemo(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_FlickerDemo()
        self.ui.setupUi(self)

def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = FlickerDemo()
    window.setWindowTitle("Flicker Demo")
    window.setFixedSize(1024, 600)
    window.show()
    sys.exit(app.exec_())