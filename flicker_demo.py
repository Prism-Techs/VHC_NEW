from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal, Qt
import time
from globalvar import pageDisctonary, globaladc
from PerodicThread import PeriodicThread

# Constants 
Text_Fliker_OFF = "Fliker is Off Press to Change"
Text_Fliker_ON = "Fliker is On Press to Change"
DEFAULT_DEPTH = 7
MAX_DEPTH = 15
INTERVAL = globaladc.get_flicker_delay()

class FlickerThread(QThread):
    trigger = pyqtSignal()
    
    def __init__(self, interval, parent=None):
        super().__init__(parent)
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



class FlickerDemo(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # Initialize variables
        self.flicker_bool = True
        self.threadCreated = False
        self.depth_value = DEFAULT_DEPTH
        self._prepared = False
        self.worker_flik = None
        self.flicker_on = False
        globaladc.blue_led_on()
        # Setup UI
        self.setupUi()
        
    def periodic_event(self):
        """Handle periodic flicker events using DAC output"""
        if self.flicker_on:
            if self.flicker_bool:
                # Apply the DAC voltage based on depth value
                globaladc.fliker(self.depth_value)  # Set DAC output with current depth
                self.flicker_bool = False
            else:
                # Reset DAC voltage to 0
                globaladc.fliker(0)
                self.flicker_bool = True

    def setupUi(self):
        self.setObjectName("FlickerDemo")
        self.resize(1024, 600)
        self.setStyleSheet("background-color:#000000;")
        
        # Setup components
        self.setupHeader()
        self.setupMainContent()
        self.setupSideMenu()
        
        # Initialize states
        self.upButton.setEnabled(False)
        self.downButton.setEnabled(False)
        
    def setupHeader(self):
        self.header_frame = QtWidgets.QFrame(self)
        self.header_frame.setGeometry(QtCore.QRect(0, 0, 1024, 40))
        self.header_frame.setStyleSheet("background-color:#1f2836;")
        
        self.title_label = QtWidgets.QLabel(self.header_frame)
        self.title_label.setGeometry(QtCore.QRect(60, 0, 900, 41))
        font = QtGui.QFont("Helvetica Neue", 16)
        font.setBold(True)
        self.title_label.setFont(font)
        self.title_label.setStyleSheet("color:white;")
        self.title_label.setText("Macular Densitometer                                                          Flicker Demo")
        
    def setupMainContent(self):
        self.main_frame = QtWidgets.QFrame(self)
        self.main_frame.setGeometry(QtCore.QRect(280, 100, 711, 441))
        self.main_frame.setStyleSheet("""
            QFrame {
                background-color:#1f2836;
                border-radius:30px;
            }
        """)
        
        # Depth label
        self.depth_label = QtWidgets.QLabel(self.main_frame)
        self.depth_label.setGeometry(QtCore.QRect(100, 40, 131, 61))
        font = QtGui.QFont("Helvetica Rounded", 18)
        font.setBold(True)
        self.depth_label.setFont(font)
        self.depth_label.setStyleSheet("color:white;")
        self.depth_label.setText("Depth")
        self.depth_label.setAlignment(Qt.AlignCenter)
        
        # Up button
        self.upButton = QtWidgets.QPushButton(self.main_frame)
        self.upButton.setGeometry(QtCore.QRect(120, 130, 60, 60))
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
        self.numberLabel = QtWidgets.QLabel(self.main_frame)
        self.numberLabel.setGeometry(QtCore.QRect(110, 206, 80, 60))
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
        self.downButton = QtWidgets.QPushButton(self.main_frame)
        self.downButton.setGeometry(QtCore.QRect(120, 280, 60, 60))
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
        
        # Flicker control button
        self.flickerButton = QtWidgets.QPushButton(self.main_frame)
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
        self.flickerButton.setText(Text_Fliker_OFF)
        
        # Connect button signals
        self.upButton.clicked.connect(self.up_button_clicked)
        self.downButton.clicked.connect(self.down_button_clicked)
        self.flickerButton.clicked.connect(self.toggle_flicker)
        
    def setupSideMenu(self):
        buttons = [
            ("Flicker Demo", 150, True),
            ("CFF Fovea", 210, False),
            ("BRK Fovea", 270, False),
            ("CFF Para-Fovea", 330, False),
            ("BRK Para-Fovea", 390, False),
            ("Test Result", 450, False)
        ]
        
        for text, y, is_active in buttons:
            btn = QtWidgets.QPushButton(self)
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

    def up_button_clicked(self):
        """Handle up button click"""
        y = self.depth_value
        if y < MAX_DEPTH:
            self.depth_value = y + 1
            self.numberLabel.setText(str(self.depth_value))
        globaladc.buzzer_1()

    def down_button_clicked(self):
        """Handle down button click"""
        if self.depth_value > 0:
            self.depth_value -= 1
            self.numberLabel.setText(str(self.depth_value))
        globaladc.buzzer_1()

    def toggle_flicker(self):
        """Toggle flicker state"""
        globaladc.buzzer_1()
        
        if not self.threadCreated:
            self.worker_flik = FlickerThread(INTERVAL, self)
            self.worker_flik.trigger.connect(self.periodic_event)
            self.threadCreated = True
            
        if self.flickerButton.text() == Text_Fliker_OFF:
            self.flickerButton.setText(Text_Fliker_ON)
            self.flicker_on = True
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
            self.flickerButton.setText(Text_Fliker_OFF)
            self.flicker_on = False
            self.depth_value = 0
            self.numberLabel.setText(str(self.depth_value))
            self.upButton.setEnabled(False)
            self.downButton.setEnabled(False)
            self.upButton.setStyleSheet(self.upButton.styleSheet().replace("#a0f291", "#f56c87"))
            self.downButton.setStyleSheet(self.downButton.styleSheet().replace("#a0f291", "#f56c87"))
            if self.threadCreated:
                self.worker_flik.stop()

                
    def showEvent(self, event):
        """Handle show event"""
        try:
            if not self._prepared:
                globaladc.flicker_Prepair()
                globaladc.all_led_off()
                globaladc.blue_led_on()  # Turn on the blue light
                self._prepared = True
            
            # Reset UI state
            self.depth_value = 0
            self.numberLabel.setText(str(self.depth_value))
            self.upButton.setEnabled(False)
            self.downButton.setEnabled(False)
            self.flickerButton.setText(Text_Fliker_OFF)
            
            # Start thread if needed
            if self.threadCreated and not self.worker_flik.isStarted:
                self.run_thread()
                
        except Exception as e:
            print(f"Error in showEvent: {str(e)}")
        super().showEvent(event)

    def hideEvent(self, event):
        """Handle hide event"""
        try:
            if self.threadCreated:
                self.stop_thread()
            self._prepared = False
            globaladc.all_led_off()  # Turn off all LEDs when hiding the screen
            
        except Exception as e:
            print(f"Error in hideEvent: {str(e)}")
        super().hideEvent(event)



def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = FlickerDemo()
    window.setWindowTitle("Flicker Demo")
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()