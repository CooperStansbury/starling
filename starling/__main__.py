import argparse
from mido import Message, MidiFile, MidiTrack
import numpy as np
import random


def get_scale(scale='major', key=60):
    """A function to return an octave run of the major scale starting at
    C3 (note = 60).

    Args:
        - scale (str): the scale to use to generate the melody
        - key (int): 60 represents C3

    Returns:
        - notes (list of int): list of note values
    """
    SCALE_DICT = {
        'major': [2,2,1,2,2,2,1],
        'minor':[2,1,2,2,1,2,2],
        'chrom':[1,1,1,1,1,1,1,1,1,1,1,1],
        'ionanian':[2,2,1,2,2,2,1],
        'dorian':[2,1,2,2,2,1,2],
        'phrygian':[1,2,2,2,1,2,2],
        'lydian':[2,2,2,1,2,2,1],
        'mixolydian':[2,2,1,2,2,1,2],
        'aeolian':[2,1,2,2,1,2,2],
        'locrian':[1,2,2,1,2,2,2]
    }
    notes = [key] + [(key + i) for i in np.cumsum(SCALE_DICT[scale])]
    return notes


def build_melody(notes, beat=480, max_length=16):
    """A function to build a monophonic melody

    Args:
        - notes (list of int): list of allowable note values
        - beat (int): beat length value of a 'quarter note' at 120bpm,
            480 represents a 'regular' quarter note
        - max_length (int): the maximum number of 'beats' as defined above of
            the entire phrase. phrase may be shorter.

    Returns:
        - melody (tuple of lists): (notes, timing)
    """
    BEAT_DICT = {
        'sixteenth':int(beat/4),
        'eighth':int(beat/2),
        'quarter':int(beat),
        'half':int(beat*2),
        'whole':int(beat*4)
    }

    total_steps = beat*max_length

    timing = []
    while total_steps > 0:
        b = random.sample(list(BEAT_DICT), 1)
        duration = BEAT_DICT[b[0]]
        total_steps -= duration
        timing.append(duration)

    _notes = [random.sample(notes, 1)[0] for i in range(len(timing))]

    return zip(_notes, timing)


def build_midi(melody, velocity, save_path):
    """A function to create a single track midi object.

    Default is 120bpm.

    Args:
        - melody (tuple of lists): (notes, timing)
        - velocity (int): velocity of the midi notes
        - save_path (str): what to name the file
    """
    mid = MidiFile(type=0) # all messages are saved in one track
    track = MidiTrack()
    mid.tracks.append(track)

    t = 0
    for note, timing in melody:
        track.append(Message('note_on', note=note, velocity=velocity, time=t))
        track.append(Message('note_off', note=note, velocity=velocity, time=t+timing))
        t = timing
    mid.save(save_path)


if __name__ == "__main__":
    desc = """ A Python3 commandline tool to generate midi melodies. """
    parser = argparse.ArgumentParser(description=desc)

    """
    TODO:
        - add probability of note deviance from the scale
        - add a base note param (for different keys)
        - add more scales
        - allow output location specs
        - make timing more advanced
        - add multiple voices (up to three)
    """

    BASE_NOTE = {
        'C':60,'C#':61,
        'D':62,'D#':63,
        'E':64,
        'F':65,'F#':66,
        'G':67,'G#':68,
        'A':69,'A#':70,
        'B':71,
    }

    parser.add_argument("-n", default=10, help="Number of melodies to generate.")
    parser.add_argument("-s", nargs='?', default='major', help="Scale to base melody off of")
    parser.add_argument("-vel", nargs='?', default=127, help="Velocity of the notes")
    parser.add_argument("-key", nargs='?', default='C', help="Key to produce melodies in.")

    args = parser.parse_args()

    KEY = BASE_NOTE[str(args.key).upper()]
    SCALE = get_scale(scale=str(args.s).lower(), key=KEY)
    N_MELODIES = int(args.n)

    for i in range(N_MELODIES):
        MELODY = build_melody(SCALE)

        save_path = f'{args.key}_{args.s}_{i}.mid'
        build_midi(melody=MELODY,
                   velocity=int(args.vel),
                   save_path=save_path)
