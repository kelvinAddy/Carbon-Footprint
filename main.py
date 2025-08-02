# Written By Kelvin Addy

# Imports the required modules
import sys, os, time
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QHBoxLayout, QWidget, QStatusBar, QSplashScreen
from PyQt6.QtGui import QIcon, QPixmap
from ctypes import windll
from scope1 import Scope1
from scope2 import Scope2
from netzero import NetZero

# Gets the absolute path of the current script file
BASE_DIR = os.path.dirname(__file__)

# APPID to ensure windows recognizes the app icon on taskbar, does not on macos
myappid = "CarbonPanorama007"
windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

# Stylesheet for some widgets
style = """
        QGroupBox#main{
                color: green;
                font-size: 16px;
                font: bold;
        }

        QGroupBox#sub-main{
                font-size: 13px;
                font: bold;
        }
"""


class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.initialiazeUI()

    def initialiazeUI(self):
        "Set up the application window"
        self.setWindowTitle("CarbonPanorama")
        self.setMinimumSize(1350, 690)
        self.setUpMainWindow()
        self.show()



    def setUpMainWindow(self):
        "Sets up the main window with the required widgets"
        self.scope_1, self.scope_2, self.netzero = [QWidget() for _ in range(3)]
        
        self.main_tab = QTabWidget()

        # Creates a statusbar object to show a message
        statusbar = QStatusBar()
        statusbar.showMessage("CarbonPanorama 1.00")
        self.setStatusBar(statusbar)

        # Dictionary to hold widgets for self.main_tab and their respective names
        method_dict = {self.scope_1: "SCOPE 1",
                       self.scope_2: "SCOPE 2 AND SCOPE 3",
                       self.netzero: "ACHIEVE NET-ZERO"
                       }
        for key in method_dict:
            self.main_tab.addTab(key, method_dict[key])

        self.setCentralWidget(self.main_tab)
        self.createScope1Window()
        self.createScope2Window()
        self.createNetZero()

    
    def createScope1Window(self):
        "Creates the scope 1 window tab"
        scope1_wdgt = Scope1()
        scope1_wdgt_hbox = QHBoxLayout()
        scope1_wdgt_hbox.addWidget(scope1_wdgt)
        self.scope_1.setLayout(scope1_wdgt_hbox)

    def createScope2Window(self):
        "Creates the scope 2 window tab"
        scope2_wdgt = Scope2()
        scope2_wdgt_hbox = QHBoxLayout()
        scope2_wdgt_hbox.addWidget(scope2_wdgt)
        self.scope_2.setLayout(scope2_wdgt_hbox)

    def createNetZero(self):
        "Creates the Assumptions window tab"
        netzero_wdgt = NetZero()
        netzero_wdgt_hbox = QHBoxLayout()
        netzero_wdgt_hbox.addWidget(netzero_wdgt)
        self.netzero.setLayout(netzero_wdgt_hbox)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(style)
    app.setWindowIcon(QIcon(os.path.join(BASE_DIR, "./Assets/renewable-energy.png")))
    splash = QSplashScreen(QPixmap(os.path.join(BASE_DIR, "./Assets/renewable-energy.png")))
    splash.show()
    time.sleep(1)
    window = MainWindow()
    splash.finish(window)
    sys.exit(app.exec())