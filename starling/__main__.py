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


def get_timings(beat, max_length):
    """A function to return a list of note timings.

    Args:
        - beat (int): beat length value of a 'quarter note' at 120bpm,
            480 represents a 'regular' quarter note
        - max_length (int): the maximum number of 'beats' as defined above of
            the entire phrase. phrase may be shorter.

    Returns:
        - timings (list): a list of note durations
    """
    BEAT_DICT = {
        'sixteenth':int(beat/4),
        'eighth':int(beat/2),
        'quarter':int(beat),
        'half':int(beat*2),
        'whole':int(beat*4)
    }
    total_steps = beat*max_length
    timings = []
    while total_steps > 0:
        b = random.sample(list(BEAT_DICT), 1)
        duration = BEAT_DICT[b[0]]
        total_steps -= duration
        timings.append(duration)
    return timings


def gen_melody(scale, timings):
    """A function to build a monophonic melody

    Args:
        - scale (list of int): list of 'allowable' notes
        - timings (list of int): list of knote durations

    Returns:
        - melody (tuple of lists): (notes, timing)
    """
    melody = [random.sample(scale, 1)[0] for i in range(len(timings))]
    return zip(melody, timings)


def build_melody(scale, beat, max_length, velocity, save_path):
    """A function to create a single track midi object.

    Default is 120bpm.

    Args:
        - scale (list): list of 'allowable' notes
        - beat (int): beat length value of a 'quarter note' at 120bpm,
            480 represents a 'regular' quarter note.
        - max_length (int): the maximum number of 'beats' as defined above of
            the entire phrase. phrase may be shorter.
        - velocity (int): velocity of the midi notes
        - save_path (str): what to name the file
    """
    mid = MidiFile(type=0) # all messages are saved in one track
    track = MidiTrack()
    mid.tracks.append(track)

    timings = get_timings(beat, max_length)
    melody = gen_melody(scale, timings)

    t = 0
    for note, timing in melody:
        track.append(Message('note_on', note=note, velocity=velocity, time=t))
        track.append(Message('note_off', note=note, velocity=velocity, time=t+timing))
        t = timing
    mid.save(save_path)


if __name__ == "__main__":
    desc = """A Python3 commandline tool to generate midi melodies. """
    parser = argparse.ArgumentParser(description=desc)

    """
    TODO:
        - add probability of note deviance from the scale
        - add more scales
        - make timing more advanced
        - add multiple voices (up to three)
    """

    parser.add_argument("-n", default=10,
                        help="Number of melodies to generate.")
    parser.add_argument("-scale", nargs='?', default='major',
                        help="Scale to generate melodies/chords from.")
    parser.add_argument("-octave", nargs='?', default=0,
                        help="When octave == 0: C3 = 60. All offsets are +1, -1\
                        from C3. You need to specify negative offsets.")
    parser.add_argument("-oct_range", nargs='?', default=1,
                        help="The number of octaves of the scale used to generate\
                        the melody. Octaves start at the default key center\
                        at the root specified by the `octave` parameter.")
    parser.add_argument("-beat", nargs='?', default=480,
                        help="Beat length value of a 'quarter note' at 120bpm,\
                            480 represents a 'regular' quarter note.")
    parser.add_argument("-max_length", nargs='?', default=16,
                        help="The maximum number of 'beats' from the `beat`\
                        parameter of the entire phrase. Phrase may be shorter.")
    parser.add_argument("-vel", nargs='?', default=127,
                        help="Velocity of the notes.")
    parser.add_argument("-key", nargs='?', default='C',
                        help="Key to produce melodies in.")
    parser.add_argument("-output", nargs='?', default='output/',
                        help="Output path. Defaults to `output/`. Path is\
                        relative to execution.")

    args = parser.parse_args()

    BASE_NOTE = {
        'C':60,'C#':61,
        'D':62,'D#':63,
        'E':64,
        'F':65,'F#':66,
        'G':67,'G#':68,
        'A':69,'A#':70,
        'B':71,
    }

    # when octave == 0, C3 = 60
    OCTAVE = int(args.octave)
    OCTAVE_RANGE = int(args.oct_range)
    KEY_ARG = str(args.key).upper()
    KEY = BASE_NOTE[KEY_ARG]
    BEAT = int(args.beat)
    MAX_LENGTH = int(args.max_length)
    VELOCITY = int(args.vel)
    SCALE_ARG = str(args.scale).lower()
    N_MELODIES = int(args.n)
    OUTPUT_PATH = args.output

    SCALE = [(OCTAVE*12 + note) for note in get_scale(scale=SCALE_ARG, key=KEY)]

    # octave scaling
    if OCTAVE_RANGE != 1:
        for oct in range(1, OCTAVE_RANGE):
            # since the scale already has the octave we skip the last item
            SCALE += [(12*oct)+note for note in SCALE[:-1]]

    print("INPUT PARAMETERS:")
    print(f'Key: "{KEY_ARG}"')
    print(f'Scale: "{SCALE_ARG}"')
    print(f'Octave: "{OCTAVE}"')
    print(f'Octave Range: "{OCTAVE_RANGE}"')
    print(f'Notes: "{SCALE}"')

    for i in range(N_MELODIES):
        save_path = f'{OUTPUT_PATH}{KEY_ARG}_{SCALE_ARG}_{i}.mid'
        build_melody(scale=SCALE,beat=BEAT,max_length=MAX_LENGTH,
                    velocity=VELOCITY,
                    save_path=save_path)
