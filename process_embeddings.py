#!/usr/bin/env python3
import sys
import requests
from requests.exceptions import ConnectionError
import numpy as np
import numpy.typing as npt

def get_embedding(filepath: str, embedding_gen_endp: str="http://127.0.0.1:5000/model/predict") -> npt.NDArray[np.float32]:
    """
    Get embeddings as a numpy ndarray out of floats for a music file from a server endpoint running the MAX-Audio-Embedding-Generator specified through embedding_gen_endp.
    
    :param str filepath: The filepath to the wav file to get embeddings from
    :param str embedding_gen_endp: The url to the server endpoint to request the embedding
    :return: the embedding
    :rtype: numpy.NDArray[numpy.float32]
    """
    # prepare a post request to send a audio file to the server endpoint
    files = {
        "audio": (filepath, open(filepath, "rb"), "audio/x-wav")
    }
    try:
        response = requests.post(embedding_gen_endp, files=files)
    except ConnectionError:
        print(f'Could not connect to the server endpoint "{embedding_gen_endp}". Is the MAX-Audio-Embedding-Generator correctly setup and running?')
        sys.exit(1)

    # if something on the serverside went wrong print a appropriate message
    if response.status_code != 200:
        print(f'Something went wrong on sending a post request to endpoint "{embedding_gen_endp}". Aborting...')
        sys.exit(1)

    # return just the embedding from the response
    return np.array(response.json()["embedding"])

# some test code to test the functions functionality
# if __name__ == "__main__":
#     embd = get_embedding("dataset_converted/Beast - Vicetone Vs. Nico Vega.wav")
#     print(embd.flatten())
