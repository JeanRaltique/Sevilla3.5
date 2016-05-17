import numpy as np
from process_signals import smooth
from process_signals import root_signal
from load_channels.read_file import read_header
from scipy.ndimage import filters


def load_channel_emg(file, ch_n):

    version, date, time, fs_original, channels, nbits, mac, dig_channels = read_header(file)
    ch_values = []    #vector containing the values from channel 'ch'

    for line in open(file):
        curr_line = line.split()    #current line

        if(curr_line[0] != '#'):
            ch_values.append(float(curr_line[ch_n - 1]))

    raw_data = np.array(ch_values)
    data = root_signal(raw_data)
    #data = abs(smooth(data, window_len=100))

    return data, raw_data


def load_channel(file, ch_n):

    version, date, time, fs_original, channels, nbits, mac, dig_channels = read_header(file)
    ch_values = []    #vector containing the values from channel 'ch'

    for line in open(file):
        curr_line = line.split()    #current line

        if(curr_line[0] != '#'):
            ch_values.append(float(curr_line[ch_n - 1]))

    data = np.array(ch_values)

    return data