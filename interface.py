import sys
import threading
import os

import keylogger
import networkscanner
import wifipasswords
import pythonexe
import httppacketsniffer

from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QGridLayout,
    QLabel,
    QWidget,
    QStackedLayout,
    QLineEdit,
    QFileDialog,
) # Import PyQt

class Window(QWidget): # Create the window

    def __init__(self):
        super().__init__()

        try:
            os.mkdir('log_folder')
        except:
            pass

        self.setWindowTitle('PyPen')
        self.setStyleSheet('''
                                QWidget{background-color: #4caef4;}
                                
                                QPushButton {
                                    background-color: #5dc99a;
                                    width: 15em;
                                    max-width: 20em;
                                    color: #ffffff;
                                    font: 20px;
                                    border-radius: 10px;
                                    padding: 12px;
                                    }

                                QPushButton:pressed {background-color: #9bebc8;}
                                QPushButton:disabled {background-color: #9bebc8;}
                                
                                QLineEdit{background-color: #ffffff}
                                QLabel{color: #ffffff; font: 15px em;}
                                QVBoxLayout{alignment: center;}
                                QLineEdit{max-width: 100px;}
                            ''')

        self.stackedLayout = QStackedLayout() # Create the stack that will contain all the layouts(pages)
        
        layout = QVBoxLayout() # Create the main vertical layout
        layoutWidget = QWidget()
        layoutWidget.setLayout(layout)

        logo = QLabel(self)
        #logo.setMaximumSize(QSize(40,40))
        logo_image = QPixmap('logo.png')
        logo.setPixmap(logo_image)
        logo_layout = QVBoxLayout()
        logo_layout.addWidget(logo)
        logo_layout.setAlignment(Qt.AlignRight)
        logo_layout_widget = QWidget()
        logo_layout_widget.setLayout(logo_layout)
        layout.addWidget(logo_layout_widget)

        title_layout = QVBoxLayout()
        title_text = QLabel('<p style="font-size: 50px; font-weight: bold;">PyPen</p>')
        title_layout.addWidget(title_text)
        title_layout.setAlignment(Qt.AlignCenter)
        title_layout_widget = QWidget()
        title_layout_widget.setLayout(title_layout)

        layout.addWidget(title_layout_widget)

        layout.addWidget(QLabel('<h1>Please choose an option:</h1>')) 
        
        buttonLayout = QVBoxLayout()
        buttonLayout.setAlignment(Qt.AlignCenter)
        buttonWidget = QWidget()
        buttonWidget.setLayout(buttonLayout)
        
        layout.addWidget(buttonWidget)

        # Add key logger button to the layout
        keylogbutton = QPushButton('Key Logger')
        keylogbutton.clicked.connect(self.keyLoggerClicked)
        
        buttonLayout.addWidget(keylogbutton)
        buttonLayout.addSpacing(10)
        #-----------------------------------------------------
 
        # Add network scanner button to the layout
        networkscannerbutton = QPushButton('Network Scanner')
        networkscannerbutton.clicked.connect(self.networkscannerClicked)

        buttonLayout.addWidget(networkscannerbutton)
        buttonLayout.addSpacing(10)
        #-----------------------------------------------------

        # Add wifi password button to the layout
        wifipasswordsbutton = QPushButton('Wifi Passwords')
        wifipasswordsbutton.clicked.connect(self.wifiPasswordsClicked)

        buttonLayout.addWidget(wifipasswordsbutton)
        buttonLayout.addSpacing(10)
        # ----------------------------------------------------
        
        # Add python to exe button to the layout
        pythonexebutton = QPushButton('Python to EXE') 
        pythonexebutton.clicked.connect(self.pythonExeClicked)

        buttonLayout.addWidget(pythonexebutton)
        buttonLayout.addSpacing(10)
        # ----------------------------------------------------


        # Add http packet sniffer to the layout
        httpsnifferbutton = QPushButton('HTTP Sniffer')
        httpsnifferbutton.clicked.connect(self.httpSnifferClicked)

        buttonLayout.addWidget(httpsnifferbutton)
        buttonLayout.addSpacing(10)
        # ----------------------------------------------------

        self.stackedLayout.addWidget(layoutWidget)
        self.stackedLayout.addWidget(self.keyLoggerLayout())
        self.stackedLayout.addWidget(self.networkScannerLayout())
        self.stackedLayout.addWidget(self.wifiPasswordsLayout())  
        self.stackedLayout.addWidget(self.pythonExeLayout())
        self.stackedLayout.addWidget(self.httpSnifferLayout())

        self.setLayout(self.stackedLayout) # Set the layout on the application's window
    
    # ------------------------ keylogger interface functions -------------------------
    def keyLoggerLayout(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        layout.addWidget(QLabel('<h2>This is the keylogger page</h2>'))

        layout.addSpacing(100)

        self.keyLoggerResults = QLabel()
        self.keyLoggerResults.setDisabled(True)
        self.keyLoggerResults.wordWrap()
        layout.addWidget(self.keyLoggerResults)

        self.keyLoggerStartButton = QPushButton('Start key logger')
        self.keyLoggerStartButton.clicked.connect(self.keyLoggerStartClicked)
        layout.addWidget(self.keyLoggerStartButton)

        self.keyLoggerEndButton = QPushButton('End key logger')
        self.keyLoggerEndButton.setDisabled(True)
        self.keyLoggerEndButton.clicked.connect(self.keyLoggerEndClicked)
        layout.addWidget(self.keyLoggerEndButton)

        homeButton = QPushButton('Home')
        homeButton.clicked.connect(self.homeClicked)
        layout.addWidget(homeButton)

        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def keyLoggerClicked(self):
        self.stackedLayout.setCurrentIndex(1)
    
    def homeClicked(self):
        self.stackedLayout.setCurrentIndex(0)
    
    def keyLoggerStartClicked(self): # called when the keylogger start button is pressed
        self.kl = keylogger.KeyLogger()
        self.keyLoggerStartButton.setDisabled(True)
        self.keyLoggerEndButton.setDisabled(False)
        self.kl.start_recording() # key logger is started
    
    def keyLoggerEndClicked(self): # called when the keylogger end button is pressed
        self.keyLoggerStartButton.setDisabled(False) 
        self.keyLoggerEndButton.setDisabled(True)
        self.kl.stop_recording() # key logger is stopped

        self.keyLoggerResults.setText(f'<h3>{self.kl.log}</h3>')
    # --------------------------------------------------------------------------------

    # --------------------- Network scanner interface functions ----------------------

    def networkScannerLayout(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel('<h2>Network scanner</h2>'))
        layout.setAlignment(Qt.AlignCenter)

        layout.addWidget(QLabel('Start Ip'))
        self.networkscannerStartIp = QLineEdit()
        layout.addWidget(self.networkscannerStartIp)

        layout.addWidget(QLabel('End Ip'))
        self.networkscannerEndIp = QLineEdit()
        layout.addWidget(self.networkscannerEndIp)

        scanButton = QPushButton('Scan network')
        scanButton.clicked.connect(self.scanNetwork)
        layout.addWidget(scanButton)

        self.networkscannerResults = QWidget()
        layout.addWidget(self.networkscannerResults)
        layout.addSpacing(30)

        homeButton = QPushButton('Home')
        homeButton.clicked.connect(self.homeClicked)
        layout.addWidget(homeButton)

        widget = QWidget()
        widget.setLayout(layout)

        return widget

    def networkscannerClicked(self):
        self.stackedLayout.setCurrentIndex(2)

    def scanNetwork(self):
        results = networkscanner.start(int(self.networkscannerStartIp.text()), int(self.networkscannerEndIp.text()))
        try:
            QWidget().setLayout(self.scannerResultsLayout)
            self.scannerResultsLayout = QVBoxLayout()
        except:
            self.scannerResultsLayout = QVBoxLayout()

        for result in results:
            self.scannerResultsLayout.addWidget(QLabel(f'Ip: {result[0]["ip"]}    Mac address: {result[0]["mac"]}'))
        
        self.networkscannerResults.setLayout(self.scannerResultsLayout)
    # --------------------------------------------------------------------------------

    # -------------------------- Stored Wifi Passwords -------------------------------

    def wifiPasswordsLayout(self):

        self.wifiLayout = QVBoxLayout()
        self.wifiLayout.addWidget(QLabel('<h2>Saved Wifi passwords</h2>'))
        self.wifiLayout.setAlignment(Qt.AlignCenter)
        self.wifiLayout.addSpacing(30)

        getPasswordsButton = QPushButton('Get passwords')
        getPasswordsButton.clicked.connect(self.getPasswords)
        self.wifiLayout.addWidget(getPasswordsButton)
        self.wifiLayout.addSpacing(30)

        self.wifiPasswordsResult = QWidget()
        self.wifiLayout.addWidget(self.wifiPasswordsResult)
        self.wifiLayout.addSpacing(30)

        homeButton = QPushButton('Home')
        homeButton.clicked.connect(self.homeClicked)
        self.wifiLayout.addWidget(homeButton)

        widget = QWidget()
        widget.setLayout(self.wifiLayout)

        return widget

    def wifiPasswordsClicked(self):
        self.stackedLayout.setCurrentIndex(3)
        
    def getPasswords(self):
        
        profiles = wifipasswords.get_wifi_passwords()

        try:
            QWidget().setLayout(self.wifiPasswordResultsLayout)
            self.wifiPasswordResultsLayout = QVBoxLayout()
        except:
            self.wifiPasswordResultsLayout = QVBoxLayout()

        for profile in profiles:
            self.wifiPasswordResultsLayout.addWidget(QLabel(f'Name: {profile}         Password: {profiles[profile]}'))

        self.wifiPasswordsResult.setLayout(self.wifiPasswordResultsLayout)

    # --------------------------------------------------------------------------------

    # ---------------------------- Python to exe functions ---------------------------

    def pythonExeLayout(self):

        exeLayout = QVBoxLayout()
        exeLayout.addWidget(QLabel('<h2>Python to exe:<h2>'))
        exeLayout.setAlignment(Qt.AlignCenter)


        self.chooseFileButton = QPushButton('Choose file')
        self.chooseFileButton.clicked.connect(self.enablePythonFileSelection)
        exeLayout.addWidget(self.chooseFileButton)

        self.chosenFileLabel = QLabel('')
        exeLayout.addWidget(self.chosenFileLabel)

        self.convertToExeButton = QPushButton('Convert to exe')
        self.convertToExeButton.clicked.connect(self.convertToExe)
        self.convertToExeButton.setDisabled(True)
        exeLayout.addWidget(self.convertToExeButton)

        homeButton = QPushButton('Home')
        homeButton.clicked.connect(self.homeClicked)
        exeLayout.addWidget(homeButton)

        widget = QWidget()
        widget.setLayout(exeLayout)

        return widget

    def pythonExeClicked(self):
        self.stackedLayout.setCurrentIndex(4)

    def enablePythonFileSelection(self):
        self.chosenFile = QFileDialog.getOpenFileName(filter="Python File (*.py)")[0]
        self.chosenFileLabel.setText(f'Chosen file directory: {self.chosenFile}')
        self.convertToExeButton.setDisabled(False)

    def convertToExe(self):
        pythonexe.convert(self.chosenFile)
# ------------------------------------------------------------------------------------

# ------------------------------- Http sniffer functions -----------------------------

    def httpSnifferLayout(self):
        sniffLayout = QVBoxLayout()
        sniffLayout.addWidget(QLabel('<h2>Http sniffer:</h2>'))
        sniffLayout.setAlignment(Qt.AlignCenter)

        self.startSniffingButton = QPushButton('Start http sniffer')
        self.startSniffingButton.clicked.connect(self.startSniffing)
        sniffLayout.addWidget(self.startSniffingButton)


        sniffLayout.addWidget(QLabel('Exit program to stop sniffing'))

        homeButton = QPushButton('Home')
        homeButton.clicked.connect(self.homeClicked)
        sniffLayout.addWidget(homeButton)

        widget = QWidget()
        widget.setLayout(sniffLayout)

        return widget

    def startSniffing(self):
        self.startSniffingButton.setDisabled(True)

        self.thread = threading.Thread(target=httppacketsniffer.sniff_packets)
        self.thread.start()

    def httpSnifferClicked(self):
        self.stackedLayout.setCurrentIndex(5)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.resize(700,700)
    window.show()
    sys.exit(app.exec_())