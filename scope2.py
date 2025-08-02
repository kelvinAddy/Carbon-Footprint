# Written by Kelvin Addy

# Imports the required modules
import os, threading
from PyQt6.QtWidgets import (QWidget, QLineEdit, QLabel,
                             QVBoxLayout, QHBoxLayout, QPushButton,
                             QMessageBox,QGroupBox, QProgressBar, 
                             QComboBox, QFormLayout, QPlainTextEdit)

from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression
from chatgpt import get_completion
import json

BASE_DIR = os.path.dirname(__file__)

EMISSION_DIESEL = (2.68 * 0.001)
EMISSION_MGO = (4.68 * 0.001)
EMISSION_OIL = (46.8 * 0.001)



class Scope2(QWidget):
    def __init__(self):
        super().__init__()
        self.initializeUI()
    

    def initializeUI(self):
        """Sets up the scope 2 and 3 window with the required widgets"""
        self.createScope2AndScope3Sources()
        self.createResultsAndMitigation()
        self.validateFields()

    
    def createScope2AndScope3Sources(self):
        """Creates the required widgets for user inputs for scope 2"""
        # SCOPE 2 EMISSION SOURCES
        scope2_grpbx = QGroupBox("Scope 2")
        scope2_grpbx.setObjectName("main")
        
        drillrig_grpbx = QGroupBox("DrillRig Transportation")
        drillrig_grpbx.setObjectName("sub-main")

        self.fuel_combobx = QComboBox()
        self.fuel_combobx.addItems(("Diesel", "MGO"))
        self.fuel_combobx.setMaximumSize(120, 20)
        self.fuel_consumed_linedit = QLineEdit()
        self.distance_linedit = QLineEdit()
        self.scope2_co2e = QLabel("             ----")

        drillrig_frmlyt = QFormLayout()
        drillrig_frmlyt.addRow(QLabel("Fuel Used:"), self.fuel_combobx)
        drillrig_frmlyt.addRow(QLabel("Fuel Consumed (gal/km):"), self.fuel_consumed_linedit)
        drillrig_frmlyt.addRow(QLabel("Distance to site (km):"), self.distance_linedit)
        drillrig_frmlyt.addRow(QLabel("Equivalent Co2 (ton):"), self.scope2_co2e)
        drillrig_frmlyt.setSpacing(20)

        drillrig_grpbx.setLayout(drillrig_frmlyt)
        drillrig_vbox = QVBoxLayout()
        drillrig_vbox.addWidget(drillrig_grpbx)
        scope2_grpbx.setLayout(drillrig_vbox)
        scope2_grpbx.setMaximumWidth(400)

        # SCOPE 3 EMISSION SOURCES
        scope3_grpbx = QGroupBox("Scope 3")
        scope3_grpbx.setObjectName("main")
        scope3_grpbx.setMaximumWidth(400)

        self.crude_amount_linedit = QLineEdit()
        self.total_cost_linedit = QLineEdit()
        self.drillcost_linedit = QLineEdit()
        self.oil_equivalent = QLabel("              ----")
        self.scope3_co2e = QLabel("               ----")

        scope3_frmlyt = QFormLayout()
        scope3_frmlyt.addRow(QLabel("Crude Oil Produced (bbl):"), self.crude_amount_linedit)
        scope3_frmlyt.addRow(QLabel("Total cost of Operation ($):"), self.total_cost_linedit)
        scope3_frmlyt.addRow(QLabel("Drilling cost ($):"), self.drillcost_linedit)
        scope3_frmlyt.addRow(QLabel("Oil Equivalent of drilling (bbl):"), self.oil_equivalent)
        scope3_frmlyt.addRow(QLabel("Equivalent Co2 (ton):"), self.scope3_co2e)
        scope3_frmlyt.setSpacing(20)

        scope3_grpbx.setLayout(scope3_frmlyt)

        self.calculate_emissions_btn = QPushButton("Calculate Emissions")
        self.calculate_emissions_btn.clicked.connect(self.calculatebtnClicked)

        # Layout for groupboxes 
        self.scopes_vbox1 = QVBoxLayout()
        self.scopes_vbox1.addWidget(scope2_grpbx)
        self.scopes_vbox1.addWidget(scope3_grpbx)
        self.scopes_vbox1.addWidget(self.calculate_emissions_btn)

    def validateFields(self):
        """Ensures every field allows entry of only numbers"""
        regex = QRegularExpression(r"^\d*[.]?\d*$")

        for i in (self.crude_amount_linedit, self.total_cost_linedit, self.drillcost_linedit, 
                    self.fuel_consumed_linedit, self.distance_linedit):            
                i.setValidator(QRegularExpressionValidator(QRegularExpression(regex)))
                i.setMaximumSize(120, 20)


    def createResultsAndMitigation(self):
        """Creates the required widgets for displaying the carbon footprint and migitation measures"""

        # TOTAL CARBON EMISSION RESULTS
        result_grpbx = QGroupBox("Results")
        result_grpbx.setObjectName("main")

        self.total_scope2_co2e = QLabel("")
        
        results_hbox = QHBoxLayout()
        results_hbox.addWidget(QLabel("TOTAL CARBON EMISSIONS:"))
        results_hbox.addWidget(self.total_scope2_co2e)
        
        result_grpbx.setLayout(results_hbox)

        # MITIGATION
        mitigation_grpbx = QGroupBox("Mitigation")
        mitigation_grpbx.setObjectName("main")

        self.mitigate_btn = QPushButton("Mitigate")
        self.mitigate_btn.clicked.connect(self.mitigateClicked)

        mitigation_vbox = QVBoxLayout()
        self.mitigation_plaintext = QPlainTextEdit()
        mitigation_vbox.addWidget(self.mitigation_plaintext)
        mitigation_grpbx.setLayout(mitigation_vbox)

        self.progress_bar = QProgressBar()

        self.scopes_vbox2 = QVBoxLayout()
        self.scopes_vbox2.addWidget(result_grpbx)
        self.scopes_vbox2.addWidget(mitigation_grpbx)
        self.scopes_vbox2.addWidget(self.mitigate_btn)
        self.scopes_vbox2.addWidget(self.progress_bar)

        self.scopes_main_lyt = QHBoxLayout()
        self.scopes_main_lyt.addLayout(self.scopes_vbox1)
        self.scopes_main_lyt.addLayout(self.scopes_vbox2)
        self.setLayout(self.scopes_main_lyt)
    
    def getData(self):
        """Gets the required inputs from the QLineEdits"""
        self.int_fuel_consumed = float(self.fuel_consumed_linedit.text())
        self.int_distance = float(self.distance_linedit.text())
        self.str_fuel = self.fuel_combobx.currentText()

        self.int_crude_amount = float(self.crude_amount_linedit.text())
        self.int_total_cost = float(self.total_cost_linedit.text())
        self.int_drill_cost = float(self.drillcost_linedit.text())

    def checkForEmptyFields(self, function):
        """Checks and prompts the user if any field is empty"""
        if not all((self.fuel_consumed_linedit.text(), self.distance_linedit.text(), self.crude_amount_linedit.text(), 
                    self.total_cost_linedit.text(),self.drillcost_linedit.text())):
            
            QMessageBox.warning(self, "Empty Fields Error",
                                "Empty field found, please ensure every field is not empty!",
                                QMessageBox.StandardButton.Ok)
        else:
            function()
    
    def calculateEmissions(self):
        """Calculates and displays the equivalent carbon emissions for each operation"""
        self.getData()
        
        # SCOPE 2
        if self.str_fuel == "Diesel":
            scope2_co2e = round(EMISSION_DIESEL * self.int_distance * self.int_fuel_consumed, 2)
        else:
            scope2_co2e = round(EMISSION_MGO * self.int_distance * self.int_fuel_consumed, 2)
        self.scope2_co2e.setText(f"         {scope2_co2e}")

        filename = os.path.join(BASE_DIR, "./Assets/scope.json")

        with open(filename, 'r') as file:
            data = json.load(file)
        if len(data) == 3: 
            data[1] = (scope2_co2e)
        else:
            data.append(scope2_co2e)
        
        with open(filename, 'w') as file:
            json.dump(data, file)


        # SCOPE 3
        scope3_co2e = round(self.int_crude_amount * (self.int_drill_cost/self.int_total_cost) * EMISSION_OIL, 2)
        
        with open(filename, 'r') as file:
            data = json.load(file)
        if len(data) == 3: 
            data[2] = (scope3_co2e)
        else:
            data.append(scope3_co2e)
        
        with open(filename, 'w') as file:
            json.dump(data, file)
        
        
        self.scope3_co2e.setText(f"         {scope3_co2e}")
        self.oil_equivalent.setText(f"          {self.int_crude_amount * (self.int_drill_cost/self.int_total_cost)}")

        # TOTAL EMISSIONS
        self.total_emissions = (scope2_co2e + scope3_co2e)
        self.total_scope2_co2e.setText(f"           {self.total_emissions} tons Co2e")


    def calculatebtnClicked(self):
        self.checkForEmptyFields(self.calculateEmissions)
        
    def post(self):
        self.prompt = f"""
                    Given these carbons emissions for scope 2 and scope 3 of a typical oil well drilling operation, i would like you
                    present mitigation measures for these scope 2 and scope 3 carbon emissions,

                    1. Scope 2: {self.scope2_co2e.text()}
                    2. Scope 3: {self.scope3_co2e.text()}
                    """
        
        try:
            self.response = get_completion(self.prompt)
            self.mitigation_plaintext.setPlainText(self.response)
        except:
            QMessageBox.warning(self, "Network Error", 
                        "Error establishin network with GPT 3.5 model", QMessageBox.StandardButton.Ok)


    
    def mitigateEmissions(self):
        """Gets mitigation measures from chatgpt and displays to the user"""
        # Creates a seperate thread for this function process to improve performance
        t = threading.Thread(target=self.post)
        t.start()
        
        i = 0
        # Fills the progress bar as long as the function process is not dead
        while t.is_alive():
            self.progress_bar.setValue(i)
            i+=1
        self.progress_bar.setValue(0)

    
    def mitigateClicked(self):
         self.checkForEmptyFields(self.mitigateEmissions)
    

