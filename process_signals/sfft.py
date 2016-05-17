from scipy import fft
import numpy as np

def sfft(signal, fmax, doplot = True):

    mags =  abs(fft(signal))
    freqs = np.linspace(0, fmax/2, len(signal)/2)


    return (freqs[1 : len(signal)/2].copy(), mags[1: len(signal)/2].copy())
