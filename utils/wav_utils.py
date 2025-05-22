import os
import wave


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


if __name__ == "__main__":
    filename = "audio/output.wav"
    wav_info, data = parse_wav(filename)
    nfiles = split_wav(wav_info, data)
