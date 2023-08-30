#!/usr/bin/env python3
from pydub import AudioSegment
import pydub.exceptions as dubex
import os 
from typing import List, Final
import argparse
import sys
import music_recommender as mr
import shutil

DATASET_CONVERTED: Final[str] = os.path.join(os.path.dirname(__file__), ".cache", "dataset_converted")
REQ_SONG_CONVERTED: Final[str] = os.path.join(os.path.dirname(__file__), ".cache", "requestet_song_converted")

def is_directory(arg: str):
    if not os.path.isdir(arg):
        raise argparse.ArgumentTypeError("The given argument was not a valid Path!")
    return arg

def parse_arguments():

    parser = argparse.ArgumentParser(prog="music recommendation engine", description="provides song suggestions based on a previously processed dataset", add_help=True)

    subparser = parser.add_subparsers(title="mode specifier", dest="mode", help="choose mode to use")
    dataset_mode = subparser.add_parser('ds-mode', help="specify this to change to dataset conversion mode")
    dataset_group = dataset_mode.add_argument_group("dataset conversion arguments")
    
    dataset_group.add_argument('-p', '--path', help="specifies the folder to the input dataset", required=True)
    dataset_group.add_argument('-df', '--destinationfolder', type=is_directory, help="filepath where the intermediate converted dataset will be stored",
                   default=None)
    dataset_group.add_argument('-t', '--starttime', type=int, help="starttime of the songs in ms as of when the embedding will be created",
                    default=60000)
    dataset_group.add_argument('-l', '--length', type=int,  help="length of the song excerpts in, on which basis the embedding is calculated",
                    default=10000)
    
    suggestion_mode = subparser.add_parser("sg-mode", help="specify this to change to suggestion mode")
    suggestion_group = suggestion_mode.add_argument_group('song suggestion arguments')

    suggestion_group.add_argument('-p', '--path', help="specifies the input to the file on which the suggestion is based on.", required=True)
    suggestion_group.add_argument('-t', '--starttime', type=int, help="starttime of the song in ms as of when the embedding will be created",
                    default=60000)
    suggestion_group.add_argument('-l', '--length', type=int,  help="length of the song excerpt in ms on which basis the embedding is calculated",
                    default=10000)
    suggestion_group.add_argument('-n', '--nn-count', type=int, help="number of nearest neighbor suggestions", default=1)

    return parser.parse_args()


def process_dataset_args(path: str, dest_folder: str, starttime: int, length: int) -> List[str]:
    # set defaults if no argument is specified by the user
    if dest_folder == None:
        if not os.path.isdir(DATASET_CONVERTED):
            os.makedirs(DATASET_CONVERTED)

        dest_folder = DATASET_CONVERTED
    input_dir = os.path.join(os.path.dirname(__file__), path)
    output_dir = os.path.join(os.path.dirname(__file__), dest_folder)
        
    m_files: List[str] = os.listdir(input_dir)
    ret = []

    if len(m_files) != 0:
        for f in m_files:
            s = os.path.splitext(f)[-1]
            try:
                converted_song_path = os.path.join(input_dir, f)
                song: AudioSegment = AudioSegment.from_file(converted_song_path, s[1:])
                ret.append(converted_song_path)
            except dubex.CouldntDecodeError:
                print("The format '" + s + "' is not supported")
                sys.exit(1)
            
            song_clip = song[starttime:starttime+length]
            song_clip.export(os.path.join(output_dir, os.path.splitext(f)[0] + ".wav"), format="wav")

    return ret

def process_suggestion_args(path: str, starttime: int, length: int) -> str:
    if not os.path.isfile(mr.ANNOY_INDEX_FILE):
        print("annoy indexfile does not exists, please provide a non empty dataset folder")
        sys.exit(1)
    if not os.path.isfile(path):
        print("filepath does not point to a file")
        sys.exit(1)

    input_dir = os.path.join(os.path.dirname(__file__), path)
    output_dir = os.path.join(os.path.dirname(__file__), REQ_SONG_CONVERTED)

    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
        os.makedirs(output_dir)

    dir = os.listdir(os.path.join(os.path.dirname(__file__), REQ_SONG_CONVERTED))

    if len(dir) == 0: 
        s = os.path.splitext(input_dir)[-1]
        try:
            song: AudioSegment = AudioSegment.from_file(os.path.join(input_dir), s[1:])
        except dubex.CouldntDecodeError:
            print("The format '" + s + "' is not supported")
            sys.exit(1)
        song_clip = song[starttime:starttime+length]
        output_path = os.path.join(output_dir, os.path.splitext(path)[0] + ".wav")
        song_clip.export(output_path, format="wav")
    else: 
        raise ValueError("destination directory: '" + REQ_SONG_CONVERTED + "' is not empty")
    return output_path

if __name__ == "__main__":
    args = parse_arguments()

    if args.mode == "ds-mode":
        dataset_converted_paths: List[str] = process_dataset_args(args.path, args.destinationfolder, args.starttime, args.length) 
        mr.build_ann_index(dataset_converted_paths)

    elif args.mode == "sg-mode":
        song_converted_path = process_suggestion_args(args.path, args.starttime, args.length)
        print(mr.get_recommendation(song_converted_path, args.nn_count))
