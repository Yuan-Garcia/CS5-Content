from scipy.io import wavfile
import scipy.signal as sps

import sys
import math
import time
import random
import os
import winsound
import librosa
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from IPython.display import Audio

sys.path.insert(1, '/content/gdrive/Shared drives/CS5_Test/hw3pr1_files')

import wave
wave.big_endian = 0



class CS5Audio:      
    # CODE DEFINTIONS
    def printParams(params):
        print('Parameters:')
        print('  nchannels:', params[0])
        print('  sampwidth:', params[1])
        print('  framerate:', params[2])
        print('  nframes  :', params[3])
        print('  comptype :', params[4])
        print('  compname :', params[5])

    def tr(params, rf):
        """tr transforms raw frames to floating-point samples"""
        samps = [x for x in rf]    # convert to numeric bytes
        # give parameters nicer names
        nchannels = params[0]
        sampwidth = params[1]
        nsamples  = params[3]
        if sampwidth == 1:

            for i in range(nsamples):
                if samps[i] < 128:
                    samps[i] *= 256.0       # Convert to 16-bit range, floating
                else:
                    samps[i] = (samps[i] - 256) * 256.0

        elif sampwidth == 2:
            newsamps = nsamples * nchannels * [0]
            for i in range(nsamples * nchannels):
                # The wav package gives us the data in native
                # "endian-ness".  The clever indexing with wave.big_endian
                # makes sure we unpack in the proper byte order.
                sampval = samps[2*i + 1 - wave.big_endian] * 256 + samps[2*i + wave.big_endian]
                if sampval >= 32768:
                    sampval -= 65536
                newsamps[i] = float(sampval)
            samps = newsamps
        else:
            print('A sample width of', params[1], 'is not supported.')
            print('Returning silence.')
            samps = nsamples * [0.0]

        if nchannels == 2:
            # Mix to mono
            newsamps = nsamples * [0]
            for i in range(nsamples):
                newsamps[i] = (samps[2 * i] + samps[2 * i + 1]) / 2.0
            samps = newsamps
        return samps

    def tri(params, samps):
        """tri is tr inverse, i.e. from samples to rawframes"""
        if params[1] == 1:                 # one byte per sample
            samps = [int(x+127.5) for x in samps]
            #print 'max, min are', max(samps), min(samps)
            rf = [chr(x) for x in samps]
        elif params[1] == 2:               # two bytes per sample
            bytesamps = (2*params[3])*[0]  # start at all zeros
            for i in range(params[3]):
                # maybe another rounding strategy in the future?
                intval = int(samps[i])
                if intval >  32767:
                    intval = 32767
                if intval < -32767:
                    intval = -32767  # maybe could be -32768
                if intval < 0:
                    intval += 65536 # Handle negative values
                # The wav package wants its data in native "endian-ness".
                # The clever indexing with wave.big_endian makes sure we
                # pack in the proper byte order.
                bytesamps[2*i + 1 - wave.big_endian] = intval // 256
                bytesamps[2*i + wave.big_endian] = intval % 256
            samps = bytesamps
            #print 'max, min are', max(samps), min(samps)
            rf = [chr(x).encode("latin-1") for x in samps]
        return b''.join(rf)

    def get_data(filename):
        """The file needs to be in .wav format.
        There are lots of conversion programs online, however,
        that can create .wav from .mp3 and other formats.
        """
        # this will complain if the file isn't there!
        fin = wave.open(filename, 'rb')
        params = fin.getparams()
        #printParams(params)
        rawFrames = fin.readframes(params[3])
        # need to extract just one channel of sound data at the right width...
        fin.close()
        return params, rawFrames

    def readwav(filename, printing = True):
        """readwav returns the audio data from the file
        named filename, which must be a .wav file.

        Call this function as follows:

        samps, sr = readwav(filename)

        samps will be a list of the raw sound samples (floats)
        sr will be the sampling rate for that list (integer)
        """
        sound_data = [0, 0]
        if printing:
            CS5Audio.read_wav(filename, sound_data)
        else:
            CS5Audio.read_wav(filename, sound_data, printing = False)
        samps = sound_data[0]
        sr = sound_data[1]
        if type(samps) != type([]): samps = [42] # default value
        return samps, sr

    def read_wav(filename, sound_data, printing = True):
        """read_wav returns the audio data from the file
        named filename (the first input) in the list
        named sound_data (the second input)

        If the file exists and is the correct .wav format,
        then after this call sound_data will be a list of two
        elements:

        sound_data[0] will be a list of the raw sound samples
        sound_data[1] will be the sampling rate for that list

        That is, sound_data will be the following:

            [[d0, d1, d2, ...], samplingrate]

        where each d0, d1, d2, ... is a floating-point value
        and sampling rate is an integer, representing the
        frequency with which audio samples were taken.

        No value is returned from this function!
        """
        if type(sound_data) != type([]):
            print("""
                read_wav was called with a second input,
                sound_data, that was _not_ of type list.

                That input needs to be a list, e.g., []
                """)
            return # nothing
        # sound_data is a list: we create/clear its first two elements
        if len(sound_data) < 1:
            sound_data.append(0)
        if len(sound_data) < 2:
            sound_data.append(0)
        # now it has at least two elements, and we reset them
        sound_data[0] = 42
        sound_data[1] = 42
        try:
            params, rf = CS5Audio.get_data(filename)
            samps = CS5Audio.tr(params, rf)
        except:
            print("There was a problem with the file", filename)
            print("You might check if it's here and of")
            print("the correct format (.wav) ... ")
            return # nothing

        numchannels = params[0]
        datawidth = params[1]
        framerate = params[2]
        numsamples = params[3]

        if printing:
            print()
            print('You opened', filename, 'which has')
            print('   ', numsamples, 'audio samples, taken at')
            print('   ', framerate, 'hertz (samples per second).')
            print()
        sound_data[0] = samps
        sound_data[1] = framerate
        return # nothing

    def write_data(params=None, rawFrames=None, filename="out.wav"):
        """Write data out to .wav format"""

        fout = wave.open(filename, 'wb')
        if params:
            fout.setparams(params)
            if rawFrames:
                fout.writeframes(rawFrames)
            else:
                print('no frames')
        else:
            print('no params')
        fout.close()

    def write_wav(sound_data, filename="out.wav", printing = True):
        """write_wav creates a .wav file whose contents are sound_data.
        sound_data is [audio data, srate] as a list.

        The second parameter is the output file name.
        If no name is specified, this parameter defaults to 'out.wav'.
        """
        # first, make the sampling rate an int...
        sound_data[1] = int(sound_data[1])

        # then do some other checking
        if type(sound_data) != type([]) or \
        len(sound_data) < 2 or \
        type(sound_data[0]) != type([]) or \
        type(sound_data[1]) != type(42):
            print("""
                write_wav was called with a first input,
                sound_data, that was _not_ an appropriate list.

                That input needs to be a list such that
                sound_data[0] are the raw sound samples and
                sound_data[1] is the sampling rate, e.g.,

                    [[d0, d1, d2, ...], samplingrate]

                where each d0, d1, d2, ... is a floating-point value
                and sampling rate is an integer, representing the
                frequency with whi audio samples were taken.
                """)
            return # nothing
        # name the two components of sound_data
        data = sound_data[0]
        samplingrate = sound_data[1]
        # compose the file...
        framerate = int(samplingrate)
        if framerate < 0:
            framerate = -framerate
        if framerate < 1:
            framerate = 1
        # always 1 channel and 2 output bytes per sample
        params = [1, 2, framerate, len(data), "NONE", "No compression"]
        # convert to raw frames
        rawframesstring = CS5Audio.tri(params, data)
        CS5Audio.write_data(params, rawframesstring, filename)
        if printing:
            print()
            print('You have written the file', filename, 'which has')
            print('   ', len(data), 'audio samples, taken at')
            print('   ', samplingrate, 'hertz.')
            print()
        return # nothing


    

    def play(filename):
        """Play a .wav file for Windows, Linux, or Mac.
        On a Mac, you need to have the "play"
        application in the current folder (.)
        """
        if type(filename) != type(''):
            raise TypeError('filename must be a string')
        if os.name == 'nt':
            winsound.PlaySound(filename, winsound.SND_FILENAME)
        elif os.uname()[0] == 'Linux':
            os.system('/usr/bin/play ' + filename + ' || /usr/bin/aplay ' + filename)
        # assume MAC, if not a Windows or Linux machine
        # if you're using another OS, you'll need to adjust this...
        else:
            # this was the pre MacOS 10.5 method...
            #os.system(('./play ' + filename))
            # now, it seems that /usr/bin/afplay is provided with MacOS X
            # and it seems to work in the same way play did
            # perhaps Apple simply used play?!
            os.system(('/usr/bin/afplay ' + filename))


    def plot_wave(filename1, filename2):
        """plot_wave plots up to two sound waves using matplotlib
        Arugments: filename1, the file of the first wave to be plotted
                    filename2, the file of the second wave to be plotted
        Result: returns nothing, but instead diplays the generated plot(s)!
        """
        if filename2 == None:                                    # if only one file to graph:
            fig = plt.figure(figsize = (6,3))                    # create empty plot
            samps, sr = CS5Audio.readwav(filename1, printing = False)     # get the sound data
            x_samp_data = list(range(len(samps)))                # for the x-data, create a list of the number of each sample (i.e. [0,1,2,...,len(samps)])
            x_time_data = [samp/sr for samp in x_samp_data]      # divide each sample number by the sample rate to find the time each sample occurs at
            y_data = samps                                       # assign the sample values to the y-data
            plt.plot(x_time_data, y_data)                        # plot the data
            plt.yticks([-32768,-16384, 0, 16384, 32767])         # set the ticks on the y-axis
            plt.xlim(0,len(samps)/sr)                            # set the limits of the x-axis to be 0 and the time of the final sample
            plt.ylim(-36000,36000)                               # set the limits of the y-axis to be a little about the min and max values of y
            plt.title("Sound Wave")                              # Set the graph title
            plt.xlabel("Time (s)")                               # Set the x-axis label
            plt.ylabel("Amplitude")                              # set the y-axis label
            plt.show()                                           # show the graph!
            return

        fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(6, 6))                # create 2 empty plots
        samps1, sr1 = CS5Audio.readwav(filename1, printing = False)                        # get the sound data of the first sound
        samps2, sr2 = CS5Audio.readwav(filename2, printing = False)                        # get the sound data of the second sound

        if len(samps1)/sr1 >= len(samps2)/sr2:                                    # this conditional finds the duration of the longer of the sounds
            x_samp_lim = len(samps1)                                                # which is used to give the graphs the same x-scale
            x_time_lim = len(samps1)/sr1
        else:
            x_samp_lim = len(samps2)
            x_time_lim = len(samps2)/sr2



        x1_samp_data = np.linspace(0,int(x_time_lim*sr1)+1,int(x_time_lim*sr1)+1) # number the samples from 0 to len(samps)
        x1_time_data = [samp_num/sr1 for samp_num in x1_samp_data]                # divide each sample number by the sample rate to find the time each sample occurs at

        y1_data = np.zeros((int(x_time_lim*sr1)+1,), dtype=int)                   # intially set all of the y data to 0
        for i in range(len(samps1)):                                              # for all of the samples we have, assign the y-data to be the sample values
            y1_data[i] = samps1[i]


        axes[0].plot(x1_time_data, y1_data)                                       # same plotting process as the one-sound case
        axes[0].set_xlim(0,x_time_lim)
        axes[0].set_ylim(-36000,36000)
        axes[0].set_yticks([-32768,-16384, 0, 16384, 32767])
        axes[0].set_title("Sound Wave 1")
        axes[0].set_xlabel("Time (s)")
        axes[0].set_ylabel("Amplitude")

        x2_samp_data = list(range(len(samps2)))                                   # repeat plotting for second sound

        x2_samp_data = np.linspace(0,int(x_time_lim*sr2)+1,int(x_time_lim*sr2)+1)
        x2_time_data = [samp_num/sr2 for samp_num in x2_samp_data]

        y2_data = np.zeros((int(x_time_lim*sr2)+1,), dtype=int)
        for i in range(len(samps2)):
            y2_data[i] = samps2[i]

        axes[1].plot(x2_time_data, y2_data, c='#cc2323')
        axes[1].set_xlim(0,x_time_lim)
        axes[1].set_ylim(-36000,36000)
        axes[1].set_yticks([-32768,-16384, 0, 16384, 32767])
        axes[1].set_title("Sound Wave 2")
        axes[1].set_xlabel("Time (s)")
        axes[1].set_ylabel("Amplitude")

        plt.tight_layout()
        plt.ion()                                                       # set the layout to prevent text and graphs from overlapping
        plt.show()                                                                # show the plot
        return


    def test():
        """A test function that plays swfaith.wav
        You'll need swfaith.wav in this folder.
        """
        CS5Audio.play('swfaith.wav')

