#!/usr/bin/env python3
from pydub import AudioSegment
from pydub.utils import mediainfo
import pydub.exceptions as dubex
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
    
    parser.add_argument('-t', '--starttime', help="Time at which the clip starts in ms",
                    default=60000)
    parser.add_argument('-l', '--length', help="Value how long the clip should be in ms",
                    default=10000)
    
    return parser.parse_args()

def converter(des:str, imp:str, is_dir:bool, starttime: int, length: int):
    OUTPUT_DIR = os.path.join(os.path.dirname(__file__), des)
    INPUT_DIR = os.path.join(os.path.dirname(__file__), imp) 
    
    if is_dir == True:
        m_files: List[str] = os.listdir(INPUT_DIR)
        if len(m_files) != 0:
            for f in m_files:
                s = os.path.splitext(f)[1]
                try:
                    song: AudioSegment = AudioSegment.from_file(os.path.join(INPUT_DIR, f), s[1:])
                except dubex.CouldntDecodeError:
                    print("The format '" + s + "' is not supported")
                    sys.exit()
                sliced_ten_secs = song[starttime:starttime+length]
                print(os.path.splitext(f)[1])
                sliced_ten_secs.export(os.path.join(OUTPUT_DIR, os.path.splitext(f)[0] + ".wav"), format="wav")
        else:
            print("The folder '" + INPUT_DIR + "' is empty!")

        return m_files            
    elif is_dir == False:
        dir = os.listdir(os.path.join(os.path.dirname(__file__), des))
        if len(dir) == 0: 
            song: AudioSegment = AudioSegment.from_mp3(os.path.join(INPUT_DIR))
            sliced_ten_secs = song[starttime:starttime+length]
            sliced_ten_secs.export(os.path.join(OUTPUT_DIR, os.path.splitext(imp)[0] + ".wav"), format="wav")
        else: 
            raise ValueError("Destination Folder: '" + des + "' is not empty")
    
    

if __name__ == "__main__":

    args = parse_arguments()
    ret =[]
    if args.directory:
        ret.append("directory")
        ret.append(args.directory)
        if args.destinationfolder == None:
            if not os.path.isdir("dataset_converted"):
                os.makedirs("dataset_converted")
            args.destinationfolder = "dataset_converted"
        ret.append(args.destinationfolder)
        converter(args.destinationfolder, args.directory, True, args.starttime, args.length)
    elif args.file:
        ret.append("file")
        ret.append(args.file)
        if args.destinationfolder == None:
            if not os.path.isdir("requestet_song_converted"):
                os.makedirs("requestet_song_converted")
            args.destinationfolder = "requestet_song_converted"
        ret.append(args.destinationfolder)
        converter(args.destinationfolder, args.file, False, args.starttime, args.length)

    

    