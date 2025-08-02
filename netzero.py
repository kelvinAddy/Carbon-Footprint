import os, threading
from PyQt6.QtWidgets import (QWidget, QGroupBox, QVBoxLayout, 
                             QHBoxLayout, QPushButton,QMessageBox, 
                             QSpinBox, QLabel, QPlainTextEdit)                            
import matplotlib
matplotlib.rcParams.update({'font.size':8})
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from chatgpt import get_completion
import json

BASE_DIR = os.path.dirname(__file__)


class CreateCanvas(FigureCanvasQTAgg):
    def __init__(self, parent = None, nrows = 1, ncols = 1):
        # Create matplotlib figure object
        self.fig = Figure(figsize=(17,17))

        self.add_subplot()
        super().__init__(self.fig)

    def add_subplot(self):
        # Create axes and set the number of subplots 
        self.axes = self.fig.add_subplot(111)

class NetZero(QWidget):
    def __init__(self):
        super().__init__()
        self.initializeUI()
    
    def initializeUI(self):
        """Sets up the NetZero window with the rquired widgets"""
        self.createMainWindow()
    
    def createMainWindow(self):
        # EMISSION OVERVIEW
        emission_overview_grpbx = QGroupBox("Carbon Emissions Overview")
        emission_overview_grpbx.setObjectName("main")
        emission_overview_grpbx.setMaximumWidth(450)

        self.canvas1 = CreateCanvas()
        self.plot_btn = QPushButton("Plot")
        self.plot_btn.clicked.connect(self.plotBarChart)
        navigation_toolbar1 = NavigationToolbar2QT(self.canvas1)
        canvas_layout1 = QVBoxLayout()
        canvas_layout1.addWidget(navigation_toolbar1)
        canvas_layout1.addWidget(self.canvas1)
        canvas_layout1.addWidget(self.plot_btn)
        
        emission_overview_grpbx.setLayout(canvas_layout1)

        # NETZERO PLOT
        netzero_grpbx = QGroupBox("Net-Zero Overview")
        netzero_grpbx.setObjectName("main")
        netzero_grpbx.setMaximumWidth(450)
        
        self.num_years = QSpinBox()
        self.num_years.setMaximumWidth(40)
        self.num_years.setMinimum(1)
        num_years_hbox = QHBoxLayout()
        num_years_hbox.setSpacing(10)
        num_years_hbox.addWidget(QLabel("Number of years:"))
        num_years_hbox.addWidget(self.num_years)

        netzero_vbox = QVBoxLayout()
        netzero_vbox.addLayout(num_years_hbox)
        self.canvas2 = CreateCanvas()
        navigation_toolbar1 = NavigationToolbar2QT(self.canvas2)
        netzero_vbox.addWidget(navigation_toolbar1)
        netzero_vbox.addWidget(self.canvas2)


        self.netzero_btn = QPushButton("Net-Zero")
        self.netzero_btn.clicked.connect(self.plotNetZero)
        netzero_vbox.addWidget(self.netzero_btn)
        netzero_grpbx.setLayout(netzero_vbox)

        netzero_layout = QHBoxLayout()
        netzero_layout.addWidget(emission_overview_grpbx)
        netzero_layout.addWidget(netzero_grpbx)
        
        # NETZERO PLAN
        netzero_plan_grpbx = QGroupBox("Net-Zero Plan")
        netzero_plan_grpbx.setObjectName("main")
        
        self.plain_txt = QPlainTextEdit()
        self.netzero_plan_btn = QPushButton("Get Yearly Plan")
        self.netzero_plan_btn.clicked.connect(self.getNetZeroPlan)

        plan_vbox = QVBoxLayout()
        plan_vbox.addWidget(self.plain_txt)
        plan_vbox.addWidget(self.netzero_plan_btn)

        netzero_plan_grpbx.setLayout(plan_vbox)
        netzero_layout.addWidget(netzero_plan_grpbx)
        
        self.setLayout(netzero_layout)


    def drawOnCanvas(self, x, y):
        """Embeds a matplotlib plot figure onto the canvas"""
        # Clears the canvas and embeds a plot figure on it
        self.canvas1.fig.clear()
        self.canvas1.add_subplot()
        self.canvas1.axes.bar(x, y, color = "green")
        self.canvas1.axes.set_ylabel("ton Co2e")
        self.canvas1.draw()
    
    def plotBarChart(self):
        """Plots a pie chart of the scope emissions"""
        
        filename = os.path.join(BASE_DIR, "./Assets/scope.json")
        with open(filename, 'r') as file:
            self.data = json.load(file)
        self.drawOnCanvas(["Scope 1", "Scope 2", "Scope 3"], self.data)
    
    def yearlyCarbonReduction(self):
        "Returns a list of yearly carbon emissions if migitation is applied"
        total_emissions = sum(self.data)
        reduction_potential = (total_emissions / self.num_years.value()) * 0.3 
        emission_per_annum = total_emissions
        reduction_list = [total_emissions]
        for year in range(self.num_years.value()):
            emission_per_annum = emission_per_annum * (0.8) - reduction_potential
            reduction_list.append(emission_per_annum)
        return reduction_list
    
    def plotNetZero(self):
        """Plots the carbon emissions throughout each year"""
        self.canvas2.fig.clear()
        self.canvas2.add_subplot()
        self.canvas2.axes.bar(list(range(self.num_years.value() + 1)), self.yearlyCarbonReduction(),color = "green")
        self.canvas2.axes.set_ylabel("ton Co2e")
        self.canvas2.axes.set_xlabel("Years")
        self.canvas2.axes.set_xticks(list(range(self.num_years.value() + 1)))
        self.canvas2.draw()

    def getNetZeroPlan(self):
        self.prompt = f"""
                    Given a list of reduction targets for carbon emissions of a typical oil well drilling operation over {self.num_years.value()} years, 
                    provide detailed mitigation strategies for each year.
                    The carbon reduction targets is listed in this list: {self.yearlyCarbonReduction()}.
                    Please outline the strategies for each year to attain these reduction targets, but dont add the reduction
                    targets in your response.
                    """
        try:
            self.response = get_completion(self.prompt)
            self.plain_txt.setPlainText(self.response)
        except:
            QMessageBox(self, "Network Error", 
                        "Error establishin network with GPT 3.5 model", QMessageBox.StandardButton.Ok)