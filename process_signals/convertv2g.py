def convertV2G(signal, vmin, vmax):
    vmean = (vmax+vmin)/2
    v_g = (signal-vmean)/(vmax-vmean)
    return v_g