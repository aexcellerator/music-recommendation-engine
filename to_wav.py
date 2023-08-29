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
    
    parser.add_argument('-t', '--starttime', type=int, help="Time at which the clip starts in ms",
                    default=60000)
    parser.add_argument('-l', '--length', type=int,  help="Value how long the clip should be in ms",
                    default=10000)
    
    return parser.parse_args()


def converter(impd:str, impf:str, des:str, starttime: int, length: int):

    ret =[]
    if impf == None:
        ret.append("directory")
        ret.append(impd)
        if des == None:
            if not os.path.isdir("dataset_converted"):
                os.makedirs("dataset_converted")
            des = "dataset_converted"
        ret.append(des)
        input_dir = os.path.join(os.path.dirname(__file__), impd)
        output_dir = os.path.join(os.path.dirname(__file__), des)

        m_files: List[str] = os.listdir(input_dir)
        if len(m_files) != 0:
            for f in m_files:
                s = os.path.splitext(f)[-1]
                try:
                    song: AudioSegment = AudioSegment.from_file(os.path.join(input_dir, f), s[1:])
                except dubex.CouldntDecodeError:
                    print("The format '" + s + "' is not supported")
                    sys.exit()
                
                sliced_ten_secs = song[starttime:starttime+length]
                sliced_ten_secs.export(os.path.join(output_dir, os.path.splitext(f)[0] + ".wav"), format="wav")
                
        else:
            print("The folder '" + input_dir + "' is empty!")
            sys.exit()

        ret = [os.path.join(des, x) for x in os.listdir(output_dir)]
        return ret
    else:
        ret.append("file") 
        ret.append(impf)
        if des == None:
            if not os.path.isdir("requestet_song_converted"):
                os.makedirs("requestet_song_converted")
            des = "requestet_song_converted"
        ret.append(des)
        input_dir = os.path.join(os.path.dirname(__file__), impf)
        output_dir = os.path.join(os.path.dirname(__file__), des)
        dir = os.listdir(os.path.join(os.path.dirname(__file__), des))
        if len(dir) == 0: 
            s = os.path.splitext(input_dir)[-1]
            song: AudioSegment = AudioSegment.from_file(os.path.join(input_dir), s[1:])
            sliced_ten_secs = song[starttime:starttime+length]
            sliced_ten_secs.export(os.path.join(output_dir, os.path.splitext(impf)[0] + ".wav"), format="wav")
        else: 
            raise ValueError("Destination Folder: '" + des + "' is not empty")
        
        return os.path.join(des, os.listdir(output_dir)[0])
    

if __name__ == "__main__":

    args = parse_arguments()
    print(converter(args.directory, args.file, args.destinationfolder, args.starttime, args.length))
    