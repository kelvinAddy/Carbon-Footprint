# Written by Kelvin Addy

# imports required modules
import os, time
import threading
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, 
                             QGroupBox, QSpinBox, QHBoxLayout, 
                             QGridLayout, QPushButton, QPlainTextEdit, 
                             QMessageBox, QProgressBar, QComboBox)

from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression
from chatgpt import get_completion
import json
BASE_DIR = os.path.dirname(__file__)

EMISSION_CALC1 = (60 * 3.785 * 2.68 * 0.001)
EMISSION_CALC2 = (60 * 24 * 2.14 * 0.001)

class Scope1(QWidget):
    def __init__(self):
        super().__init__()
        self.initializeUI()
    
    def initializeUI(self):
        "Sets up the scope 1 window with the required widgets"
        self.createEmissionSources()
        self.createResultsAndMitigation()
        self.validatFields()

    def createEmissionSources(self):
        "Creates widgets for taking inputs on emission sources"
        self.scope1_lyt1 = QVBoxLayout()
        emission_grpbx = QGroupBox("Emission Sources")
        emission_grpbx.setMaximumSize(450,800)
        emission_grpbx.setObjectName("main")
        emission_vbox = QVBoxLayout()
        
        self.fuel_combobx = QComboBox()
        self.fuel_combobx.addItems(("Diesel", "MGO", "Natural Gas"))
        self.fuel_combobx.setMaximumSize(120, 20)
        self.fuel_combobx.setStyleSheet("font:bold")

        # Circulatory System
        circulatory_grpbx = QGroupBox("Circulatory System")
        circulatory_grpbx.setObjectName("sub-main")

        (self.mud_linedit, self.pump_linedit, self.degas_linedit,
        self.desilt_linedit, self.desand_linedit) = [QLineEdit() for _ in range(5)]
        
        for i in (self.mud_linedit, self.pump_linedit, self.degas_linedit, self.desilt_linedit, self.desand_linedit):
            i.setMaximumSize(123, 20)

        activity_label1 = QLabel("Activity")
        activity_label1.setStyleSheet("font:bold")

        self.energy_label1 = QComboBox()
        self.energy_label1.addItems(("Fuel (gal/d)", "Electricity (Kw/h)"))
        self.energy_label1.setMaximumSize(123, 20)
        self.energy_label1.setStyleSheet("font:bold")

        co2e_label1 = QLabel("Equivalent Co2 (ton)")
        co2e_label1.setStyleSheet("font:bold")
        
        (self.mud_c02e, self.pump_co2e, self.degas_c02e, self.desilt_co2e, self.desand_co2e) = [QLabel("           ---") for _ in range(5)]
        
        circulatory_grdbx = QGridLayout()
        circulatory_grdbx.addWidget(activity_label1, 0, 0)
        circulatory_grdbx.addWidget(self.energy_label1, 0, 1)
        circulatory_grdbx.addWidget(co2e_label1, 0, 2)
        circulatory_grdbx.addWidget(QLabel("Mud Mixing:"), 1, 0)
        circulatory_grdbx.addWidget(self.mud_linedit, 1, 1)
        circulatory_grdbx.addWidget(self.mud_c02e, 1, 2)
        circulatory_grdbx.addWidget(QLabel("Mud Pumping:"), 2, 0)
        circulatory_grdbx.addWidget(self.pump_linedit, 2, 1)
        circulatory_grdbx.addWidget(self.pump_co2e, 2, 2)
        circulatory_grdbx.addWidget(QLabel("Degassing:"), 3, 0)
        circulatory_grdbx.addWidget(self.degas_linedit, 3, 1)
        circulatory_grdbx.addWidget(self.degas_c02e, 3, 2)
        circulatory_grdbx.addWidget(QLabel("Desilting:"), 4, 0)
        circulatory_grdbx.addWidget(self.desilt_linedit, 4, 1)
        circulatory_grdbx.addWidget(self.desilt_co2e, 4, 2)
        circulatory_grdbx.addWidget(QLabel("Desanding:"), 5, 0)
        circulatory_grdbx.addWidget(self.desand_linedit, 5, 1)
        circulatory_grdbx.addWidget(self.desand_co2e, 5, 2)

        circulatory_grpbx.setLayout(circulatory_grdbx)
        emission_vbox.addWidget(circulatory_grpbx)
                
        # Hoisting system
        hoisting_grpbx = QGroupBox("Hoisting sytem")
        hoisting_grpbx.setObjectName("sub-main")
       
        
        activity_label2 = QLabel("Activity")
        activity_label2.setStyleSheet("font:bold")

        energy_label2 = QLabel("Fuel Consumed (gal/d)")
        energy_label2.setStyleSheet("font:bold")

        co2e_label2 = QLabel("Equivalent Co2 (ton)")
        co2e_label2.setStyleSheet("font:bold")

        self.energy_label2 = QComboBox()
        self.energy_label2.addItems(("Fuel (gal/d)", "Electricity (Kw/h)"))
        self.energy_label2.setMaximumSize(123, 20)
        self.energy_label2.setStyleSheet("font:bold")

        (self.casing_linedit, self.tripping_linedit, self.bha_linedit) = [QLineEdit() for _ in range(3)]
        for i in (self.casing_linedit, self.tripping_linedit, self.bha_linedit):
            i.setMaximumSize(120,20)

        (self.casing_co2e, self.trip_co2e, self.bha_co2e) = [QLabel("           ---") for _ in range(3)]
      
        hoisting_grdbx = QGridLayout()
        hoisting_grdbx.addWidget(activity_label2, 0, 0)
        hoisting_grdbx.addWidget(self.energy_label2, 0, 1)
        hoisting_grdbx.addWidget(co2e_label2, 0, 2)
        hoisting_grdbx.addWidget(QLabel("Running Casing:"), 1, 0)
        hoisting_grdbx.addWidget(self.casing_linedit, 1, 1)
        hoisting_grdbx.addWidget(self.casing_co2e, 1, 2)
        hoisting_grdbx.addWidget(QLabel("Running BHA:"), 2, 0)
        hoisting_grdbx.addWidget(self.bha_linedit, 2, 1)
        hoisting_grdbx.addWidget(self.bha_co2e, 2, 2)
        hoisting_grdbx.addWidget(QLabel("Tripping:"), 3, 0)
        hoisting_grdbx.addWidget(self.tripping_linedit, 3, 1)
        hoisting_grdbx.addWidget(self.trip_co2e, 3, 2)
        hoisting_grpbx.setLayout(hoisting_grdbx)
        emission_vbox.addWidget(hoisting_grpbx)

        # Rotary System
        rotary_grpbx = QGroupBox("Rotary System")
        rotary_grpbx.setObjectName("sub-main")
        
        activity_label3 = QLabel("Activity")
        activity_label3.setStyleSheet("font:bold")

        self.energy_label3 = QComboBox()
        self.energy_label3.addItems(("Fuel (gal/d)", "Electricity (Kw/h)"))
        self.energy_label3.setMaximumSize(123, 20)
        self.energy_label3.setStyleSheet("font:bold")

        co2e_label3 = QLabel("Equivalent Co2 (ton)")
        co2e_label3.setStyleSheet("font:bold")

        self.drillstring_linedit = QLineEdit()
        self.drillstring_linedit.setMaximumSize(123,20)

        self.drillstring_Co2e = QLabel("           ---")

        rotary_grdbx = QGridLayout()
        rotary_grdbx.addWidget(activity_label3, 0, 0)
        rotary_grdbx.addWidget(self.energy_label3, 0, 1)
        rotary_grdbx.addWidget(co2e_label3, 0, 2)
        rotary_grdbx.addWidget(QLabel("Drillstring rotation:"), 1, 0)
        rotary_grdbx.addWidget(self.drillstring_linedit, 1, 1)
        rotary_grdbx.addWidget(self.drillstring_Co2e, 1, 2)

        rotary_grpbx.setLayout(rotary_grdbx)
        emission_vbox.addWidget(rotary_grpbx)

        # Venting And Flaring
        flaring_grpbx = QGroupBox("Flaring And Venting")
        flaring_grpbx.setObjectName("sub-main")
        
        self.natgas_linedit = QLineEdit()
        self.natgas_linedit.setToolTip("Enter the Total natural gas produced during drilling")
        self.natgas_linedit.setMaximumSize(123,20)

        methane_label = QLabel("Methane")
        methane_label.setStyleSheet("font:bold")

        natgas_amount_label = QLabel("Amount (scf)")
        natgas_amount_label.setStyleSheet("font:bold")

        self.methane_spnbx = QSpinBox()
        self.methane_spnbx.setMaximum(100)
        self.methane_spnbx.setMinimum(0)
        self.methane_spnbx.setSuffix("    %")

        co2e_label4 = QLabel("Equivalent Co2 (ton)")
        co2e_label4.setStyleSheet("font:bold")

        self.flaring_co2e = QLabel("           ---")

        flaring_grdbx = QGridLayout()
        flaring_grdbx.addWidget(QLabel(""), 0, 0)
        flaring_grdbx.addWidget(natgas_amount_label, 0, 1)
        flaring_grdbx.addWidget(methane_label, 0, 2)
        flaring_grdbx.addWidget(co2e_label4, 0, 3)
        flaring_grdbx.addWidget(QLabel("Natural gas flared:"), 1, 0)
        flaring_grdbx.addWidget(self.natgas_linedit, 1, 1)
        flaring_grdbx.addWidget(self.methane_spnbx, 1, 2)
        flaring_grdbx.addWidget(self.flaring_co2e, 1, 3)

        flaring_grpbx.setLayout(flaring_grdbx)
        emission_vbox.addWidget(flaring_grpbx)
        
        self.calculate_emissions = QPushButton("Calculate Emissions")
        self.calculate_emissions.clicked.connect(self.calculateButton)

        emission_vbox.addWidget(self.calculate_emissions)
        emission_grpbx.setLayout(emission_vbox)
        self.scope1_lyt1.addWidget(emission_grpbx)

    
    def createResultsAndMitigation(self):
        """Creates the required widgets for displaying the carbon footprint and migitation measures"""

        # TOTAL CARBON EMISSION RESULTS
        result_grpbx = QGroupBox("Results")
        result_grpbx.setObjectName("main")

        self.total_scope1_co2e = QLabel("")
        
        results_hbox = QHBoxLayout()
        results_hbox.addWidget(QLabel("TOTAL CARBON EMISSIONS:"))
        results_hbox.addWidget(self.total_scope1_co2e)
        
        result_grpbx.setLayout(results_hbox)

        # MITIGATION
        mitigation_grpbx = QGroupBox("Mitigation")
        mitigation_grpbx.setObjectName("main")

        self.mitigate_btn = QPushButton("Mitigate")
        self.mitigate_btn.clicked.connect(self.mitigateClicked)

        self.progress_bar = QProgressBar()

        mitigation_vbox = QVBoxLayout()
        self.mitigation_plaintext = QPlainTextEdit()
        mitigation_vbox.addWidget(self.mitigation_plaintext)
        mitigation_vbox.addWidget(self.mitigate_btn)
        mitigation_vbox.addWidget(self.progress_bar)
        mitigation_grpbx.setLayout(mitigation_vbox)

        self.scope1_lyt2 = QVBoxLayout()
        self.scope1_lyt2.addWidget(result_grpbx)
        self.scope1_lyt2.addWidget(mitigation_grpbx)

        self.scope1_main_lyt = QHBoxLayout()
        self.scope1_main_lyt.addLayout(self.scope1_lyt1)
        self.scope1_main_lyt.addLayout(self.scope1_lyt2)
        self.setLayout(self.scope1_main_lyt)
    
    def getData(self):
        """Gets the required inputs from the QLineEdits"""
        self.int_mud = float(self.mud_linedit.text())
        self.int_pump = float(self.pump_linedit.text())
        self.int_degas = float(self.degas_linedit.text())
        self.int_desilt = float(self.desilt_linedit.text())
        self.int_desand = float(self.desand_linedit.text())

        self.int_casing = float(self.casing_linedit.text())
        self.int_bha = float(self.bha_linedit.text())
        self.int_trip = float(self.tripping_linedit.text())

        self.int_drillstring = float(self.drillstring_linedit.text())

        self.int_natgas_amount = float(self.natgas_linedit.text())
        self.int_methane = int(self.methane_spnbx.value())

        self.str_energy1 = self.energy_label1.currentText()
        self.str_energy2 = self.energy_label2.currentText()
        self.str_energy3 = self.energy_label3.currentText()


    def checkForEmptyFields(self, function):
        """Checks and prompts the user if any field is empty"""
        if not all((self.mud_linedit.text(), self.pump_linedit.text(), self.degas_linedit.text(), self.desilt_linedit.text(),
                   self.desand_linedit.text(), self.casing_linedit.text(), self.bha_linedit.text(), self.tripping_linedit.text(),
                   self.drillstring_linedit.text(), self.natgas_linedit.text(), self.methane_spnbx.text())):
            
            QMessageBox.warning(self, "Empty Fields Error",
                                "Empty field found, please ensure every field is not empty!",
                                QMessageBox.StandardButton.Ok)
        else:
            function()


    def calculateEmissions(self):
        """Calculates and displays the equivalent carbon emissions for each operation"""
        self.getData()
        if self.str_energy1 == "Electricity (Kw/h)":
            mud_co2e = round(self.int_mud * EMISSION_CALC2, 2)
            self.mud_c02e.setText(f"          {mud_co2e}")
            pump_co2e = round(self.int_pump * EMISSION_CALC2, 2)
            self.pump_co2e.setText(f"          {pump_co2e}")
            degas_co2e = round(self.int_degas * EMISSION_CALC2,2)
            self.degas_c02e.setText(f"          {degas_co2e}")
            desand_co2e = round(self.int_desand * EMISSION_CALC2,2)
            self.desand_co2e.setText(f"          {desand_co2e}")
            desilt_co2e = round(self.int_desilt * EMISSION_CALC2,2)
            self.desilt_co2e.setText(f"          {desilt_co2e}")
        
        else:
            mud_co2e = round(self.int_mud * EMISSION_CALC1, 2)
            self.mud_c02e.setText(f"          {mud_co2e}")
            pump_co2e = round(self.int_pump * EMISSION_CALC1, 2)
            self.pump_co2e.setText(f"          {pump_co2e}")
            degas_co2e = round(self.int_degas * EMISSION_CALC1,2)
            self.degas_c02e.setText(f"          {degas_co2e}")
            desand_co2e = round(self.int_desand * EMISSION_CALC1,2)
            self.desand_co2e.setText(f"          {desand_co2e}")
            desilt_co2e = round(self.int_desilt * EMISSION_CALC1,2)
            self.desilt_co2e.setText(f"          {desilt_co2e}")
        
        if self.str_energy2  == "Electricity (Kw/h)":
            casing_co2e = round(self.int_casing * EMISSION_CALC2,2)
            self.casing_co2e.setText(f"          {casing_co2e}")
            bha_co2e = round(self.int_bha * EMISSION_CALC2,2)
            self.bha_co2e.setText(f"          {bha_co2e}")
            trip_co2e = round(self.int_trip * EMISSION_CALC2,2)
            self.trip_co2e.setText(f"          {trip_co2e}")
        else:
            casing_co2e = round(self.int_casing * EMISSION_CALC1,2)
            self.casing_co2e.setText(f"          {casing_co2e}")
            bha_co2e = round(self.int_bha * EMISSION_CALC1,2)
            self.bha_co2e.setText(f"          {bha_co2e}")
            trip_co2e = round(self.int_trip * EMISSION_CALC1,2)
            self.trip_co2e.setText(f"          {trip_co2e}")
        
        if self.str_energy3 == "Electricity (Kw/h)":
            drillstring_co2e = round(self.int_drillstring * EMISSION_CALC2,2)
            self.drillstring_Co2e.setText(f"          {drillstring_co2e}")
        else:
            drillstring_co2e = round(self.int_drillstring * EMISSION_CALC1,2)
            self.drillstring_Co2e.setText(f"          {drillstring_co2e}")

        methane_co2e = round(self.int_natgas_amount * self.int_methane * 0.01* 2.18,2)
        self.flaring_co2e.setText(f"          {methane_co2e}")

        # TOTAL EMISSIONS
        self.total_co2e = round(mud_co2e + pump_co2e + degas_co2e + desand_co2e + desilt_co2e + drillstring_co2e + casing_co2e + bha_co2e + trip_co2e + methane_co2e, 2)
        
        filename = os.path.join(BASE_DIR, "./Assets/scope.json")
        with open(filename, 'r') as file:
            data = json.load(file)
        if len(data) == 3: 
            data[0] = (self.total_co2e)
        else:
            data.append(self.total_co2e)
        
        with open(filename, 'w') as file:
            json.dump(data, file)

        self.total_scope1_co2e.setText(f"       {self.total_co2e} tons Co2e")


    def calculateButton(self):
        """"Links the calculating emissions to the calculate emission button"""
        try:
            self.checkForEmptyFields(self.calculateEmissions)
        except RuntimeError as error:
            QMessageBox.warning(self, "Runtime Error",
                                f"{error}", QMessageBox.StandardButton.Ok)
        except OverflowError as error:
            QMessageBox.warning(self, "Overflow Error",
                                f"{error}", QMessageBox.StandardButton.Ok)

    
    def validatFields(self):
        """Ensures every field allows entry of only numbers"""
        regex = QRegularExpression(r"^\d*[.]?\d*$")

        for i in (self.mud_linedit, self.pump_linedit, self.degas_linedit, self.desilt_linedit,
                   self.desand_linedit, self.casing_linedit, self.bha_linedit, self.tripping_linedit,
                   self.drillstring_linedit, self.natgas_linedit):
            
                i.setValidator(QRegularExpressionValidator(QRegularExpression(regex)))

    
    def post(self):
        self.prompt = f"""
                    Given these carbons emissions for these respective drilling activities, i would like you
                    present mitigation measures for these scope 1 carbon emissions,

                    1. Mud mixing: {self.mud_c02e.text()}
                    2. Mud Pumping: {self.pump_co2e.text()}
                    3. Degassing: {self.degas_c02e.text()}
                    4. Desilting: {self.desilt_co2e.text()}
                    5. Desanding: {self.desand_co2e.text()}
                    6. Running BHA: {self.bha_co2e.text()}
                    7. Tripping: {self.trip_co2e.text()}
                    8. Drillstring rotation: {self.drillstring_Co2e.text()}
                    9. Running Casing: {self.casing_co2e.text()}
                    10. Flaring and venting of natural gas: {self.flaring_co2e.text()}
                    11. Total Scope 1 emissions: {self.total_scope1_co2e.text()}
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


