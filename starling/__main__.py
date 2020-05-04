import argparse
from mido import Message, MidiFile, MidiTrack
import numpy as np
import random
from distutils.util import strtobool


"""
TODO:
    - chord mode
    - rest p(x)
    - add more scales
    - make timing more advanced
"""


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
        'locrian':[1,2,2,1,2,2,2],
        'minor_pent':[3,2,2,3,2],
        'major_pent':[2,2,3,2,3],
        'pent_6':[2,2,3,1,3],
        'pent_2':[1,3,3,2,3],
        'pent_3':[2,1,4,2,3],
        'pent_5':[2,2,2,3,3],
        'mixo_pent':[2,2,3,3,2],
        'phryg_pent':[1,2,3,1,3],
        'dim_pent':[2,1,3,1,3],
        'blues':[3,2,1,1,3,2],
        'harmonic_minor':[2,1,2,2,1,3,2],
        'melodic_mimnor':[2,1,2,2,1,3,2],
        'whole_tone':[2,2,2,2,2,2],
        'whole_half':[2,1,2,1,2,1,2,1],
        'half_whole':[1,2,1,2,1,2,1,2]
    }
    notes = [key] + [(key + i) for i in np.cumsum(SCALE_DICT[scale])]
    return notes


def get_timings(beat, max_length, rand_beat):
    """A function to return a list of note timings.

    Args:
        - beat (int): beat length value of a 'quarter note' at 120bpm,
            480 represents a 'regular' quarter note
        - max_length (int): the maximum number of 'beats' as defined above of
            the entire phrase. phrase may be shorter.
        - rand_beat (bool): should the beats be randon (True), or uniform
            (False)?

    Returns:
        - timings (list): a list of note durations
    """
    BEATS = [int(beat/4),
             int(beat/2),
             int(beat),
             int(beat*2),
             int(beat*4)]

    total_steps = beat * max_length
    timings = [beat] * max_length

    if rand_beat == True:
        timings = []
        while total_steps > 0:
            duration = random.sample(BEATS, 1)[0]
            total_steps -= duration
            timings.append(duration)

    return timings


def gen_melody(scale, timings, note_deviance):
    """A function to build a monophonic melody

    Args:
        - scale (list of int): list of 'allowable' notes
        - timings (list of int): list of knote durations
        - note_deviance (float): the probability that a note is altered by a
            half-step.

    Returns:
        - melody (list of ints): the notes, in order, of the melody
    """
    melody = [random.sample(scale, 1)[0] for i in range(len(timings))]

    px = np.random.rand(len(timings))
    idx = np.argwhere(px <= note_deviance)
    direction = [-1, 1]
    for i in idx:
        melody[i[0]] = melody[i[0]] + random.sample(direction, 1)[0]
    return melody


def build_melody(scale, tracks, note_deviance, beat, max_length, rand_beat,
                 velocity,rests, save_path):
    """A function to create a single track midi object.

    Default is 120bpm.

    Args:
        - scale (list): list of 'allowable' notes
        - tracks (int): how many voices, as separate tracks, in the midi file?
        - note_deviance (float): the probability that a note is altered by a
            half-step
        - beat (int): beat length value of a 'quarter note' at 120bpm,
            480 represents a 'regular' quarter note.
        - max_length (int): the maximum number of 'beats' as defined above of
            the entire phrase. phrase may be shorter.
        - rand_beat (bool): should the beats be randon (True), or uniform
            (False)?
        - velocity (int): velocity of the midi notes
        - rests (bool): if true output will contain random offsets in note
            start position
        - save_path (str): what to name the file
    """
    # (synchronous): all tracks start at the same time
    mid = MidiFile(type=1)

    for v in range(tracks):
        track = MidiTrack()
        mid.tracks.append(track)
        timings = get_timings(beat, max_length, rand_beat)
        melody = gen_melody(scale, timings, note_deviance)

        if rests == True:
            t = 0
            for note, timing in zip(melody, timings):
                track.append(Message('note_on', note=note,
                                     velocity=velocity, time=t))
                track.append(Message('note_off', note=note,
                                     velocity=velocity, time=timing+t))

                t += timing
        else:
            for note, timing in zip(melody, timings):
                track.append(Message('note_on', note=note,
                                     velocity=velocity, time=1))
                track.append(Message('note_off', note=note,
                                     velocity=velocity, time=timing+1))
    mid.save(save_path)


