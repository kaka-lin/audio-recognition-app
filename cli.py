import os, sys
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import wave
import speech_recognition as sr
from argparse import ArgumentParser

from utils import *


def parse_wav(filename):
    print("Parsing {} file ...".format(filename))

    with wave.open(filename, "rb") as wav:
        frames = wav.getnframes()
        channel = wav.getnchannels()
        rate = wav.getframerate()
        resolution = wav.getsampwidth()
        str_data = wav.readframes(frames)

    return (channel, rate, resolution, frames), str_data


def split_wav(info, data, time=10):
    channel, rate, resolution, frames = info

    # frames of n seconds: rate * n(s)
    wav_max = rate * time
    _bytes = wav_max * 4

    # add Window (overlapping 1 second)
    window = rate * 4

    # How many files will be produced
    # by split the origin file with n seconds.
    nums = frames // wav_max
    mod = frames % wav_max
    split_file_nums = nums if mod == 0 else nums+1

    # confirm if the folder is exist
    dir_name = os.path.dirname(os.path.abspath(__file__))
    split_dir = dir_name + "/" + "audio/" + "split/"
    if not os.path.exists(split_dir):
        os.makedirs(split_dir)

    print("Split the origin file in {} files with {} seconds.".format(split_file_nums, time))
    for i in range(split_file_nums):
        with wave.open(split_dir + "split{}.wav".format(i), "wb") as wav:
            wav.setnchannels(channel)
            wav.setframerate(rate)
            wav.setsampwidth(resolution)

            if i == split_file_nums:
                str_data = data[(i-1) * _bytes:]
            else:
                str_data = data[i * _bytes:(i+1) * _bytes + window]

            wav.writeframes(str_data)

    return split_file_nums


def audio_recognition(filename, language="en-US"):
    r = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = r.record(source) # read the entire audio file

    try:
        answer = r.recognize_google(audio, language=language)
        print(answer, "\n")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument("-f", "--file", dest="filename", help="name of audio file.")
    parser.add_argument("-c", "--convert", action="store_true", help="Converting mp3 to wav.")
    parser.add_argument("-t", "--time", dest="time", help="split the origin file with n seconds.")

    args = parser.parse_args()

    if (args.filename is None):
        filename = "audio/output.wav"
    else:
        filename = args.filename

    if (args.convert):
        # confirm if the folder is exist
        dir_name = os.path.dirname(os.path.abspath(__file__))
        audio_folder = dir_name + "/" + "audio/"
        if not os.path.exists(audio_folder):
            os.makedirs(audio_folder)

        src = filename
        dst = audio_folder + "output.wav"
        convert_mp3_to_wav(src, dst)
        filename = dst

    if (filename[-3:] != "wav"):
        print("Only support WAVE now, please use -c to convert mp3 to wave file.")
        sys.exit()

    wav_info, data = parse_wav(filename)

    if (args.time):
        nfiles = split_wav(wav_info, data, args.time)
    else:
        nfiles = split_wav(wav_info, data)

    print("Audio recognition ... \n")
    for i in range(nfiles):
        audio_recognition("audio/split/" + "split{}.wav".format(i),
            language="en-AU")
