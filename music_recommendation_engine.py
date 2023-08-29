#!/usr/bin/env python3
from pydub import AudioSegment
import pydub.exceptions as dubex
import os 
from typing import List
import argparse
import sys
import music_recommender as mr
import shutil

DATASET_CONVERTED = "dataset_converted"
REQ_SONG_CONVERTED = "requestet_song_converted"


def is_directory(arg: str):
    if not os.path.isdir(arg):
        raise argparse.ArgumentTypeError("The given argument was not a valid Path!")
    return arg

def parse_arguments():

    parser = argparse.ArgumentParser(description="formats a music file of various formats into a formatted wav music file")
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument('-d', '--dataset-directory', help="takes a directory and converts everything to a wav file")
    group.add_argument('-f', '--file', help="file on which basis a recommendation will be performed")

    parser.add_argument('-df', '--destinationfolder', type=is_directory, help="filepath where the converted file will be stored",
                    default=None)
    
    parser.add_argument('-t', '--starttime', type=int, help="starttime of the song(s) as of when the embedding will be created in ms",
                    default=60000)
    parser.add_argument('-l', '--length', type=int,  help="length of the song excerpt, on which basis the embedding is calculated in ms",
                    default=10000)
    parser.add_argument('-n', '--nn-count', type=int, help="number of nearest neighbor suggestions", default=1)
    return parser.parse_args()


def converter(inpd: str, inpf: str, des: str, starttime: int, length: int) -> str | List[str]:

    if inpf == None:
        if des == None:
            if not os.path.isdir(DATASET_CONVERTED):
                os.makedirs(DATASET_CONVERTED)

            des = DATASET_CONVERTED
            
        input_dir = os.path.join(os.path.dirname(__file__), inpd)
        output_dir = os.path.join(os.path.dirname(__file__), des)

        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
            os.makedirs(output_dir)
            
        m_files: List[str] = os.listdir(input_dir)

        if len(m_files) != 0:
            for f in m_files:
                s = os.path.splitext(f)[-1]
                try:
                    song: AudioSegment = AudioSegment.from_file(os.path.join(input_dir, f), s[1:])
                except dubex.CouldntDecodeError:
                    print("The format '" + s + "' is not supported")
                    sys.exit(1)
                
                song_clip = song[starttime:starttime+length]
                song_clip.export(os.path.join(output_dir, os.path.splitext(f)[0] + ".wav"), format="wav")
                
        else:
            print("The directory '" + input_dir + "' is empty, please provide files for the dataset")
            sys.exit(1)

        ret = [os.path.join(des, x) for x in os.listdir(output_dir)]
        return ret
    else:
        if not os.path.isfile(mr.ANNOY_INDEX_FILE):
            print("annoy indexfile does not exists, please provide a dataset using the flag --dataset-directory")
            sys.exit(1)
        if not os.path.isfile(inpf):
            print("filepath does not point to a file")
            sys.exit(1)
        if des == None:
            if not os.path.isdir(REQ_SONG_CONVERTED):
                os.makedirs(REQ_SONG_CONVERTED)
            des = REQ_SONG_CONVERTED
        input_dir = os.path.join(os.path.dirname(__file__), inpf)
        output_dir = os.path.join(os.path.dirname(__file__), des)
        dir = os.listdir(os.path.join(os.path.dirname(__file__), des))

        if len(dir) == 0: 
            s = os.path.splitext(input_dir)[-1]
            try:
                song: AudioSegment = AudioSegment.from_file(os.path.join(input_dir), s[1:])
            except dubex.CouldntDecodeError:
                print("The format '" + s + "' is not supported")
                sys.exit(1)
            song_clip = song[starttime:starttime+length]
            song_clip.export(os.path.join(output_dir, os.path.splitext(inpf)[0] + ".wav"), format="wav")
        else: 
            raise ValueError("destination directory: '" + des + "' is not empty")
        
        return os.path.join(des, os.listdir(output_dir)[0])
    

if __name__ == "__main__":

    args = parse_arguments()
    paths = converter(args.dataset_directory, args.file, args.destinationfolder, args.starttime, args.length)
    if type(paths) == str:
        print(mr.get_recommendation(paths, args.nn_count))
        if args.destinationfolder == None:
            args.destinationfolder = REQ_SONG_CONVERTED
        shutil.rmtree(args.destinationfolder)
    elif type(paths) == type(list()):
        mr.build_ann_index(paths)