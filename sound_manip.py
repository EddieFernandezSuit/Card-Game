from pydub import AudioSegment
import os

# download ffmpeg for mp3 files

def slice_audio(filename, start_time):
    """
    Slice an audio file and export it as a new file.

    Args:
    filename (str): The name of the audio file.
    start_time (int): The time in milliseconds to start slicing from.
    """
    input_file = os.path.join('original_sounds', filename)
    output_file = os.path.join('sounds', filename)
    format = os.path.splitext(filename)[1][1:]
    audio = AudioSegment.from_file(input_file, format)
    audio = audio[start_time:]
    audio.export(output_file, format=format)

# slice_audio("metal_card_shuffle.wav", 300)


import numpy as np

def audio_levels(audio_file):
    audio = AudioSegment.from_file(audio_file)
    sample_width = audio.sample_width
    frame_rate = audio.frame_rate
    audio_array = np.frombuffer(audio.raw_data, dtype=np.int16)
    audio_levels = {}
    for i in range(0, (frame_rate // 1000) * 400, (frame_rate // 1000) * 10):
        ms = i // (frame_rate // 1000)
        rms = round(np.sqrt(np.mean(audio_array[i:i+frame_rate//1000]**2)), 2)
        audio_levels[ms] = rms

    print(audio_levels)
    return audio_levels


def remove_empty_audio(filename):
    audio_level = audio_levels(os.path.join('original_sounds', filename))
    start_time = 0
    for ms, level in audio_level.items():
        if level > 5:
            start_time = ms
            break
    slice_audio(filename, start_time)

# audio_levels('original_sounds/metal_card_shuffle.wav')
remove_empty_audio('bird.mp3')