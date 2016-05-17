import os
import numpy as np

def get_file_name(folder):

    file_name = folder.split('/')[-2]

    return file_name

def list_files(path):
    dirList=os.listdir(path)

    return dirList

#read header
def read_header(source_file, print_header = False):

    f = open(source_file, 'r')

    f_head = [f.readline() for i in range(9)]

    version = int( f_head[1].split()[2] )
    #start date
    date = f_head[2].split()[2]
    #start time
    time = f_head[2].split()[3]
    #sampling frequency
    fs = int(f_head[3].split()[2])
    #number the sampled channels
    channels = np.array(f_head[4].split()[2:]).astype(int)
    #number of bits
    nbits = int( f_head[5].split()[2] )
    #acquisition device information (mac address)
    mac = f_head[6].split()[2]

    #get the first line of data to obtain the number of digital channels
    line1 = f_head[8].split()

    #dig channels is the difference between the number of columns in the first data line
    #and the total number of channels. This enables to select the correct channel when desired
    dig_channels = len(line1) - len(channels) - 1

    return version, date, time, fs, channels, nbits, mac, dig_channels