if __name__ == "__main__":
    desc = """A Python3 commandline tool to generate midi melodies. """
    parser = argparse.ArgumentParser(description=desc)

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
    parser.add_argument("-tracks", nargs='?', default=1,
                        help="The number of 'voices' (as separate tracks) in\
                        the output files.")
    parser.add_argument("-note_dev", nargs='?', default=0,
                        help="The probability [0, 1] that a note is altered by\
                        one half-step. The probability is for EACH NOTE in the\
                        chord or melody.")
    parser.add_argument("-beat", nargs='?', default=480,
                        help="Beat length value of a 'quarter note' at 120bpm,\
                            480 represents a 'regular' quarter note.")
    parser.add_argument("-max_length", nargs='?', default=16,
                        help="The maximum number of 'beats' from the `beat`\
                        parameter of the entire phrase. Phrase may be shorter.")
    parser.add_argument("-rand_beat", nargs='?', default=True,
                        help="Should the beats be random (True), or should they\
                        be constant (False)?")
    parser.add_argument("-vel", nargs='?', default=100,
                        help="Velocity of the notes.")
    parser.add_argument("-key", nargs='?', default='C',
                        help="Key to produce melodies in.")
    parser.add_argument("-output", nargs='?', default='output/',
                        help="Output path. Defaults to `output/`. Path is\
                        relative to execution.")
    parser.add_argument("-rests", nargs='?', default=False,
                        help="Should the output contain random rests?")

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
    TRACKS = int(args.tracks)
    BEAT = int(args.beat)
    MAX_LENGTH = int(args.max_length)
    NOTE_DEVIANCE = float(args.note_dev)
    VELOCITY = int(args.vel)
    SCALE_ARG = str(args.scale).lower()
    N = int(args.n)
    RESTS = args.rests
    RAND_BEAT = args.rand_beat
    OUTPUT_PATH = args.output


    SCALE = [(OCTAVE*12 + note) for note in get_scale(scale=SCALE_ARG, key=KEY)]

    # octave scaling
    if OCTAVE_RANGE != 1:
        for oct in range(1, OCTAVE_RANGE):
            # since the scale already has the octave we skip the last item
            SCALE += [(12*oct)+note for note in SCALE[:-1]]

    print("INPUT PARAMETERS:")
    print(f'Key: {KEY_ARG}')
    print(f'Scale: {SCALE_ARG}')
    print(f'Octave: {OCTAVE}')
    print(f'Octave Range: {OCTAVE_RANGE}')
    print(f'Velocity: {VELOCITY}')
    print(f'Beat: {BEAT}')
    print(f'Maximum Phrase Length: {MAX_LENGTH}')
    print(f'Note Deviance: {NOTE_DEVIANCE}')
    print(f'Random Beats: {RAND_BEAT}')
    print(f'Tracks: {TRACKS}')
    print(f'Rests Enabled: {RESTS}')
    print(f'Notes: {SCALE}')


    for i in range(N):
        save_path = f'{OUTPUT_PATH}{KEY_ARG}_{SCALE_ARG}_{i}.mid'
        build_melody(scale=SCALE,tracks=TRACKS, note_deviance=NOTE_DEVIANCE,
                    beat=BEAT,max_length=MAX_LENGTH, rand_beat=RAND_BEAT,
                    velocity=VELOCITY,rests=RESTS,save_path=save_path)
