import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import seaborn as sns
from matplotlib.figure import SubplotParams



def plot_data(valey_index, sm_rms, file_name, max_acceleration, preact_index, ACC_X_amplitude, ACC_Y_amplitude, ACC_Z_amplitude, EMG_femoris, EMG_hamstring, Femoris_freq_X, Femoris_freq, Hamstring_freq_X,  Hamstring_freq):

    # color
    face_color_r = 248 / 255.0
    face_color_g = 247 / 255.0
    face_color_b = 249 / 255.0

    # pars
    left = 0.05  # the left side of the subplots of the figure
    right = 0.95  # the right side of the subplots of the figure
    bottom = 0.05  # the bottom of the subplots of the figure
    top = 0.92  # the top of the subplots of the figure
    wspace = 0.2  # the amount of width reserved for blank space between subplots
    hspace = 0.6  # the amount of height reserved for white space between subplots

    pars = SubplotParams(left, bottom, right, top, wspace, hspace)
    pre_act_patch = mpatches.Patch(color='springgreen')
    max_acc_patch = mpatches.Patch(color='crimson')

    # figure
    fig = plt.figure(figsize=(22, 14), facecolor=(face_color_r, face_color_g, face_color_b), dpi=50, subplotpars=pars)
    fig.suptitle(file_name, fontsize=20, horizontalalignment='center', verticalalignment='top')
    fig.legend(labels=[ 'Maximum Acceleration', 'Preactivation Peak'], handles=[max_acc_patch, pre_act_patch], fontsize=14)

    #seaborn layout with whitegrid
    with sns.axes_style("whitegrid"):

        # subplot
        ax1 = plt.subplot(611)
        ax1.patch.set_facecolor('ivory')
        ax1.plot(np.linspace(0, len(ACC_X_amplitude) / 1000.0, len(ACC_X_amplitude)), ACC_X_amplitude, color='darkslategray',
                linewidth=1.5)
        #ax1.plot(sm_rms)
        ax1.axis('tight')
        ax1.plot(valey_index/1000.0, ACC_X_amplitude[valey_index], 'ro')

        m = 0.1 * max(ACC_X_amplitude)
        ax1.axvline(max_acceleration / 1000.0, min(ACC_X_amplitude) - m, max(ACC_X_amplitude) + m, color='crimson',
                    linestyle='solid', linewidth=2.0)
        ax1.axvline(preact_index / 1000.0, min(ACC_X_amplitude) - m, max(ACC_X_amplitude) + m, color='springgreen',
                    linestyle='solid', linewidth=2.0)
        ax1.set_title(r'ACC_X ', size=12)
        ax1.set_ylabel("Acceleration (g)")
        ax1.set_xlabel("Time(s)")

        ax2 = plt.subplot(612)
        ax2.plot(np.linspace(0, len(ACC_Y_amplitude) / 1000.0, len(ACC_Y_amplitude)), ACC_Y_amplitude, color='darkslategray',
                 linewidth=1.5)
        ax2.plot(valey_index / 1000.0, ACC_Y_amplitude[valey_index], 'ro')
        ax2.axis('tight')
        m = 0.1 * max(ACC_Y_amplitude)
        ax2.axvline(max_acceleration / 1000.0, min(ACC_Y_amplitude) - m, max(ACC_Y_amplitude) + m, color='crimson',
                    linestyle='solid', linewidth=2.0)
        ax2.axvline(preact_index / 1000.0, min(ACC_X_amplitude) - m, max(ACC_X_amplitude) + m, color='springgreen',
                    linestyle='solid', linewidth=2.0)
        ax2.patch.set_facecolor('ivory')
        ax2.set_title(r'ACC_Y', size=12)
        ax2.set_ylabel("Acceleration (g)")
        ax2.set_xlabel("Time(s)")

        ax3 = plt.subplot(613)
        ax3.patch.set_facecolor('ivory')
        ax3.plot(np.linspace(0, len(ACC_Z_amplitude) / 1000.0, len(ACC_Z_amplitude)), ACC_Z_amplitude, color='darkslategray',
                 linewidth=1.5)
        ax3.axis('tight')
        m = 0.1 * max(ACC_Z_amplitude)
        ax3.axvline(max_acceleration / 1000.0, min(ACC_Z_amplitude) - m, max(ACC_Z_amplitude) + m, color='crimson',
                    linestyle='solid', linewidth=2.0)
        ax3.axvline(preact_index / 1000.0, min(ACC_X_amplitude) - m, max(ACC_X_amplitude) + m, color='springgreen',
                    linestyle='solid', linewidth=2.0)
        ax3.set_title(r'ACC_Z', size=12)
        ax3.set_ylabel("Acceleration (g)")
        ax3.set_xlabel("Time(s)")

        ax4 = plt.subplot(614)
        ax4.patch.set_facecolor('ivory')
        ax4.plot(np.linspace(0, len(EMG_femoris) / 1000.0, len(EMG_femoris)), EMG_femoris,
                 color='darkslategray', linewidth=1.5)
        ax4.axvline(preact_index/ 1000.0, min(ACC_X_amplitude) - m, max(ACC_X_amplitude) + m, color='springgreen',
                    linestyle='solid', linewidth=2.0)
        ax4.axis('tight')
        m = 0.1 * max(EMG_femoris)
        ax4.axvline(max_acceleration / 1000.0, min(EMG_femoris) - m, max(EMG_femoris) + m, color='crimson',
                    linestyle='solid', linewidth=2.0)
        ax4.set_title(r'EMG Femoris', size=12)
        ax4.set_ylabel("%MVC")
        ax4.set_xlabel("Time(s)")


        ax5 = plt.subplot(6, 2, 11)
        ax5.patch.set_facecolor('ivory')
        ax5.plot(Femoris_freq_X, Femoris_freq, color='darkslategray', linewidth=1.5)
        ax5.axis('tight')
        ax5.set_title(r"EMG Femoris - Frequency analysis in the knee's maximum acceleration", size=12)
        ax5.set_ylabel("Amplitude (mV)")
        ax5.set_xlabel("Frequency (Hz)")


        ax6 = plt.subplot(615)
        ax6.patch.set_facecolor('ivory')
        ax6.plot(np.linspace(0, len(EMG_hamstring) / 1000.0, len(EMG_hamstring)), EMG_hamstring,
                 color='darkslategray', linewidth=1.5)

        ax6.axis('tight')
        m = 0.1 * max(EMG_hamstring)
        ax6.axvline(max_acceleration/1000.0, min(EMG_hamstring) - m, max(EMG_hamstring) + m, color='crimson',
                    linestyle='solid', linewidth = 2.0)
        ax6.axvline(preact_index / 1000.0, min(ACC_X_amplitude) - m, max(ACC_X_amplitude) + m, color='springgreen',
                    linestyle='solid', linewidth=2.0)
        ax6.set_title(r'EMG Hamstring', size=12)
        ax6.set_ylabel("%MVC")
        ax6.set_xlabel("Time(s)")


        ax7 = plt.subplot(6, 2, 12)
        ax7.patch.set_facecolor('ivory')
        ax7.plot(Hamstring_freq_X, Hamstring_freq, color='darkslategray', linewidth=1.5)
        ax7.axis('tight')
        ax7.set_title(r"EMG Hamstring - Frequency analysis in the knee's maximum acceleration", size=12)
        ax7.set_ylabel("Amplitude (mV)")
        ax7.set_xlabel("Frequency (Hz)")
    sns.despine()
    return fig