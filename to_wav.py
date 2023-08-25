#!/usr/bin/env python3
from pydub import AudioSegment
from pydub.utils import mediainfo
import os 
from typing import List
import argparse
import sys


def is_directory(arg:str):
    if not os.path.isdir(arg):
        raise argparse.ArgumentTypeError("The givin argument was not an valid Path!")
    return arg

def parse_arguments():

    parser = argparse.ArgumentParser(description="Formats a music file of various formats into a formatted wav music file")
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument('-d', '--directory', help="takes a directory and converts everything to an wav file")
    group.add_argument('-f', '--file', help="takes an file and on base of this file will perferm an recommendation")

  

    parser.add_argument('-df', '--destinationfolder', type=is_directory, help="takes an filepath, where the convertet file will be stored",
                    default=None)


    return parser.parse_args()

def converter(des:str, imp:str, is_dir:bool):
    OUTPUT_DIR = os.path.join(os.path.dirname(__file__), des)
    INPUT_DIR = os.path.join(os.path.dirname(__file__), imp) 
    FIRST_MIN = 60000
    
    if is_dir == True:
        m_files: List[str] = os.listdir(INPUT_DIR)
        for f in m_files:
            song: AudioSegment = AudioSegment.from_mp3(os.path.join(INPUT_DIR, f))
            sliced_ten_secs = song[FIRST_MIN:FIRST_MIN+10000]
            sliced_ten_secs.export(os.path.join(OUTPUT_DIR, os.path.splitext(f)[0] + ".wav"), format="wav")
            
    elif is_dir == False:
        dir = os.listdir(os.path.join(os.path.dirname(__file__), des))
        if len(dir) == 0: 
            song: AudioSegment = AudioSegment.from_mp3(os.path.join(INPUT_DIR))
            sliced_ten_secs = song[FIRST_MIN:FIRST_MIN+10000]
            sliced_ten_secs.export(os.path.join(OUTPUT_DIR, os.path.splitext(imp)[0] + ".wav"), format="wav")
        else: 
            raise ValueError("Destination Folder: " + des + " is not empty")



if __name__ == "__main__":

    args = parse_arguments()


    if args.directory:
        if args.destinationfolder == None:
            if not os.path.isdir("dataset_converted"):
                os.makedirs("dataset_converted")
            args.destinationfolder = "dataset_converted"
        converter(args.destinationfolder, args.directory, True)
    elif args.file:
        if args.destinationfolder == None:
            if not os.path.isdir("requestet_song_converted"):
                os.makedirs("requestet_song_converted")
            args.destinationfolder = "requestet_song_converted"
        converter(args.destinationfolder, args.file, False)

    