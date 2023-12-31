#!/usr/bin/env python3
import os
import sys
from typing import List, Final
import process_embeddings as pe
import pandas as pd
from annoy import AnnoyIndex

DEFAULT_MAPPINGS_METADATA: Final[str] = os.path.join(os.path.dirname(__file__), ".cache", "recommendation-metadata.csv")
ANNOY_INDEX_FILE: Final[str] = os.path.join(os.path.dirname(__file__), ".cache", "annoy_indices.ann")
METRIC = "euclidean"

def get_recommendation(input_song: str, nn_count: int = 1, metadata_file: str = DEFAULT_MAPPINGS_METADATA, annoy_idx_file: str = ANNOY_INDEX_FILE) -> List[str] | None:
    """
    Returns based on the input_song a list of nn_count recommendations.
    
    :param str input_song: The filepath to the input song
    :param int nn_count: amount of suggested to return
    :param str metadata_file: The filepath to the metadata_file containing mappings of indices to dataset song filepaths
    :param str annoy_idx_file: The filepath to the dataset based annoy index file
    """  
    # retrieve dimensionality of the embeddings, which is put on the first line of the metadata_file
    if os.path.exists(metadata_file):
        with open(metadata_file, "r") as f:
                embedding_dim_str = f.readline().strip("\n")
        try:
            embedding_dim = int(embedding_dim_str)
        except:
            print("Could not load dimensions of embeddings, metadata file is corrupted please retry converting the dataset.")
            return
    else:
        print("Could not load metadata file, the file does not exist please retry converting the dataset.")
        return
    
    # skip dimensions entry and read the index to file mappings
    idx_songs_df = pd.read_csv(metadata_file, skiprows=1, header=None, names=["song_filepath"], index_col=0)

    # load the previously build index file
    ann_index = AnnoyIndex(embedding_dim, METRIC)
    if not os.path.exists(annoy_idx_file):
        print("Could not load annoy index file, the file does not exist please retry converting the dataset.")
        return

    if not ann_index.load(annoy_idx_file):
        print("Could not properly load annoy index file, the file may be corrupted please retry converting the dataset.")
        return
    
    # check that length of the input song and the songs in the dataset are of the same length
    embd = pe.get_embedding(input_song).flatten()
    if len(embd) != embedding_dim:
        print("Could not provide a suggestion, the length of the input song does not match the length of the songs in the converted dataset. Specify the length via --startime and --length.")
        return

    # retrieve from annoy the nn_count nearest neighbors and return their idx
    idxs_nn = ann_index.get_nns_by_vector(embd, nn_count)

    # return the file mappings of the indices
    return idx_songs_df.iloc[idxs_nn]["song_filepath"].to_list()

def build_ann_index(file_list: List[str]):
    """
    Builds and saves a AnnoyIndex based on the intermediate song filepaths in file_list to a file which is the basis for the later recommended songs.
    
    :param str file_list: The list of files to base the AnnoyIndex on
    """
    if len(file_list) == 0:
        print("dataset is empty, please rerun the dataset conversion with data!")
        sys.exit(1)

    # calculate the length of the embeddings of the converted intermediate files
    n_dimensions = len(pe.get_embedding(file_list[0]).flatten())

    with open(DEFAULT_MAPPINGS_METADATA, 'w') as opened_file:
        opened_file.write(str(n_dimensions) + "\n")
     
    print("Generating embeddings for the files...")

    # save the file to index mappings and prepare the building of the AnnoyIndex
    df = pd.DataFrame(file_list)
    df.to_csv(DEFAULT_MAPPINGS_METADATA, header=False, mode='a')
    annoy_index = AnnoyIndex(n_dimensions, METRIC)
    annoy_index.on_disk_build(ANNOY_INDEX_FILE)
    
    # for each file retrieve the embedding and add it to the AnnoyIndex
    for index, file in enumerate(file_list):
        annoy_index.add_item(index, pe.get_embedding(file).flatten())
    annoy_index.build(50)
    print("done.")

# some test code to test the functions functionality
# if __name__ == "__main__":
#     dataset_filelist = [
#             "dataset_converted/24 Karat (Remix) - Kollegah feat. Seyed & Ali As.wav",
#             "dataset_converted/Beast - Vicetone Vs. Nico Vega.wav",
#             "dataset_converted/Benzin im Blut (G4bby Feat. Bazz Boyz Remix) - Dj Gollum Feat. Akustikrausch.wav",
#             "dataset_converted/Bleib in der Schule - Trailerpark.wav",
#             "dataset_converted/500 PS - Bonez MC & Raf Camora.wav",
#             "dataset_converted/Animals Anthem (Watch out for this) - Mashup Germany.wav"
#             ]
#     recommendation_base = "dataset_converted/Bück Dich hoch - Deichkind.wav"
# 
#     build_ann_index(dataset_filelist) 
#     print(get_recommendation(recommendation_base, 3))
