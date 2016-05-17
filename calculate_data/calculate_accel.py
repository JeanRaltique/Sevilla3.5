import numpy as np
from process_signals import smooth, detect_peaks

#def max acceleration
def ACCel_indexes(ACCKneeX, ACCKneeY, ACCKneeZ, start, run_period):
    # smooth each channel
    smx = smooth(ACCKneeX, window_len=75)
    smy = smooth(ACCKneeY, window_len=75)
    smz = smooth(ACCKneeZ, window_len=75)

    # rms of the signal
    sm_rms = np.sqrt(smx ** 2 + smy ** 2 + smz ** 2)

    # root_signals
    sm_rms_root = sm_rms - np.mean(sm_rms)
    # find indexes of peaks
    valley_ind_val = detect_peaks(sm_rms_root, valley=True, mpd=250, mph=-0.5*min(sm_rms_root), show=False)
    # select indexes after the change of direction
    ind_after = valley_ind_val[valley_ind_val > (start + run_period)]
    # select indexes before the change of direction
    ind_before = valley_ind_val[valley_ind_val < (start + run_period)]

    # Borders issues:
    # if found the segmented signal
    if (len(ind_after) > 1):
        win_ind1 = ind_after[0]
        win_ind2 = ind_after[1]
    # if no minimum found, select the last peak
    elif (len(ind_after) < 1):
        win_ind1 = ind_before[-1]
        win_ind2 = len(sm_rms)
    # if found one minimum
    else:
        # if doesn't have space enough for a peak until the end of the sigal window
        if (len(sm_rms) - ind_after[0] < 250):
            win_ind1 = ind_before[-1]
            win_ind2 = ind_after[0]
        # if space is enough select from minimum to length of sgnal window
        else:
            win_ind1 = ind_after[0]
            win_ind2 = len(sm_rms)

    # find max and pre-max
    smooth_max_ACC = np.argmax(sm_rms[win_ind1:win_ind2])
    ind_max = win_ind1 + smooth_max_ACC
    # find peaks before max peak
    pre_peak_ind = detect_peaks(sm_rms[0:ind_max])

    # select peak right before the main peak, if the distance is minimum (50 dots)
    if (ind_max - pre_peak_ind[-1]) < 90:
        preact_ind = pre_peak_ind[-2]
    else:
        preact_ind = pre_peak_ind[-1]


    return ind_max, preact_ind, valley_ind_val, sm_rms


def abs_max(ind_max, ACCx, ACCy, ACCz):
    max_accx = np.mean(ACCx[ind_max - 10:ind_max + 10])
    max_accy = np.mean(ACCy[ind_max - 10:ind_max + 10])
    max_accz = np.mean(ACCz[ind_max - 10:ind_max + 10])

    absolute_max = (max_accx ** 2 + max_accy ** 2 + max_accz ** 2) ** 0.5

    return absolute_max


def abs_preact(preact_ind, ACCx, ACCy, ACCz):
    # max Pre_activation
    pre_actx = ACCx[preact_ind - 10:preact_ind + 10]
    pre_acty = ACCy[preact_ind - 10:preact_ind + 10]
    pre_actz = ACCz[preact_ind - 10:preact_ind + 10]

    absolute_preact = (pre_actx ** 2 + pre_acty ** 2 + pre_actz ** 2) ** 0.5

    return absolute_preact