def changeSpeed(filename, newsr, graph = False):
    """changeSpeed allows the user to change an audio file's speed.
       Arguments: filename, the name of the original file
                  newsr, the new sampling rate in samples per second
       Result: no return value, but
               this creates the sound file 'out.wav'
               and plays it
    """
    samps, sr = CS5Audio.readwav(filename)   # get samps and sr from the file!

    print("Playing the original sound...")
    CS5Audio.play(filename)
    print()

    print("The first 10 sound-pressure samples are\n", samps[:10])
    print("The number of samples per second is", sr, '\n')


    time.sleep(len(samps)/sr + 0.5) #wait until the first sound finishes playing before playing the altered one!


    # we don't really need this line, but for consistency...
    newsr = newsr             # from the input! (not needed, a reminder!)
    newsamps = samps          # same samples as before
    CS5Audio.write_wav([newsamps, newsr], "out.wav") # write data to out.wav

    print("\nPlaying new sound...")
    CS5Audio.play('out.wav')   # play the new file, 'out.wav'

    if graph == True:
        CS5Audio.plot_wave(filename, 'out.wav') #plot both filename and the output file


def pitch_shift(filename, shift_hz):
    samps, sr = CS5Audio.readwav(filename)
    
    framerate = 20 #hertz, how many frames we divide a second into
    framesize = sr//framerate

    num_frames = len(samps) // framesize # number of frames to process
    shift = 2 * shift_hz // framerate

    newsamps = []
    for num in range(num_frames):
        data = np.array(samps[2*num * framesize : 2*(num + 1) * framesize])
        data = [int(samp) for samp in data]

        if len(data)==0:
            break

        freqs = np.fft.rfft(data)
        freqs = np.roll(freqs, shift)
        freqs[0:shift] = 0
        new_freqs = np.fft.irfft(freqs)

        newsamps.extend(new_freqs.tolist())

    sound_data = [newsamps, sr]
    CS5Audio.write_wav(sound_data, "out.wav") 
    print(type(sound_data))


    #CS5Audio.printParams(CS5Audio.get_data(filename)[0])


