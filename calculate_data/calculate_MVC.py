import os
import numpy as np
from load_channels import load_channel
from process_signals import root_signal, smooth, RMS_moving_window
from scipy.ndimage import filters


def calculate_MVC_hamstring(dir_files):

    for file in os.listdir(dir_files):

            if "hamstring" in file or "hamstrings" in file:
                f = open(dir_files + "/" + file, 'r')
                f_head = [f.readline() for i in range(9)]
                first_line = f_head[8].split()

                for i in range(len(first_line)):
                    if(int(first_line[i]) > 1000):
                        channel1 = i+1
                        channel2 = i+2
                        break

                #-------------------------------------------
                #      Select which channel s activated
                #-------------------------------------------
                emg_MVC_1 = load_channel(dir_files + "/" + file,channel1)
                emg_MVC_2 = load_channel(dir_files + "/" + file,channel2)
                #Select channel based in the sum of absolute values of the rooted signal


                #the channel with the highest sum is more activated
                emg_smooth1 = max(abs(smooth(root_signal(emg_MVC_1), window_len=50)))
                emg_smooth2 = max(abs(smooth(root_signal(emg_MVC_2), window_len=50)))

                if(emg_smooth1>emg_smooth2):
                    emg_MVC_root = reject_outliers(emg_MVC_1, m = 6)
                else:
                    emg_MVC_root = reject_outliers(emg_MVC_2, m = 6)

                MVC = max(abs(emg_MVC_root))

                return float(MVC), emg_MVC_root

#------------------------------------------------------------------------------
#Carefully use this function. It removes dots and is not recomended to use if
#time or frequency analysis will be performed
#------------------------------------------------------------------------------
def reject_outliers(data, m = 2):
    data[abs(data - np.mean(data)) > m * np.std(data)] = 0
    return data
#------------------------------------------------------------------------------

def calculate_MVC_femoris(dir_files):


    for file in os.listdir(dir_files):

        print ("calculate MVC femoris, file = ", file)

        if "femoris" in file:
            f = open(dir_files + "/" + file, 'r')
            f_head = [f.readline() for i in range(9)]
            first_line = f_head[8].split()

            for i in range(len(first_line)):
                if(int(first_line[i]) > 1000):
                    channel1 = i+1
                    channel2 = i+2
                    break

            emg_MVC_1 = load_channel(dir_files + "/" + file, channel1)
            emg_MVC_2 = load_channel(dir_files + "/" + file, channel2)

            emg_smooth1 = max(abs(smooth(root_signal(emg_MVC_1), window_len=50)))
            emg_smooth2 = max(abs(smooth(root_signal(emg_MVC_2), window_len=50)))

            if (emg_smooth1 > emg_smooth2):
                emg_MVC_root = reject_outliers(emg_MVC_1, m=6)
            else:
                emg_MVC_root = reject_outliers(emg_MVC_2, m=6)

            MVC = max(abs(emg_MVC_root))

            return float(MVC), emg_MVC_root