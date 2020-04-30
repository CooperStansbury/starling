import argparse
from mido import Message, MidiFile, MidiTrack
import numpy as np
import random


def get_scale(scale='major', base=60):
    """A function to return an octave run of the major scale starting at
    C3 (note = 60).

    Args:
        - scale (str): the scale to use to generate the melody
        - base (int): this represents C3

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
    notes = [base] + [(base + i) for i in np.cumsum(SCALE_DICT[scale])]
    return notes



def build_melody(notes, beat=480, length=16):
    """A function to build a monophonic melody

    Args:
        - notes (list of int): list of allowable note values
        - beat (int): beat length value of a 'quarter note' at 120bpm,
            480 represents a 'regular' quarter note
        -length (int): the number of 'beats' as defined above of the entire
            phrase

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

    total_steps = beat*length

    timing = []
    while total_steps > 0:
        b = random.sample(list(BEAT_DICT), 1)
        duration = BEAT_DICT[b[0]]
        total_steps -= duration
        timing.append(duration)

    _notes = [random.sample(notes, 1)[0] for i in range(len(timing))]

    return zip(_notes, timing)


def build_midi(melody, file_id):
    """A function to create a single track midi object.

    Default is 120bpm.

    Args:
        - melody (tuple of lists): (notes, timing)
        - file_id (str): what to name the file
    """
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    t = 0
    for note, timing in melody:
        track.append(Message('note_on', note=note, velocity=64, time=t))
        track.append(Message('note_off', note=note, velocity=127, time=t+timing))

        t = timing


    save_path = f"{file_id}.mid"
    mid.save(save_path)


if __name__ == "__main__":
    desc = """ A Python3 commandline tool to generate midi melodies. """


    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument("-n", default=10, help="Number of melodies to generate.")
    parser.add_argument("-s", nargs='?', default='major', help="Scale to base melody off of")
    args = parser.parse_args()

    notes = get_scale(scale=args.s)
    print(f'scale: "{args.s}" ({notes})')
    melody = build_melody(notes)

    for i in range(args.n):
        build_midi(melody, str(i))
