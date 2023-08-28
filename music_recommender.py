from annoy import AnnoyIndex
import process_embeddings as pe
import pandas as pd

def build_ann_index(file_list):
    
    n_dimensions = len(pe.get_embedding(file_list[1]).flatten())

    with open("test3.csv", 'w') as opened_file:
        opened_file.write(str(n_dimensions) + "\n")
     
    df = pd.DataFrame(file_list)
    df.to_csv("test3.csv", header=False, mode='a')
    
    annoy_index = AnnoyIndex(n_dimensions, "euclidean")
    annoy_index.on_disk_build("annoy_indices.ann")
    
    for index, file in enumerate(file_list):
        annoy_index.add_item(index, pe.get_embedding(file).flatten())

    annoy_index.build(10)