#pitch_shift('swfaith.wav', 400)


def note_to_hz(note_name):
    # Dictionary to map note names to their corresponding MIDI note numbers
    note_mapping = {
        'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3,
        'E': 4, 'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8,
        'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11
    }
    
    # Parse the input note name into its components (note letter and octave)
    note_name = note_name.strip().upper()
    note_letter = note_name[:-1]
    octave = int(note_name[-1])

    # Calculate the MIDI note number for the given note name
    midi_note = note_mapping[note_letter] + (octave + 1) * 12

    # Calculate the frequency using the formula: f = 440 * 2^((MIDI_note - 69) / 12)
    frequency = 440 * math.pow(2, (midi_note - 69) / 12)
    
    return frequency

def estimate_fundamental_freq(samps, sr):
    
    fmin = note_to_hz('C2')
    fmax = note_to_hz('C7')

    f0, voiced_flag, voiced_probs = librosa.pyin(samps, sr=sr, fmin=fmin, fmax=fmax, max_transition_rate=100)
    times = librosa.times_like(f0, sr=sr)

    return f0, np.array(times)

def autotune(f0):
    '''
    Autotune takes in a numpy array of fundamental frequencies (f0, calculated with estimate_fundamental_freq)
    and "rounds" each frequency to the nearest MIDI note.
    '''
    # Convert f0 to midi and round to the nearest "whole" note (12-TET)
    corrected_notes = np.around(librosa.hz_to_midi(f0))

    # Preserve nan values
    nan_indices = np.isnan(f0)
    corrected_notes[nan_indices] = np.nan

    # Convert back to Hz.
    corrected_freqs = librosa.midi_to_hz(corrected_notes)

    return corrected_freqs

