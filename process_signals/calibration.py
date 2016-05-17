import os
import numpy as np
from process_signals import filter



def calibration(file_name, directory, standard_calibration = True):

    if(standard_calibration == True):

        directory = os.path.realpath("/home/jeanraltique/PycharmProjects/Sevilla_3.4/Data")
        file_name = "xyzcal.txt"
        files = os.listdir(directory)
        for i in files:
            if i == file_name:
                dir_i = directory + "/" + i
                # load data from selected file
                d = np.loadtxt(dir_i)
                # select channels (7:10) are the columns for calibration
                file = d
                return std_calib(i, file)


    files = os.listdir(directory)
    #s = input("Enter channels used for acc calibration: ")
    #channels = [int(i) for i in s.split()]

    #check files in directory
    for i in files:
        #open file named for calibration
        if i == file_name:
            dir_i = directory + "/" + i
            #load data from selected file
            d = np.loadtxt(dir_i)
            #select channels (7:10) are the columns for calibration
            file = d[:, 7:10]
            return calib(i, file)

def calib(i, file):
    Sgn_X = filter.smooth(file[:,0], window_len=200)
    Sgn_X_max = max(Sgn_X)
    Sgn_X_min = min(Sgn_X)

    Sgn_Y = filter.smooth(file[:,1], window_len=200)
    Sgn_Y_max = max(Sgn_Y)
    Sgn_Y_min = min(Sgn_Y)

    Sgn_Z = filter.smooth(file[:,2], window_len=200)
    Sgn_Z_max = max(Sgn_Z)
    Sgn_Z_min = min(Sgn_Z)

    X_Cal = [Sgn_X_max, Sgn_X_min]
    Y_Cal = [Sgn_Y_max, Sgn_Y_min]
    Z_Cal = [Sgn_Z_max, Sgn_Z_min]

    return X_Cal, Y_Cal, Z_Cal

def std_calib(i, file):
    Sgn_X = filter.smooth(file[2500:4999], window_len=200)
    Sgn_X_max = max(Sgn_X)
    Sgn_X_min = min(Sgn_X)

    Sgn_Y = filter.smooth(file[5000:7499], window_len=200)
    Sgn_Y_max = max(Sgn_Y)
    Sgn_Y_min = min(Sgn_Y)

    Sgn_Z = filter.smooth(file[7500:9999], window_len=200)
    Sgn_Z_max = max(Sgn_Z)
    Sgn_Z_min = min(Sgn_Z)

    X_Cal = [Sgn_X_max, Sgn_X_min]
    Y_Cal = [Sgn_Y_max, Sgn_Y_min]
    Z_Cal = [Sgn_Z_max, Sgn_Z_min]

    return X_Cal, Y_Cal, Z_Cal