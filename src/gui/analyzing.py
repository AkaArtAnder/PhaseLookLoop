from math import pi, sqrt
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import pyqtgraph as pg
import numpy as np
from scipy.stats import chi2
from PyQt5.QtWidgets import QWidget, QGridLayout, QGroupBox, QLabel, QVBoxLayout, QComboBox, QPushButton, QHBoxLayout

frequency_input_signal: float

class PrintSingle(pg.GraphicsLayoutWidget):
    def __init__(self, result_data, parent=None):
        pg.GraphicsLayoutWidget.__init__(self, parent)
        pg.setConfigOptions(antialias=True)
        pg.setConfigOption('background', 'k')
        pg.setConfigOption('foreground', 'k')

        self.setBackground('w')

        self.resize(1000,600)
        self.setWindowTitle('Plotting single mode')
        self.result_data = result_data

        p1 = self.addPlot(title="Signals input and VCO", col = 0, rowspan = 2)
        p1.plot(self.result_data['input_signal']['time_pulse'],self.result_data['input_signal']['amplitude'], pen='k')
        p1.plot(np.array(self.result_data['generator_signal']['time_pulse'], dtype=float),self.result_data['generator_signal']['amplitude'], pen='k')
        p1.showGrid(x=True, y=True)
        p1.setRange(yRange=[-0.2,1])
        lr = pg.LinearRegionItem([0,result_data['input_signal']['time_pulse'][-1]])
        lr.setZValue(-10)
        p1.addItem(lr)

        p2 = self.addPlot(title="Zoom signals", col=1, colspan=2)
        p2.addLegend()
        p2.plot(self.result_data['input_signal']['time_pulse'],self.result_data['input_signal']['amplitude'], pen=('b'), name="Input signal")
        p2.plot(np.array(self.result_data['generator_signal']['time_pulse'], dtype=float),self.result_data['generator_signal']['amplitude'], pen='r', name="VCO signal")
        p2.setRange(yRange=[-0.2,2])
        p2.showGrid(x=True, y=True)

        self.nextRow()

        p3 = self.addPlot(title="Current detect", col=1, colspan=2)
        p3.plot(np.array(self.result_data['current_detector']['time_pulse_current'], dtype=float),self.result_data['current_detector']['current'], pen='k', name="Current detector")
        p3.setRange(yRange=[-1,1])
        p3.showGrid(x=True, y=True)
        p3.setXLink(p2)

        def updatePlot():
            p2.setXRange(*lr.getRegion(), padding=0)
        def updateRegion():
            lr.setRegion(p2.getViewBox().viewRange()[0])
        lr.sigRegionChanged.connect(updatePlot)
        p2.sigXRangeChanged.connect(updateRegion)
        updatePlot()

        self.nextRow()
        p4 = self.addPlot(title="Error signal", col = 0, rowspan = 3)
        p4.plot(np.array(self.result_data['error_signal'], dtype=float), pen='k', name="Error signal")
        p4.showGrid(x=True, y=True)
        lr1 = pg.LinearRegionItem([0,len(self.result_data['error_signal'])])
        lr1.setZValue(-10)
        p4.addItem(lr1)

        p5 = self.addPlot(title="Error signal", col=1, colspan=2)
        p5.plot(np.array(self.result_data['error_signal'], dtype=float), pen='k', name="Error signal")
        p5.showGrid(x=True, y=True)

        self.nextRow()

        p6 = self.addPlot(title="Phase", col = 1 , colspan=2)
        p6.plot(self.result_data['static_phase']['phase_generator'], pen='k', name="Phase")
        p6.plot(self.result_data['static_phase']['correct_phase_down'], pen='r', name="Phase")
        p6.plot(self.result_data['static_phase']['correct_phase_up'], pen='r', name="Phase")
        p6.showGrid(x=True, y=True)
        p6.setXLink(p5)

        self.nextRow()

        p7 = self.addPlot(title="Current detect", col = 1 , colspan=2)
        p7.plot(np.array([ (i * frequency_input_signal) for i in self.result_data['current_detector']['time_pulse_current']], dtype=float),self.result_data['current_detector']['current'], pen='k', name="Current detector")
        p7.setRange(yRange=[-1,1])
        p7.showGrid(x=True, y=True)
        p7.setXLink(p5)

        def updatePlot1():
            p5.setXRange(*lr1.getRegion(), padding=0)
        def updateRegion1():
            lr1.setRegion(p5.getViewBox().viewRange()[0])
        lr1.sigRegionChanged.connect(updatePlot1)
        p5.sigXRangeChanged.connect(updateRegion1)
        updatePlot1()
        
