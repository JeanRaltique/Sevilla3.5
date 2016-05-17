from __future__ import unicode_literals
import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.pylab import find
from load_channels import get_file_name, load_channel, load_channel_emg
from calculate_data import calculate_MVC_femoris, calculate_MVC_hamstring, ACCel_indexes, get_limits, abs_max, abs_preact
from process_signals import calib, calibration, convertV2G, sfft,compute_RMS, smooth, detect_peaks
from matplotlib.figure import SubplotParams
import seaborn as sns
from plot_data import plot_data
from pdf_report_creator import pdf_report_creator



def emg_process(calib_file_name, subject_name, file_path = None, doplot = True):

    #close previously opened plots.
    plt.close('all')

    #Eachs subject's directory of files
    ACC_CALIBRATION = os.path.realpath(file_path + "ACC_CALIBRATION/")
    SIGNALS = os.path.realpath(file_path + "SIGNALS/")
    EMG_MVC = os.path.realpath(file_path + "EMG_MVC/")


    """
    channels 1,2,3 (ACCknee)
    channel  4 	   (EMG_femoris)
    channel  5	   (EMG_hamstring)
    """

    all_files = os.listdir(file_path)

    print ("DOPLOT = ", doplot)


    #Open pdf and saves images in it
    #Open report.txt file and saves necessary data in it
    if doplot == True:
        pp, REPORTfile = pdf_report_creator(file_path)

    # ------------------------------------------------------------------------------------------------
    #                                 Knee Calibration
    # ------------------------------------------------------------------------------------------------

    print("\nKnee Calibration")

    # performs calibration of the Accelerometer based on the '.txt' file in ACC_Calibration path
    # if the calibration signal is not correct, select a standard file for calibration: xyzcal.txt
    X_Cal_K, Y_Cal_K, Z_Cal_K = calibration(calib_file_name, ACC_CALIBRATION, standard_calibration=True)

    # values of the knee calibration
    Vmin_X_K = X_Cal_K[1]
    Vmax_X_K = X_Cal_K[0]
    Vmin_Y_K = Y_Cal_K[1]
    Vmax_Y_K = Y_Cal_K[0]
    Vmin_Z_K = Z_Cal_K[1]
    Vmax_Z_K = Z_Cal_K[0]


    #------------------------------------------------------------------------------------------------
    #                                 Calculate Maximum Voluntary Contraction
    #------------------------------------------------------------------------------------------------

    #Calculate MVC
    MVC_femoris, emg_fsmooth = calculate_MVC_femoris(EMG_MVC)
    MVC_hamstring, emg_hsmooth = calculate_MVC_hamstring(EMG_MVC)

    #------------------------------------------------------------------------------------------------
    #                                   SIGNALS
    #------------------------------------------------------------------------------------------------

    #load and read all '.txt' files in SIGNALS folder
    #performs a frequency analysis of the EMG signal
    #find the maximum acceleration values
    #plot tests
    #save plots in PDF
    #create a report.txt file with relevant results

    print ("\nOpened SIGNALS folder. Processing Signals from: ", subject_name)
    for file_name in os.listdir(SIGNALS):
        if (("dj" not in file_name) and "DJ" not in file_name) and file_name[0] != '.':
            print ("\nFILE NAME = ", file_name)

            file = os.path.realpath(SIGNALS + "/" + file_name)

            print ("\nLoading channels...")

            #channels 4, 5 and 6 are used for the knee acceleration
            #and channels 7 and 8/9 for emg_femoris_and_hamstring
            ACCKneeX    =   load_channel(file,4)
            ACCKneeY    =   load_channel(file,5)
            ACCKneeZ    =   load_channel(file,6)
            emg_femoris, emg_femoris_raw = load_channel_emg(file, 7)

            f = open(file, 'r')
            f_head = [f.readline() for i in range(9)]
            first_line = f_head[8].split()
            if (first_line[7] == '0'):
                emg_hamstring, emg_hamstring_raw = load_channel_emg(file, 9)
            else:
                emg_hamstring, emg_hamstring_raw = load_channel_emg(file, 8)

            print ("done")

            #------------- KNEE --------------#

            #Acceleration
            ACCKneeX_G = convertV2G(ACCKneeX, Vmin_X_K, Vmax_X_K)
            ACCKneeY_G = convertV2G(ACCKneeY, Vmin_Y_K, Vmax_Y_K)
            ACCKneeZ_G = convertV2G(ACCKneeZ, Vmin_Z_K, Vmax_Z_K)

            # start running (differentiation of the ACCX signal)
            events = np.argwhere(smooth(abs(100 * np.diff(ACCKneeX)), window_len=200) > 500)
            start = events[0]
            # running period
            run_period = 2500

            # threshold of the signal window
            threshold_window = start + run_period + 100
            # find peak
            if (threshold_window < (len(ACCKneeX))):

                # calculate parameters
                max_index, preact_index, valley_ind_val, sm_rms = ACCel_indexes(ACCKneeX, ACCKneeY, ACCKneeZ, start, run_period)
                #run_period = 2500

                #find maximums
                ACC_max = abs_max(max_index, ACCKneeX_G, ACCKneeY_G, ACCKneeZ_G)
                Preact_max = abs_preact(preact_index, ACCKneeX_G, ACCKneeY_G, ACCKneeZ_G)

                print("\nFrequency Analysis...")
                n_samples = len(ACCKneeX)
                #defining a window where the frequency analysis will be done
                min_knee, max_knee = get_limits(ACC_max, n_samples, 500)

                #Performing an FFT to the EMG_femoris and hamstring signals with a maximum frequency of 100 Hz
                freqs_femoris_knee, mags_femoris_knee = sfft(emg_femoris_raw[min_knee:max_knee]/float(MVC_femoris), 100)
                freqs_hamstring_knee, mags_hamstring_knee = sfft(emg_hamstring_raw[min_knee:max_knee]/float(MVC_hamstring), 100)

                #Calculating the EMG frequency in the maximum acceleration
                maximum_freq_femoris_knee_position = find(mags_femoris_knee == max(mags_femoris_knee))
                maximum_freq_femoris_knee = float(freqs_femoris_knee[maximum_freq_femoris_knee_position])

                maximum_freq_hamstring_knee_position = find(mags_hamstring_knee == max(mags_hamstring_knee))
                maximum_freq_hamstring_knee = float(freqs_hamstring_knee[maximum_freq_hamstring_knee_position])

                #-------------------------------------------
                #                  Plot Test
                #-------------------------------------------

                print("\nPrinting results...")

                emg_femoris_MVC = 100.0*(emg_femoris/float(MVC_femoris))
                emg_hamstring_MVC = 100.0*(emg_hamstring/float(MVC_hamstring))

                fig = plot_data(valley_ind_val, sm_rms, file_name, max_index, preact_index, ACCKneeX_G, ACCKneeY_G, ACCKneeZ_G, emg_femoris_MVC, emg_hamstring_MVC, freqs_femoris_knee, mags_femoris_knee, freqs_hamstring_knee, mags_hamstring_knee)



            # #color
            #     face_color_r = 248 / 255.0
            #     face_color_g = 247 / 255.0
            #     face_color_b = 249 / 255.0
            #
            #     # pars
            #     left = 0.05  # the left side of the subplots of the figure
            #     right = 0.95  # the right side of the subplots of the figure
            #     bottom = 0.05  # the bottom of the subplots of the figure
            #     top = 0.92  # the top of the subplots of the figure
            #     wspace = 0.2  # the amount of width reserved for blank space between subplots
            #     hspace = 0.6  # the amount of height reserved for white space between subplots
            #
            #     pars = SubplotParams(left, bottom, right, top, wspace, hspace)
            #
            #     # figure
            #     fig = plt.figure(figsize=(22, 14), facecolor=(face_color_r, face_color_g, face_color_b), dpi=50,
            #                      subplotpars=pars)
            #     fig.suptitle(file_name, fontsize=20, horizontalalignment='center', verticalalignment='top')
            #
            #
            #     #seaborn layout with whitegrid
            #     with sns.axes_style("whitegrid"):
            #
            #         ax1 = plt.subplot(511)
            #         ax1.patch.set_facecolor('ivory')
            #         ax1.plot(sm_rms, color='darkslategray', linewidth=1.5)
            #         ax1.plot(valley_ind_val, sm_rms[valley_ind_val], 'ro')
            #         ax1.axis('tight')
            #         ax1.set_ylim([0,max(sm_rms)])
            #         ax1.axvline(start, color='springgreen', linestyle='solid')
            #         ax1.annotate('Started Running', xy=(start, max(sm_rms)), xytext=(start+100, max(sm_rms)),
            #                      arrowprops=dict(facecolor='black', shrink=0.1))
            #         ax1.axvline(start + run_period, color='springgreen', linestyle='solid')
            #         ax1.annotate('next peak is the change of direction', xy=(start+run_period, max(sm_rms)), xytext=(start + run_period + 100, max(sm_rms)),
            #                      arrowprops=dict(facecolor='black', shrink=0.1))
            #         ax1.set_title(r'ACC_smoothed ', size=12)
            #         ax1.set_ylabel("Acceleration (mV)")
            #         ax1.set_xlabel("Time(ms)")
            #
            #         ax2 = plt.subplot(512)
            #         ax2.patch.set_facecolor('ivory')
            #         ax2.plot(sm_rms, color='darkslategray', linewidth=1.5)
            #         ax2.axis('tight')
            #         ax2.axvline(win_ind1, color='springgreen', linestyle='solid')
            #         ax2.axvline(win_ind2, color='springgreen', linestyle='solid')
            #         ax2.plot(np.linspace(win_ind1, win_ind2, win_ind2 - win_ind1), sm_rms[win_ind1:win_ind2], color='darkslategray',
            #                  linewidth=1.5)
            #         ax2.plot(max_index, sm_rms[max_index], 'ro')
            #         ax2.plot(preact_index, sm_rms[preact_index], 'ro')
            #         ax2.annotate('Pre Act', xy=(preact_index, sm_rms[preact_index]), xytext=(preact_index, sm_rms[preact_index] + 300),
            #                      arrowprops=dict(facecolor='black', shrink=0.05))
            #         ax2.annotate('Max Act', xy=(max_index, sm_rms[max_index]), xytext=(max_index, sm_rms[max_index] + 300),
            #                      arrowprops=dict(facecolor='black', shrink=0.05))
            #         ax2.set_title(r'ACC_smoothed ', size=12)
            #         ax2.set_ylabel("Acceleration (mV)")
            #         ax2.set_xlabel("Time(ms)")
            #
            #         ax3 = plt.subplot(513)
            #         ax3.patch.set_facecolor('ivory')
            #         ax3.plot(ACCKneeX, color='darkslategray', linewidth=1.5)
            #         ax3.axvline(preact_index, color='red', linestyle='solid')
            #         ax3.axvline(max_index, color='red', linestyle='solid')
            #         ax3.axis('tight')
            #         ax3.set_title(r'ACC_X ', size=12)
            #         ax3.set_ylabel("Acceleration (mV)")
            #         ax3.set_xlabel("Time(ms)")
            #
            #         ax4 = plt.subplot(514)
            #         ax4.patch.set_facecolor('ivory')
            #         ax4.plot(ACCKneeY, color='darkslategray', linewidth=1.5)
            #         ax4.axvline(preact_index, color='red', linestyle='solid')
            #         ax4.axvline(max_index, color='red', linestyle='solid')
            #         ax4.axis('tight')
            #         ax4.set_title(r'ACC_Y ', size=12)
            #         ax4.set_ylabel("Acceleration (mV)")
            #         ax4.set_xlabel("Time(ms)")
            #
            #         ax5 = plt.subplot(515)
            #         ax5.patch.set_facecolor('ivory')
            #         ax5.plot(ACCKneeZ, color='darkslategray', linewidth=1.5)
            #         ax5.axvline(preact_index, color='red', linestyle='solid')
            #         ax5.axvline(max_index, color='red', linestyle='solid')
            #         ax5.axis('tight')
            #         ax5.set_title(r'ACC_Z ', size=12)
            #         ax5.set_ylabel("Acceleration (mV)")
            #         ax5.set_xlabel("Time(ms)")

                #Returns the instant where the maximum acceleration occurred
                #accel_max_knee, absolute_acc_knee, max_absolute_acc_knee = max_accel(ACCKneeX_G, ACCKneeY_G, ACCKneeZ_G)

                #-------------------------------------------
                #                  Plot Test
                #-------------------------------------------

                pp.savefig()
                print("\nCalculating maximum acceleration...")


        #fig = plot_data(file_name, accel_max_knee, ACCKneeX_G, ACCKneeY_G, ACCKneeZ_G, emg_femoris_MVC, emg_hamstring_MVC, freqs_femoris_knee, mags_femoris_knee, freqs_hamstring_knee, mags_hamstring_knee)

        #fig.show()
        #plt.show()


        #save figures in PDF


        newLine = '\n----------------------------------------------------------------------\n'


        #In report file integrate:
        #Max ACCX,Y and Z after 3 s
        #Preactivation: smooth signal and find peak with pre-peak
        #MVC with max acceleration
        #max acceleration in landing
        #max emg in max landing acceleration

        print("\nCreating Report file...")
        #Save Report
        REPORTfile.write(newLine)
        REPORTfile.write(str(file_name) + "\n")
        REPORTfile.write("Maximum knee total acceleration (in CD): "+ str(ACC_max) + " g\n")
        REPORTfile.write("Maximum ACCX: " + str(max(np.mean(ACCKneeX_G[max_index-10:max_index+10]))) + ' g\n')
        REPORTfile.write("Maximum ACCY: " + str(max(ACCKneeY_G[max_index-10:max_index+10])) + ' g\n')
        REPORTfile.write("Maximum ACCZ: " + str(max(ACCKneeZ_G[max_index-10:max_index+10])) + ' g\n')
        REPORTfile.write("%MVC [Rectus Femoris]: " + str(emg_femoris_MVC[max_index-10:max_index+10])+' %\n')
        REPORTfile.write("%MVC [Hamstring]: " + str(emg_hamstring_MVC[max_index-10:max_index+10])+' %\n')
        REPORTfile.write("RMS [Rectus Femoris]: " + str(RMS_femoris_knee)+'\n')
        REPORTfile.write("RMS [Hamstring]: " + str(RMS_hamstring_knee)+'\n')
        REPORTfile.write("Frequency [Rectus Femoris]: " + str(maximum_freq_femoris_knee)+'\n')
        REPORTfile.write("Frequency [Hamstring]: " + str(maximum_freq_hamstring_knee)+'\n')

    #Close report and graphics PDF
    REPORTfile.close()
    pp.close()

    print ("Closing...")
    #plt.show()
    return

