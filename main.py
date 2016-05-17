from __future__ import unicode_literals
import os
from emg_processing import emg_process


#select patient to process
#Main directory

MAIN_D = os.path.realpath("Data/EMG Data Collection from Sergio Romero, PhD (University of Seville)")
#MAIN_D = os.path.realpath("Data/EMG Data Collection from Sergio Romero, PhD (University of Seville)/First Measure Control Group (GC)")


GROUP_FOLDERS = os.listdir(MAIN_D)
print (GROUP_FOLDERS)

for g_folder in GROUP_FOLDERS:
    FOLDERS_DIR = os.path.realpath(MAIN_D + "/" + g_folder)
    FOLDERS = os.listdir(FOLDERS_DIR)
    for file_D in FOLDERS:
        if "." not in str(file_D):
    #if "." not in str(g_folder):
            print("file in: ", MAIN_D + g_folder + "/" + file_D + "/")
            #print ("file in: ", MAIN_D + "/" + g_folder  + "/")
            emg_process("calib_knee.txt", file_D, MAIN_D + "/" + g_folder + "/" + file_D + "/", doplot=True)
            #emg_process("calib_knee.txt", g_folder, MAIN_D + "/" + g_folder + "/", doplot=True)
