for d in output/*.mid ; do
  BASE="${d%.mid}"
  midi2audio $d $BASE".wav"
done

mv output/*.wav wav_files/
