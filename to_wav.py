#!/usr/bin/env python3
from pydub import AudioSegment
import os 
from typing import List
import argparse

parser = argparse.ArgumentParser(description="Formats a music file of various formats into a formatted wav music file")
parser.add_argument('-f', default=None, help="", required=True)
args = parser.parse_args()
print(args.f)
parser.print_help()


INPUT_DIR = os.path.join(os.path.dirname(__file__), "dataset_raw")  
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "dataset_converted")
OUTPUT_DIR_request = os.path.join(os.path.dirname(__file__), "requestet_song_converted")

FIRST_MIN = 60000

if args.f != None:
    INPUT_DIR_request = os.path.join(os.path.dirname(__file__), args.f)
    requestet_song: AudioSegment = AudioSegment.from_mp3(os.path.join(INPUT_DIR_request))
    sliced_ten_secs1 = requestet_song[FIRST_MIN:FIRST_MIN+10000]
    sliced_ten_secs1.export(os.path.join(OUTPUT_DIR_request, os.path.splitext(args.f)[0] + ".wav"), format="wav")


m_files: List[str] = os.listdir(INPUT_DIR)

for f in m_files:
    song: AudioSegment = AudioSegment.from_mp3(os.path.join(INPUT_DIR, f))
    sliced_ten_secs = song[FIRST_MIN:FIRST_MIN+10000]
    sliced_ten_secs.export(os.path.join(OUTPUT_DIR, os.path.splitext(f)[0] + ".wav"), format="wav")

