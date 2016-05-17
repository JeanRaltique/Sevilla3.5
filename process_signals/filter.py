import numpy as np



def smooth(input_signal, window_len = 50, window = 'hanning'):
    if input_signal.ndim != 1:
        raise ValueError ("smooth only accepts 1 dimension arrays.")
    if window_len < 3:
        return input_signal
    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError ("Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")
    sig = np.r_[2*input_signal[0]-input_signal[window_len:1:-1], input_signal, 2*input_signal[-1]-input_signal[-1:-window_len:-1]]
    if window == 'flat':  # moving average
        win = np.ones(window_len, 'd')
    else:
        win = eval('np.' + window + '(window_len)')
    # convolution:
    sig_conv = np.convolve(win / win.sum(), sig, mode='same')
    return sig_conv[window_len - 1:-window_len + 1]



def RMS_moving_window(signal, window = 200):

    #RMS Moving Window
    border_signal = np.zeros(window)                              #For the beginning of the signal
    sample_number = 0
    n_samples = len(signal)
    RMS_Total = np.zeros(n_samples)
    while sample_number < n_samples:
        process_signal = []
        #for the first 250 samples
        if sample_number <= 250:
            process_signal += list(border_signal[sample_number:window-1])
            process_signal += list(signal[0:sample_number+window-1])
        #for the last 250 samples
        elif sample_number > ((n_samples-1)-window):
            s = (sample_number + window) - n_samples
            process_signal += list(signal[sample_number-window:n_samples-1])
            process_signal += list(border_signal[0:s])
        #for the samples between 250 and length - 250
        else:
            process_signal += list(signal[(sample_number-window):(sample_number+(window-1))])
        RMS_Total[sample_number] = compute_RMS(np.array(process_signal))
        sample_number+=1

    return RMS_Total

def compute_RMS(signal):
    return np.sqrt(sum(signal**2)/len(signal))
    