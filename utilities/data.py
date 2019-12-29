"""This part of the code is only to process the data. It was provided with the dataset but 
was didn't work sometimes because of using older versions of code or not referencing itself properly.
So this is a slightly edited version of that code.

E.g.: I had to use matplotlib.pyplot.imread to read the spectrograms instead of scipy."""


from __future__ import division, print_function
from os import listdir
from os.path import isfile, join

from matplotlib import pyplot as plt
import scipy.io.wavfile as wav

import os
from collections import defaultdict
import scipy.io.wavfile
import scipy.ndimage
import matplotlib
from matplotlib.pyplot import imread


def wav_to_spectrogram(audio_path, save_path, spectrogram_dimensions=(64, 64), noverlap=16, cmap='gray_r'):
    """ Creates a spectrogram of a wav file.

    :param audio_path: path of wav file
    :param save_path:  path of spectrogram to save
    :param spectrogram_dimensions: number of pixels the spectrogram should be. Defaults (64,64)
    :param noverlap: See http://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.spectrogram.html
    :param cmap: the color scheme to use for the spectrogram. Defaults to 'gray_r'
    :return:
    """

    sample_rate, samples = wav.read(audio_path)

    fig = plt.figure()
    fig.set_size_inches((spectrogram_dimensions[0]/fig.get_dpi(), spectrogram_dimensions[1]/fig.get_dpi()))
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.specgram(samples, cmap=cmap, Fs=2, noverlap=noverlap)
    ax.xaxis.set_major_locator(plt.NullLocator())
    ax.yaxis.set_major_locator(plt.NullLocator())
    fig.savefig(save_path, bbox_inches="tight", pad_inches=0)


def dir_to_spectrogram(audio_dir, spectrogram_dir, spectrogram_dimensions=(64, 64), noverlap=16, cmap='gray_r'):
    """ Creates spectrograms of all the audio files in a dir

    :param audio_dir: path of directory with audio files
    :param spectrogram_dir: path to save spectrograms
    :param spectrogram_dimensions: tuple specifying the dimensions in pixes of the created spectrogram. default:(64,64)
    :param noverlap: See http://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.spectrogram.html
    :param cmap: the color scheme to use for the spectrogram. Defaults to 'gray_r'
    :return:
    """
    file_names = [f for f in listdir(audio_dir) if isfile(join(audio_dir, f)) and '.wav' in f]

    for file_name in file_names:
        print(file_name)
        audio_path = audio_dir + file_name
        spectogram_path = spectrogram_dir + file_name.replace('.wav', '.png')
        wav_to_spectrogram(audio_path, spectogram_path, spectrogram_dimensions=spectrogram_dimensions, noverlap=noverlap, cmap=cmap)


if __name__ == '__main__':
    audio_dir = os.path.dirname(__file__) + '/../recordings/'
    spectrogram_dir = os.path.dirname(__file__) + '/../spectrograms/'
    dir_to_spectrogram(audio_dir, spectrogram_dir)
    


class FSDD:
    """Summary

    Attributes:
        file_paths (TYPE): Description
        recording_paths (TYPE): Description
    """

    def __init__(self, data_dir):
        """Initializes the FSDD data helper which is used for fetching FSDD data.

        :param data_dir: The directory where the audiodata is located.
        :return: None

        Args:
            data_dir (TYPE): Description
        """

        # A dict containing lists of file paths, where keys are the label and vals.
        self.recording_paths = defaultdict(list)
        file_paths = [f for f in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, f))]
        self.file_paths = file_paths

        for digit in range(0, 10):
            # fetch all the file paths that start with this digit
            digit_paths = [os.path.join(data_dir, f) for f in file_paths if f[0] == str(digit)]
            self.recording_paths[digit] = digit_paths

    @staticmethod
    def get_spectrograms(data_dir=None):
        """

        Args:
            data_dir (string): Path to the directory containing the spectrograms.

        Returns:
            (spectrograms, labels): a tuple of containing lists of spectrograms images(as numpy arrays) and their corresponding labels as strings
        """
        spectrograms = []
        labels = []

        if data_dir is None:
            data_dir = os.path.dirname(__file__) + '/../spectrograms'
            print(data_dir)

        file_paths = [f for f in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, f)) and '.png' in f]
        
        if len(file_paths) == 0:
            raise Exception('There are no files in the spectrogram directory. Make sure to run the spectrogram.py before calling this function.')

        for file_name in file_paths:
            label = file_name[0]
            spectrogram = matplotlib.pyplot.imread(data_dir + '/' + file_name).flatten()
            spectrograms.append(spectrogram)
            labels.append(label)

        return spectrograms, labels
