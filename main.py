from typing import overload
from xml.etree.ElementTree import tostring
import numpy as np

#MIMO layers - liczba, 38.802
#Modulation order - 38.214/804
#Nprb - 38.104

def mod_order_table(table_number):
    mod_order = np.loadtxt(f'mod_order_{table_number}.csv', delimiter=';', skiprows=1)

    return mod_order

def choose_Nrb_table(FR_band):

    Nrb_fr1 = np.loadtxt('Nrb_FR1.csv', delimiter=';', skiprows=1, usecols=(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15))
    Nrb_fr2 = np.loadtxt('Nrb_FR2.csv', delimiter=';', skiprows=1, usecols=(1,2,3,4))

    if FR_band == "FR1":

        nrb = {}
        BW = np.loadtxt('Nrb_FR1.csv', delimiter=';', max_rows = 1, usecols=(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15))
        SCS = np.loadtxt('Nrb_FR1.csv', delimiter=';', skiprows=1, usecols=0)
        for scs in range(Nrb_fr1.shape[0]):
            nrb[SCS[scs]] = {}
            for bw in range(Nrb_fr1.shape[1]):
                nrb[SCS[scs]][BW[bw]] = Nrb_fr1[scs][bw]

        return nrb
    else:

        nrb = {}
        BW = np.loadtxt('Nrb_FR2.csv', delimiter=';', max_rows = 1, usecols=(1,2,3,4))
        SCS = np.loadtxt('Nrb_FR2.csv', delimiter=';', skiprows=1, usecols=0)
        for scs in range(Nrb_fr2.shape[0]):
            nrb[SCS[scs]] = {}
            for bw in range(Nrb_fr2.shape[1]):
                nrb[SCS[scs]][BW[bw]] = Nrb_fr2[scs][bw]

        return nrb

def set_MIMO(MIMO_layers, MU_MIMO, MU_MIMO_beams):
    mimo = int(MIMO_layers)
    if MU_MIMO:
        mimo *= int(MU_MIMO_beams)

    return mimo

def set_scaling_factor(scaling_factor, custom_scaling_factor):
    f = 1
    if scaling_factor == "Custom":
        f = custom_scaling_factor
    else:
        f = scaling_factor

    return f

def Data_Rate_Mbps(MIMO, n_carriers, MCS_Index, scs, bw, FR_band, channel_direction, scaling_factor, Table_number):
    
    mod_order = mod_order_table(Table_number)
    config = choose_Nrb_table(FR_band)

    overhead = {
        "DL":
            {
                "FR1": 0.14,
                "FR2": 0.18
            },
        "UL":
            {
                "FR1": 0.08,
                "FR2": 0.10
            }
    }
    
    numerology = 0

    match scs:
        case '15.0':
            numerology = 0
        case '30.0':
            numerology = 1
        case '60.0':
            numerology = 2
        case '120.0':
            numerology = 3

    Tofdm = (pow(10, -3))/(14*pow(2, numerology))

    R = 0

    for j in np.arange(start = 1, stop = n_carriers+1, step = 1):
        R += ((MIMO * (mod_order[MCS_Index][1]) * (scaling_factor)) * (mod_order[MCS_Index][2]/1024) * (((config[int(float(scs))][int(float(bw))]) * 12)/(Tofdm)) * (1 - overhead[channel_direction][FR_band]))

    R *= pow(10, -6)

    return np.round(R, 0)

# CA
n_carriers = 3

# MIMO
MIMO_layers = 4
MU_MIMO = False
MU_MIMO_beams = 4

# Resource block
scs = 60
bw = 40
FR_band = "FR1"
channel_direction = "DL"

# Modulation order
MCS_Index = 18
Table_number = 1

# Scaling factor
scaling_factor = 1
custom_scaling_factor = 1

#print(Data_Rate_Mbps(set_MIMO(MIMO_layers, MU_MIMO, MU_MIMO_beams), n_carriers, MCS_Index, scs, bw, FR_band, channel_direction,  set_scaling_factor(scaling_factor, custom_scaling_factor)))

#trzeba zrobić gui i wykresy