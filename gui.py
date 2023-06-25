from main import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import sys

class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)

class myWindow(QMainWindow):
    def __init__(self):
        super(myWindow, self).__init__()
        self.setWindowTitle('Data rate [Mbps]')

        #CA
        self.label_CA_carriers = QLabel('CA carriers')
        self.label_Carrier_components = QLabel('Carrier components:')
        self.input_Carrier_components = QLineEdit()
        self.input_Carrier_components.textChanged.connect(self.carrier_components_change)
        #MIMO
        self.label_MIMO = QLabel('MIMO')
        self.label_MIMO_layers = QLabel('MIMO layers:')
        self.input_MIMO_layers = QLineEdit()
        self.input_MIMO_layers.textChanged.connect(self.MIMO_layers_change)
        self.label_MU_MIMO = QLabel('MU-MIMO:')
        self.checkbox_MU_MIMO = QCheckBox()
        self.checkbox_MU_MIMO.stateChanged.connect(self.change_MU_MIMO_input)
        self.label_MU_MIMO_beams = QLabel('MU-MIMO beams:')
        self.input_MU_MIMO_beams = QLineEdit()
        self.input_MU_MIMO_beams.setDisabled(True)
        self.input_MU_MIMO_beams.textChanged.connect(self.MU_MIMO_beams_change)
        #modulation
        self.label_Modulation_order = QLabel('Modulation')
        self.label_table_number = QLabel('Table:')
        self.combobox_table_number = QComboBox()
        self.combobox_table_number.addItems(['1','2','3','4'])
        self.combobox_table_number.currentTextChanged.connect(self.change_mod_table)
        self.label_mcs_index = QLabel('MCS Index:')
        self.spinbox_mcs = QSpinBox()
        self.spinbox_mcs.valueChanged.connect(self.mcs_change)
        self.change_mod_table(1)
        self.label_modulation = QLabel('Modulation:')
        self.display_modulation = QLineEdit()
        self.display_modulation.setDisabled(True)
        self.label_mod_order = QLabel('Modulation order')
        self.display_mod_order = QLineEdit()
        self.display_mod_order.setDisabled(True)

        self.mod_order = mod_order_table(1)
        #resource block
        self.nrb = np.loadtxt('Nrb_FR1.csv', delimiter=';', skiprows=1, usecols=(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15))
        self.bw_l = np.loadtxt('Nrb_FR1.csv', delimiter=';', max_rows = 1, usecols=(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15))
        self.scs_l = np.loadtxt('Nrb_FR1.csv', delimiter=';', skiprows = 1, usecols=0)
        self.bw_list_vals = []
        self.scs_list_vals = []

        self.FR_bands = QComboBox()
        self.FR_bands.addItems(['FR1', 'FR2'])
        self.FR_bands.currentTextChanged.connect(self.FR_band_change)
        self.scs_list = QComboBox()
        self.scs_list.addItems(self.scs_list_vals)
        self.scs_list.currentTextChanged.connect(self.scs_change)
        self.bw_list = QComboBox()
        self.bw_list.addItems(self.bw_list_vals)
        self.bw_list.currentTextChanged.connect(self.bw_change)
        self.label_resource_block = QLabel('Resource block')
        self.label_FR_band = QLabel('FR band:')
        self.label_subcarrier_spacing = QLabel('Subcarrier spacing [MHz]:')
        self.label_channel_bandwidth = QLabel('Channel bandwidth [MHz]:')
        #other
        self.label_channel_scaling_factor = QLabel('Channel direction and scaling factor')
        self.label_channel = QLabel('Channel:')
        self.ch_dir = QComboBox()
        self.ch_dir.addItems(['DL', 'UL'])
        self.ch_dir.currentTextChanged.connect(self.ch_dir_change)

        self.label_scaling_factor = QLabel('Scaling factor:')
        self.combobox_scaling_factor = QComboBox()
        self.combobox_scaling_factor.addItems(['1', '0.8', '0.75', '0.4', 'Custom'])
        self.combobox_scaling_factor.currentTextChanged.connect(self.scaling_factor_change)
        self.label_custom_scaling_factor = QLabel('Custom scaling factor:')
        self.input_custom_scaling_factor = QLineEdit()
        self.input_custom_scaling_factor.setDisabled(True)
        self.input_custom_scaling_factor.textChanged.connect(self.custom_scaling_factor_change)

        #rate button
        self.btn_data_rate = QPushButton('Calculate')
        self.btn_data_rate.pressed.connect(self.btn_data_rate_pressed)
        self.display_data_rate = QLabel('')
        self.display_data_rate.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.initUI()
        self.show()

    def initUI(self):

        #layout
        layout = QGridLayout()
        #CA
        layout.addWidget(self.label_CA_carriers, 0, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_Carrier_components, 1, 0)
        layout.addWidget(self.input_Carrier_components, 1, 1)
        #MIMO
        layout.addWidget(self.label_MIMO, 2, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_MIMO_layers, 3, 0)
        layout.addWidget(self.input_MIMO_layers, 3, 1)
        layout.addWidget(self.label_MU_MIMO, 4, 0)
        layout.addWidget(self.checkbox_MU_MIMO, 4, 1)
        layout.addWidget(self.label_MU_MIMO_beams, 5, 0)
        layout.addWidget(self.input_MU_MIMO_beams, 5, 1)
        #modulation
        layout.addWidget(self.label_Modulation_order, 0, 3, 1, 4, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_table_number, 1, 3)
        layout.addWidget(self.combobox_table_number, 1, 4)
        layout.addWidget(self.label_mcs_index, 2, 3)
        layout.addWidget(self.spinbox_mcs, 2, 4)
        layout.addWidget(self.label_modulation, 1, 5)
        layout.addWidget(self.display_modulation, 1, 6)
        layout.addWidget(self.label_mod_order, 2, 5)
        layout.addWidget(self.display_mod_order, 2, 6)
        #Resource block
        layout.addWidget(self.label_resource_block, 3, 3, 1, 4, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_FR_band, 4, 3)
        layout.addWidget(self.FR_bands, 4, 4)
        layout.addWidget(self.label_subcarrier_spacing, 4, 5)
        layout.addWidget(self.scs_list, 4, 6)
        layout.addWidget(self.label_channel_bandwidth, 5, 5)
        layout.addWidget(self.bw_list, 5, 6)
        #other
        layout.addWidget(self.label_channel_scaling_factor, 6, 2, 1, 3)
        layout.addWidget(self.label_channel, 7, 0)
        layout.addWidget(self.ch_dir, 7, 1)
        layout.addWidget(self.label_scaling_factor, 7, 3)
        layout.addWidget(self.combobox_scaling_factor, 7, 4)
        layout.addWidget(self.label_custom_scaling_factor, 7, 5)
        layout.addWidget(self.input_custom_scaling_factor, 7, 6)
        #rate button
        layout.addWidget(self.btn_data_rate, 8, 2, 1, 3, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.display_data_rate, 9, 2, 1, 3, alignment=Qt.AlignmentFlag.AlignCenter)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def change_MU_MIMO_input(self, state):
        global MU_MIMO 
        MU_MIMO = self.checkbox_MU_MIMO.isChecked()
        if state == self.checkbox_MU_MIMO.isChecked():
            self.input_MU_MIMO_beams.setDisabled(True)
        else:
            self.input_MU_MIMO_beams.setDisabled(False)
    
    def change_mod_table(self, number):
        global Table_number
        Table_number = number
        self.mod_order = mod_order_table(int(number))
        self.spinbox_mcs.setRange(0, self.mod_order.shape[0] - 1)

    def mcs_change(self, mcs):
        global MCS_Index
        MCS_Index = mcs
        m_order = str(self.mod_order[MCS_Index][1])

        self.display_mod_order.setText(m_order)
        
        match m_order:
            case '2.0':
                self.display_modulation.setText('QPSK')
            case '4.0':
                self.display_modulation.setText('QAM-16')
            case '6.0':
                self.display_modulation.setText('QAM-64')
            case '8.0':
                self.display_modulation.setText('QAM-256')
            case '10.0':
                self.display_modulation.setText('QAM-1024')
            case _:
                self.display_modulation.setText('No match')

    def FR_band_change(self, band):
        global FR_band
        FR_band = band
        
        match band:
            case 'FR1':
                self.nrb = np.loadtxt(f'Nrb_FR1.csv', delimiter=';', skiprows=1, usecols=(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15))
                self.bw_l = np.loadtxt(f'Nrb_FR1.csv', delimiter=';', max_rows = 1, usecols=(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15))
                self.scs_l = np.loadtxt(f'Nrb_FR1.csv', delimiter=';', skiprows = 1, usecols=0)
                self.bw_list_vals = [str(x) for x in self.bw_l]
                self.scs_list_vals = [str(x) for x in self.scs_l]
            case 'FR2':
                self.nrb = np.loadtxt(f'Nrb_FR2.csv', delimiter=';', skiprows=1, usecols=(1,2,3,4))
                self.bw_l = np.loadtxt(f'Nrb_FR2.csv', delimiter=';', max_rows = 1, usecols=(1,2,3,4))
                self.scs_l = np.loadtxt(f'Nrb_FR2.csv', delimiter=';', skiprows = 1, usecols=0)
                self.bw_list_vals = [str(x) for x in self.bw_l]
                self.scs_list_vals = [str(x) for x in self.scs_l]
        
        self.scs_list.clear()
        self.scs_list.addItems(self.scs_list_vals)
        self.bw_list.clear()
        self.bw_list.addItems(self.bw_list_vals)

    def carrier_components_change(self, number):
        global n_carriers
        n_carriers = number

    def MIMO_layers_change(self, number):
        global MIMO_layers
        MIMO_layers = number

    def MU_MIMO_beams_change(self, number):
        global MU_MIMO_beams
        MU_MIMO_beams = number

    def scs_change(self, number):
        global scs
        scs = number

    def bw_change(self, number):
        global bw
        bw = number

    def ch_dir_change(self, ch):
        global channel_direction
        channel_direction = ch

    def scaling_factor_change(self, factor):
        global scaling_factor

        if factor != 'Custom':
            self.input_custom_scaling_factor.setDisabled(True)
            scaling_factor = float(factor)
        else:
            self.input_custom_scaling_factor.setDisabled(False)
    
    def custom_scaling_factor_change(self, factor):
        global scaling_factor
        global custom_scaling_factor
        scaling_factor = 'Custom'
        custom_scaling_factor = float(factor)
        print(custom_scaling_factor)


    def btn_data_rate_pressed(self):
        print(f'MIMO: {set_MIMO(MIMO_layers, MU_MIMO, MU_MIMO_beams)}')
        print(f'carriers: {n_carriers}')
        print(f'mcs: {MCS_Index}')
        print(f'scs: {scs}')
        print(f'bw: {bw}')
        print(f'FR: {FR_band}')
        print(f'channel: {channel_direction}')
        print(f'scaling: {set_scaling_factor(scaling_factor, custom_scaling_factor)}')
        print(f'table number: {Table_number}')
        print(f'data rate: {Data_Rate_Mbps(set_MIMO(MIMO_layers, MU_MIMO, MU_MIMO_beams), int(float(n_carriers)), MCS_Index, scs, bw, FR_band, channel_direction,  set_scaling_factor(scaling_factor, custom_scaling_factor), Table_number)}')
        R = (str(Data_Rate_Mbps(set_MIMO(MIMO_layers, MU_MIMO, MU_MIMO_beams), int(float(n_carriers)), MCS_Index, scs, bw, FR_band, channel_direction,  set_scaling_factor(scaling_factor, custom_scaling_factor), Table_number)))
        self.display_data_rate.setText(R + ' [Mbps]')


def window():
    app = QApplication(sys.argv)
    win = myWindow()

    sys.exit(app.exec())

window()