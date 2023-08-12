#!/usr/bin/env python3
from pydub import AudioSegment
import os
from typing import List


INPUT_DIR = "dataset_raw"
OUTPUT_DIR = "dataset_converted"

FIRST_MIN = 60000

m_files: List[str] = os.listdir(INPUT_DIR)

for f in m_files:
    song: AudioSegment = AudioSegment.from_mp3(os.path.join(INPUT_DIR, f))
    sliced_ten_secs = song[FIRST_MIN:FIRST_MIN+10000]
    sliced_ten_secs.export(os.path.join(OUTPUT_DIR, os.path.splitext(f)[0] + ".wav"), format="wav")


