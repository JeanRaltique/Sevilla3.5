import numpy as np

def root_signal(sig):
    root_sig = sig - np.mean(sig)
    return root_sig