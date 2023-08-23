#!/usr/bin/env python3
from pydub import AudioSegment
from pydub.utils import mediainfo
import os 
from typing import List
import argparse
import sys


parser = argparse.ArgumentParser(description="Formats a music file of various formats into a formatted wav music file")


# MIT FLAGS::

#parser.add_argument('-f', default=None, help="", required=True)
#args = parser.parse_args()
#print(args.f)
#parser.print_help()

##


# MIT PARSER GRUPPEN

group = parser.add_mutually_exclusive_group(required=True)

group.add_argument('-d', '--directory', help="takes a directory and converts everything to an wav file")
group.add_argument('-f', '--file', help="takes an file and on base of this file will perferm an recommendation")

#parser.add_argument('-df', '--destinationfile', help="destination, where the file should be safed", default="requestet_song_converted")
#parser.add_argument('-dd', '--destinationdirectory', help="destination, where the datasat should be safed", default="dataset_converted")

#BEIDE ZUSAMMENGEFASST ZU EINEN:    

parser.add_argument('-df', '--destinationfolder', help="takes an filepath, where the convertet file will be stored",
                    default=None)


args = parser.parse_args()

##


FIRST_MIN = 60000


if args.directory:
    print(args.directory)
    if args.destinationfolder == None:
        args.destinationfolder = "dataset_converted"
    OUTPUT_DIR = os.path.join(os.path.dirname(__file__), args.destinationfolder)
    INPUT_DIR = os.path.join(os.path.dirname(__file__), args.directory) 
    m_files: List[str] = os.listdir(INPUT_DIR)

    for f in m_files:
        song: AudioSegment = AudioSegment.from_mp3(os.path.join(INPUT_DIR, f))
        sliced_ten_secs = song[FIRST_MIN:FIRST_MIN+10000]
        sliced_ten_secs.export(os.path.join(OUTPUT_DIR, os.path.splitext(f)[0] + ".wav"), format="wav")
    

elif args.file:
    print(args.file)
    if args.destinationfolder == None:
        args.destinationfolder = "requestet_song_converted"
    dir = os.listdir(os.path.join(os.path.dirname(__file__), args.destinationfolder))
    
    if len(dir) == 0: 
        print("Empty directory") 
        OUTPUT_DIR_request = os.path.join(os.path.dirname(__file__), args.destinationfolder)
        INPUT_DIR_request = os.path.join(os.path.dirname(__file__), args.file)
        requestet_song: AudioSegment = AudioSegment.from_mp3(os.path.join(INPUT_DIR_request))

        

        sliced_ten_secs1 = requestet_song[FIRST_MIN:FIRST_MIN+10000]
        sliced_ten_secs1.export(os.path.join(OUTPUT_DIR_request, os.path.splitext(args.file)[0] + ".wav"), format="wav")
        #print(mediainfo("requestet_song_converted\Bück_Dich_hoch_-_Deichkind.wav"))
    else: 
        print("Not empty directory")
        raise ValueError("Destination Folder: " + args.destinationfolder + " is not empty")
        
    
    

# if args.f != None:
 #   INPUT_DIR_request = os.path.join(os.path.dirname(__file__), args.f)
  #  requestet_song: AudioSegment = AudioSegment.from_mp3(os.path.join(INPUT_DIR_request))
   # sliced_ten_secs1 = requestet_song[FIRST_MIN:FIRST_MIN+10000]
    #sliced_ten_secs1.export(os.path.join(OUTPUT_DIR_request, os.path.splitext(args.f)[0] + ".wav"), format="wav")


#m_files: List[str] = os.listdir(INPUT_DIR)

#for f in m_files:
 #   song: AudioSegment = AudioSegment.from_mp3(os.path.join(INPUT_DIR, f))
  #  sliced_ten_secs = song[FIRST_MIN:FIRST_MIN+10000]
   # sliced_ten_secs.export(os.path.join(OUTPUT_DIR, os.path.splitext(f)[0] + ".wav"), format="wav")