class PrintCompare(pg.GraphicsLayoutWidget):
    def __init__(self, result_data, parent=None):
        pg.GraphicsLayoutWidget.__init__(self, parent)
        pg.setConfigOptions(antialias=True)
        pg.setConfigOption('background', 'k')
        pg.setConfigOption('foreground', 'k')

        self.setBackground('w')

        self.resize(1000,600)
        self.setWindowTitle('Plotting compare mode')
        self.result_data = result_data

        p1 = self.addPlot(title="Error signals")
        p1.addLegend()
        p1.showGrid(x=True, y=True)
        i = 3
        for index, value in self.result_data.items():
            p1.plot(np.array(value['error_signal'], dtype=float), pen=(i, len(self.result_data)+2), name=value['Information'])
            i+=1

class PrintStatistic(QWidget):
    def __init__(self, result_data, parent=None):
        QWidget.__init__(self, parent)

        self.setWindowTitle("Statistic mode")
        self.result_data = result_data
        self.sort_data()

        self.plotButton = QPushButton("Plot result statistic")

        self.calculate()
        self.create_data_graph_array()
        self.create_resultGroupBox()
        self.create_histGroupBox()

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.plotButton, 0, 1)
        mainLayout.addWidget(self.resultGroupBox, 1, 0)
        mainLayout.addWidget(self.histGroupBox, 1, 1)
        self.setLayout(mainLayout)

        self.result_histButton.clicked.connect(self.click_histButton)
        self.plotButton.clicked.connect(self.click_statisticButton)

    def click_statisticButton(self):
        self.win_stat = PlotDataStatistic(self.data_statistic)
        self.win_stat.show()

    def click_histButton(self):
        _count = self.result_histComboBox.currentIndex()

        plt.figure()
        sb.set()
        sb.distplot(self.result_data[str(_count)]['error_signal'])
        plt.title("Гистограмма анализируемых данных")
        plt.show()

    def sort_data(self):
        _sort_value = []
        _sorted_dict = {}
        for key, value in self.result_data.items():
            _sort_value.append(value["value_param"])
        _sort_value.sort()
        for i in _sort_value:
            for keys in self.result_data.keys():
                if self.result_data[keys]['value_param'] == i:
                    _sorted_dict[keys] = self.result_data[keys]
                    break
        self.result_data = _sorted_dict.copy()


        

    def calculate(self):
        for key, value in self.result_data.items():
            _part_array = list(value['error_signal'][30:])

            _mean = sum(_part_array)/len(_part_array)
            _std = sqrt(sum(map(lambda arr: (arr - _mean)**2, _part_array))/(len(_part_array) - 1))

            _std_mean = _std/sqrt(len(_part_array))
            _error_mean = 1.96 * _std_mean

            _error_std = [_std * sqrt((len(_part_array)-1))/sqrt(chi2.ppf(0.975, (len(_part_array)-1))), _std * sqrt((len(_part_array)-1))/sqrt(chi2.ppf(0.025, (len(_part_array)-1)))]

            self.result_data[key]['mean'] = [_mean, _error_mean]
            self.result_data[key]['std'] = _error_std
    
    def create_data_graph_array(self):
        self.data_statistic = {
            'error_signal': [],
            'information': [],
            'mean': [],
            'error': [],
            'std': [],
            'param': [],  
        }
        for key, value in self.result_data.items():
            self.data_statistic['error_signal'].append(value['error_signal'][:60])
            self.data_statistic['information'].append(value['information'])
            self.data_statistic['mean'].append(value['mean'][0])
            self.data_statistic['error'].append(value['mean'][1])
            self.data_statistic['std'].append((value['std'][0] + value['std'][1])/2)
            self.data_statistic['param'].append(float(value['value_param']))
        

    def create_resultGroupBox(self):
        self.resultGroupBox = QGroupBox("Calculation results")

        result_paramLabel = QLabel("Value parameter")
        result_meanLabel = QLabel("    Mean")
        result_stdLabel = QLabel(" Std")

        resultLayout = QGridLayout()
        resultLayout.addWidget(result_paramLabel, 0, 0)
        resultLayout.addWidget(result_meanLabel, 0, 1)
        resultLayout.addWidget(result_stdLabel, 0, 2)

        _i = 1
        for key, value in self.result_data.items():
            _inf = str(value['information'])
            _mean = "    (" + str(value['mean'][0]) + " +/- " + str(value['mean'][1]) + ")    "
            _std = "(" + str(value['std'][0]) + " ; " + str(value['std'][1]) + ")"

            _paramLabel = QLabel(_inf)
            _meanLabel = QLabel(_mean)
            _stdLabel = QLabel(_std)

            resultLayout.addWidget(_paramLabel, _i, 0)
            resultLayout.addWidget(_meanLabel, _i, 1)
            resultLayout.addWidget(_stdLabel, _i, 2)
            _i += 1

        self.resultGroupBox.setLayout(resultLayout)
    
    def create_histGroupBox(self):
        self.histGroupBox = QGroupBox("Plot hist")

        self.result_histComboBox = QComboBox()
        for key, value in self.result_data.items():
            self.result_histComboBox.addItem(value['information'])
        self.result_histButton = QPushButton("Plot")

        histLayout = QHBoxLayout()
        histLayout.addWidget(self.result_histComboBox)
        histLayout.addWidget(self.result_histButton)
        self.histGroupBox.setLayout(histLayout)


