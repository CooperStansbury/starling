# starling
midi melody generation

```
usage:  [-h] [-n N] [-scale [SCALE]] [-octave [OCTAVE]]
        [-oct_range [OCT_RANGE]] [-tracks [TRACKS]] [-note_dev [NOTE_DEV]]
        [-beat [BEAT]] [-max_length [MAX_LENGTH]] [-rand_beat [RAND_BEAT]]
        [-vel [VEL]] [-key [KEY]] [-output [OUTPUT]] [-rests [RESTS]]

A Python3 commandline tool to generate midi melodies.

optional arguments:
  -h, --help            show this help message and exit
  -n N                  Number of melodies to generate.
  -scale [SCALE]        Scale to generate melodies/chords from.
  -octave [OCTAVE]      When octave == 0: C3 = 60. All offsets are +1, -1 from
                        C3. You need to specify negative offsets.
  -oct_range [OCT_RANGE]
                        The number of octaves of the scale used to generate
                        the melody. Octaves start at the default key center at
                        the root specified by the `octave` parameter.
  -tracks [TRACKS]      The number of 'voices' (as separate tracks) in the
                        output files.
  -note_dev [NOTE_DEV]  The probability [0, 1] that a note is altered by one
                        half-step. The probability is for EACH NOTE in the
                        chord or melody.
  -beat [BEAT]          Beat length value of a 'quarter note' at 120bpm, 480
                        represents a 'regular' quarter note.
  -max_length [MAX_LENGTH]
                        The maximum number of 'beats' from the `beat`
                        parameter of the entire phrase. Phrase may be shorter.
  -rand_beat [RAND_BEAT]
                        Should the beats be random (True), or should they be
                        constant (False)?
  -vel [VEL]            Velocity of the notes.
  -key [KEY]            Key to produce melodies in.
  -output [OUTPUT]      Output path. Defaults to `output/`. Path is relative
                        to execution.
  -rests [RESTS]        Should the output contain random rests?
```