def non_constant_pitch_shift(stft, freq_contour):
#vertical bin: width of [time], height of 1024 indecies, up to sr/2 hz

# divide x axis into bins of width [distance between pyin/corrected points] center at the point (includes nan) <-- here rn
# roll bin up by difference between pyin and corrected [stay in loc form], remove the roll over
# istft and rewrite into wave 

# tune pyin to be higher resolution for steep pitch changes? [find example and test]

# for cs5, convert the index-based spectrogram to 3d data (time, freq, amplitude) to not have to deal with locs?

    print(len(freq_contour))



def plot_spectrogram(filename, fft_h_res = 2048, fft_v_scale = 16, plot_f0 = False, plot_corrected_f0 = False):
    '''plot_spectrogram plots the spectrogram of the audio file specified by filename.
       The spectrographic data is calculated using Librosa's Short-Time Fourier Transform (STFT) function.
       fft_h_res specifies the number of samples in each FFT window.
       fft_v_scale specifies the how narrow the vertical bins of the FFT are relative to fft_h_res (v-res = fft_h_res // fft_v_scale).
    '''
    fig, ax = plt.subplots()
    #samps, sr = librosa.load(librosa.ex('trumpet'))
    samps, sr = CS5Audio.readwav(filename)
    samps = np.array(samps)         # Convert the list of samples to a numpy array
        
    # Compute the Short-Time Fourier Transform (STFT) of the audio signal
    frame_length = fft_h_res
    hop_length = frame_length // fft_v_scale
    stft = librosa.stft(np.array(samps), n_fft=frame_length, hop_length=hop_length)   # Compute the STFT, which returns a complex matrix of FFT coeffecients
    log_stft = librosa.amplitude_to_db(np.abs(stft), ref=np.max)    #np.abs(stft) returns only the amplitude of each matric entry
    print(stft.shape)
    

    
    # Y-Axis Settings
    ax.set_yscale(matplotlib.scale.LogScale(2))
    ys =[0]+[64*2**x for x in range(8)]      # 0-8192 by powers of 2, skipping to 64
    y_loc = lambda y: (fft_h_res/sr) * y    # conversion between frequency and y index
    ax.set_yticks([y_loc(y) for y in ys], ys)
    ax.minorticks_off()
    ax.set_ylim(2,fft_h_res/2)
    ax.set_ylabel('Frequency [Hz]')

    #X-Axis Settings
    for possible_x_scale in [0.1, 0.25, 0.5, 1, 2, 5, 10]:        # Find the resolution of the x-axis that keeps the ticks to a resonable amount
        num_ticks = (len(samps) / sr) // possible_x_scale
        if num_ticks > 3 and num_ticks < 8:
            num_of_x_ticks = int(num_ticks)
            x_scale = possible_x_scale
            break
    xs = [round(x_scale * x, 2) for x in range(num_of_x_ticks + 1)]
    x_loc = lambda x: (sr / hop_length) * x            # conversion between time and x index
    #default 22050/128 = 172.265
    ax.set_xticks([x_loc(x) for x in xs], xs)
    ax.set_xlabel('Time [s]')


    # Plot the spectrogram
    spect = ax.imshow(log_stft, aspect='auto', origin='lower', cmap='magma')
    fig.colorbar(spect, ax=ax, format="%+2.0f dB")
    ax.set_title('Power Spectrogram of ' + filename)


    # Plot indentified/corrected pitches
    if plot_f0 == True:
        f0, times = estimate_fundamental_freq(samps, sr)
        times_loc = [x_loc(time) for time in times if time != np.nan]
        freqs_loc = [y_loc(freq) for freq in f0 if freq != np.nan]
        ax.plot(times_loc, freqs_loc, label='f0', color='red', linewidth=4)

    if plot_corrected_f0 == True and plot_f0 == True:
        corrected_freqs = autotune(f0)
        corrected_freqs_loc = np.array([y_loc(freq) for freq in corrected_freqs if freq != np.nan])
        #print(corrected_freqs_loc)
        #corrected_freqs_loc[np.isnan(corrected_freqs_loc)] = 5
        #print(len(corrected_freqs_loc))
        ax.plot(times_loc, corrected_freqs_loc, label='corrected f0', color='cyan', linewidth=2)

    elif plot_corrected_f0 == True and plot_f0 == False:
        print("f0 must be plotted for corrected_f0 to be plotted")
        #maybe change?
    

    non_constant_pitch_shift(log_stft, corrected_freqs_loc)
    
    
    plt.legend(loc='upper left', labelcolor = 'white', framealpha = 0.1)
    plt.show()



plot_spectrogram('ronjo.wav', plot_f0 = True, plot_corrected_f0 = True)