class PlotDataStatistic(pg.GraphicsLayoutWidget):
    def __init__(self, result_data, parent=None):
        pg.GraphicsLayoutWidget.__init__(self, parent)

        pg.setConfigOptions(antialias=True)
        pg.setConfigOption('background', 'k')
        pg.setConfigOption('foreground', 'k')

        self.setBackground('w')

        self.setWindowTitle('Plotting statistic mode')

        self.result_data = result_data
        
        

        p1 = self.addPlot(title="Mx(param)")
        p1.plot(np.array(self.result_data['param'], dtype=float), np.array(self.result_data['mean'], dtype=float), symbol='o', pen={'color': 0.8, 'width': 2})
        p1.showGrid(x=True, y=True)
        p1.setLabel('left', 'Value Mx')
        p1.setLabel('bottom', 'Parameter ' + self.result_data['information'][0][0])

        self.nextRow()

        p2 = self.addPlot(title="Std(param)")
        p2.plot(np.array(self.result_data['param'], dtype=float), np.array(self.result_data['std'], dtype=float), symbol='o', pen={'color': 0.8, 'width': 2})
        p2.showGrid(x=True, y=True)
        p2.setLabel('left', 'Value Std')
        p2.setLabel('bottom', 'Parameter ' + self.result_data['information'][0][0])

        self.nextRow()

        p3 = self.addPlot(title="Error signals")
        p3.addLegend()
        _i = 0
        for error, information in zip(self.result_data["error_signal"], self.result_data['information']):
            p3.plot(np.array(error, dtype=float), pen=(_i, len(self.result_data['information'])), name=information)
            p3.showGrid(x=True, y=True)
            p3.setLabel('left', 'Value error')
            p3.setLabel('bottom', 'Time(S) * frequency(1/S)')
            _i += 1

# Functions correct data
def correct_data(result_data: dict, freq_unput: float) -> dict:

    global frequency_input_signal
    frequency_input_signal = freq_unput
    _correct_data = {}

    _data = {
        'phase_generator': result_data["full_phase"],
        'correct_phase_down': [2 * pi] * len(result_data['full_phase']),
        'correct_phase_up': [4 * pi] * len(result_data['full_phase'])
    }

    _correct_data['static_phase'] = pd.DataFrame(_data)
    _correct_data['static_phase']['phase_generator'] = _correct_data['static_phase'].phase_generator.astype('float64')

    result_data['time_all_pulse'].insert(0, -1/frequency_input_signal)
    _data = {
        'current': result_data['current_detector'],
        'time_pulse_current': result_data['time_all_pulse'],
    }
    _correct_data['current_detector'] = correct_pulse_current(_data)

    _correct_data['input_signal'] = correct_pulse_signal(result_data['time_pulse_input_signal'], 10)
    _correct_data['generator_signal'] = correct_pulse_signal(result_data['time_pulse_generator'], 10)
    _correct_data['error_signal'] = result_data['error_signal']

    return _correct_data


def correct_pulse_signal(time_pulse, duty):
    _amplitude = list()
    _time = list()
    _count = 0
    period = 1/frequency_input_signal
    for t in time_pulse:
        try:
            _time.append(t)
            _amplitude.append(1)

            _time.append(
                t + period/100*duty
            )
            _amplitude.append(1)

            _time.append(
                _time[-1] + period/100*0.0001
            )
            _amplitude.append(0)

            _time.append(
                time_pulse[_count + 1] - period/100*0.0001
            )
            _amplitude.append(0)

            _count += 1
        except IndexError:
            break

    return {'amplitude': _amplitude, 'time_pulse': _time}


def correct_pulse_current(current_detector):
    _count = 0
    _value_current = list()
    _time_pulse_current = list()

    for time, current in zip(current_detector['time_pulse_current'], current_detector['current']):
        try:
            next_pulse = current_detector['time_pulse_current'][_count + 1]
            _value_current.append(current)
            _time_pulse_current.append(time)

            _value_current.append(current)
            _time_pulse_current.append(
                next_pulse - (1/frequency_input_signal)/100000
            )
            _count += 1
        except IndexError:
            _value_current.append(current)
            _time_pulse_current.append(time)

    return {'current': _value_current, 'time_pulse_current': _time_pulse_current}
