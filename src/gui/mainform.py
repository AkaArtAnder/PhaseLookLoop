from PyQt5.QtWidgets import (
                            QApplication, QWidget, QLabel, QLineEdit, QPushButton, 
                            QHBoxLayout, QGridLayout, QGroupBox, QComboBox, QRadioButton, 
                            QVBoxLayout, QSlider, QProgressBar, QMessageBox
)
from PyQt5.QtCore import Qt
from sympy import Matrix
from math import pi
import pickle

from src.pll.algoritm import main_algoritm
from src.gui.analyzing import correct_data, PrintSingle, PrintCompare, PrintStatistic
from src.libs.genormal import Genormal

class MainWindow(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setWindowTitle('Model PLL')
        self.count_compare = 0
        self.noise_compare = []
        self.result_data_compare = {}
        self.result_data_statistic = {}
        self.create_topGroup()
        self.create_input_dataGroupBox()
        self.create_parameters_systemGroupBox()
        self.create_select_modeGroupBox()
        self.create_statisticGroupBox()
        self.create_ProgressBar()
        mainLayout = QGridLayout()
        mainLayout.addLayout(self.topLayout, 0, 0, 1, 2)
        mainLayout.addWidget(self.input_dataGroupBox, 1, 0)
        mainLayout.addWidget(self.parameters_systemGroupBox, 1, 1)
        mainLayout.addWidget(self.select_modeGroupBox, 2, 0)
        mainLayout.addWidget(self.select_mode_statGroupBox, 2, 1)
        mainLayout.addWidget(self.progressBar, 3, 0, 1, 2)
        self.setLayout(mainLayout)
        self.run_modelButton.clicked.connect(self.click_runButton)
        self.noise_inputRadioButton_add.toggled.connect(self.click_noiseRadio)
        self.noise_inputRadioButton_nadd.toggled.connect(self.click_noiseRadio)
        self.filter_select_oneRadioButton.toggled.connect(self.click_filterRadio)
        self.filter_select_twoRadioButton.toggled.connect(self.click_filterRadio)
        self.filter_select_threeRadioButton.toggled.connect(self.click_filterRadio)
        self.select_mode_standRadioButton.toggled.connect(self.click_select_modeRadio)
        self.select_mode_statRadioButton.toggled.connect(self.click_select_modeRadio)
        self.select_mode_stand_singleRadioButton.toggled.connect(self.click_select_mode_standRadio)
        self.select_mode_stand_compareRadioButton.toggled.connect(self.click_select_mode_standRadio)
        self.mode_stand_compare_resetButton.clicked.connect(self.click_compare_resetButton)
        self.mode_stand_compare_plotButton.clicked.connect(self.click_compare_plotButton)
        self.mode_stand_compare_plot_singleButton.clicked.connect(self.click_compare_plot_singleButton)
        self.mode_stat_continueRadioButton.toggled.connect(self.click_select_mode_statRadio)
        self.mode_stat_newRadioButton.toggled.connect(self.click_select_mode_statRadio)
        self.mode_stat_loadButton.clicked.connect(self.click_stat_loadButton)
        self.mode_stat_saveButton.clicked.connect(self.click_stat_saveButton)
        self.mode_stat_continue_resetButton.clicked.connect(self.click_stat_continue_resetButton)
        self.mode_stat_new_addButton.clicked.connect(self.click_stat_new_addButton)
        self.mode_stat_continueComboBox.currentIndexChanged.connect(self.click_stat_paramButton)
        self.mode_stat_continue_calculateButton.clicked.connect(self.click_stat_calculateButton)

    def create_topGroup(self):
        self.number_of_countsText = QLineEdit()
        self.number_of_countsText.setText('200')
        number_of_countsLabel = QLabel('Number of counts: ')
        number_of_countsLabel.setBuddy(self.number_of_countsText)
        self.run_modelButton = QPushButton('Run')
        top_buttonLayout = QGridLayout()
        top_buttonLayout.addWidget(number_of_countsLabel, 0, 1)
        top_buttonLayout.addWidget(self.number_of_countsText, 0, 2)
        top_buttonLayout.addWidget(self.run_modelButton, 0, 3)
        self.topLayout = QHBoxLayout()
        self.topLayout.addStretch(1)
        self.topLayout.addLayout(top_buttonLayout)

    def create_input_dataGroupBox(self):
        self.input_dataGroupBox = QGroupBox('Input data')
        self.freq_inputComboBox = QComboBox()
        self.freq_inputComboBox.addItems(['KHz', 'Hz', 'MHz'])
        self.freq_inputText = QLineEdit()
        self.freq_inputText.setPlaceholderText('example: 100.35')
        self.freq_inputText.setText('100')
        freq_inputLabel = QLabel('Frequency: ')
        freq_inputLabel.setBuddy(self.freq_inputText)
        freqLayout = QHBoxLayout()
        freqLayout.addWidget(freq_inputLabel)
        freqLayout.addWidget(self.freq_inputText)
        freqLayout.addWidget(self.freq_inputComboBox)
        self.noise_inputRadioButton_add = QRadioButton('Add')
        self.noise_inputRadioButton_nadd = QRadioButton('Not add')
        noise_inputLabel = QLabel('Noise: ')
        self.noise_paramLabel = QLabel('Parameter: ')
        self.noise_paramText = QLineEdit()
        self.noise_paramText.setPlaceholderText('example: 0.35')
        self.noise_paramText.setText('0.005')
        self.noise_paramLabel.hide()
        self.noise_paramText.hide()
        noiseLayout = QGridLayout()
        noiseLayout.addWidget(noise_inputLabel, 0, 0)
        noiseLayout.addWidget(self.noise_inputRadioButton_add, 1, 0)
        noiseLayout.addWidget(self.noise_inputRadioButton_nadd, 2, 0)
        noiseLayout.addWidget(self.noise_paramLabel, 1, 1)
        noiseLayout.addWidget(self.noise_paramText, 2, 1)
        layout = QVBoxLayout()
        layout.addLayout(freqLayout)
        layout.addLayout(noiseLayout)
        layout.addStretch(1)
        self.input_dataGroupBox.setLayout(layout)

    def create_parameters_systemGroupBox(self):
        self.parameters_systemGroupBox = QGroupBox('Parameters system')
        self.freq_vcoComboBox = QComboBox()
        self.freq_vcoComboBox.addItems(['KHz', 'Hz', 'MHz'])
        self.freq_vcoText = QLineEdit()
        self.freq_vcoText.setPlaceholderText('example: 100.35')
        self.freq_vcoText.setText('100')
        freq_vcoLabel = QLabel('Frequency VCO: ')
        freqLayout = QHBoxLayout()
        freqLayout.addWidget(freq_vcoLabel)
        freqLayout.addWidget(self.freq_vcoText)
        freqLayout.addWidget(self.freq_vcoComboBox)
        phase_vcoLabel = QLabel('Phase VCO: ')
        self.phase_vcoText = QLineEdit()
        self.phase_vcoText.setPlaceholderText('(-2pi:2pi)')
        self.phase_vcoText.setText('0')
        coefficient_vcoLabel = QLabel('Coefficient VCO: ')
        self.coefficient_vcoText = QLineEdit()
        self.coefficient_vcoText.setText('1')
        phase_coeffLayout = QGridLayout()
        phase_coeffLayout.addWidget(phase_vcoLabel, 0, 0)
        phase_coeffLayout.addWidget(self.phase_vcoText, 1, 0)
        phase_coeffLayout.addWidget(coefficient_vcoLabel, 0, 1)
        phase_coeffLayout.addWidget(self.coefficient_vcoText, 1, 1)
        filter_selectLabel = QLabel('Filter: ')
        self.filter_select_oneRadioButton = QRadioButton('1')
        self.filter_select_twoRadioButton = QRadioButton('2')
        self.filter_select_threeRadioButton = QRadioButton('3')
        self.filter_resistLabel = QLabel('R: ')
        self.filter_resistComboBox = QComboBox()
        self.filter_resistComboBox.addItems(['KOm', 'Om'])
        self.filter_resistText = QLineEdit()
        self.filter_resistText.setText('3')
        self.filter_capacity_firstLabel = QLabel('C1: ')
        self.filter_capacity_firstText = QLineEdit()
        self.filter_capacity_firstText.setText('7')
        self.filter_capacity_secondLabel = QLabel('C2: ')
        self.filter_capacity_secondText = QLineEdit()
        self.filter_capacity_secondText.setText('3')
        self.filter_capacityComboBox = QComboBox()
        self.filter_capacityComboBox.addItems(['nF', 'mkF', 'pF'])
        self.filter_resistLabel.setVisible(False)
        self.filter_resistComboBox.setVisible(False)
        self.filter_resistText.setVisible(False)
        self.filter_capacity_firstLabel.setVisible(False)
        self.filter_capacity_firstText.setVisible(False)
        self.filter_capacity_secondLabel.setVisible(False)
        self.filter_capacity_secondText.setVisible(False)
        self.filter_capacityComboBox.setVisible(False)
        filterLayout = QGridLayout()
        filterLayout.addWidget(filter_selectLabel, 0, 0)
        filterLayout.addWidget(self.filter_select_oneRadioButton, 0, 1)
        filterLayout.addWidget(self.filter_select_twoRadioButton, 1, 1)
        filterLayout.addWidget(self.filter_select_threeRadioButton, 2, 1)
        filterLayout.addWidget(self.filter_resistLabel, 0, 2)
        filterLayout.addWidget(self.filter_resistText, 0, 3)
        filterLayout.addWidget(self.filter_resistComboBox, 0, 4)
        filterLayout.addWidget(self.filter_capacity_firstLabel, 1, 2)
        filterLayout.addWidget(self.filter_capacity_firstText, 1, 3)
        filterLayout.addWidget(self.filter_capacityComboBox, 1, 4)
        filterLayout.addWidget(self.filter_capacity_secondLabel, 2, 2)
        filterLayout.addWidget(self.filter_capacity_secondText, 2, 3)
        current_selectLabel = QLabel('Current detector: ')
        self.current_selectComboBox = QComboBox()
        self.current_selectComboBox.addItems(['0', '-1', '1'])
        currentLayout = QHBoxLayout()
        currentLayout.addWidget(current_selectLabel)
        currentLayout.addWidget(self.current_selectComboBox)
        layout = QVBoxLayout()
        layout.addLayout(freqLayout)
        layout.addLayout(phase_coeffLayout)
        layout.addLayout(filterLayout)
        layout.addLayout(currentLayout)
        layout.addStretch(1)
        self.parameters_systemGroupBox.setLayout(layout)

    def create_select_modeGroupBox(self):
        self.select_modeGroupBox = QGroupBox('Select mode')
        self.select_mode_standGroupBox = QGroupBox('')
        self.select_mode_statGroupBox = QGroupBox('')
        self.select_mode_standRadioButton = QRadioButton('Standart:')
        self.select_mode_stand_singleRadioButton = QRadioButton('Single')
        self.select_mode_stand_compareRadioButton = QRadioButton('Compare')
        self.select_mode_stand_compareComboBox = QComboBox()
        self.select_mode_stand_compareComboBox.addItems(['R', 'C1', 'C2', 'Coefficient VCO', 'Frequency', 'Noise', 'Current detector', 'Phase error'])
        self.select_mode_stand_compareComboBox.setVisible(False)
        self.mode_stand_compare_resetButton = QPushButton('Reset')
        self.mode_stand_compare_resetButton.setVisible(False)
        self.mode_stand_compare_plotButton = QPushButton('Plot')
        self.mode_stand_compare_plotButton.setVisible(False)
        self.mode_stand_compare_plot_singleButton = QPushButton('Plot single')
        self.mode_stand_compare_plot_singleButton.setVisible(False)
        self.mode_stand_compare_plot_singleComboBox = QComboBox()
        self.mode_stand_compare_plot_singleComboBox.setVisible(False)
        standLayout = QGridLayout()
        standLayout.addWidget(self.select_mode_stand_singleRadioButton, 0, 0)
        standLayout.addWidget(self.select_mode_stand_compareRadioButton, 1, 0)
        standLayout.addWidget(self.select_mode_stand_compareComboBox, 1, 1)
        standLayout.addWidget(self.mode_stand_compare_plot_singleButton, 2, 0)
        standLayout.addWidget(self.mode_stand_compare_plot_singleComboBox, 2, 1)
        standLayout.addWidget(self.mode_stand_compare_plotButton, 1, 2)
        standLayout.addWidget(self.mode_stand_compare_resetButton, 2, 2)
        self.select_mode_standGroupBox.setLayout(standLayout)
        self.select_mode_standGroupBox.setVisible(False)
        self.select_mode_statRadioButton = QRadioButton('Statistic:')
        layout = QGridLayout()
        layout.addWidget(self.select_mode_standRadioButton, 0, 0)
        layout.addWidget(self.select_mode_standGroupBox, 1, 0)
        layout.addWidget(self.select_mode_statRadioButton, 2, 0)
        self.select_modeGroupBox.setLayout(layout)

    def create_statisticGroupBox(self):
        self.select_mode_statGroupBox = QGroupBox('Statistic mode: ')
        self.select_mode_stat_newGroupBox = QGroupBox('')
        self.select_mode_stat_continueGroupBox = QGroupBox('')
        self.mode_stat_newRadioButton = QRadioButton('New experiment:')
        self.mode_stat_newLabel = QLabel('New experiment')
        self.mode_stat_newText = QLineEdit()
        self.mode_stat_newText.setPlaceholderText('experiment 1')
        self.mode_stat_new_selectLabel = QLabel('select param: ')
        self.mode_stat_new_selectComboBox = QComboBox()
        self.mode_stat_new_selectComboBox.addItems(['R', 'C1', 'C2', 'Coefficient VCO', 'Frequency', 'Noise', 'Current detector', 'Phase error'])
        self.mode_stat_new_addButton = QPushButton('Add')
        stat_newLayout = QGridLayout()
        stat_newLayout.addWidget(self.mode_stat_newLabel, 0, 0)
        stat_newLayout.addWidget(self.mode_stat_newText, 0, 1)
        stat_newLayout.addWidget(self.mode_stat_new_selectLabel, 1, 0)
        stat_newLayout.addWidget(self.mode_stat_new_selectComboBox, 1, 1)
        stat_newLayout.addWidget(self.mode_stat_new_addButton, 2, 0)
        self.select_mode_stat_newGroupBox.setLayout(stat_newLayout)
        self.select_mode_stat_newGroupBox.setVisible(False)
        self.mode_stat_continueRadioButton = QRadioButton('Continue experiment:')
        self.mode_stat_continueLabel = QLabel('Select experiment')
        self.mode_stat_continueComboBox = QComboBox()
        self.mode_stat_continue_paramText = QLabel('Parameters: ')
        self.mode_stat_continue_paramLabel = QLabel('')
        self.mode_stat_continue_resetButton = QPushButton('Reset experiment')
        self.mode_stat_continue_calculateButton = QPushButton('Calculate experiment')
        self.mode_stat_loadButton = QPushButton('Load')
        self.mode_stat_saveButton = QPushButton('Save')
        stat_continueLayout = QGridLayout()
        stat_continueLayout.addWidget(self.mode_stat_continueLabel, 0, 0)
        stat_continueLayout.addWidget(self.mode_stat_continueComboBox, 0, 1)
        stat_continueLayout.addWidget(self.mode_stat_continue_paramText, 1, 0)
        stat_continueLayout.addWidget(self.mode_stat_continue_paramLabel, 1, 1)
        stat_continueLayout.addWidget(self.mode_stat_continue_resetButton, 2, 0)
        stat_continueLayout.addWidget(self.mode_stat_continue_calculateButton, 3, 0)
        self.select_mode_stat_continueGroupBox.setLayout(stat_continueLayout)
        self.select_mode_stat_continueGroupBox.setVisible(False)
        stat_modeLayout = QGridLayout()
        stat_modeLayout.addWidget(self.mode_stat_newRadioButton, 0, 0)
        stat_modeLayout.addWidget(self.mode_stat_continueRadioButton, 0, 1)
        stat_modeLayout.addWidget(self.select_mode_stat_newGroupBox, 1, 0)
        stat_modeLayout.addWidget(self.select_mode_stat_continueGroupBox, 1, 1)
        stat_modeLayout.addWidget(self.mode_stat_loadButton, 2, 0)
        stat_modeLayout.addWidget(self.mode_stat_saveButton, 2, 1)
        self.select_mode_statGroupBox.setLayout(stat_modeLayout)
        self.select_mode_statGroupBox.setVisible(False)

    def create_ProgressBar(self):
        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, 100)
        self.progressBar.setValue(0)
        self.progressBar.hide()

    def click_noiseRadio(self):
        self
        radioButton = self.sender()
        if radioButton.isChecked():
            if radioButton.text() == 'Add':
                self.noise_paramLabel.setVisible(True)
                self.noise_paramText.setVisible(True)
                self.value_noise = True
            else:
                self.noise_paramLabel.setVisible(False)
                self.noise_paramText.setVisible(False)
                self.value_noise = False

    def click_filterRadio(self):
        self
        radioButton = self.sender()
        if radioButton.isChecked():
            if radioButton.text() == '1':
                self.filter_resistLabel.setVisible(True)
                self.filter_resistComboBox.setVisible(True)
                self.filter_resistText.setVisible(True)
                self.filter_capacity_firstLabel.setVisible(True)
                self.filter_capacity_firstText.setVisible(True)
                self.filter_capacity_secondLabel.setVisible(False)
                self.filter_capacity_secondText.setVisible(False)
                self.filter_capacityComboBox.setVisible(True)
                self.value_filter = '1'
            else:
                if radioButton.text() == '2':
                    self.filter_resistLabel.setVisible(True)
                    self.filter_resistComboBox.setVisible(True)
                    self.filter_resistText.setVisible(True)
                    self.filter_capacity_firstLabel.setVisible(True)
                    self.filter_capacity_firstText.setVisible(True)
                    self.filter_capacity_secondLabel.setVisible(True)
                    self.filter_capacity_secondText.setVisible(True)
                    self.filter_capacityComboBox.setVisible(True)
                    self.value_filter = '2'
                else:
                    self.filter_resistLabel.setVisible(True)
                    self.filter_resistComboBox.setVisible(True)
                    self.filter_resistText.setVisible(True)
                    self.filter_capacity_firstLabel.setVisible(True)
                    self.filter_capacity_firstText.setVisible(True)
                    self.filter_capacity_secondLabel.setVisible(True)
                    self.filter_capacity_secondText.setVisible(True)
                    self.filter_capacityComboBox.setVisible(True)
                    self.value_filter = '3'

    def click_select_modeRadio(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            if radioButton.text() == 'Standart:':
                self.select_mode_standGroupBox.setVisible(True)
                self.select_mode_statGroupBox.setVisible(False)
                self.set_mode = 'Standart'
            else:
                if radioButton.text() == 'Statistic:':
                    self.select_mode_standGroupBox.setVisible(False)
                    self.select_mode_statGroupBox.setVisible(True)
                    self.set_mode = 'Statistic'

    def click_select_mode_standRadio(self):
        self.set_mode_stat = 0
        radioButton = self.sender()
        if radioButton.isChecked():
            if radioButton.text() == 'Single':
                self.select_mode_stand_compareComboBox.setVisible(False)
                self.mode_stand_compare_resetButton.setVisible(False)
                self.mode_stand_compare_plotButton.setVisible(False)
                self.mode_stand_compare_plot_singleButton.setVisible(False)
                self.mode_stand_compare_plot_singleComboBox.setVisible(False)
                self.set_mode_stand = 'Single'
            else:
                self.select_mode_stand_compareComboBox.setVisible(True)
                self.mode_stand_compare_resetButton.setVisible(True)
                self.mode_stand_compare_plotButton.setVisible(True)
                self.mode_stand_compare_plot_singleButton.setVisible(True)
                self.mode_stand_compare_plot_singleComboBox.setVisible(True)
                self.set_mode_stand = 'Compare'

    def click_select_mode_statRadio(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            if radioButton.text() == 'New experiment:':
                self.select_mode_stat_newGroupBox.setVisible(True)
                self.select_mode_stat_continueGroupBox.setVisible(False)
                self.set_mode_stat = 'New'
            else:
                self.select_mode_stat_continueGroupBox.setVisible(True)
                self.select_mode_stat_newGroupBox.setVisible(False)
                self.set_mode_stat = 'Continue'

    def click_compare_resetButton(self):
        self.count_compare = 0
        self.noise_compare = []
        self.result_data_compare = {}
        self.mode_stand_compare_plot_singleComboBox.clear()
        inf = QMessageBox()
        inf.setWindowTitle('Success')
        inf.setText('Data is delete')
        inf.setIcon(QMessageBox.Information)
        inf.exec_()

    def click_stat_paramButton(self):
        _str_param = ''
        try:
            for i in range(self.result_data_statistic[self.mode_stat_continueComboBox.currentText()]['count']):
                _str_param += self.result_data_statistic[self.mode_stat_continueComboBox.currentText()]['num_test'][str(i)]['information']
                _str_param += '; '
            else:
                self.mode_stat_continue_paramLabel.setText(_str_param)

        except KeyError:
            _str_param = ''

    def click_stat_continue_resetButton(self):
        try:
            del self.result_data_statistic[self.mode_stat_continueComboBox.currentText()]
            self.mode_stat_continueComboBox.clear()
            self.mode_stat_continueComboBox.addItems(list(self.result_data_statistic.keys()))
            self.mode_stat_continue_paramLabel.setText('')
        except KeyError:
            inf = QMessageBox()
            inf.setWindowTitle('Success')
            inf.setText('Data is delete')
            inf.setIcon(QMessageBox.Information)
            inf.exec_()

    def click_stat_loadButton(self):
        try:
            with open('src/gui/save/statistic', 'rb') as (f):
                self.result_data_statistic = pickle.load(f)
            self.mode_stat_continueComboBox.clear()
            self.mode_stat_continueComboBox.addItems(list(self.result_data_statistic.keys()))
            self.click_stat_paramButton()
            message = QMessageBox()
            message.setWindowTitle('Information')
            message.setText('Data is loaded')
            message.setIcon(QMessageBox.Information)
            message.exec_()
        except FileNotFoundError:
            error = QMessageBox()
            error.setWindowTitle('Error')
            error.setText('File not Found')
            error.setIcon(QMessageBox.Warning)
            error.exec_()

    def click_stat_saveButton(self):
        try:
            with open('src/gui/save/statistic', 'wb') as (f):
                pickle.dump(self.result_data_statistic, f)
            message = QMessageBox()
            message.setWindowTitle('Information')
            message.setText('Data is save')
            message.setIcon(QMessageBox.Information)
            message.exec_()
        except:
            error = QMessageBox()
            error.setWindowTitle('Error')
            error.setText('Data not save')
            error.setIcon(QMessageBox.Warning)
            error.exec_()

    def click_stat_new_addButton(self):
        self.result_data_statistic[self.mode_stat_newText.text()] = {'input_signal':0, 
         'count':0, 
         'select_parameter':self.mode_stat_new_selectComboBox.currentText(), 
         'num_test':{}}
        self.mode_stat_continueComboBox.clear()
        self.mode_stat_continueComboBox.addItems(list(self.result_data_statistic.keys()))
        print(self.result_data_statistic)

    def click_compare_plotButton(self):
        self.print_compare = PrintCompare(self.result_data_compare)
        self.print_compare.show()

    def click_compare_plot_singleButton(self):
        _count = int(self.mode_stand_compare_plot_singleComboBox.currentIndex())
        self.print_single = PrintSingle(self.result_data_compare[_count])
        self.print_single.show()

    def click_stat_calculateButton(self):
        try:
            self.win_stat = PrintStatistic(self.result_data_statistic[self.mode_stat_continueComboBox.currentText()]['num_test'])
            self.win_stat.show()
        except KeyError:
            error = QMessageBox()
            error.setWindowTitle('Error')
            error.setText('Add experiment')
            error.setIcon(QMessageBox.Warning)
            error.exec_()

    def click_runButton(self):
        self.initial_data = self.collect_parameters()
        if self.initial_data is not None:
            self.select_run_algoritm()

    def get_freq_input(self):
        _value_freq_inputCmbBx = self.freq_inputComboBox.currentText()
        _value_freq = float(self.freq_inputText.text())
        if _value_freq_inputCmbBx == 'Hz':
            _value_mult = 1
        else:
            if _value_freq_inputCmbBx == 'KHz':
                _value_mult = 1000
            else:
                _value_mult = 1000000
        return _value_freq * _value_mult

    def get_input_signal(self):
        _count = self.initial_data['counts']
        _freq_input_signal = self.initial_data['freq_input_signal']
        _noise_param = self.initial_data['noise'][1]
        _input_signal = [1 / _freq_input_signal * i for i in range(_count)]
        if self.initial_data['noise'][0]:
            gen = Genormal(
                0, 
                1 / _freq_input_signal * _noise_param,
                _count + _count % 4
            )
            _noise_value = gen.thread_generation()
            _input_signal = [sig + noise for sig, noise in zip(_input_signal, _noise_value)]
            _input_signal[0] = 0
            return _input_signal
        return _input_signal

    def get_freq_vco(self):
        _value_freq_vcoCmbBx = self.freq_vcoComboBox.currentText()
        _value_freq = float(self.freq_vcoText.text())
        if _value_freq_vcoCmbBx == 'Hz':
            _value_mult = 1
        else:
            if _value_freq_vcoCmbBx == 'KHz':
                _value_mult = 1000
            else:
                _value_mult = 1000000
        return _value_freq * _value_mult

    def get_filter_parameters(self):
        _value_mult: int

        _value_resistCmbBx = self.filter_resistComboBox.currentText()
        _value_resist = float(self.filter_resistText.text())

        if _value_resistCmbBx == "Om":
            _value_mult = 1
        elif _value_resistCmbBx == "KOm":
            _value_mult = 1000

        _value_resist = _value_resist * _value_mult

        _value_capacityCmbBx = self.filter_capacityComboBox.currentText()
        _value_capacity_one = float(self.filter_capacity_firstText.text())

        if _value_capacityCmbBx == "mkF":
            _value_mult = 1e-06
        elif _value_capacityCmbBx == "nF":
            _value_mult = 1e-09
        else:
            _value_mult = 1e-12

        _value_capacity_one = _value_capacity_one * _value_mult

        if self.value_filter == '1':

            return [
                        _value_resist, 
                        [_value_capacity_one], 
                        float(self.coefficient_vcoText.text())
            ]
            
        else:
            _value_capacity_two = float(self.filter_capacity_secondText.text())
            _value_capacity_two = _value_capacity_two * _value_mult
            
            return [
                        _value_resist, 
                        [_value_capacity_one, _value_capacity_two], 
                        float(self.coefficient_vcoText.text())
            ]

 #Function collecting initial parameters
    def collect_parameters(self):
        try:
            #Initial matrix: first matrix_x_init, second ,atrix_v_init
            _matrixs_init = {
                            '1': [Matrix([[0],[0]]), Matrix([[0, 1]]), '1'],
                            '2': [Matrix([[0],[0], [0]]), Matrix([[0, 0, 1]]), '2'],
                            '3': [Matrix([[0],[0], [0]]), Matrix([[0, 0, 1]]), '3'],
            }

            _freq_input_signal = self.get_freq_input()
            _noise_input = [self.value_noise, float(self.noise_paramText.text())]
            _freq_vco_signal = self.get_freq_vco()
            _phase_vco_signal = float(self.phase_vcoText.text()) % (2 * pi)
            _current_detector = int(self.current_selectComboBox.currentText())
            _select_filter = _matrixs_init[self.value_filter]
            _counts = int(self.number_of_countsText.text())
            self.val = 0
            return  {
                        'input_signal': [],
                        'freq_input_signal': _freq_input_signal,
                        'freq_vco_signal': _freq_vco_signal,
                        'phase': _phase_vco_signal,
                        'current': _current_detector,
                        'counts': _counts,
                        'noise': _noise_input,
                        'matrix_init': _select_filter,
                        'filter_params': self.get_filter_parameters(),
            }
        except:
            error = QMessageBox()
            error.setWindowTitle("Error")
            error.setText("The fields value are incorrectly")
            error.setIcon(QMessageBox.Warning)
            error.exec_()


    #Functions progress bar

    def start_progressBar(self):
        self.step = 0
        self.progressBar.setVisible(True)
        self.run_modelButton.hide()

    def reset_progressBar(self):
        message = QMessageBox()
        message.setWindowTitle('Information')
        message.setText('Generation is successful')
        message.setIcon(QMessageBox.Information)
        message.exec_()
        self.progressBar.hide()
        self.step = 0
        self.progressBar.setValue(0)
        self.run_modelButton.setVisible(True)

    def run_algoritm(self):
        self.start_progressBar()
        result_data = main_algoritm(self.initial_data, self)
        result_data = correct_data(result_data, self.initial_data['freq_input_signal'])
        self.reset_progressBar()
        return result_data

    def stand_single_algoritm(self):
        self.initial_data['input_signal'] = self.get_input_signal()
        self.print = PrintSingle(self.run_algoritm())
        self.print.show()

    def stand_compare_algoritm(self):
        if self.select_mode_stand_compareComboBox.currentText() == 'Noise':
            self.initial_data['input_signal'] = self.get_input_signal()
        else:
            if self.count_compare == 0:
                self.noise_compare = self.get_input_signal()
                self.initial_data['input_signal'] = self.noise_compare
            else:
                self.initial_data['input_signal'] = self.noise_compare
        self.result_data_compare[self.count_compare] = self.run_algoritm()
        _return_params = self.return_value_params(self.select_mode_stand_compareComboBox.currentText(), '1')
        self.result_data_compare[self.count_compare]['Information'] = _return_params
        self.mode_stand_compare_plot_singleComboBox.addItem(_return_params)
        self.count_compare += 1

    def return_value_params(self, combo_box_value, point):
        _value_compare_mode = combo_box_value
        if point == '1':
            if _value_compare_mode == 'R':
                return _value_compare_mode + '=' + self.filter_resistText.text() + self.filter_resistComboBox.currentText()
            if _value_compare_mode == 'C1':
                return _value_compare_mode + '=' + self.filter_capacity_firstText.text() + self.filter_capacityComboBox.currentText()
            if _value_compare_mode == 'C2':
                return _value_compare_mode + '=' + self.filter_capacity_secondText.text() + self.filter_capacityComboBox.currentText()
            if _value_compare_mode == 'Coefficient VCO':
                return _value_compare_mode + '=' + self.coefficient_vcoText.text()
            if _value_compare_mode == 'Frequency':
                return _value_compare_mode + '=' + self.freq_inputText.text() + self.freq_inputComboBox.currentText()
            if _value_compare_mode == 'Noise':
                return _value_compare_mode + '=' + self.noise_paramText.text()
            if _value_compare_mode == 'Current detector':
                return _value_compare_mode + '=' + self.current_selectComboBox.currentText()
            if _value_compare_mode == 'Phase error':
                return _value_compare_mode + '=' + self.phase_vcoText.text()
        else:
            if _value_compare_mode == 'R':
                return self.filter_resistText.text()
            if _value_compare_mode == 'C1':
                return self.filter_capacity_firstText.text()
            if _value_compare_mode == 'C2':
                return self.filter_capacity_secondText.text()
            if _value_compare_mode == 'Coefficient VCO':
                return self.coefficient_vcoText.text()
            if _value_compare_mode == 'Frequency':
                return self.freq_inputText.text()
            if _value_compare_mode == 'Noise':
                return self.noise_paramText.text()
            if _value_compare_mode == 'Current detector':
                return self.current_selectComboBox.currentText()
        if _value_compare_mode == 'Phase error':
            return self.phase_vcoText.text()

    def stat_continue_algoritm(self):
        _result = 0
        _num_exp = self.mode_stat_continueComboBox.currentText()
        _count = self.result_data_statistic[_num_exp]['count']
        self.result_data_statistic[_num_exp]['num_test'][str(_count)] = {'information':0, 
         'value_param':0, 
         'error_signal':0}
        if _count == 0:
            if self.result_data_statistic[_num_exp]['select_parameter'] == 'Noise':
                self.result_data_statistic[_num_exp]['input_signal'] = 0
                self.initial_data['input_signal'] = self.get_input_signal()
            else:
                self.initial_data['input_signal'] = self.get_input_signal()
                self.result_data_statistic[_num_exp]['input_signal'] = self.initial_data['input_signal']
        elif self.result_data_statistic[_num_exp]['select_parameter'] == 'Noise':
            self.initial_data['input_signal'] = self.get_input_signal()
        else:
            self.initial_data['input_signal'] = self.result_data_statistic[_num_exp]['input_signal']
        self.start_progressBar()
        _result = main_algoritm(self.initial_data, self)
        self.reset_progressBar()
        self.result_data_statistic[_num_exp]['num_test'][str(_count)]['information'] = self.return_value_params(self.mode_stat_new_selectComboBox.currentText(), '1')
        self.result_data_statistic[_num_exp]['num_test'][str(_count)]['value_param'] = self.return_value_params(self.mode_stat_new_selectComboBox.currentText(), '2')
        self.result_data_statistic[_num_exp]['num_test'][str(_count)]['error_signal'] = _result['error_signal']
        self.result_data_statistic[_num_exp]['count'] += 1
        self.click_stat_paramButton()
        print(self.result_data_statistic)

    def select_run_algoritm(self):
        try:
            if self.set_mode == 'Standart':
                if self.set_mode_stand == 'Single':
                    self.stand_single_algoritm()
                elif self.set_mode_stand == 'Compare':
                    self.stand_compare_algoritm()
            elif self.set_mode == 'Statistic':
                if self.set_mode_stat == 'New':
                    error = QMessageBox()
                    error.setWindowTitle('Error')
                    error.setText('Incorrectly mode')
                    error.setIcon(QMessageBox.Warning)
                    error.exec_()
                else:
                    if self.set_mode_stat == 'Continue':
                        if int(self.number_of_countsText.text()) < 150:
                            error = QMessageBox()
                            error.setWindowTitle('Error')
                            error.setText('Size number of counts minimum 150')
                            error.setIcon(QMessageBox.Warning)
                            error.exec_()
                        else:
                            self.stat_continue_algoritm()
        except AttributeError:
            error = QMessageBox()
            error.setWindowTitle('Error')
            error.setText('Mode not selected')
            error.setIcon(QMessageBox.Warning)
            error.exec_()


def open_main_window():
    import sys
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    open_main_window()
