from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import sys
import time
from PyQt5.QtCore import QThread, pyqtSignal
from globalvar import pageDisctonary, globaladc


class FlickerThread(QThread):
    """Thread class for handling periodic flicker events"""
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
        """Set up the main UI components"""
        self.Form = Form
        Form.setObjectName("FlickerDemo")
        Form.resize(1024, 600)
        Form.setStyleSheet("background-color:#000000;")
        
        # Initialize state variables
        self.flicker_bool = True
        self.threadCreated = False
        self.depth_value = 7
        self.max_depth = 15
        self.interval = globaladc.get_flicker_delay()
        self.is_prepared = False
        
        # Create main layout
        self.setupMainFrame(Form)
        self.setupTopBar(Form)
        self.setupSideMenu(Form)
        self.setupCentralWidget(Form)
        self.setupControls()
        self.retranslateUi()
        
        # Initialize LED
        try:
            globaladc.all_led_off()  # Turn off all LEDs initially
            globaladc.blue_led_on()  # Turn on blue LED
        except Exception as e:
            print(f"Error initializing LED: {str(e)}")
        
        # Set window title
        Form.setWindowTitle("Flicker Demo")
        
        # Initialize button states
        self.upButton.setEnabled(False)
        self.downButton.setEnabled(False)

    def setupMainFrame(self, Form):
        """Set up the main frame"""
        self.main_frame = QtWidgets.QFrame(Form)
        self.main_frame.setGeometry(QtCore.QRect(280, 100, 711, 441))
        self.main_frame.setStyleSheet("""
            QFrame {
                background-color:#1f2836;
                border-radius:30px;
            }
        """)
        self.main_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.main_frame.setFrameShadow(QtWidgets.QFrame.Raised)

    def setupTopBar(self, Form):
        """Set up the top bar"""
        self.top_frame = QtWidgets.QFrame(Form)
        self.top_frame.setGeometry(QtCore.QRect(0, 0, 1024, 40))
        self.top_frame.setStyleSheet("background-color:#1f2836;")
        
        # Company name label
        self.company_label = QtWidgets.QLabel(self.top_frame)
        self.company_label.setGeometry(QtCore.QRect(60, 0, 281, 41))
        font = QtGui.QFont("Helvetica Neue", 16)
        font.setBold(True)
        self.company_label.setFont(font)
        self.company_label.setStyleSheet("color:white;")
        
        # Version label
        self.version_label = QtWidgets.QLabel(self.top_frame)
        self.version_label.setGeometry(QtCore.QRect(930, 0, 71, 41))
        self.version_label.setStyleSheet("color:white;")

    def setupSideMenu(self, Form):
        """Set up the side menu buttons"""
        button_data = [
            ("Flicker Demo", 150, True),  # Active button
            ("CFF Fovea", 210, False),
            ("BRK Fovea", 270, False),
            ("CFF Para-Fovea", 330, False),
            ("BRK Para-Fovea", 390, False),
            ("Test Result", 450, False)
        ]
        
        for text, y_pos, is_active in button_data:
            btn = QtWidgets.QPushButton(Form)
            btn.setGeometry(QtCore.QRect(10, y_pos, 240, 40))
            style = """
                QPushButton {
                    background-color: white;
                    color: black;
                    border: 2px solid white;
                }
            """ if is_active else """
                QPushButton {
                    background-color: black;
                    color: white;
                    border: 2px solid white;
                }
            """
            btn.setStyleSheet(style)
            btn.setText(text)
            font = QtGui.QFont("Helvetica Neue", 16)
            btn.setFont(font)

    def setupCentralWidget(self, Form):
        """Set up the central widget area"""
        # Depth control frame
        self.depth_frame = QtWidgets.QFrame(self.main_frame)
        self.depth_frame.setGeometry(QtCore.QRect(50, 120, 191, 221))
        
        # Depth label
        self.depth_label = QtWidgets.QLabel(self.main_frame)
        self.depth_label.setGeometry(QtCore.QRect(100, 40, 131, 61))
        font = QtGui.QFont("Helvetica Rounded", 18)
        font.setBold(True)
        self.depth_label.setFont(font)
        self.depth_label.setStyleSheet("color:white;")
        
        # Up button
        self.upButton = QtWidgets.QPushButton(self.depth_frame)
        self.upButton.setGeometry(QtCore.QRect(70, 10, 60, 60))
        self.upButton.setStyleSheet(self.get_button_style())
        self.upButton.setText("+")
        
        # Depth display
        self.numberLabel = QtWidgets.QLabel(self.depth_frame)
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
        self.downButton = QtWidgets.QPushButton(self.depth_frame)
        self.downButton.setGeometry(QtCore.QRect(70, 160, 60, 60))
        self.downButton.setStyleSheet(self.get_button_style())
        self.downButton.setText("-")
        
        # Flicker status label
        self.status_label = QtWidgets.QLabel(self.main_frame)
        self.status_label.setGeometry(QtCore.QRect(350, 170, 240, 50))
        self.status_label.setStyleSheet("color: white;")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setText("Press Button\nTo ON/OFF")
        font = QtGui.QFont("Helvetica Rounded", 14)
        font.setBold(True)
        self.status_label.setFont(font)
        
        # Flicker control button
        self.flickerButton = QtWidgets.QPushButton(self.main_frame)
        self.flickerButton.setGeometry(QtCore.QRect(350, 90, 240, 51))
        self.flickerButton.setStyleSheet(self.get_control_button_style())
        
        # Navigation buttons
        self.homeButton = QtWidgets.QPushButton(self.main_frame)
        self.homeButton.setGeometry(QtCore.QRect(490, 350, 160, 51))
        self.homeButton.setStyleSheet(self.get_control_button_style())
        
        self.exitButton = QtWidgets.QPushButton(self.main_frame)
        self.exitButton.setGeometry(QtCore.QRect(300, 350, 160, 51))
        self.exitButton.setStyleSheet(self.get_control_button_style())

    def setupControls(self):
        """Set up control connections"""
        self.upButton.clicked.connect(self.up_button_clicked)
        self.downButton.clicked.connect(self.down_button_clicked)
        self.flickerButton.clicked.connect(self.toggle_flicker)
        self.homeButton.clicked.connect(self.on_home)
        self.exitButton.clicked.connect(self.on_exit)

    def get_button_style(self):
        """Get style for control buttons"""
        return """
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
            QPushButton:pressed {
                background-color: #177bad;
            }
            QPushButton {
                text-align: center;
                padding-bottom: 9px;
            }
        """

    def get_control_button_style(self):
        """Get style for main control buttons"""
        return """
            QPushButton {
                background-color: black;
                color: white;
                border: none;
                border-radius: 15px;
                padding: 10px;
                border: 2px solid white;
                font-family: 'Helvetica Rounded';
                font-size: 16pt;
                font-weight: bold;
            }
        """

    def retranslateUi(self):
        """Set up text for UI elements"""
        _translate = QtCore.QCoreApplication.translate
        self.depth_label.setText(_translate("Form", "Depth"))
        self.company_label.setText(_translate("Form", "Vekaria Healthcare"))
        self.version_label.setText(_translate("Form", "V1.0"))
        self.flickerButton.setText(_translate("Form", "Flicker On"))
        self.homeButton.setText(_translate("Form", "HOME"))
        self.exitButton.setText(_translate("Form", "EXIT"))

    def up_button_clicked(self):
        """Handle up button click"""
        try:
            if self.depth_value < self.max_depth:
                self.depth_value += 1
                self.numberLabel.setText(str(self.depth_value))
            globaladc.buzzer_1()
        except Exception as e:
            print(f"Error in up_button_clicked: {str(e)}")

    def down_button_clicked(self):
        """Handle down button click"""
        try:
            if self.depth_value > 0:
                self.depth_value -= 1
                self.numberLabel.setText(str(self.depth_value))
            globaladc.buzzer_1()
        except Exception as e:
            print(f"Error in down_button_clicked: {str(e)}")

    def toggle_flicker(self):
        """Toggle flicker state"""
        try:
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
        except Exception as e:
            print(f"Error in toggle_flicker: {str(e)}")

    def periodic_event(self):
        """Handle periodic flicker event"""
        try:
            if self.flicker_bool:
                globaladc.fliker(self.depth_value)
                self.flicker_bool = False
            else:
                globaladc.fliker(0)
                self.flicker_bool = True
        except Exception as e:
            print(f"Error in periodic_event: {str(e)}")

    def show(self):
        """Show the window"""
        try:
            if not self.is_prepared:
                globaladc.all_led_off()  # Ensure all LEDs are off
                globaladc.blue_led_on()  # Turn on blue LED
                globaladc.flicker_Prepair()
                self.is_prepared = True
            self.Form.show()
            self.depth_value = 0
            self.numberLabel.setText(str(self.depth_value))
            self.upButton.setEnabled(False)
            self.downButton.setEnabled(False)
            self.flickerButton.setText("Flicker On")
        except Exception as e:
            print(f"Error in show method: {str(e)}")

    def hide(self):
            """Hide the window"""
            try:
                if self.threadCreated:
                    self.worker_flik.stop()
                    self.worker_flik.kill()
                    self.threadCreated = False
                self.is_prepared = False
                globaladc.all_led_off()  # Turn off all LEDs when hiding
                self.Form.hide()
            except Exception as e:
                print(f"Error in hide method: {str(e)}")

    def on_home(self):
        """Handle home button click"""
        self.hide()
        if 'MainScreen' in pageDisctonary:
            pageDisctonary['MainScreen'].show()

    def on_exit(self):
        """Handle exit button click"""
        self.hide()
        if 'MainScreen' in pageDisctonary:
            pageDisctonary['MainScreen'].show()

class FlickerDemo(QtWidgets.QWidget):
    """Main FlickerDemo widget class"""
    def __init__(self):
        super().__init__()
        self.ui = Ui_FlickerDemo()
        self.ui.setupUi(self)
        self._prepared = False
        
    def show(self):
        """Show the widget"""
        if not self._prepared:
            try:
                self.ui.show()
                self._prepared = True
            except Exception as e:
                print(f"Error preparing FlickerDemo: {str(e)}")
        else:
            self.ui.show()
        
    def hide(self):
        """Hide the widget"""
        self.ui.hide()
        self._prepared = False

def main():
    """Main application entry point"""
    app = QtWidgets.QApplication(sys.argv)
    window = FlickerDemo()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()